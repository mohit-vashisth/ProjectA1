import { selectedLanguage } from "../UI/populateTranslateLangOptions";
import { displayError } from "../utils/errorDisplay";
import { userFinalSpeech } from "./generateSpeechService";

const inputArea = document.querySelector("#inputText");
const translateBtn = document.querySelector(".translateSpeechBtn");
const generateBtn = document.querySelector(".generateSpeechBtn");
const translateURL = import.meta.env.VITE_TRANSLATE_SPEECH_EP;

let currentController = null;
let translateSpeechOb = {
  text: null,
  dest: null,
};

async function translateHandle() {
  translateBtn.disabled = true;
  generateBtn.disabled = true;
  if (currentController) {
    currentController.abort();
    currentController = null;
  }

  translateSpeechOb.text = userFinalSpeech();
  translateSpeechOb.dest = selectedLanguage();

  console.log(translateSpeechOb);

  currentController = new AbortController();
  let timeout;
  try {
    timeout = setTimeout(() => {
      currentController.abort();
      currentController = null;
      displayError("Request Aborted");
    }, 8000);
    const response = await fetch(translateURL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(translateSpeechOb),
      signal: currentController.signal,
    });
    clearTimeout(timeout);

    translateBtn.disabled = false;
    generateBtn.disabled = false;

    const data = await response.json();

    if (!response.ok) {
      const errorDetails = data?.detail;
      switch (response.status) {
        case 400:
          displayError(errorDetails);
          break;
        case 401:
          displayError(errorDetails);
          break;
        case 404:
          displayError(errorDetails);
          break;
        case 500:
          displayError(errorDetails);
          break;
        default:
          displayError(errorDetails);
      }
      return;
    }

    if (!data?.text) {
      displayError("Unable to translate speech");
      return;
    }

    inputArea.value = data.text;
    
  } catch (error) {
    clearTimeout(timeout);
    if (error.message === "AbortError") {
      displayError("Request Aborted");
    } else {
      displayError("Something went wrong. Try again.");
    }
  } finally {
    clearTimeout(timeout);
    translateBtn.disabled = false;
    generateBtn.disabled = false;
  }
}

export function translateServiceEXP() {
  translateBtn.addEventListener("click", translateHandle);
}
