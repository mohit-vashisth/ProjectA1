const mainWebsiteLink = document.querySelector(".mainWebsite")

mainWebsiteLink.addEventListener("click", (e)=>{
    e.preventDefault()
    window.location.href = "/index.html"
})