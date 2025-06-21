import { displayError } from "../../../../frontend2/src/pages/modules/errorDisplay";
import { LoginDTO } from "../../schemas/loginDTO"

const email = document.querySelector("#email");
const password = document.querySelector("#password");
const loginButton = document.querySelector("#login");
const loadingAnimation = document.querySelector(".loading");

const loginURL = import.meta.env.VITE_LOGIN_EP;
const dashBoardPage = import.meta.env.VITE_DASHBOARD_PAGE;

let currentController = null;

const validationCriteria = {
    email: value => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
    password: value => value.trim().length >= 8
};

function updateButtonState(isValid) {
    loginButton.style.pointerEvents = isValid ? "auto" : "none";
    loginButton.style.cursor = isValid ? "pointer" : "not-allowed";
    loginButton.style.opacity = isValid ? "1" : "0.5";
}

function validateFields() {
    const isEmailValid = validationCriteria.email(email.value.trim());
    const isPasswordValid = validationCriteria.password(password.value.trim());
    
    const isValid = isEmailValid && isPasswordValid;
    updateButtonState(isValid);
    
    return isValid;
}

email.addEventListener("input", validateFields);
password.addEventListener("input", validateFields);

loginButton.addEventListener('click', async (event) => {
    event.preventDefault();
    
    if (!validateFields()) return;
    
    loginButton.style.pointerEvents = "none";
    loginButton.style.cursor = "not-allowed";
    loginButton.style.opacity = "0.5";
    
    if (currentController) currentController.abort();
    currentController = new AbortController();

    const newUser = new LoginDTO(
            email.value.trim(),
            password.value
        );

    try {
        loadingAnimation.style.display = "flex";
        
        document.body.style.cursor = "wait";
        
        const timeout = setTimeout(() => {
            currentController.abort();
            displayError("Request timed out - please try again");
        }, 8000);

        const response = await fetch(loginURL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newUser),
            credentials: "include",
            signal: currentController.signal
        });

        clearTimeout(timeout);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Authentication failed");
        }

        window.location.href = dashBoardPage;
    } catch (error) {
        if (error.name !== "AbortError") {
            const errorMessage = error.message.includes("fetch")
                ? "Network error - check internet connection"
                : error.message;
            
            displayError(errorMessage);
            password.value = "";
        }
    } finally {
        loadingAnimation.style.display = "none";
        currentController = null;
        document.body.style.cursor = "default";
        validateFields();
    }
});

window.addEventListener('offline', () => {
    displayError("No internet connection - working offline");
    updateButtonState(false);
});

window.addEventListener('online', validateFields);