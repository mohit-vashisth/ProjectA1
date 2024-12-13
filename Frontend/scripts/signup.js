import ApiService from '../services/apiService.js';

document.querySelector(".createButton").addEventListener("click", async function () {
    try {
        const userData = {
            name: nameInputSignUp.value.trim(),
            email: emailInputSignUp.value.trim(),
            password: passwordInputSignUp.value
        };

        const response = await ApiService.registerUser(userData);
        
        if (response.token) {
            localStorage.setItem('token', response.token);
            localStorage.setItem('user', JSON.stringify(response.user));
            window.location.href = '/Frontend/pages/home.html';
        }
    } catch (error) {
        errorMessage.textContent = error.message;
        errorMessage.style.display = "block";
    }
});

// Google Login Integration
document.querySelector('.googleLoginSystem').addEventListener('click', async () => {
    try {
        window.location.href = `${BASE_URL}/auth/google`;
    } catch (error) {
        console.error('Google login error:', error);
        errorMessage.textContent = "Google login failed";
        errorMessage.style.display = "block";
    }
}); 