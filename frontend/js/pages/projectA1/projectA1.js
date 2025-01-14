const profileImg = document.querySelector(".img");
const userName = document.querySelector(".userName span");
const logout = document.querySelector("#logout");
const popup = document.querySelector(".errorPopup")
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
    errorPopup("request timeout")
    clearErrorPopup()
  }, 2000);
}
function setUser() {
  nameOfUser = localStorage.getItem("userName");
  emailOfUser = localStorage.getItem("userEmail");
  userName.textContent = nameOfUser;
  profileImg.textContent = emailOfUser[0].toLowerCase();
}

async function validateUserCred() {
  if (currentController) {
    currentController.abort();
    currentController = null;
  }

  currentController = new AbortController();
  const signal = currentController.signal;

  try {
    const response = await fetch(`${baseURL}/api/verifing`, {
      method: "GET",
      credentials: "include",
      signal: signal,
    });
    clearTimeout(timeoutID)

    if (!response.ok) {
      if (response.status === 401) {
        const refreshResponse = await fetch(`${baseURL}/api/session`, {
          method: "POST",
          credentials: "include",
          signal: signal,
        });
        clearTimeout(timeoutID)

        if (refreshResponse.ok) {
          return await validateUserCred();
        } else {
          window.location.href = "/frontend/pages/auth/login.html";
        }
      } else {
        window.location.href = "/frontend/pages/auth/login.html";
      }
      return;
    }
    const data = await response.json();

    if (data && data.status && data.userInfo) {
      localStorage.setItem("userName", data.userName);
      localStorage.setItem("userEmail", data.userEmail);
    }
  } catch (error) {
    clearTimeout(timeoutID)
    if(error.name === "AbortError"){
      errorPopup("request aborted")
      clearErrorPopup()
    }
    console.error("Error verifying token:", error);
    window.location.href = "/frontend/pages/auth/login.html";
  }
}

// document.addEventListener("DOMContentLoaded", async () => {
//   try {
//       await validateUserCred();
//   } catch (error) {
//       console.error("Error during user validation:", error);
//   }
// });
// logout.addEventListener("click", logoutUser);