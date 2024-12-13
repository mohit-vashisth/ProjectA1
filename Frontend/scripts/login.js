import ApiService from '../services/apiService.js';

document.querySelector(".loginButton").addEventListener("click", async function () {
    try {
        const credentials = {
            email: document.getElementById('userEmailSignUpID').value.trim(),
            password: document.getElementById('userPasswordInputID').value
        };

        const response = await ApiService.loginUser(credentials);
        
        if (response.token) {
            localStorage.setItem('token', response.token);
            localStorage.setItem('user', JSON.stringify(response.user));
            window.location.href = '/Frontend/pages/home.html';
        }
    } catch (error) {
        document.getElementById('errorMessageLogin').textContent = error.message;
        document.getElementById('errorMessageLogin').style.display = "block";
    }
}); 