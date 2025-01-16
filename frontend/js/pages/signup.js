//  G-variables
const userName = document.querySelector("#name");
const email = document.querySelector("#email");
const password = document.querySelector("#password");
const confirmPassword = document.querySelector("#confirmPassword");
const continueButton = document.querySelector("#continue");
const errors = document.querySelector(".errors"); 
const popupErr = document.querySelector(".popupErrors");
const loadingAnimation = document.querySelector(".loading");
const signinLink = document.querySelector("#signinLink");
const isPrivacyChecked = document.querySelector("#T_C_Privacy")
const baseURL = import.meta.env.VITE_BASE_URL;

let currentController = null;
let userInfo = {
    userName: "",
    userEmail: "",
    userPassword: ""
}

// user side signin form
if(signinLink){
    signinLink.addEventListener('click', (event)=>{
        event.preventDefault()
        window.location.href = "/frontend/pages/auth/login.html";
    })
}

// css dynamic inject
document.addEventListener('DOMContentLoaded', () => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/frontend/css/pages/signup.css';
    document.head.appendChild(link);
});

// continue button initial state
continueButton.style.pointerEvents = "none";
continueButton.style.opacity = "0.5";

// error display inside user's form
function errorDisplay(error) {
    errors.textContent = error;
    errors.style.color = "red";
}

// popup form of error right top corner display
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

// clearing popup 2sec time
function clearErrorPopup(time) {
    setTimeout(() => errorPopup(""), time);
}

// reset form after successfull or fail login
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
    const isPrivacyCheckedValid = isPrivacyChecked.checked; // Check if privacy policy is agreed

    // Enable the button if all inputs are valid
    if (isUserNameValid && isEmailValid && isPasswordValid && isConfirmPasswordValid && isPrivacyCheckedValid) {
        continueButton.style.pointerEvents = "auto";
        continueButton.style.opacity = "1";
        errorDisplay("");
        return true;
    } else {
        continueButton.style.pointerEvents = "none";
        continueButton.style.opacity = "0.5"; // Optional: Make it look disabled
    }
}

// Add event listeners to all input fields
isPrivacyChecked.addEventListener("change", validateInputs);
userName.addEventListener("blur", validateInputs);
email.addEventListener("blur", validateInputs);
password.addEventListener("blur", validateInputs);
confirmPassword.addEventListener("input", validateInputs);

// check if user is offline
window.addEventListener('offline', () => {
    popupError("You are offline. Please check your internet connection.");
    continueButton.style.pointerEvents = "none";
    continueButton.style.opacity = "0.5";
});

// check if user is online
window.addEventListener('online', () => {
    popupError("You are back online. You can now continue.");
    continueButton.style.pointerEvents = "auto";
    continueButton.style.opacity = "1";
});

// Add click event for the continue button
continueButton.addEventListener("click", async (e) => {
    e.preventDefault();

    if(currentController){
        currentController.abort()
        currentController = null;
    };

    loadingAnimation.style.display = "flex";

    currentController = new AbortController();  //api request control

    userInfo.userName = userName.value;
    userInfo.userEmail = email.value;
    userInfo.userPassword = password.value;
    

    try{
        const timeout = setTimeout(() => {
            currentController.abort();
            popupError("Request timed out! Please try again.");
            loadingAnimation.style.display = "none"
            clearErrorPopup(2000)
        }, 8000);
        const response = await fetch(`${baseURL}/api/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userInfo}),
            credentials: "include",
            signal: currentController.signal,
        })
        clearTimeout(timeout)
        loadingAnimation.style.display = "none";

        if(!response.ok){
            popupError("Server is not responding");
            clearErrorPopup(2000)
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
            window.location.href = "/frontend/pages/projectA1.html"; // dashboard
            resetForm();
        } else {
            popupError("Signup failed");
            clearErrorPopup(2000)
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
        clearErrorPopup(2000)
    }
});
