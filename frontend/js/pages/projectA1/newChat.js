const newChat = document.querySelector(".newChat");
const popup = document.querySelector(".errorPopup")
const baseURL = import.meta.env.VITE_BASE_URL;
let currentController = null;

function errorPopup(errorText) {
    if (popup) {
        if (errorText !== "") {
            popup.textContent = errorText;
            popup.style.width = "30vmin";
        } else {
            popup.style.width = "0";
        }
    }
}

function clearErrorPopup() {
    setTimeout(() => errorPopup(""), 2000);
}

async function handleNewChat() {
    if(!newChat && !popup){
        errorPopup("something went wrong, try again later.")
        clearErrorPopup()
        return;
    }

    if(currentController){
        currentController.abort()
        currentController = null;
    }

    currentController = new AbortController()

    const timeout = setTimeout(() => {
        currentController.abort()
        errorPopup("Can't able to create new Session")
        clearErrorPopup()
    }, 8000);

    try{
        const response = await fetch(`${baseURL}/c/`, {
            method: "POST",
            credentials: "include",
            signal: currentController.signal,
        })
        clearTimeout(timeout)
        if(!response.ok){
            errorPopup("Error Creating New Chat")
            clearErrorPopup()
        }
        const data = await response.json()
        if(data && data.status){
            // it will run a effect of animation of loading assets of new chat or session
            localStorage.setItem("animationPlayed", "false");
            window.location.reload()
        }
        else{
            errorPopup("Unexpected response from the server")
            clearErrorPopup()
        }
    }
    catch(error){
        if(error.name === "AbortError") console.error("Request Aborted");
        clearTimeout(timeout)
        errorPopup("Error Creating New Chat")
        clearErrorPopup()
    }
}

newChat.addEventListener('click', handleNewChat)