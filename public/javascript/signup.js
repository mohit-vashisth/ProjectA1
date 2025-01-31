//  Imports
import { displayError } from "../../src/javascript/utils/errorDisplay";

//  G-variables
const userName = document.querySelector("#name");
const email = document.querySelector("#email");
const password = document.querySelector("#password");
const confirmPassword = document.querySelector("#confirmPassword");
const continueButton = document.querySelector("#continue");
const errors = document.querySelector(".errors"); 
const popupErr = document.querySelector(".displayErrors");
const loadingAnimation = document.querySelector(".loading");
const signinLink = document.querySelector("#signinLink");
const isPrivacyChecked = document.querySelector("#T_C_Privacy")
const signUpURL = import.meta.env.VITE_SIGNUP_EP;
const dashboardPage = import.meta.env.VITE_DASHBOARD_PAGE;

let currentController = null;
let userInfo = {
    userName: "",
    userEmail: "",
    userPassword: ""
}

// user side signin form
if(signinLink){
    signinLink.addEventListener('click', (event)=>{
        event.preventDefault()
        window.location.href = signUpURL;
    })
}

// css dynamic inject
document.addEventListener('DOMContentLoaded', () => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/frontend/css/pages/signup.css';
    document.head.appendChild(link);
});

// continue button initial state
continueButton.style.pointerEvents = "none";
continueButton.style.opacity = "0.5";

// error display inside user's form
function errorDisplay(error) {
    errors.textContent = error;
    errors.style.color = "red";
}

// reset form after successfull or fail login
function resetForm(){
    userName.value = "",
    email.value = ""
}

// Function to check if all inputs are valid
function validateInputs() {
    const isUserNameValid = userName.value.trim() !== "";
    const isEmailValid = email.value.trim() !== "";
    const isPasswordValid = password.value.trim() !== "";
    const isConfirmPasswordValid = confirmPassword.value.trim() !== "" && confirmPassword.value === password.value;
    const isPrivacyCheckedValid = isPrivacyChecked.checked; // Check if privacy policy is agreed

    // Enable the button if all inputs are valid
    if (isUserNameValid && isEmailValid && isPasswordValid && isConfirmPasswordValid && isPrivacyCheckedValid) {
        continueButton.style.pointerEvents = "auto";
        continueButton.style.opacity = "1";
        errorDisplay("");
        return true;
    } else {
        continueButton.style.pointerEvents = "none";
        continueButton.style.opacity = "0.5"; // Optional: Make it look disabled
    }
}

// Add event listeners to all input fields
isPrivacyChecked.addEventListener("change", validateInputs);
userName.addEventListener("blur", validateInputs);
email.addEventListener("blur", validateInputs);
password.addEventListener("blur", validateInputs);
confirmPassword.addEventListener("input", validateInputs);

// check if user is offline
window.addEventListener('offline', () => {
    displayError("You are offline. Please check your internet connection.");
    continueButton.style.pointerEvents = "none";
    continueButton.style.opacity = "0.5";
});

// check if user is online
window.addEventListener('online', () => {
    displayError("You are back online. You can now continue.");
    continueButton.style.pointerEvents = "auto";
    continueButton.style.opacity = "1";
});

// Add click event for the continue button
continueButton.addEventListener("click", async (e) => {
    e.preventDefault();

    if(currentController){
        currentController.abort()
        currentController = null;
    };
    
    loadingAnimation.style.display = "flex";
    
    currentController = new AbortController();  //api request control
    
    userInfo.userName = userName.value;
    userInfo.userEmail = email.value;
    userInfo.userPassword = password.value;
    
    
    try{
        const timeout = setTimeout(() => {
            currentController.abort();
            displayError("Request timed out! Please try again.");
        }, 8000);
        const response = await fetch(signUpURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userInfo}),
            credentials: "include",
            signal: currentController.signal,
        })
        clearTimeout(timeout)
        
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

                const data = await response.json().catch(() => null); 
        if (data && data.status === "success" && data.userName && data.userEmail && data.access_token) {
            
            window.location.href = dashboardPage; // dashboard
            resetForm();
        } else {
            displayError("Signup failed");
            resetForm();
        }
    }
    catch (error){
        clearTimeout(timeout);
        if (error.name === "AbortError") {
            displayError("Request timeout.");
        }
        else if (error.message.includes("Failed to fetch")) {
            displayError("Unable to connect. Please check your internet connection.");
        }
        else if (!navigator.onLine) {
            setTimeout(() => {
                if (!navigator.onLine) {
                    window.location.reload();
                }
            }, 5000);
        }
        else {
            displayError("An unexpected error occurred.");
        }
        
        console.error("fetch Error:", error)
        displayError("Something went wrong! Please try again.");
    }
    finally {
        loadingAnimation.style.display = "none";
        clearTimeout(timeout)
    }
});