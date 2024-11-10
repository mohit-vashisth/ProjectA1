const nameInputSignUp = document.getElementById("userNameSignUpID");
const emailInputSignUp = document.getElementById("userEmailSignUpID");
const passwordInputSignUp = document.getElementById("userPasswordInputID");
const confirmPasswordInputSignUp = document.getElementById("userConfirmPasswordInputID");
const errorMessage = document.getElementById("errorMessage");

emailInputSignUp.addEventListener('blur', function() {
    let emailValue = emailInputSignUp.value.trim();
    if (emailValue && !emailValue.includes('@')) {
        emailInputSignUp.value = `${emailValue}@gmail.com`;
    }
});

document.querySelector(".createButton").addEventListener("click", function () {
    errorMessage.style.display = "none";
    errorMessage.textContent = "";

    const name = nameInputSignUp.value.trim();
    const email = emailInputSignUp.value.trim();
    const password = passwordInputSignUp.value;
    const confirmPassword = confirmPasswordInputSignUp.value;

    if (name === "") {
        errorMessage.textContent = "Name is required.";
        errorMessage.style.display = "block";
        nameInputSignUp.focus();
        return;
    }

    const emailPattern = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
    if (!emailPattern.test(email)) {
        errorMessage.textContent = "Please enter a valid Gmail address.";
        errorMessage.style.display = "block";
        emailInputSignUp.focus();
        return;
    }

    if (password !== confirmPassword) {
      errorMessage.textContent = "Passwords do not match.";
      errorMessage.style.display = "block";
      confirmPasswordInputSignUp.focus();
      return;
    }

    if (password === "") {
        errorMessage.textContent = "Password is required.";
        errorMessage.style.display = "block";
        passwordInputSignUp.focus();
        return;
    }

    if (password.length < 8) {
        errorMessage.textContent = "Password must be at least 8 characters long.";
        errorMessage.style.display = "block";
        passwordInputSignUp.focus();
        return;
    }

    if (!/[A-Za-z]/.test(password)) {
        errorMessage.textContent = "Password must contain at least one letter.";
        errorMessage.style.display = "block";
        passwordInputSignUp.focus();
        return;
    }

    if (!/\d/.test(password)) {
        errorMessage.textContent = "Password must contain at least one number.";
        errorMessage.style.display = "block";
        passwordInputSignUp.focus();
        return;
    }

    if (confirmPassword === "") {
        errorMessage.textContent = "Please confirm your password.";
        errorMessage.style.display = "block";
        confirmPasswordInputSignUp.focus();
        return;
    }

    nameInputSignUp.value = "";
    emailInputSignUp.value = "";
    passwordInputSignUp.value = "";
    confirmPasswordInputSignUp.value = "";
});
