import { displayError } from "../../src/javascript/utils/errorDisplay";
const email = document.querySelector("#email");
const password = document.querySelector("#password");
const login = document.querySelector("#login");
const loadingAnimation = document.querySelector(".loading");
const loginURL = import.meta.env.VITE_LOGIN_EP;
const dashBoardPage = import.meta.env.VITE_DASHBOARD_PAGE;

let currentController = null;
let userLoginInfo = {
    email: "",
    password: ""
};
document.addEventListener('DOMContentLoaded', () => {
    const link = document.createElement('link'); // Create a <link> element
    link.rel = 'stylesheet'; // Set the relationship as "stylesheet"
    link.href = '/frontend/css/pages/signin.css'; // Path to your CSS file
    document.head.appendChild(link); // Append the <link> to the <head>
});

function resetForm() {
    password.value = "";
}

function validateFields() {
    const isEmailValid = email.value.trim() !== "";
    const isPasswordValid = password.value.trim() !== "";
    
    if (isEmailValid && isPasswordValid) {
        login.style.pointerEvents = "auto";
        login.style.opacity = "1";
    } else {
        login.style.pointerEvents = "none";
        login.style.opacity = "0.5";
    }
}

email.addEventListener("blur", validateFields);
password.addEventListener("input", validateFields);

login.addEventListener('click', async (event)=>{
    event.preventDefault()

    if (login.style.pointerEvents === "none") return;

    userLoginInfo.email = email.value;
    userLoginInfo.password = password.value;
    
    if(currentController){
        currentController.abort()
        currentController = null;
    };
    
    loadingAnimation.style.display = "flex";
    
    currentController = new AbortController();
    let timeout
    try{

        timeout = setTimeout(() => {
            currentController.abort();
            displayError("Request timed out! Please try again.");
        }, 8000);

        const response = await fetch(loginURL, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(userLoginInfo),
            credentials: "include",
            signal: currentController.signal,
        })
        clearTimeout(timeout);

        const data = await response.json();
        if (!response.ok) {
            const errorDetails = data?.detail;
            switch (response.status) {
                case 400:
                    displayError(errorDetails);
                    break;
                case 401:
                    displayError(errorDetails);
                    break;
                case 404:
                    displayError(errorDetails);
                    break;
                case 500:
                    displayError(errorDetails);
                    break;
                default:
                    displayError(errorDetails);
            }
            continueButton.disabled = false;
            return;
        }
        
        if(data?.message === "User logged in successfully."){
            window.location.href = dashBoardPage;
            resetForm()
        }
        else{
            displayError("Invalid login credentials");
            resetForm()
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
    } finally{
        clearTimeout(timeout)
        loadingAnimation.style.display = "none";
    }
})