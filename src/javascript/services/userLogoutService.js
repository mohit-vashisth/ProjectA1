import { displayError } from "../utils/errorDisplay";

const logoutPopupContainer = document.querySelector(".logoutPopupContainer");
const logoutIcon = document.querySelector(".logoutIcon");
const noButton = document.querySelector(".noButton");
const logout = document.querySelector("#logout");

const userLogoutURL = import.meta.env.VITE_LOGOUT_EP;
const loginPageURL = import.meta.env.VITE_LOGIN_PAGE;

let currentController = null;

logoutIcon.addEventListener("click", () => {
  logoutPopupContainer.style.display = "flex";
});

noButton.addEventListener("click", () => {
  logoutPopupContainer.style.display = "none";
});

document.addEventListener("click", (event) => {
  if (!logoutPopupContainer.contains(event.target) && event.target !== logoutIcon) {
    logoutPopupContainer.style.display = "none";
  }
});

async function logoutUser() {
  if (!logout || !logoutPopupContainer) {
    displayError("Something went wrong");
    return;
  }

  if (currentController) {
    currentController.abort();
    currentController = null;
  }

  currentController = new AbortController();

  try {
    const timeoutID = setTimeout(() => {
      currentController.abort();
      displayError("Request timeout.");
    }, 8000);

    const response = await fetch(userLogoutURL, {
      method: "POST",
      credentials: "include",
      signal: currentController.signal,
    });

    clearTimeout(timeoutID);

    const data = await response.json();
    if (!response.ok || !data?.status) {
      displayError(data?.detail || "Something went wrong, unable to logout");
      return;
    }

    window.location.href = loginPageURL;
  } catch (error) {
    if (error.name === "AbortError") {
      displayError("Request timeout.");
    } else if (error.message.includes("Failed to fetch")) {
      displayError("Unable to connect. Please check your internet connection.");
    } else {
      displayError("An unexpected error occurred.");
    }
  }
}

export function logoutUserEXP() {
  logout.addEventListener("click", logoutUser);
}