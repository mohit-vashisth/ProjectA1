import { selectedLanguage } from "../UI/populateTranslateLangOptions";
import { displayError } from "../utils/errorDisplay";
import { userFinalSpeech } from "./generateSpeechService";

const inputArea = document.querySelector("#inputText");
const translateBtn = document.querySelector(".translateSpeechBtn");
const generateBtn = document.querySelector(".generateSpeechBtn");
const translateURL = import.meta.env.VITE_TRANSLATE_SPEECH_EP;

let currentController = null;
let translateSpeechOb = { text: null, dest: null };

async function translateHandle() {
  translateBtn.disabled = true;
  generateBtn.disabled = true;

  if (currentController) {
    currentController.abort();
    currentController = null;
  }

  const previousText = inputArea.value; // Store previous text for rollback
  translateSpeechOb.text = userFinalSpeech();
  translateSpeechOb.dest = selectedLanguage();

  console.log(translateSpeechOb);

  currentController = new AbortController();
  let timeout;
  
  try {
    timeout = setTimeout(() => {
      currentController.abort();
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

    const data = await response.json();
    if (!response.ok || !data?.text) {
      throw new Error(data?.detail || "Unable to translate speech");
    }

    inputArea.value = data.text; // Update input field with translated text

  } catch (error) {
    inputArea.value = previousText; // Restore previous text on failure
    displayError(error.message || "Something went wrong. Try again.");
  } finally {
    clearTimeout(timeout);
    translateBtn.disabled = false;
    generateBtn.disabled = false;
  }
}

export function translateServiceEXP() {
  translateBtn.addEventListener("click", translateHandle);
}
