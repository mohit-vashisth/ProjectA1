const popupErr = document.querySelector(".errorPopup");

export function displayError(text, time = 2000) {
    popupErr.textContent = text;
    popupErr.style.width = "30vmin";
    popupErr.style.padding = "1vmin";
    setTimeout(() => {
      popupErr.style.width = "0";
      popupErr.style.padding = "0";
    }, time);
}