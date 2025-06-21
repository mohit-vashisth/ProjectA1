const validationCriteria = {
    userName: value => value.trim().length >= 2,
    email: value => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
    password: value => value.length >= 8,
    confirmPassword: value => value === password.value,
    contactNumber: value => value.replace(/\D/g, '').length >= 8,
    privacy: checked => checked
};

export function validateInputs() {
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