import { newChatEXP } from "./javascript/services/newChatService";
import { addVoiceServiceEXP } from "./javascript/services/addVoiceCloneService";
import { slideMobileEXP } from "./javascript/UI/screenSlider_M_UI";
import { aboutWWebsiteEXP } from "./javascript/UI/aboutWebsite_UI";
import { assetsLoadingEXP } from "./javascript/UI/loadingAssets_UI";
import { dragDisabledEXP } from "./javascript/utils/dragIconsSvg_UI";
import { recentChatsEXP } from "./javascript/services/chatListService";

const popup = document.querySelector(".errorPopup")
const verifyTokenURL = import.meta.env.VITE_VERIFYTOKEN_URL;
const signupURL = import.meta.env.VITE_SIGNUP_URL;

let currentController = null;
let timeout;

function errorPopup(text, time) {
      popup.textContent = text;
      popup.style.width = "30vmin";
      setTimeout(()=>{
        popup.style.width = "0";
      }, time)
}

async function validateUserCred() {
  if (currentController) {
    currentController.abort();
    currentController = null;
  }

  currentController = new AbortController();
  const signal = currentController.signal;

  try {
    timeout = setTimeout(()=>{
      currentController.abort()
      errorPopup("Request Timeout, Try Again", 2000)
    }, 8000)
    const response = await fetch(verifyTokenURL, {
      method: "GET",
      credentials: "include",
      signal: signal,
    });
    clearTimeout(timeout)

    if (!response.ok) {
      if (response.status === 401) {
        const refreshResponse = await fetch(verifyTokenURL, {
          method: "POST",
          credentials: "include",
          signal: signal,
        });
        clearTimeout(timeout)

        if (refreshResponse.ok) {
          return await validateUserCred();
        } else {
          window.location.href = signupURL;
        }
      } else {
        window.location.href = signupURL;
      }
      return;
    }
    const data = await response.json();

    if (data && data.status && data.userInfo) {
      localStorage.setItem("userName", data.userName);
      localStorage.setItem("userEmail", data.userEmail);
    }
  } catch (error) {
    clearTimeout(timeout)
    if(error.name === "AbortError"){
      errorPopup("request aborted", 2000)
    }
    console.error("Error verifying token:", error);
    window.location.href = signupURL;
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

newChatEXP()
addVoiceServiceEXP()
slideMobileEXP()
aboutWWebsiteEXP()
assetsLoadingEXP()
dragDisabledEXP()
recentChatsEXP()