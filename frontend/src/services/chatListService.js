import { displayError } from "../utils/errorDisplay";
const recentChatsButton = document.querySelector(".recentChatsButton");
const chatsSection = document.querySelector(".chatsSection");
const iconRotate = document.querySelector(".dropdownRecentChats img");
const userRecentChatsURL = import.meta.env.VITE_RECENT_CHATS_FILES_EP;

let currentController = null;
let currentChat = {
  name: null,
  link: null,
};

function openCloseChatList() {
  const isOpen = chatsSection.classList.contains("openChatListDisplay");
  recentChatsButton.classList.toggle("openChatList", !isOpen);
  chatsSection.classList.toggle("openChatListDisplay", !isOpen);
  iconRotate.style.transform = isOpen ? "rotate(0deg)" : "rotate(180deg)";
}

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

  chatItem.querySelector(".chatHereLink").addEventListener("click", () => {
    currentChat.name = chatName;
    currentChat.link = chatLink;
  });
}

async function loadUserChats() {
  if (currentController) {
    currentController.abort();
  }
  currentController = new AbortController();

  try {
    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("Request timeout")), 8000)
    );

    const fetchPromise = fetch(userRecentChatsURL, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      signal: currentController.signal,
    }).then(async (response) => {
      if (!response.ok) {
        throw new Error((await response.json())?.detail || "Failed to load chats");
      }
      return response.json();
    });

    const data = await Promise.race([fetchPromise, timeoutPromise]);

    if (data?.status && Array.isArray(data.chats) && data.chats.length > 0) {
      const fragment = document.createDocumentFragment();
      const chatStorage = [];
      
      data.chats.forEach(({ chatLink, chatName }) => {
        const chatItem = document.createElement("li");
        chatItem.innerHTML = `
          <a href="${chatLink}" class="chatHereLink">
            <div class="chatHereDiv">
              <span>${chatName}</span>
            </div>
          </a>
        `;
        fragment.appendChild(chatItem);

        chatItem.querySelector(".chatHereLink").addEventListener("click", () => {
          currentChat.name = chatName;
          currentChat.link = chatLink;
        });

        chatStorage.push({ name: chatName, link: chatLink });
      });
      document.querySelector(".chatsHistoryHereNow").appendChild(fragment);
      localStorage.setItem("recentChats", JSON.stringify(chatStorage));
    } else {
      displayError("No chats found.");
    }
  } catch (error) {
    displayError(error.message.includes("Failed to fetch")
      ? "Unable to connect. Please check your internet connection."
      : error.message
    );
  }
}

export function recentChatsEXP() {
  recentChatsButton.addEventListener("click", openCloseChatList);
  loadUserChats();

  if (import.meta.env.MODE === "development") {
    addChatToList("#", "Google");
    addChatToList("#", "YouTube");
    addChatToList("#", "Facebook");
  }
}

export function userCurrentChatEXP() {
  return currentChat;
}
