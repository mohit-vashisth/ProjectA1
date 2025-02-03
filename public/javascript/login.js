import { displayError } from "../../src/javascript/utils/errorDisplay";
const email = document.querySelector("#email");
const password = document.querySelector("#password");
const login = document.querySelector("#login");
const errShow = document.querySelector("#errorDisplay");
const popupErr = document.querySelector(".displayErrors");
const loadingAnimation = document.querySelector(".loading");
const loginURL = import.meta.env.VITE_LOGIN_EP;
const dashBoardPage = import.meta.env.VITE_DASHBOARD_PAGE;
const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

let currentController = null;
let userLoginInfo = {
    email: "",
    password: "",
    timeZone: userTimeZone
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

    try{

        const timeout = setTimeout(() => {
            currentController.abort();
            displayError("Request timed out! Please try again.");
        }, 8000);

        const response = await fetch(loginURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ userLoginInfo }),
            signal: currentController.signal,
        })
        clearTimeout(timeout);

        if (!response.ok) {
            switch (response.status) {
                case 400:
                    displayError("Invalid input. Please check your text or voice selection.");
                    break;
                case 401:
                    displayError("You are not logged in. Please log in and try again.");
                    break;
                case 403:
                    displayError("You do not have permission to perform this action.");
                    break;
                case 404:
                    displayError("The requested resource was not found.");
                    break;
                case 500:
                    displayError("A server error occurred. Please try again later.");
                    break;
                default:
                    displayError("Something went wrong, Try again.");
            }
            return;
        }

        const data = await response.json().catch(()=> null);
        if(data?.success && data.email && data.access_token){
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