import { displayError } from "../utils/errorDisplay";

const card = document.querySelector('.storagePopup');
const storageBackDisplay100VH = document.querySelector('.storagePopup100VH');
const storageButton = document.querySelector('.storageAudios');
const selectAllCheckbox = document.querySelector('.checkboxSelect');
const deleteChatButton = document.querySelector('.deleteChatButton');
const chatListUL = document.querySelector('.chatList');
const searchBar = document.querySelector(".searchInput");
const storageURL = import.meta.env.VITE_STORAGE_FILES_EP;

let currentChat = { name: null, link: null };
let currentController = null;
let currentController2 = null;

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

function addChatToStorage(chats) {
  if (!Array.isArray(chats)) {
    console.error("Invalid chat data:", chats);
    return;
  }

  const fragment = document.createDocumentFragment();
  chats.forEach(chat => {
    const chatItem = document.createElement("li");
    chatItem.setAttribute("data-chat-id", chat.id); // Ensure `id` is present
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

    const data = await response.json();
    if (!response.ok) {
      displayError(data?.detail || "Failed to fetch chats.");
      return;
    }
    if (data?.chats) addChatToStorage(data.chats);
  } catch (error) {
    displayError(error.message || "An unexpected error occurred.");
  }
}

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

function selectChats() {
  selectAllCheckbox.addEventListener('change', () => {
    const allCheckboxes = chatListUL.querySelectorAll(".chatCheckbox");
    allCheckboxes.forEach(checkbox => {
      checkbox.checked = selectAllCheckbox.checked;
    });
  });

  chatListUL.addEventListener('change', (e) => {
    if (e.target.classList.contains('chatCheckbox')) {
      const allCheckboxes = chatListUL.querySelectorAll(".chatCheckbox");
      const checkedCheckboxes = chatListUL.querySelectorAll(".chatCheckbox:checked");
      selectAllCheckbox.checked = allCheckboxes.length === checkedCheckboxes.length;
    }
  });
}

async function deleteChats() {
  if (currentController2) {
    currentController2.abort();
    currentController2 = null;
  }

  currentController2 = new AbortController();

  if (deleteChatButton) {
    deleteChatButton.addEventListener('click', async () => {
      const selectedChats = Array.from(chatListUL.querySelectorAll(".chatCheckbox:checked"));
      const chatIds = selectedChats.map(chatCheckbox => chatCheckbox.closest("li").dataset.chatId);
      
      const deletedChatsBackup = selectedChats.map(chatCheckbox => chatCheckbox.closest("li").cloneNode(true));

      selectedChats.forEach(chatCheckbox => chatCheckbox.closest("li").remove());

      try {
        const timeout = setTimeout(() => {
          currentController2.abort();
          displayError("Request Aborted");
        }, 8000);

        const response = await fetch(`${storageURL}/delete-chats`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          signal: currentController2.signal,
          body: JSON.stringify({ chatIds }),
        });

        clearTimeout(timeout);

        const data = await response.json();
        if (!response.ok || !data?.success) {
          throw new Error(`Error: ${data?.detail || "Failed to delete chats."}`);
        }

        displayError("Selected chats deleted successfully");
      } catch (error) {
        displayError(error.message || "Failed to delete chats. Restoring...");

        deletedChatsBackup.forEach(chat => chatListUL.appendChild(chat));
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