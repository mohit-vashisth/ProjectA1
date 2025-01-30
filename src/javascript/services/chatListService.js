import { displayError } from "../utils/errorDisplay";
const recentChatsButton = document.querySelector(".recentChatsButton");
const chatsSection = document.querySelector(".chatsSection");
const iconRotate = document.querySelector(".dropdownRecentChats img");
const userChatsURL = import.meta.env.VITE_CHATS_URL;

let currentController = null;
let currentChat = {
  name: null,
  link: null
};

// Function to open or close the chat list dropdown
function openCloseChatList() {
  if (!chatsSection.classList.contains("openChatListDisplay")) {
    recentChatsButton.classList.add("openChatList");
    chatsSection.classList.add("openChatListDisplay");
    iconRotate.style.transform = "rotate(180deg)";
  } else {
    recentChatsButton.classList.remove("openChatList");
    chatsSection.classList.remove("openChatListDisplay");
    iconRotate.style.transform = "rotate(0deg)";
  }
}

// Function to add a single chat to the list
function addChatToList(chatLink, chatName) {
  if (!chatLink || !chatName) {
    console.error("Invalid chat data:", { chatLink, chatName });
    return;
  }

  const chatsHistory = document.querySelector(".chatsHistoryHereNow");
  const chatItem = document.createElement("li");
  chatItem.innerHTML = `
    <a href="${chatLink}" class="chatHereLink">
      <div class="chatHereDiv">
        <span>${chatName}</span>
      </div>
    </a>
  `;
  chatsHistory.appendChild(chatItem);

  // Update the currentChat object when a chat is clicked
  chatItem.querySelector(".chatHereLink").addEventListener("click", () => {
    currentChat.name = chatName;
    currentChat.link = chatLink;
  });
}

// Function to load user chats from the server
async function loadUserChats() {
  if (currentController) {
    currentController.abort();
    currentController = null;
  }

  currentController = new AbortController();

  try {
    const timeout = setTimeout(() => {
      currentController.abort();
      displayError("Taking too much time, try again later.");
    }, 8000);

    const response = await fetch(userChatsURL, {
      method: "POST",
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

    if (data && data.status && data.chats.length > 0) {
      const fragment = document.createDocumentFragment();
      data.chats.forEach((chat) => {
        const chatItem = document.createElement("li");
        chatItem.innerHTML = `
          <a href="${chat.chatLink}" class="chatHereLink">
            <div class="chatHereDiv">
              <span>${chat.chatName}</span>
            </div>
          </a>
        `;
        fragment.appendChild(chatItem);

        // Add click listener to update currentChat
        chatItem.querySelector(".chatHereLink").addEventListener("click", () => {
          currentChat.name = chat.chatName;
          currentChat.link = chat.chatLink;
        });

        // Save to localStorage
        localStorage.setItem(chat.chatName, chat.chatLink);
      });
      document.querySelector(".chatsHistoryHereNow").appendChild(fragment);
    } else {
      displayError("No chats found.");
    }
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

// Function to initialize recent chats
export function recentChatsEXP() {
  recentChatsButton.addEventListener("click", openCloseChatList);
  loadUserChats();

  // Add sample chats (for testing purposes)
  addChatToList("#", "Google");
  addChatToList("#", "YouTube");
  addChatToList("#", "Facebook");
}

// Function to return the current chat
export function userCurrentChatEXP() {
  return currentChat;
}
