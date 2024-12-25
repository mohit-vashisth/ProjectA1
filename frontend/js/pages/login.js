const userLoginEmail = document.querySelector('.userLoginEmail');
const userPasswordInput = document.querySelector('.userPasswordInput');
const continueLoginButton = document.querySelector('.continueLoginButton');
const displayError = document.querySelector('.passwordConfirmPasswordContainerP');

function checkPasswordInDataBase(event) {
    event.preventDefault();

    const email = userLoginEmail.value.trim();
    const password = userPasswordInput.value.trim();

    if (!email || !password) {
        displayError.textContent = 'Both email and password are required.';
        displayError.style.color = 'red';
        return;
    } else {
        displayError.textContent = '';
    }

    // Fetch request to backend
    fetch('http://127.0.0.1:5000/api/users/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.status === 'success') {
                alert('Login successful!');
                window.location.href = '/home';
            } else {
                displayError.textContent = data.message || 'Invalid login credentials.';
                displayError.style.color = 'red';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            displayError.textContent = 'An error occurred while logging in. Please try again.';
            displayError.style.color = 'red';
        });
    
}

continueLoginButton.addEventListener('click', checkPasswordInDataBase);
