import { debounce } from "../utils/deBounce";
import { displayError } from "../utils/errorDisplay";

const inputText = document.querySelector("#inputText");
const charCountDisplay = document.querySelector(".maximumChar");
const generateButton = document.querySelector(".generateSpeechBtn");
const preAvailableRadio = document.getElementById("preAvailable");
const useOwnVoiceRadio = document.getElementById("useOwnVoice");
const preAvailableDropdown = document.getElementById("preAvailableDropdown");
const useOwnVoiceDropdown = document.getElementById("useOwnVoiceDropdown");
const generateUserSpeechURL = import.meta.env.VITE_GENERATE_SPEECH_EP

let payload = {
    finalSpeech: "",
    voiceSelection: ""
};
let currentController = null;

document.addEventListener("DOMContentLoaded", function () {
  
    inputText.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });
});

function displayTextCount() {
    charCountDisplay.textContent = `Characters: ${1500 - inputText.value.length}`;
}

async function userSpeech() {
    inputText.addEventListener("input", debounce(() => {
            displayTextCount();
            const cursorPosition = inputText.selectionStart;
            inputText.setSelectionRange(cursorPosition, cursorPosition);
        })
    );
}

export function userFinalSpeech() {
    inputText.addEventListener('blur', () => {
        payload.finalSpeech = inputText.value;
    });
    return payload.finalSpeech
}

function selectLangPreference() {
    preAvailableRadio.addEventListener("change", function () {
      if (preAvailableRadio.checked) {
        preAvailableDropdown.disabled = false;
        useOwnVoiceDropdown.disabled = true;
      }
    });
  
    useOwnVoiceRadio.addEventListener("change", function () {
      if (useOwnVoiceRadio.checked) {
        useOwnVoiceDropdown.disabled = false;
        preAvailableDropdown.disabled = true;
      }
    });
}
  
function userCurrentSelection() {
    if (preAvailableRadio.checked) {
        payload.voiceSelection = preAvailableDropdown.value;
    } else if (useOwnVoiceRadio.checked) {
        payload.voiceSelection = useOwnVoiceDropdown.value;
    }
    return payload.voiceSelection;
}

async function generateUserSpeech() {
    if(currentController){
        currentController.abort()
        currentController = null
    }

    currentController = new AbortController()

    try{
        const timeout = setTimeout(()=>{
            currentController.abort()
            displayError("Request timeout.")
        }, 8000)
        const response = await fetch(generateUserSpeechURL, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            credentials: "include",
            body: JSON.stringify(payload),
            signal: currentController.signal,
        })
        clearTimeout(timeout)
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

        const data = await response.json()
        if(data?.success && data.voiceURL){
            console.log(data.voiceURL)
        }
    }
    catch (error) {
        if (error.name === "AbortError") {
            displayError("Request timeout.");
        } else if (error.message.includes("Failed to fetch")) {
            displayError("Unable to connect. Please check your internet connection.");
        } else {
            displayError("An unexpected error occurred.");
        }
    }
}
export function generateSpeechToVoiceEXP() {
    displayTextCount()
    userSpeech()
    selectLangPreference()
    userFinalSpeech()
    userCurrentSelection()
    generateButton.addEventListener('click', ()=>{
        payload.finalSpeech = inputText.value
        userCurrentSelection()
        generateUserSpeech()
    });
}
