const email = document.querySelector("#email");
const password = document.querySelector("#password");
const login = document.querySelector("#login");
const errShow = document.querySelector("#errorDisplay");

let userLoginInfo = {
    email: "",
    password: ""
};

function errorDisplay(err) {
    if (err !== "") {
        errShow.textContent = err;
    } else {
        errShow.textContent = "";
    }
}

function resetForm() {
    email.value = "";
    password.value = "";
}

function validateFields() {
    const isEmailValid = email.value.trim() !== "";
    const isPasswordValid = password.value.trim() !== "";
    if (isEmailValid && isPasswordValid) {
        login.style.pointerEvents = "auto";
        login.style.opacity = "1";
        errorDisplay("");
        return true;
    } else {
        login.style.pointerEvents = "none";
        login.style.opacity = "0.5";
    }
}

email.addEventListener("blur", validateFields);
password.addEventListener("input", validateFields);

login.addEventListener('click', ()=>{
    
})