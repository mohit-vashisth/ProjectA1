//  Imports
import { displayError } from "../../src/javascript/utils/errorDisplay";
import { initializePhoneInput } from "./signup/userContactjs";
//  G-variables
const userName = document.querySelector("#name");
const email = document.querySelector("#email");
const password = document.querySelector("#password");
const confirmPassword = document.querySelector("#confirmPassword");
const contactNumber = document.querySelector("#contactNumber");
const countryCode = document.querySelector("#countryCode");
const continueButton = document.querySelector("#continue");
const errors = document.querySelector(".errors");
const loadingAnimation = document.querySelector(".loading");
const signinLink = document.querySelector("#signinLink");
const isPrivacyChecked = document.querySelector("#T_C_Privacy");
const signUpURL = import.meta.env.VITE_SIGNUP_EP;
const loginPage = import.meta.env.VITE_LOGIN_PAGE;
const dashboardPage = import.meta.env.VITE_DASHBOARD_PAGE;

let currentController = null;
let userInfo = {
    userName: null,
    userEmail: null,
    ContactNumber: null,
    userPassword: null,
    timeZone: null,
    privacyCheck: null,
};

// user side signin form
if (signinLink) {
    signinLink.addEventListener('click', (event) => {
        event.preventDefault();
        window.location.href = loginPage;
    });
}

document.addEventListener('DOMContentLoaded', ()=>{
    initializePhoneInput()
})

// continue button initial state
continueButton.style.pointerEvents = "none";
continueButton.style.opacity = "0.5";

// error display inside user's form
function errorDisplay(error) {
    errors.textContent = error;
    errors.style.color = "red";
}

// reset form after successful or failed login
function resetForm() {
    password.value = "";
    confirmPassword.value = "";
    contactNumber.value = "";
}

// Email validation function
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidContactNumber() {
    const phoneNumber = contactNumber.value.trim();
    return phoneNumber.length > 5;
}

// Function to check if all inputs are valid
function validateInputs() {
    const isUserNameValid = userName.value.trim() !== "";
    const isEmailValid = isValidEmail(email.value.trim());
    const isPasswordValid = password.value.trim() !== "";
    const isConfirmPasswordValid = confirmPassword.value.trim() !== "" && confirmPassword.value === password.value;
    const isPrivacyCheckedValid = isPrivacyChecked.checked; // Check if privacy policy is agreed
    const isContactNumberValid = isValidContactNumber();
    userInfo.privacyCheck = isPrivacyCheckedValid

    if (!isContactNumberValid) {
        errorDisplay("Contact number cannot be empty.");
    }

    // Enable the button if all inputs are valid
    if (isUserNameValid && isEmailValid && isPasswordValid && isConfirmPasswordValid && isContactNumberValid && isPrivacyCheckedValid) {
        continueButton.style.pointerEvents = "auto";
        continueButton.style.opacity = "1";
        errorDisplay("");
        return true;
    } else {
        continueButton.style.pointerEvents = "none";
        continueButton.style.opacity = "0.5";
        errorDisplay("Please fill out all fields correctly.");
        return false;
    }

}

// Add event listeners to all input fields
isPrivacyChecked.addEventListener("change", validateInputs);
userName.addEventListener("blur", validateInputs);
email.addEventListener("blur", validateInputs);
password.addEventListener("blur", validateInputs);
confirmPassword.addEventListener("input", validateInputs);
contactNumber.addEventListener("blur", validateInputs);

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

    // Prevent multiple submissions
    continueButton.disabled = true;

    if (!validateInputs()) {
        continueButton.disabled = false;
        return;
    }

    if (currentController) {
        currentController.abort();
        currentController = null;
    }

    loadingAnimation.style.display = "flex";
    
    currentController = new AbortController(); // API request control
    
    userInfo.userName = userName.value;
    userInfo.userEmail = email.value;
    userInfo.ContactNumber = await initializePhoneInput();
    userInfo.userPassword = password.value;
    userInfo.timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    try {
        const timeout = setTimeout(() => {
            currentController.abort();
            displayError("Request timed out! Please try again.");
        }, 8000);

        const response = await fetch(signUpURL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            signal: currentController.signal,
            body: JSON.stringify(userInfo),
        });
        clearTimeout(timeout);

        const data = await response.json();
        if (!response.ok) {
            const errorDetails = data?.detail || "Something went wrong. Try again.";
            switch (response.status) {
                case 400:
                    displayError(errorDetails || "Invalid input. Please check your text or voice selection.");
                    break;
                case 401:
                    displayError(errorDetails || "You are not logged in. Please log in and try again.");
                    break;
                case 404:
                    displayError(errorDetails || "The requested resource was not found.");
                    break;
                case 409:
                    displayError(errorDetails || "Email id already in use.");
                    break;
                case 500:
                    displayError(errorDetails || "A server error occurred. Please try again later.");
                    break;
                default:
                    displayError(errorDetails);
            }
            continueButton.disabled = false;
            return;
        }

        if (data.message === "User signed up successfully") {
            window.location.href = dashboardPage;
            resetForm();
        } else {
            displayError("Signup failed. Please try again.");
        }
        
    } catch (error) {
        if (error.name === "AbortError") {
            displayError("Request timeout.");
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
    } finally {
        loadingAnimation.style.display = "none";
        resetForm();
        continueButton.disabled = false;
    }
});