import { displayError } from "../../src/javascript/utils/errorDisplay";
import { Signup } from "../../src/schemas/signupSchema";
import { initializePhoneInput } from "./signup/userContactjs";

const userName = document.querySelector("#name");
const email = document.querySelector("#email");
const password = document.querySelector("#password");
const confirmPassword = document.querySelector("#confirmPassword");
const contactNumber = document.querySelector("#contactNumber");
const continueButton = document.querySelector("#continue");
const errors = document.querySelector(".errors");
const loadingAnimation = document.querySelector(".loading");
const signinLink = document.querySelector("#signinLink");
const isPrivacyChecked = document.querySelector("#T_C_Privacy");

const signUpURL = import.meta.env.VITE_SIGNUP_EP;
const loginPage = import.meta.env.VITE_LOGIN_PAGE;
const dashboardPage = import.meta.env.VITE_DASHBOARD_PAGE;

let currentController = null;

document.addEventListener('DOMContentLoaded', () => {
    initializePhoneInput();
});

if (signinLink) {
    signinLink.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = loginPage;
    });
}

const validationCriteria = {
    userName: value => value.trim().length >= 2,
    email: value => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
    password: value => value.length >= 8,
    confirmPassword: value => value === password.value,
    contactNumber: value => value.replace(/\D/g, '').length >= 8,
    privacy: checked => checked
};

function updateButtonState(isValid) {
    continueButton.style.pointerEvents = isValid ? "auto" : "none";
    continueButton.style.cursor = isValid ? "pointer" : "not-allowed";
    continueButton.style.opacity = isValid ? "1" : "0.5";
}

function validateInputs() {
    const errorMessages = [];
    
    if (!validationCriteria.userName(userName.value)) {
        errorMessages.push("Name must be at least 2 characters");
    }

    if (!validationCriteria.email(email.value)) {
        errorMessages.push("Invalid email address");
    }

    if (!validationCriteria.password(password.value)) {
        errorMessages.push("Password must be 8+ characters");
    }

    if (!validationCriteria.confirmPassword(confirmPassword.value)) {
        errorMessages.push("Passwords do not match");
    }

    if (!validationCriteria.contactNumber(contactNumber.value)) {
        errorMessages.push("Invalid phone number");
    }

    if (!validationCriteria.privacy(isPrivacyChecked.checked)) {
        errorMessages.push("Must accept terms & privacy");
    }

    const isValid = errorMessages.length === 0;
    errors.textContent = errorMessages.join(" • ");
    updateButtonState(isValid);
    
    return isValid;
}

[userName, email, password, confirmPassword, contactNumber].forEach(input => {
    input.addEventListener('input', validateInputs);
});

isPrivacyChecked.addEventListener('change', validateInputs);


async function handleSignup() {
    if (currentController) currentController.abort();
    currentController = new AbortController();

    continueButton.style.pointerEvents = "none";
    continueButton.style.cursor = "not-allowed";
    continueButton.style.opacity = "0.5";

    const newUser = new Signup(
        userName.value.trim(),
        email.value.trim(),
        contactNumber.value.replace(/\D/g, ''),
        password.value,
        isPrivacyChecked.checked
    );

    try {
        loadingAnimation.style.display = "flex";
        document.body.style.cursor = "wait";
        
        const response = await fetch(signUpURL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            signal: currentController.signal,
            body: JSON.stringify(newUser)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Registration failed");
        }

        window.location.href = dashboardPage;
    } catch (error) {
        if (error.name !== "AbortError") {
            displayError(error.message);
        }
    } finally {
        loadingAnimation.style.display = "none";
        document.body.style.cursor = "default";
        currentController = null;
        validateInputs();
    }
}

continueButton.addEventListener("click", async (e) => {
    e.preventDefault();
    if (validateInputs()) await handleSignup();
});

window.addEventListener('offline', () => {
    displayError("Connection lost - working in offline mode");
    updateButtonState(false);
});

window.addEventListener('online', validateInputs);

// Form Reset
function resetForm() {
    userName.value = "";
    email.value = "";
    password.value = "";
    confirmPassword.value = "";
    contactNumber.value = "";
    isPrivacyChecked.checked = false;
    errors.textContent = "";
    validateInputs();
}