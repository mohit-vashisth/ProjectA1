import { displayError } from "../utils/errorDisplay"
const newChatButton = document.querySelector(".newChat")
const newChatLoadingIndicator  = document.querySelector(".newChatButtonAnimation")
const newChatButtonText = document.querySelector(".newChatButtonText")
const newSessionURL = import.meta.env.VITE_NEW_CHAT_EP;
const loginPage = import.meta.env.VITE_LOGIN_PAGE;

let currentController = null

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

        const response = await fetch(newSessionURL, {
            method: "GET",
            credentials: "include",
            signal: currentController.signal,
        })

        clearTimeout(timeout)
        newChatButtonText.style.display = "block"
        newChatLoadingIndicator.style.display = "none"

        const data = await response.json();
        if (!response.ok) {
            const errorDetails = data?.detail;
            displayError(errorDetails);
        }

        if(data?.success && data.sessionLink){
            history.pushState(null, '', data.sessionLink);
        }
        else{   
            displayError("User timeout, redirecting to login")
            window.location.href = loginPage
        }
    }
    catch (error) {
        if (error.name === "AbortError") {
            displayError("Request timeout.");
        } else if (error.message.includes("Failed to fetch")) {
            displayError("Unable to connect. Please check your internet connection.");
        } else {
            displayError("An unexpected error occurred.");
        }
    }
}

export function newChatEXP() {
    if (newChatButton) newChatButton.addEventListener("click", newChatHandle);
}