import { debounce } from "../utils/deBounce";
import { displayError } from "../utils/errorDisplay";

const inputText = document.querySelector("#inputText");
const charCountDisplay = document.querySelector(".maximumChar");
const generateButton = document.querySelector(".generateSpeechBtn");
const preAvailableRadio = document.getElementById("preAvailable");
const useOwnVoiceRadio = document.getElementById("useOwnVoice");
const preAvailableDropdown = document.getElementById("preAvailableDropdown");
const useOwnVoiceDropdown = document.getElementById("useOwnVoiceDropdown");
const generateUserSpeechURL = import.meta.env.VITE_GENERATE_SPEECH_EP;

let payload = {
    finalSpeech: "",
    voiceSelection: ""
};

let currentController = null;

document.addEventListener("DOMContentLoaded", function () {
    inputText.addEventListener("input", function () {
        if (this.value === "") {
            this.style.height = "auto";
        }
        this.style.height = this.scrollHeight + "px";
    });
});

function displayTextCount() {
    charCountDisplay.textContent = `Characters: ${1500 - inputText.value.length}`;
}

function userSpeech() {
    inputText.addEventListener("input", () => {
        displayTextCount();
        debounce(() => {
            const cursorPosition = inputText.selectionStart;
            inputText.setSelectionRange(cursorPosition, cursorPosition);
        })();
    });
}

export function userFinalSpeech() {
    inputText.addEventListener("blur", () => {
        payload.finalSpeech = inputText.value;
    });
    return payload.finalSpeech;
}


function selectLangPreference() {
    preAvailableRadio.addEventListener("change", function () {
        preAvailableDropdown.disabled = !this.checked;
        useOwnVoiceDropdown.disabled = this.checked;
    });

    useOwnVoiceRadio.addEventListener("change", function () {
        useOwnVoiceDropdown.disabled = !this.checked;
        preAvailableDropdown.disabled = this.checked;
    });
}

function updateVoiceSelection() {
    if (preAvailableRadio.checked) {
        payload.voiceSelection = preAvailableDropdown.value;
    } else if (useOwnVoiceRadio.checked) {
        payload.voiceSelection = useOwnVoiceDropdown.value;
    }
}

async function generateUserSpeech() {
    if (currentController) {
        currentController.abort();
        currentController = null;
    }

    currentController = new AbortController();

    try {
        const timeout = setTimeout(() => {
            currentController.abort();
            displayError("Request timeout.");
        }, 8000);

        const response = await fetch(generateUserSpeechURL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify(payload),
            signal: currentController.signal,
        });

        clearTimeout(timeout);

        const data = await response.json();
        if (!response.ok) {
            displayError(data?.detail || "Failed to generate speech.");
            return;
        }

        if (data?.success && data.voiceURL) {
            console.log("Speech generated:", data.voiceURL);
        }
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

export function generateSpeechToVoiceEXP() {
    displayTextCount();
    userSpeech();
    selectLangPreference();
    userFinalSpeech();

    generateButton.addEventListener("click", () => {
        payload.finalSpeech = inputText.value;
        updateVoiceSelection();
        generateUserSpeech();
    });
}
