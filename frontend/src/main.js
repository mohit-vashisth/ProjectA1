import { handleCurrentFileNameEXP } from "./javascript/services/renameChatService";
import { addVoiceServiceEXP } from "./javascript/services/addVoiceCloneService";
import { storageHandleEXP } from "./javascript/services/storagePopupService";
import { recentChatsEXP } from "./javascript/services/chatListService";
import { dragDisabledEXP } from "./javascript/utils/dragIconsSvg_UI";
import { assetsLoadingEXP } from "./javascript/UI/loadingAssets_UI";
import { aboutWWebsiteEXP } from "./javascript/services/aboutWebsiteService";
import { slideMobileEXP } from "./javascript/UI/screenSlider_M_UI";
import { newChatEXP } from "./javascript/services/newChatService";
import { exportVoiceEXP } from "./javascript/services/exportVoiceService";
import { logoutUserEXP } from "./javascript/services/userLogoutService";
import { generateSpeechToVoiceEXP } from "./javascript/services/generateSpeechService";
import { translateServiceEXP } from "./javascript/services/translateSpeechService";

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
  translateServiceEXP()
  console.log(`voice: ${import.meta.env.VITE_USER_VOICE_ADD_EP}`)
  console.log(`login: ${import.meta.env.VITE_LOGIN_EP}`)
  console.log(`signup: ${import.meta.env.VITE_SIGNUP_EP}`)

}

document.addEventListener("DOMContentLoaded", () => {
  initApp();
});
