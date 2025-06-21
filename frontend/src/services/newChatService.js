import { displayError } from "../utils/errorDisplay";

const newChatButton = document.querySelector(".newChat");
const newChatLoadingIndicator = document.querySelector(".newChatButtonAnimation");
const newChatButtonText = document.querySelector(".newChatButtonText");

const newSessionURL = import.meta.env.VITE_NEW_CHAT_EP;
const loginPage = import.meta.env.VITE_LOGIN_PAGE;

let currentController = null;

async function newChatHandle() {
    if (currentController) {
        currentController.abort();
        currentController = null;
    }

    currentController = new AbortController();

    if (newChatButtonText) newChatButtonText.style.display = "none";
    if (newChatLoadingIndicator) newChatLoadingIndicator.style.display = "flex";

    try {
        const timeout = setTimeout(() => {
            currentController.abort();
            displayError("Request timeout.");
        }, 8000);

        const response = await fetch(newSessionURL, {
            method: "GET",
            credentials: "include",
            signal: currentController.signal,
        });

        clearTimeout(timeout);

        if (newChatButtonText) newChatButtonText.style.display = "block";
        if (newChatLoadingIndicator) newChatLoadingIndicator.style.display = "none";

        const data = await response.json();

        if (!response.ok) {
            displayError(data?.detail || "Failed to start a new chat.");
            return;
        }

        // if (data?.success && data.sessionLink) {
        //     history.pushState(null, "", data.sessionLink);
        // } else {
        //     displayError("Session link not found, redirecting to login.");
        //     window.location.href = loginPage;
        // }
    } catch (error) {
        console.error("New chat request failed:", error);

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