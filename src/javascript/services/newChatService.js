import { displayError } from "../utils/errorDisplay"

const newChatButton = document.querySelector(".newChat")
const newChatLoadingIndicator  = document.querySelector(".newChatButtonAnimation")
const newChatButtonText = document.querySelector(".newChatButtonText")
const baseURL = import.meta.env.VITE_BASE_URL;
const loginURL = import.meta.env.VITE_LOGIN_URL;
const chatsURL = import.meta.env.VITE_CHATS_URL;

let currentController = null
let socket = null

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
            displayError("request aborted")
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
            displayError("something went wrong")
            return
        }

        const data = await response.json()
        if(data?.success && data.chatID){
            const newUrl = `${chatsURL}${data.chatID}`
            history.pushState(null, '', newUrl);
        }
        else{   
            displayError("User timeout, redirecting to login")
            window.location.href = loginURL
        }
    }
    catch(error){
        if (error.name === "AbortError") {
            displayError("Request was aborted");
        } else {
            console.error("Error occurred:", error);
            displayError("something went wrong")
        }
    }
}

export function newChatEXP() {
    if (newChatButton) newChatButton.addEventListener("click", newChatHandle);
}