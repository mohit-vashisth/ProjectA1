const userName = document.querySelector("#name");
const email = document.querySelector("#email");
const password = document.querySelector("#password");
const confirmPassword = document.querySelector("#confirmPassword");
const continueButton = document.querySelector("#continue");
const errors = document.querySelector(".errors"); 
const popupErr = document.querySelector(".popupErrors");
const loadingAnimation = document.querySelector(".laoding");

let currentController = null;
let userInfo = {
    userName: "",
    userEmail: "",
    userPassowrd: ""
}

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

// Add click event for the continue button
continueButton.addEventListener("click", async (e) => {
    e.preventDefault();

    if (continueButton.style.pointerEvents === "none") return;

    if(currentController) currentController.abort();

    loadingAnimation.style.display = "flex";
    
    currentController = new AbortController();
    const signal = currentController.signal;

    userInfo.userName = userName.value;
    userInfo.userEmail = email.value;
    userInfo.userPassowrd = password.value;
    

    try{
        const timeout = setTimeout(() => {
            currentController.abort();
            popupError("Request timed out! Please try again.");
        }, 8000);
        const response = await fetch("http://127.0.0.1:3002/api/signup", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userInfo}),
            signal: signal,
        })
        clearTimeout(timeout)

        loadingAnimation.style.display = "none";

        if(!response.ok){
            popupError("Server is not responding");
            setTimeout(()=>{popupError("")}, 2000)
            return;
        }

        const data = await response.json()
        if (data.status === "success") {
            localStorage.setItem("userName", data.userName);
            localStorage.setItem("userEmail", data.userEmail);
            window.location.href = "/frontend/pages/projectA1.html";
        } else {
            popupError("Signup failed");
            setTimeout(() => popupError(""), 2500);
            resetForm();
        }
    }
    catch (error){
        if(error.name === "AbortError"){
            console.error("Login request aborted!")
        }
        console.error("fetch Error:", error)
        popupError("Something went wrong! Please try again.");
        setTimeout(() => popupError(""), 2000);
    }
});
