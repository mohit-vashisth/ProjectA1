const passwordInput = document.querySelector('.userConfirmPasswordInput');
const showPasswordIcon = document.querySelector('.showPasswordIcon');
const hidePasswordIcon = document.querySelector('.hidePasswordIcon');

let hidePasswordTimeout;

function showPassword() {
    passwordInput.type = 'text';
    showPasswordIcon.style.display = 'none';
    hidePasswordIcon.style.display = 'inline';

    // Clear any existing timeout to prevent double calls
    clearTimeout(hidePasswordTimeout);

    // Set timeout to hide password after 2 seconds
    hidePasswordTimeout = setTimeout(hidePassword, 2000);
}

function hidePassword() {
    passwordInput.type = 'password';
    showPasswordIcon.style.display = 'inline';
    hidePasswordIcon.style.display = 'none';

    // Clear the timeout in case hidePassword is called manually
    clearTimeout(hidePasswordTimeout);
}

// Event listeners for show/hide functionality
showPasswordIcon.addEventListener('click', showPassword);
hidePasswordIcon.addEventListener('click', hidePassword);
