const openDisplayButton = document.querySelector(".addVoice");
const openDisplayButtonText = document.querySelector(".addVoiceButtonText");
const loadingAnimationBTN = document.querySelector(".addVoiceAnimation");
const popupDisplay = document.querySelector(".addVoicePopup100VH");
const card = document.querySelector(".addvoicePopup");
const closeDisplayButton = document.querySelector(".closeVoicePopup");
const instantVoiceButton = document.querySelector(".voiceBox1");
const display1 = document.querySelector(".voicePopup");
const display2 = document.querySelector(".addInputLanguage");
const display3 = document.querySelector(".recordHere");
const dropDownLanguage = document.querySelector("#languageDropdown");
const continueButton = document.querySelector(".nextButtonV");
const previous = document.querySelector(".backVoicePopup");
const animation = document.querySelector(".recordingAnimation");
const player = document.querySelector(".audio-player");
const voiceText = document.querySelector(".voiceText");
const startRecButton = document.querySelector(".startButton");
const stopRecButton = document.querySelector(".stopButton");
const resetRecButton = document.querySelector(".resetButton");
const saveRecButton = document.querySelector(".saveButton");
const recordingTime = document.querySelector(".recordingTime");
const dataURL = import.meta.env.VITE_DATA_URL;
const config = {
    recordLimit: 30, // seconds
    languages: ["English", "Hindi"]
};

const today = new Date();
const payload = {
    language: "",
    audio: null,
    date: `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
};

let previousCount = 0;
let stream, recorder, audioChunks = [];
let currentController = null;
let timerInterval;
let userSeconds = 0;

function toggleDisplay() {
    openDisplayButton.addEventListener("click", () => {
        resetDisplays();
        popupDisplay.style.display = "flex";
    });
    
    document.addEventListener("click", (e) => {
        if (!card.contains(e.target) && e.target !== openDisplayButton) {
            popupDisplay.style.display = "none";
            resetDisplays()
        }
    });
    
    closeDisplayButton.addEventListener("click", () => {
        popupDisplay.style.display = "none";
        resetDisplays()
    });

    instantVoiceButton.addEventListener("click", () => {
        previousCount++;
        previousDisplay();
    });
    
    continueButton.addEventListener("click", () => {
        previousCount++;
        previousDisplay();
    });
    
    previous.addEventListener("click", () => {
        previousCount--;
        previousDisplay();
    });
}

function selectLanguages() {
    dropDownLanguage.innerHTML = "";
    
    config.languages.forEach((lang) => {
        const option = document.createElement("option");
        option.value = lang;
        option.textContent = lang;
        if (lang === "English") option.selected = true;
        dropDownLanguage.appendChild(option);
    });
    
    dropDownLanguage.addEventListener("blur", () => {
        payload.language = dropDownLanguage.value;
    });
}

function previousDisplay() {
    if (previousCount === 0) {
        display1.style.display = "flex";
        display2.style.display = "none";
        display3.style.display = "none";
        previous.style.display = "none";
    } else if (previousCount === 1) {
        display1.style.display = "none";
        display2.style.display = "flex";
        display3.style.display = "none";
        previous.style.display = "flex";
    } else if (previousCount === 2) {
        display1.style.display = "none";
        display2.style.display = "none";
        display3.style.display = "flex";
        previous.style.display = "flex";
    }
}

async function startRecording() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        recorder = new MediaRecorder(stream, {
            mimeType: "audio/webm",
            audioBitsPerSecond: 256000,
            sampleRate: 48000
        });
        
        audioChunks = [];
        recorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                audioChunks.push(e.data);
            }
        };
        
        recorder.onstart = () => {
            animation.style.display = "flex";
            player.style.display = "none"
            startRecButton.disabled = true;
            stopRecButton.disabled = false;
        };
        
        recorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            const playableURL = URL.createObjectURL(audioBlob);
            player.src = playableURL;
            player.style.display = "flex"
            animation.style.display = "none";
            saveRecButton.dataset.blobUrl = playableURL;
            payload.audio = audioBlob;
        };

        recorder.start();
        startTimer();
    } catch (error) {
        console.error("Error starting recording:", error);
    }
}

function stopRecording() {
    if (recorder && recorder.state !== "inactive") {
        recorder.stop();
        startRecButton.disabled = false;
        stopRecButton.disabled = true;
        resetRecButton.disabled = false;
        saveRecButton.disabled = false;
        clearInterval(timerInterval);
    }
}

function resetRecording() {
    stopRecording();
    player.src = ""; // Clear player source
    player.style.display = "none"; // Hide player
    audioChunks = [];
    payload.audio = null; // Reset payload audio
    resetRecButton.disabled = true;
    saveRecButton.disabled = true;
    recordingTime.textContent = "0:00";
}

function startTimer() {
    userSeconds = 0;
    recordingTime.textContent = "0:00";
    timerInterval = setInterval(() => {
        userSeconds++;
        if (userSeconds >= config.recordLimit) {
            stopRecording();
            alert("Recording limit reached!");
        }
        const minutes = Math.floor(userSeconds / 60);
        const seconds = userSeconds % 60;
        recordingTime.textContent = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    }, 1000);
}

function resetDisplays() {
    previousCount = 0; // Reset navigation state
    display1.style.display = "flex"; // Reset to initial display
    display2.style.display = "none";
    display3.style.display = "none";
    previous.style.display = "none"; // Hide previous button
    player.src = ""; // Clear audio player
    player.style.display = "none"; // Hide player
    audioChunks = []; // Clear recorded audio chunks
    payload.audio = null; // Reset audio in payload
    resetRecording(); // Reset recording timer and controls
}

async function saveRecording() {
    loadingAnimationBTN.style.display = "flex"
    openDisplayButtonText.style.display = "none"
    if (!payload.audio) {
        alert("No audio to save! Please record first.");
        return;
    }
    if (currentController){
        currentController.abort()
        currentController = null
    };
    currentController = new AbortController();
    
    const formData = new FormData();
    formData.append("language", payload.language);
    formData.append("audio", payload.audio);
    formData.append("date", payload.date);
    
    try {
        const timeout = setTimeout(() => {
            currentController.abort()
            loadingAnimationBTN.style.display = "none"
            openDisplayButtonText.style.display = "flex" 
        }, 8000);
        const response = await fetch(dataURL, {
            method: "POST",
            body: formData,
            signal: currentController.signal,
        });
        clearTimeout(timeout)
        loadingAnimationBTN.style.display = "none"
        openDisplayButtonText.style.display = "flex"

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
        
        if (data && data.success) {
            openDisplayButtonText.textContent = "1 Voice Added";
        } else {
            loadingAnimationBTN.style.display = "none"
            throw new Error("Upload failed");
        }
    } catch (error) {
        loadingAnimationBTN.style.display = "none"
        openDisplayButtonText.style.display = "flex"
        if (error.name === "AbortError") {
            displayError("Request timeout.");
        } else if (error.message.includes("Failed to fetch")) {
            displayError("Unable to connect. Please check your internet connection.");
        } else {
            displayError("An unexpected error occurred.");
        }
        voiceText.textContent = "Error saving. Try again.";
    } finally {
        currentController = null; // Clear controller
        setTimeout(() => {
            voiceText.textContent = "Create Voice Clone";
        }, 2000);
    }
}

export function addVoiceServiceEXP() {
    startRecButton.disabled = false;
    stopRecButton.disabled = true;
    resetRecButton.disabled = true;
    saveRecButton.disabled = true;

    toggleDisplay();
    selectLanguages();

    startRecButton.addEventListener("click", startRecording);
    stopRecButton.addEventListener("click", stopRecording);
    resetRecButton.addEventListener("click", resetRecording);
    saveRecButton.addEventListener("click", saveRecording);
}