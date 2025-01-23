const newChatButton = document.querySelector(".newChat")
const errPopup = document.querySelector(".errorPopup")
const newChatLoadingIndicator  = document.querySelector(".newChatButtonAnimation")
const newChatButtonText = document.querySelector(".newChatButtonText")
const baseURL = import.meta.env.VITE_BASE_URL;
const loginURL = import.meta.env.VITE_LOGIN_URL;
const chatsURL = import.meta.env.VITE_CHATS_URL;

let currentController = null

/**
 * Displays an error message in a popup.
 * @param {string} text - The error message.
 * @param {number} duration - The duration for which the popup is displayed (ms).
 */
function errDisplay(text, time) {
    errPopup.style.width = "30vmin"
    errPopup.textContent = text
    setTimeout(() => {
    errPopup.style.width = "0"
    }, time);
}

async function newChatHandle() {
    if(currentController){
        currentController.abort()
        currentController = null
    }

    currentController = new AbortController()
    newChatButtonText.style.display = "none"
    newChatLoadingIndicator.style.display = "flex"
    
    try{
        const timeout = setTimeout(() => {
            currentController.abort()
            errDisplay("request aborted", 2000)
        }, 8000);

        const response = await fetch(baseURL, {
            method: "GET",
            credentials: "include",
            signal: currentController.signal,
        })

        clearTimeout(timeout)
        newChatButtonText.style.display = "block"
        newChatLoadingIndicator.style.display = "none"

        if(!response.ok){
            errDisplay("something went wrong", 2000)
            return
        }

        const data = await response.json()
        if(data?.success && data.chatID){
            const chatURL = `${chatsURL}${data.chatID}`
            history.pushState(null, '', newUrl);
        }
        else{   
            errDisplay("User timeout, redirecting to login", 2000)
            window.location.href = loginURL
        }
    }
    catch(error){
        if (error.name === "AbortError") {
            errDisplay("Request was aborted", 2000);
        } else {
            console.error("Error occurred:", error);
            errDisplay("something went wrong", 2000)
        }
    }
}

export function newChatEXP() {
    if (newChatButton) newChatButton.addEventListener("click", newChatHandle);
}