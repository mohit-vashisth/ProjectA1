const popupErr = document.querySelector(".errorPopup");
const popupErrText = document.querySelector(".errorPopup p");

export function displayError(text, time = 2000) {
  popupErrText.textContent = text;
  popupErr.style.width = "auto";
  popupErrText.style.padding = "50px";
  setTimeout(() => {
    popupErrText.textContent = "";
    popupErrText.style.padding = "0";
  }, time);
}