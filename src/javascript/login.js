const email = document.querySelector("#email");
const password = document.querySelector("#password");
const login = document.querySelector("#login");
const errShow = document.querySelector("#errorDisplay");
const popupErr = document.querySelector(".popupErrors");
const loadingAnimation = document.querySelector(".loading");
const loginURL = import.meta.env.VITE_LOGIN_URL;
const baseURL = import.meta.env.VITE_BASE_URL;

let currentController = null;
let userLoginInfo = {
    email: "",
    password: ""
};
document.addEventListener('DOMContentLoaded', () => {
    const link = document.createElement('link'); // Create a <link> element
    link.rel = 'stylesheet'; // Set the relationship as "stylesheet"
    link.href = '/frontend/css/pages/signin.css'; // Path to your CSS file
    document.head.appendChild(link); // Append the <link> to the <head>
});

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

function clearErrorPopup() {
    setTimeout(() => errorPopup(""), 2000);
}

function resetForm() {
    password.value = "";
}

function validateFields() {
    const isEmailValid = email.value.trim() !== "";
    const isPasswordValid = password.value.trim() !== "";
    
    if (isEmailValid && isPasswordValid) {
        login.style.pointerEvents = "auto";
        login.style.opacity = "1";
    } else {
        login.style.pointerEvents = "none";
        login.style.opacity = "0.5";
    }
}

email.addEventListener("blur", validateFields);
password.addEventListener("input", validateFields);

login.addEventListener('click', async (event)=>{
    event.preventDefault()

    if (login.style.pointerEvents === "none") return;

    userLoginInfo.email = email.value;
    userLoginInfo.password = password.value;
    
    if(currentController){
        currentController.abort()
        currentController = null;
    };
    
    loadingAnimation.style.display = "flex";
    
    currentController = new AbortController();

    try{

        const timeout = setTimeout(() => {
            currentController.abort();
            popupError("Request timed out! Please try again.");
            clearErrorPopup();
            loadingAnimation.style.display = "none"
        }, 8000);

        const response = await fetch(loginURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ userLoginInfo }),
            signal: currentController.signal,
        })
        clearTimeout(timeout);
        loadingAnimation.style.display = "none";

        if(!response.ok){
            popupError("Server not responding")
            clearErrorPopup();
            loadingAnimation.style.display = "none";
            return;
        }

        const data = await response.json().catch(()=> null);
        if(data?.success && data.email && data.access_token){
            window.location.href = baseURL;
            resetForm()
        }
        else{
            popupError("Invalid login credentials");
            clearErrorPopup();
            resetForm()
        }
    }
    catch(error){
        loadingAnimation.style.display = "none";
        clearTimeout(timeout);
        if(error.name === "AbortError"){
            console.error("Login request aborted!")
        }
        else{
            console.error("Fetch error:", error);
            popupError("Something went wrong! Please try again.");
            clearErrorPopup();
        }
    }
})