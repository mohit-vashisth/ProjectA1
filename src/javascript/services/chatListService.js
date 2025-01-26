import { displayError } from "../utils/errorDisplay";
const recentChatsButton = document.querySelector(".recentChatsButton");
const chatsSection = document.querySelector(".chatsSection");
const iconRotate = document.querySelector(".dropdownRecentChats img");
const baseURL = import.meta.env.VITE_BASE_URL;

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

    const response = await fetch(baseURL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      signal: currentController.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      displayError("Something went wrong");
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
      displayError("Request aborted");
    } else {
      displayError("Server not responding");
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
