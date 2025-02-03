import { handleCurrentFileNameEXP } from "./javascript/services/renameChatService";
import { addVoiceServiceEXP } from "./javascript/services/addVoiceCloneService";
import { storageHandleEXP } from "./javascript/services/storagePopupService";
import { recentChatsEXP } from "./javascript/services/chatListService";
import { dragDisabledEXP } from "./javascript/utils/dragIconsSvg_UI";
import { assetsLoadingEXP } from "./javascript/UI/loadingAssets_UI";
import { aboutWWebsiteEXP } from "./javascript/services/aboutWebsiteService";
import { slideMobileEXP } from "./javascript/UI/screenSlider_M_UI";
import { newChatEXP } from "./javascript/services/newChatService";
import { displayError } from "./javascript/utils/errorDisplay";
import { exportVoiceEXP } from "./javascript/services/exportVoiceService";
import { logoutUserEXP } from "./javascript/services/userLogoutService";
import { generateSpeechToVoiceEXP } from "./javascript/services/generateSpeechService";

const verifyTokenURL = import.meta.env.VITE_VERIFY_TOKEN_URL;
const userLoginPAGE = import.meta.env.VITE_LOGIN_PAGE;

let currentController = null;
let timeout;
let retryCount = 0;

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
      displayError("Request Timeout, Try Again")
    }, 8000)
    const response = await fetch(verifyTokenURL, {
      method: "GET",
      credentials: "include",
      signal: signal,
    });
    clearTimeout(timeout)
    // new
    if (!response.ok) {
      switch (response.status) {
        case 400:
          displayError("Invalid input. Please check your text or voice selection.");
          break;
        case 401:
          const refreshResponse = await fetch(verifyTokenURL, {
            method: "POST",
            credentials: "include",
            signal: signal,
          });
          clearTimeout(timeout)
          if (refreshResponse.ok) {
            return await validateUserCred();
          } else {
            if (retryCount >= 1) {
              displayError("Session expired. Please log in again.");
              window.location.href = userLoginPAGE;
              return;
            }
          retryCount++;
          }
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

    if (data && data.status && data.userInfo) {
      localStorage.setItem("userName", data.userName);
      localStorage.setItem("userEmail", data.userEmail);
    }
  } catch (error) {
      clearTimeout(timeout);
      if (error.name === "AbortError") {
        displayError("Request timeout.");
      } else if (error.message.includes("Failed to fetch")) {
          displayError("Unable to connect. Please check your internet connection.");
      } else {
          displayError("An unexpected error occurred.");
      }
      console.error("Error verifying token:", error);
      window.location.href = userLoginPAGE;
    }
}

// document.addEventListener("DOMContentLoaded", async () => {
//   try {
//       await validateUserCred();
//   } catch (error) {
//       console.error("Error during user validation:", error);
//   }
// });

function initApp() {
  newChatEXP();
  addVoiceServiceEXP();
  slideMobileEXP();
  aboutWWebsiteEXP();
  assetsLoadingEXP();
  dragDisabledEXP();
  recentChatsEXP();
  handleCurrentFileNameEXP();
  storageHandleEXP();
  exportVoiceEXP()
  logoutUserEXP()
  generateSpeechToVoiceEXP()
}

document.addEventListener("DOMContentLoaded", () => {
  initApp();
});
