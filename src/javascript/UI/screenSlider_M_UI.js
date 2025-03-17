const slideBar = document.querySelector('.slider');
const leftSection = document.querySelector('.leftMain');
const rightSection = document.querySelector('.rightMain');
const closeCross = document.querySelector('.closeLeftMainContainer img');

export function slideMobileEXP() {
    slideBar.addEventListener("click", ()=>{
        if(leftSection.style.width === "100%"){
            leftSection.style.width = "0%";
            rightSection.style.pointerEvents = "auto"; 
            rightSection.style.opacity = 1;
        } else{
            leftSection.style.width = "100%"
            rightSection.style.pointerEvents = "none"; 
            rightSection.style.opacity = 0.1;
        }
    })
    closeCross.addEventListener("click", ()=>{
        if(leftSection.style.width === "100%"){
            leftSection.style.width = "0%";
            rightSection.style.pointerEvents = "auto"; 
            rightSection.style.opacity = 1;
        } else{
            leftSection.style.width = "100%"
            rightSection.style.pointerEvents = "none"; 
            rightSection.style.opacity = 0.1;
        }
    })
}