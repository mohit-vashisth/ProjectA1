const logoutPopupContainer = document.querySelector(".logoutPopupContainer");
const logoutIcon = document.querySelector(".logoutIcon");
const noButton = document.querySelector(".noButton");
const logout = document.querySelector("#logout");
const popup = document.querySelector(".errorPopup");
const baseURL = import.meta.env.VITE_BASE_URL;
let currentController = null;
let timeoutID;
function errorPopup(errorText) {
  if (popup) {
    if (errorText !== "") {
      popup.textContent = errorText;
      popup.style.width = "30vmin";
    } else {
      popup.style.width = "0";
    }
  }
}
function clearErrorPopup() {
  setTimeout(() => errorPopup(""), 2000);
}
function timeout() {
  timeoutID = setTimeout(() => {
    currentController.abort();
    errorPopup("request timeout");
    clearErrorPopup();
  }, 2000);
}

logoutIcon.addEventListener("click", function () {
    logoutPopupContainer.style.display = "flex";
});

noButton.addEventListener("click", function () {
    logoutPopupContainer.style.display = "none";
});

async function logoutUser() {
  if (!logout && !logoutPopupContainer) errorPopup("something went wrong");


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
            errorPopup("unable to logout");
            clearErrorPopup();
        }

        const data = await response.json();
        if (data && data.status) {
            localStorage.removeItem("access_token");
            window.location.href = "/frontend/pages/auth/login.html";
        } else {
            errorPopup("something went wrong, unable to logout");
            clearErrorPopup();
        }
    } catch (error) {
        clearTimeout(timeoutID);
        if (error.name === "AbortError") {
            errorPopup("Request aborted");
            clearErrorPopup();
        }
        errorPopup("Something went wrong");
        clearErrorPopup();
  }
}

logout.addEventListener('click', logoutUser)