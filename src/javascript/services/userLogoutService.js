import { displayError } from "../utils/errorDisplay";

const logoutPopupContainer = document.querySelector(".logoutPopupContainer");
const logoutIcon = document.querySelector(".logoutIcon");
const noButton = document.querySelector(".noButton");
const logout = document.querySelector("#logout");

const userLogoutURL = import.meta.env.VITE_LOGOUT_EP;
const loginPageURL = import.meta.env.VITE_LOGIN_PAGE

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
        const response = await fetch(userLogoutURL, {
        method: "POST",
        credentials: "include",
        signal: currentController.signal,
        });
        clearTimeout(timeoutID);

        if (!response.ok) {
          switch (response.status) {
              case 400:
                  displayError("Invalid input. Please check your text or voice selection.");
                  break;
              case 401:
                  displayError("You are not logged in. Please log in and try again.");
                  break;
              case 403:
                  displayError("You do not have permission to perform this action.");
                  break;
              case 404:
                  displayError("The requested resource was not found.");
                  break;
              case 500:
                  displayError("A server error occurred. Please try again later.");
                  break;
              default:
                  displayError("Something went wrong, Try again.");
          }
          return;
      }

        const data = await response.json();
        if (data && data.status) {
            localStorage.removeItem("access_token");
            window.location.href = loginPageURL;
        } else {
            displayError("something went wrong, unable to logout");
        }
    } catch (error) {
        clearTimeout(timeoutID);
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
  logout.addEventListener('click', logoutUser)
}