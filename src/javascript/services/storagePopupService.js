import { displayError } from "../utils/errorDisplay";

// Selectors
const card = document.querySelector('.storagePopup');
const storageBackDisplay100VH = document.querySelector('.storagePopup100VH');
const storageButton = document.querySelector('.storageAudios');
const selectAllCheckbox = document.querySelector('.checkboxSelect');
const deleteChatButton = document.querySelector('.deleteChatButton');
const chatListUL = document.querySelector('.chatList');
const searchBar = document.querySelector(".searchInput");
const storageURL = import.meta.env.VITE_STORAGE_FILES_EP

// State
let currentChat = {
  name: null,
  link: null,
};
let currentController = null
let currentController2 = null
//--------------Open-Close Display---------------------

function toggleStorage() {
  storageButton?.addEventListener('click', (e) => {
    e.stopPropagation();
    storageBackDisplay100VH.style.display = "flex";
  });

  if (card) {
    document.addEventListener('click', (e) => {
      if (!card.contains(e.target) && e.target !== storageButton) {
        storageBackDisplay100VH.style.display = "none";
      }
    });
  }
}

// Function to add a single chat to the storage list
function addChatToStorage(chats) {
  if (!Array.isArray(chats)) {
    console.error("Invalid chat data:", chats);
    return;
  }

  const fragment = document.createDocumentFragment();
  chats.forEach(chat => {
    const chatItem = document.createElement("li");
    chatItem.innerHTML = `
      <a href="${chat.link}" class="chatHereLink">
        <input type="checkbox" class="chatCheckbox">
        <span class="chatName">${chat.name}</span>
      </a>
    `;
    fragment.appendChild(chatItem);

    chatItem.querySelector(".chatHereLink").addEventListener("click", () => {
      currentChat.name = chat.name;
      currentChat.link = chat.link;
    });
  });

  if (chatListUL) chatListUL.appendChild(fragment);
}

// add chats in file Storage
async function populateStorage() {
  if (currentController) {
    currentController.abort();
    currentController = null;
  }

  currentController = new AbortController();

  try {
    const timeout = setTimeout(() => {
      currentController.abort();
      displayError("Request Aborted");
    }, 8000);

    const response = await fetch(`${storageURL}/get-chats`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      signal: currentController.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      switch (response.status) {
          case 400:
              displayError("Invalid input. Please check your text or voice selection.");
              break;
          case 401:
              displayError("You are not logged in. Please log in and try again.");
              break;
          case 403:
              displayError("You do not have permission to perform this action.");
              break;
          case 404:
              displayError("The requested resource was not found.");
              break;
          case 500:
              displayError("A server error occurred. Please try again later.");
              break;
          default:
              displayError("Something went wrong, Try again.");
      }
      return;
  }

    const data = await response.json();
    if (data && data.chats) addChatToStorage(data.chats);

  } catch (error) {
    if (error.name === "AbortError") {
        displayError("Request timeout.");
    } else if (error.message.includes("Failed to fetch")) {
        displayError("Unable to connect. Please check your internet connection.");
    } else {
        displayError("An unexpected error occurred.");
    }
  }
}

// Function to filter chats based on search input
function searchChats() {
  searchBar.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const allChats = chatListUL.querySelectorAll("li");
    allChats.forEach(chat => {
      const chatName = chat.querySelector(".chatName").textContent.toLowerCase();
      chat.style.display = chatName.includes(query) ? '' : 'none';
    });
  });
}

// Function to manage selection of chats
function selectChats() {
  // Handle "Select All" checkbox logic
  selectAllCheckbox.addEventListener('change', () => {
    const allCheckboxes = chatListUL.querySelectorAll(".chatCheckbox");
    allCheckboxes.forEach(checkbox => {
      checkbox.checked = selectAllCheckbox.checked;
    });
  });

  // Handle individual checkbox logic
  chatListUL.addEventListener('change', (e) => {
    if (e.target.classList.contains('chatCheckbox')) {
      const allCheckboxes = chatListUL.querySelectorAll(".chatCheckbox");
      const checkedCheckboxes = chatListUL.querySelectorAll(".chatCheckbox:checked");

      // Automatically toggle the "Select All" checkbox
      selectAllCheckbox.checked = allCheckboxes.length === checkedCheckboxes.length;
    }
  });
}


// Function to delete selected chats
async function deleteChats() {
  if(currentController2){
    currentController2.abort()
    currentController2 = null
  }

  currentController2 = new AbortController()

  if(deleteChatButton){
    deleteChatButton.addEventListener('click', async () => {
      const selectedChats = Array.from(chatListUL.querySelectorAll(".chatCheckbox:checked"));
      const chatIds = selectedChats.map(chatCheckbox => chatCheckbox.closest("li").dataset.chatId); // Ensure each <li> has a `data-chat-id`.

      // Remove chats from UI
      selectedChats.forEach(chatCheckbox => {
        chatCheckbox.closest("li").remove();
      });

      try {
        const timeout = setTimeout(() => {
          currentController2.abort();
          displayError("Request Aborted");
        }, 8000);

        const response = await fetch(`${storageURL}/delete-chats`, {
          method: "POST", // POST request for deletion
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          signal: currentController2.signal,
          body: JSON.stringify({ chatIds }), // Send selected chat IDs to the backend
        });

        clearTimeout(timeout);

        if (!response.ok) {
          displayError(`Error: ${response.status}`);
          return;
        }

        const data = await response.json();
        if (data && data.success) {
          displayError("Selected chats deleted successfully");
        }
      } catch (error) {
        if (error.name === "AbortError") {
          displayError("Request Aborted");
        } else {
          displayError("Failed to delete chats");
        }
      }
    });
  }
}

// Initialize
toggleStorage();
searchChats();
selectChats();

export function storageHandleEXP() {
  populateStorage();
  deleteChats();
}
