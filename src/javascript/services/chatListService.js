const recentChatsButton = document.querySelector(".recentChatsButton");
const chatsSection = document.querySelector(".chatsSection");
const iconRotate = document.querySelector(".dropdownRecentChats img");
const popupErr = document.querySelector(".errorPopup");
const baseURL = import.meta.env.VITE_BASE_URL;

let currentController = null;
let currentChat = {}

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

function popupError(text, time) {
  popupErr.textContent = text;
  popupErr.style.width = "30vmin";
  popupErr.style.padding = "1vmin";
  setTimeout(() => {
    popupErr.style.width = "0";
    popupErr.style.padding = "0";
  }, time);
}

function addChatToList(chatLink, chatName) {
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
}

async function loadUserChats() {
  if (currentController) {
    currentController.abort();
    currentController = null;
  }

  currentController = new AbortController();

  try {
    const timeout = setTimeout(() => {
      currentController.abort();
      popupError("Taking too much time, try again later.", 2000);
    }, 8000);

    const response = await fetch(baseURL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      signal: currentController.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      popupError("Something went wrong", 2000);
      return;
    }

    const data = await response.json();

    if (data && data.status && data.chats.length > 0) {
        data.chats.forEach(chat => {
            addChatToList(chat.chatLink, chat.chatName);
            localStorage.setItem(chat.chatName, chat.chatLink);
        });
    }
    
  } catch (error) {
    if (error.name === "AbortError") {
      popupError("Request aborted", 2000);
    } else {
      popupError("Server not responding", 2000);
    }
  }
}

export function recentChatsEXP() {
  recentChatsButton.addEventListener("click", openCloseChatList);
  loadUserChats();
  
    addChatToList("#", "Google")
    addChatToList("#", "YouTube")
    addChatToList("#", "FaceBook")
}

export function userCurrentChatEXP() {
    
}