const popupErr = document.querySelector(".errorPopup");
const popupErrText = document.querySelector(".errorPopup p");

export function displayError(text = "", time = 3000) {
  popupErrText.textContent = text;
  popupErr.style.transform = "translateY(3.5vmin)";
  popupErr.style.opacity = "1";
  
  setTimeout(() => {
    popupErrText.textContent = "";
    popupErr.style.transform = "translateY(0)";
    popupErr.style.opacity = "0";
  }, time);
}