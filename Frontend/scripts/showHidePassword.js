const passwordInput = document.querySelector('.userPasswordInput');
const showPasswordIcon = document.querySelector('.ShowPassword');
const hidePasswordIcon = document.querySelector('.passwordHideAuto');

let hidePasswordTimeout;

function showPassword() {
    passwordInput.type = 'text';
    showPasswordIcon.style.display = 'none';
    hidePasswordIcon.style.display = 'inline';

    hidePasswordTimeout = setTimeout(hidePassword, 2000);
}

function hidePassword() {
    passwordInput.type = 'password';
    showPasswordIcon.style.display = 'inline';
    hidePasswordIcon.style.display = 'none';
    
    clearTimeout(hidePasswordTimeout);
}

showPasswordIcon.addEventListener('click', showPassword);
hidePasswordIcon.addEventListener('click', hidePassword);

hidePasswordIcon.style.display = 'none';
showPasswordIcon.style.display = 'inline';
