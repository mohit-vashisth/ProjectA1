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
const voiceDataURL = import.meta.env.VITE_USER_VOICE_ADD_EP;
const config = {
    recordLimit: 30, // seconds
    languages: ["English", "Hindi"]
};

const today = new Date();
const payload = {
    language: "English", // Default language
    audio: null,
    date: `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
};

let previousCount = 0;
let stream, recorder, audioChunks = [];
let currentController = null;
let timerInterval;
let userSeconds = 0;
let downloadButton = null;
let recordingFormat = {
    extension: "mp3",
    mimeType: "audio/mpeg"
};

// Try to determine the best format support based on browser capabilities
function detectOptimalFormat() {
    // These formats are listed in order of preference for Pot Player compatibility
    const formats = [
        { mimeType: "audio/mp3", extension: "mp3" },
        { mimeType: "audio/mpeg", extension: "mp3" },
        { mimeType: "audio/wav", extension: "wav" },
        { mimeType: "audio/webm;codecs=pcm", extension: "webm" },
        { mimeType: "audio/webm", extension: "webm" }
    ];
    
    // Find the first supported format
    for (const format of formats) {
        try {
            if (MediaRecorder.isTypeSupported(format.mimeType)) {
                recordingFormat.mimeType = format.mimeType;
                recordingFormat.extension = format.extension;
                console.log(`Using format: ${format.mimeType}`);
                return true;
            }
        } catch (e) {
            console.log(`Format ${format.mimeType} check failed:`, e);
        }
    }
    
    // Default to standard WebM if nothing else works
    recordingFormat.mimeType = "";
    recordingFormat.extension = "webm";
    return false;
}

function toggleDisplay() {
    openDisplayButton.addEventListener("click", () => {
        resetDisplays();
        popupDisplay.style.display = "flex";
    });
    
    document.addEventListener("click", (e) => {
        if (!card.contains(e.target) && e.target !== openDisplayButton) {
            popupDisplay.style.display = "none";
            resetDisplays();
        }
    });
    
    closeDisplayButton.addEventListener("click", () => {
        popupDisplay.style.display = "none";
        resetDisplays();
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
    
    dropDownLanguage.addEventListener("change", () => {
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

function createDownloadButton() {
    // Only create the button if it doesn't exist
    if (!downloadButton) {
        downloadButton = document.createElement("button");
        downloadButton.className = "downloadButton";
        downloadButton.textContent = "Download Recording";
        downloadButton.style.display = "none";
        downloadButton.style.marginTop = "10px";
        downloadButton.style.padding = "8px 12px";
        
        // Insert it after the save button
        saveRecButton.parentNode.insertBefore(downloadButton, saveRecButton.nextSibling);
    }
    return downloadButton;
}

function createAudioFileForDownload(audioBlob, format) {
    // For MP3 conversion, we need to use the correct MIME type
    const outputType = format || recordingFormat.mimeType || "audio/webm";
    const extension = recordingFormat.extension;
    
    // Create a download link with the correct MIME type and extension
    const downloadBtn = createDownloadButton();
    downloadBtn.style.display = "flex";
    
    const downloadUrl = URL.createObjectURL(audioBlob);
    
    // Set up the download button to trigger the download
    downloadBtn.onclick = () => {
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = `voice-recording-${new Date().toISOString().slice(0,10)}.${extension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        // Don't revoke immediately to ensure download completes
        setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
    };
}

async function startRecording() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true,
                channelCount: 1, // Mono recording for better compatibility
                sampleRate: 44100 // Standard sample rate for better compatibility
            } 
        });
        
        // Set up recorder with optimal format
        const options = {};
        if (recordingFormat.mimeType) {
            options.mimeType = recordingFormat.mimeType;
        }
        
        // Set bitrate based on format (lower for MP3, higher for others)
        if (recordingFormat.extension === "mp3") {
            options.audioBitsPerSecond = 128000;
        } else if (recordingFormat.extension === "wav") {
            options.audioBitsPerSecond = 256000;
        } else {
            options.audioBitsPerSecond = 128000;
        }
        
        recorder = new MediaRecorder(stream, options);
        
        audioChunks = [];
        recorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                audioChunks.push(e.data);
            }
        };
        
        recorder.onstart = () => {
            animation.style.display = "flex";
            player.style.display = "none";
            startRecButton.disabled = true;
            stopRecButton.disabled = false;
            
            // Hide download button during recording
            if (downloadButton) {
                downloadButton.style.display = "none";
            }
        };
        
        recorder.onstop = () => {
            // Get MIME type - use what recorder actually used
            const blobType = recorder.mimeType || recordingFormat.mimeType || "audio/webm";
            const audioBlob = new Blob(audioChunks, { type: blobType });
            
            // Create URLs for playback
            const playableURL = URL.createObjectURL(audioBlob);
            player.src = playableURL;
            player.style.display = "flex";
            animation.style.display = "none";
            
            // Ensure audio controls are enabled but prevent direct download from player
            player.controls = true;
            player.setAttribute('controlsList', 'nodownload');
            
            saveRecButton.dataset.blobUrl = playableURL;
            payload.audio = audioBlob;
            
            // Enable proper download capability
            createAudioFileForDownload(audioBlob, blobType);
            
            // Enable buttons after recording
            startRecButton.disabled = false;
            stopRecButton.disabled = true;
            resetRecButton.disabled = false;
            saveRecButton.disabled = false;
        };

        // Ask for data frequently to ensure better quality recordings
        recorder.start(250);
        startTimer();
    } catch (error) {
        console.error("Error starting recording:", error);
        alert("Could not access microphone. Please check permissions.");
    }
}

function stopRecording() {
    if (recorder && recorder.state !== "inactive") {
        recorder.stop();
        clearInterval(timerInterval);
        
        // Stop all audio tracks
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
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
    userSeconds = 0;
    
    // Hide download button
    if (downloadButton) {
        downloadButton.style.display = "none";
    }
}

function startTimer() {
    userSeconds = 0;
    recordingTime.textContent = "0:00";
    clearInterval(timerInterval); // Clear any existing interval
    
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
    
    // Stop any active recording
    if (recorder && recorder.state !== "inactive") {
        stopRecording();
    }
    
    // Reset timer
    clearInterval(timerInterval);
    userSeconds = 0;
    recordingTime.textContent = "0:00";
    
    // Reset buttons
    startRecButton.disabled = false;
    stopRecButton.disabled = true;
    resetRecButton.disabled = true;
    saveRecButton.disabled = true;
    
    // Hide download button
    if (downloadButton) {
        downloadButton.style.display = "none";
    }
}

function displayError(message) {
    voiceText.textContent = message;
    setTimeout(() => {
        voiceText.textContent = "Create Voice Clone";
    }, 3000);
}

async function saveRecording() {
    loadingAnimationBTN.style.display = "flex";
    openDisplayButtonText.style.display = "none";
    
    if (!payload.audio) {
        alert("No audio to save! Please record first.");
        loadingAnimationBTN.style.display = "none";
        openDisplayButtonText.style.display = "flex";
        return;
    }
    
    if (currentController) {
        currentController.abort();
        currentController = null;
    }
    
    currentController = new AbortController();
    
    const formData = new FormData();
    formData.append("language", payload.language || "English"); // Ensure language is never empty
    formData.append("audio", payload.audio);
    formData.append("date", payload.date);
    
    try {
        const timeout = setTimeout(() => {
            if (currentController) {
                currentController.abort();
                loadingAnimationBTN.style.display = "none";
                openDisplayButtonText.style.display = "flex";
                displayError("Request timeout. Please try again.");
            }
        }, 8000);
        
        const response = await fetch(voiceDataURL, {
            method: "POST",
            body: formData,
            signal: currentController.signal,
        });
        
        clearTimeout(timeout);
        loadingAnimationBTN.style.display = "none";
        openDisplayButtonText.style.display = "flex";

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
                    displayError("Something went wrong. Try again.");
            }
            return;
        }

        const data = await response.json();
        
        if (data && data.success) {
            openDisplayButtonText.textContent = "1 Voice Added";
            popupDisplay.style.display = "none"; // Close popup on success
            resetDisplays(); // Reset for next use
        } else {
            throw new Error(data.message || "Upload failed");
        }
    } catch (error) {
        loadingAnimationBTN.style.display = "none";
        openDisplayButtonText.style.display = "flex";
        
        if (error.name === "AbortError") {
            displayError("Request timeout.");
        } else if (error.message.includes("Failed to fetch")) {
            displayError("Unable to connect. Please check your internet connection.");
        } else {
            displayError(error.message || "An unexpected error occurred.");
        }
    } finally {
        currentController = null; // Clear controller
    }
}

export function addVoiceServiceEXP() {
    // Detect optimal format first
    detectOptimalFormat();
    
    // Create download button at initialization
    createDownloadButton();
    
    // Initialize button states
    startRecButton.disabled = false;
    stopRecButton.disabled = true;
    resetRecButton.disabled = true;
    saveRecButton.disabled = true;

    // Set default language
    payload.language = "English";

    // Initialize event listeners
    toggleDisplay();
    selectLanguages();

    startRecButton.addEventListener("click", startRecording);
    stopRecButton.addEventListener("click", stopRecording);
    resetRecButton.addEventListener("click", resetRecording);
    saveRecButton.addEventListener("click", saveRecording);
}