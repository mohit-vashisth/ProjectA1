const userNameInput = document.querySelector(".userNameInput");
const userEmailInput = document.querySelector(".userEmailInput");
const userPasswordInput = document.querySelector(".userPasswordInput");
const userConfirmPasswordInput = document.querySelector(".userConfirmPasswordInput");
const passwordConfirmPasswordContainerP = document.querySelector(".passwordConfirmPasswordContainerP");
const continueLoginButton = document.querySelector(".continueLoginButton");

let userData = {
    userName: "",
    userEmail: "",
    userPassword: "",
    userConfirmPassword: ""
}

// Function to show error messages
function showError(message) {
    passwordConfirmPasswordContainerP.innerHTML = message;
}

// Username validation
userNameInput.addEventListener("blur", function() {
    if (userNameInput.value.trim() === "") {
        showError("Name is required");
    } else {
        showError("");
    }
});

// Email validation (Add better validation)
userEmailInput.addEventListener("blur", function() {
    if (!userEmailInput.value.includes("@") || !userEmailInput.value.includes(".")) {
        showError("Please enter a valid email");
    } else {
        showError("");
    }
});

// Password validation (Check length and strength)
userPasswordInput.addEventListener("blur", function() {
    const password = userPasswordInput.value.trim();
    if (password === "") {
        showError("Password is required");
    } else if (password.length < 6) {
        showError("Password must be at least 6 characters long");
    } else if (!/[A-Z]/.test(password) || !/[!@#$%^&*]/.test(password)) {
        showError("Password must contain an uppercase letter and a special character");
    } else {
        showError("");
    }
});

// Confirm password validation
userConfirmPasswordInput.addEventListener("blur", function() {
    if (userPasswordInput.value !== userConfirmPasswordInput.value) {
        showError("Passwords do not match");
    } else {
        showError("");
    }
});

// Handling form submission
continueLoginButton.addEventListener("click", function(event) {
    event.preventDefault();
    
    // Basic validation before sending data
    if (!userNameInput.value.trim() || !userEmailInput.value.trim() || !userPasswordInput.value.trim() || !userConfirmPasswordInput.value.trim()) {
        showError("Please fill all the fields correctly");
        return; // Stop further execution if fields are not valid
    }

    // If all fields are valid, collect data
    userData.userName = userNameInput.value;
    userData.userEmail = userEmailInput.value;
    userData.userPassword = userPasswordInput.value;
    userData.userConfirmPassword = userConfirmPasswordInput.value;
    
    // Optionally: Submit to backend here via AJAX/fetch

});
