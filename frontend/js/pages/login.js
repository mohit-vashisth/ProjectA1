const email = document.querySelector("#email");
const password = document.querySelector("#password");
const login = document.querySelector("#login");
const errShow = document.querySelector("#errorDisplay");
const popupErr = document.querySelector(".popupErrors");
const loadingAnimation = document.querySelector(".loading");

let currentController = null;
let userLoginInfo = {
    email: "",
    password: ""
};

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
    
    if(currentController) currentController.abort();
    
    loadingAnimation.style.display = "flex";
    
    currentController = new AbortController();
    const signal = currentController.signal;


    try{

        const timeout = setTimeout(() => {
            currentController.abort();
            popupError("Request timed out! Please try again.");
        }, 8000);

        const response = await fetch("http://127.0.0.1:3002/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ userLoginInfo }),
            signal: signal,
        })
        clearTimeout(timeout);
        loadingAnimation.style.display = "none";

        if(!response.ok){
            popupError("Server not responding")
            setTimeout(() => {
                popupError("")
            }, 2000);
            return;
        }

        const data = await response.json()
        if(data.status === "success"){
            localStorage.setItem("userEmail", data.email)
            resetForm()
            window.location.href = "/frontend/pages/projectA1.html"
        }
        else{
            popupError("Invalid login credentials");
            setTimeout(() => popupError(""), 2500);
            resetForm()
        }
    }
    catch(error){
        loadingAnimation.style.display = "none";

        if(error.name === "AbortError"){
            console.error("Login request aborted!")
        }
        else{
            console.error("Fetch error:", error);
            popupError("Something went wrong! Please try again.");
            setTimeout(() => popupError(""), 2000);
        }
    }

})