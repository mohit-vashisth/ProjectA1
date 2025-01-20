const recentChatsButton = document.querySelector(".recentChatsButton");
const chatsSection = document.querySelector(".chatsSection");
const iconRotate = document.querySelector(".dropdownRecentChats img");
const popupErr = document.querySelector(".errorPopup");
const baseURL = import.meta.env.VITE_BASE_URL;
let currentController = null

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
recentChatsButton.addEventListener('click', openCloseChatList)

// fetch API starts here---------------------------------------------

function popupError(error) {
    if(error !== ""){
        popupErr.textContent = error;
        popupErr.style.width = "30vmin";
        popupErr.style.padding = "1vmin";
    } else{
        popupErr.style.width = "0";
        popupErr.style.padding = "0";
    }
}

// clearing popup 2sec time
function clearErrorPopup(time) {
    setTimeout(() => errorPopup(""), time);
}

function addChatToList(chatId, chatName) {
    const chatsHistory = document.querySelector(".chatsHistoryHereNow");
    const chatItem = document.createElement("li");
    chatItem.innerHTML = `
        <a href="#" class="chatHereLink" data-chat-id="${chatId}" onclick="handleChatClick(event)">
            <div class="chatHereDiv">
                <span>${chatName}</span>
            </div>
        </a>
    `;
    chatsHistory.appendChild(chatItem);
}

function createNewChat() {
    if(currentController){
        currentController.abort()
        currentController = null
    }

    currentController = new AbortController()

    try {
        const timeout = setTimeout(() => {
            currentController.abort()
            popupError("taking much time, try again later.")
            clearErrorPopup(2000)
        }, 8000);

        const response = fetch(`${baseURL}/chats`, {
            method: "POST",
            headers: {"Content-Type": "application/json",},
            credentials: "include",
            signal: currentController.signal,
        })
        
        if(!response.ok){
            popupError("Something went wrong")
            clearErrorPopup(2000)
        }
        const data = response.json()
        if(data && data.status){
            addChatToList(data.chatID, data.chatName)
        }
    } catch (error) {
        if(error.name === "AbortError"){
            popupError("request aborted")
            clearErrorPopup(2000)
        }else{}
        popupError("server not responding")
        clearErrorPopup(2000)
    }
}


