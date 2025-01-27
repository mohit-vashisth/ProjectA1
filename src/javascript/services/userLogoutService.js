import { displayError } from "../utils/errorDisplay";

const logoutPopupContainer = document.querySelector(".logoutPopupContainer");
const logoutIcon = document.querySelector(".logoutIcon");
const noButton = document.querySelector(".noButton");
const logout = document.querySelector("#logout");
const baseURL = import.meta.env.VITE_BASE_URL;
let currentController = null;
let timeoutID;

logoutIcon.addEventListener("click", function () {
    logoutPopupContainer.style.display = "flex";
});

noButton.addEventListener("click", function () {
    logoutPopupContainer.style.display = "none";
});

async function logoutUser() {
  if (!logout && !logoutPopupContainer) displayError("something went wrong");


  document.addEventListener("click", function (event) {
    if (
      !popupContainer.contains(event.target) &&
      event.target !== logoutButton
    ) {
      popupContainer.style.display = "none";
    }
  });
  if (currentController) {
    currentController.abort();
    currentController = null;
  }

  currentController = new AbortController();

    try {
        const response = await fetch(`${baseURL}/logout`, {
        method: "POST",
        credentials: "include",
        signal: currentController.signal,
        });
        clearTimeout(timeoutID);

        if (!response.ok) {
            displayError("unable to logout");
        }

        const data = await response.json();
        if (data && data.status) {
            localStorage.removeItem("access_token");
            window.location.href = "/frontend/pages/auth/login.html";
        } else {
            displayError("something went wrong, unable to logout");
        }
    } catch (error) {
        clearTimeout(timeoutID);
        if (error.name === "AbortError") {
            displayError("Request aborted");
        }
        displayError("Something went wrong");
  }
}

export function logoutUserEXP() {
  logout.addEventListener('click', logoutUser)
}