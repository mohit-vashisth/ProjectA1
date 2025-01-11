const userName = document.querySelector("#name");
const email = document.querySelector("#email");
const password = document.querySelector("#password");
const confirmPassword = document.querySelector("#confirmPassword");
const continueButton = document.querySelector("#continue");
const errors = document.querySelector(".errors"); 
const popupErr = document.querySelector(".popupErrors");
const loadingAnimation = document.querySelector(".loading");
const signinLink = document.querySelector("#signinLink");

let currentController = null;
let userInfo = {
    userName: "",
    userEmail: "",
    userPassword: ""
}

if(signinLink){
    signinLink.addEventListener('click', (event)=>{
        event.preventDefault()
        window.location.href = "/frontend/pages/auth/login.html";
    })
}

document.addEventListener('DOMContentLoaded', () => {
    const link = document.createElement('link'); // Create a <link> element
    link.rel = 'stylesheet'; // Set the relationship as "stylesheet"
    link.href = '/frontend/css/pages/signup.css'; // Path to your CSS file
    document.head.appendChild(link); // Append the <link> to the <head>
});


continueButton.style.pointerEvents = "none";
continueButton.style.opacity = "0.5"; // Optional: To visually indicate it's disabled

function errorDisplay(error) {
    errors.textContent = error;
    errors.style.color = "red"; // Optional: Add styling for visibility
}
function popupError(error) {
    if(error !== ""){
        popupErr.textContent = error;
        popupErr.style.width = "30vmin";
        popupErr.style.padding = "1vmin";
    } else{
        popupErr.style.width = "0";
        popupErr.style.padding = "0";
    }
}

function resetForm(){
    userName.value = "",
    email.value = ""
}

// Function to check if all inputs are valid
function validateInputs() {
    const isUserNameValid = userName.value.trim() !== "";
    const isEmailValid = email.value.trim() !== "";
    const isPasswordValid = password.value.trim() !== "";
    const isConfirmPasswordValid = confirmPassword.value.trim() !== "" && confirmPassword.value === password.value;

    // Enable the button if all inputs are valid
    if (isUserNameValid && isEmailValid && isPasswordValid && isConfirmPasswordValid) {
        continueButton.style.pointerEvents = "auto";
        continueButton.style.opacity = "1";
        errorDisplay("");
        return true
    } else {
        continueButton.style.pointerEvents = "none";
        continueButton.style.opacity = "0.5"; // Optional: Make it look disabled
    }
}

// Add event listeners to all input fields
userName.addEventListener("blur", validateInputs);
email.addEventListener("blur", validateInputs);
password.addEventListener("blur", validateInputs);
confirmPassword.addEventListener("input", validateInputs);

window.addEventListener('offline', () => {
    popupError("You are offline. Please check your internet connection.");
    continueButton.style.pointerEvents = "none";
    continueButton.style.opacity = "0.5";
});

window.addEventListener('online', () => {
    popupError("You are back online. You can now continue.");
    continueButton.style.pointerEvents = "auto";
    continueButton.style.opacity = "1";
});
// Add click event for the continue button
continueButton.addEventListener("click", async (e) => {
    e.preventDefault();

    if(currentController) currentController.abort();

    loadingAnimation.style.display = "flex";
    
    currentController = new AbortController();
    const signal = currentController.signal;

    userInfo.userName = userName.value;
    userInfo.userEmail = email.value;
    userInfo.userPassword = password.value;
    

    try{
        const timeout = setTimeout(() => {
            currentController.abort();
            popupError("Request timed out! Please try again.");
            setTimeout(()=>{popupError("")}, 2000)
            loadingAnimation.style.display = "none"
        }, 8000);
        const response = await fetch("http://127.0.0.1:3000/api/signup", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userInfo}),
            signal: signal,
            credentials: "include",
        })
        clearTimeout(timeout)
        loadingAnimation.style.display = "none";

        if(!response.ok){
            popupError("Server is not responding");
            setTimeout(()=>{popupError("")}, 2000)
            loadingAnimation.style.display = "none";
            return;
        }

        const data = await response.json().catch(() => null); 
        if (data && data.status === "success" && data.userName && data.userEmail && data.access_token) {
            
            /*
            using cooking instead of localStorage

            localStorage.setItem("userName", data.userName);
            localStorage.setItem("userEmail", data.userEmail);
            localStorage.setItem("access_token", data.access_token);
            */
            window.location.href = "/frontend/pages/projectA1.html";
            resetForm();
        } else {
            popupError("Signup failed");
            setTimeout(() => popupError(""), 2500);
            loadingAnimation.style.display = "none";
            resetForm();
        }
    }
    catch (error){
        clearTimeout(timeout);
        if(error.name === "AbortError"){
            console.error("Login request aborted!")
        }
        if (!navigator.onLine) {
            setTimeout(() => {
                if (!navigator.onLine) {
                    window.location.reload();
                }
            }, 5000);
        }
        
        console.error("fetch Error:", error)
        popupError("Something went wrong! Please try again.");
        setTimeout(() => popupError(""), 2000);
    }
});
