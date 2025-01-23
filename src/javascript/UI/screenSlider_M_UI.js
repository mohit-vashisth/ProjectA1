const slideBar = document.querySelector('.slider');
const leftSection = document.querySelector('.leftMain');

export function slideMobileEXP() {
    slideBar.addEventListener("click", ()=>{
        if(leftSection.style.width === "50%"){
            leftSection.style.width = "0%";
        } else{
            leftSection.style.width = "50%"
        }
    })
}