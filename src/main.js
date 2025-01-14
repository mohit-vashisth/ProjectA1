const exploreProjectA1 = document.getElementById("exploreProjectA1");
const privacyLink = document.querySelector(".footer-link")
const tryProjectA1 = document.querySelector(".tryProjectA1")
const formName = document.querySelector(".formName")
const formEmail = document.querySelector(".formEmail")
const formText = document.querySelector(".formText")
const submitForm = document.querySelector(".submitForm")

exploreProjectA1.addEventListener("click", (e) => {
    e.preventDefault()
    window.location.href = "/frontend/pages/signup.html";
});


privacyLink.addEventListener("click", (e)=>{
    e.preventDefault()
    window.location.href = "/frontend/pages/about/legalInformation.html"
})

tryProjectA1.addEventListener("click", (e)=>{
    e.preventDefault()
    window.location.href = "/frontend/pages/signup.html";
})
