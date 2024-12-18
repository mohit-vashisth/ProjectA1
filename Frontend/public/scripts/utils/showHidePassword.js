const passwordInputs = document.querySelectorAll('.userPasswordInput, .userConfirmPasswordInput');
const showPasswordIcons = document.querySelectorAll('.ShowPassword, .ShowConfirmPassword');
const hidePasswordIcons = document.querySelectorAll('.passwordHideAuto, .confirmPasswordHideAuto');

function togglePasswordVisibility(index, show) {
    if (show) {
        passwordInputs[index].type = 'text';
        showPasswordIcons[index].style.display = 'none';
        hidePasswordIcons[index].style.display = 'inline';
        
        setTimeout(() => togglePasswordVisibility(index, false), 3000);
    } else {
        passwordInputs[index].type = 'password';
        showPasswordIcons[index].style.display = 'inline';
        hidePasswordIcons[index].style.display = 'none';
    }
}

showPasswordIcons.forEach((icon, index) => {
    icon.addEventListener('click', () => togglePasswordVisibility(index, true));
    hidePasswordIcons[index].style.display = 'none';
});

hidePasswordIcons.forEach((icon, index) => {
    icon.addEventListener('click', () => togglePasswordVisibility(index, false));
});
