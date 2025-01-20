const startButton = document.querySelector(".startButton"); // Start recording button
const stopButton = document.querySelector(".stopButton"); // Stop recording button
const resetButton = document.querySelector(".resetButton"); // Reset recording button
const saveButton = document.querySelector(".saveButton"); // Save recording button
const downloadButton = document.querySelector(".downloadButton"); // Download recording button
const audioPlayer = document.querySelector(".audio-player"); // Audio player element
const recordingTime = document.querySelector(".recordingTime"); // Timer display element
const recordingAnimation = document.querySelector(".recordingAnimation"); // Recording animation element
const dataAPI = import.meta.env.VITE_DATA_URL;
const config = {
    recordingLimit: 30, // Max recording limit in seconds
    languages: ["English", "Hindi"], // Available languages
};

let recorder, mediaStream, audioChunks = [];
let userSeconds = 0;
let timerInterval;
let currentContoller = null;
// Function to start recording
async function startRecording() {
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const options = {
            mimeType: 'audio/webm',
            audioBitsPerSecond: 256000, // High-quality bitrate
            sampleRate: 48000
        };
        recorder = new MediaRecorder(mediaStream, options);

        recorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        recorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPlayer.src = audioUrl;
            saveButton.dataset.blobUrl = audioUrl; // Save the blob URL for saving
            audioChunks = [];
        };

        recorder.start();
        toggleRecordingState(true);
        startTimer();

        startButton.disabled = true;
        stopButton.disabled = false;
    } catch (err) {
        alert("Error accessing microphone: " + err.message);
    }
}

// Function to stop recording
function stopRecording() {
    if (recorder && recorder.state === "recording") {
        recorder.stop();
        mediaStream.getTracks().forEach(track => track.stop());
        toggleRecordingState(false);
        stopTimer();

        startButton.disabled = true;
        stopButton.disabled = true;
        saveButton.disabled = false;
        downloadButton.disabled = false;
        resetButton.disabled = false;
    }
}

// Function to reset the recording
function resetRecording() {
    stopRecording();
    audioPlayer.src = "";
    recordingTime.textContent = "0:00";
    userSeconds = 0;
    saveButton.dataset.blobUrl = ""; // Clear saved blob URL
    
    startButton.disabled = false;
    stopButton.disabled = true;
    saveButton.disabled = true;
    downloadButton.disabled = true;
    resetButton.disabled = true;
}

// Function to save the recording
async function saveRecording() {
    if (!saveButton.dataset.blobUrl) {
        alert("No recording to save!");
        return;
    }

    if(currentContoller){
        currentContoller.abort()
        currentContoller = null;
    }

    currentContoller = new AbortController()

    try {
        const timeoutID = setTimeout(()=>{
            currentContoller.abort()
        }, 8000)
        const response = await fetch(`${dataAPI}`,{
            method: "POST",
            credentials: "include",
            signal: currentContoller.signal,
        })
        setTimeout(timeoutID)
        if(!response.ok){
            console.error("Something went wrong");
        }
        const data = await response.json()

        if(data && data.success){
            saveButton.innerHTML = "Saved"
        }
        else{
            console.error("server not responding")
        }
        
    } catch (error) {
        
    }
}

// Function to download the recording
function downloadRecording() {
    saveRecording(); // Same functionality as saving in this context
}

// Function to toggle recording state
function toggleRecordingState(isRecording) {
    recordingAnimation.style.display = isRecording ? "block" : "none";
}

// Function to start the timer
function startTimer() {
    timerInterval = setInterval(() => {
        userSeconds++;
        if (userSeconds >= config.recordingLimit) {
            stopRecording();
            alert("Recording limit reached!");
            return;
        }
        const minutes = Math.floor(userSeconds / 60);
        const seconds = userSeconds % 60;
        recordingTime.textContent = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    }, 1000);
}

// Function to stop the timer
function stopTimer() {
    clearInterval(timerInterval);
    userSeconds = 0;
}

// Populate language dropdown
function populateLanguageDropdown() {
    const dropdown = document.getElementById("languageDropdown");
    let selectedLanguage = "English"; // Default language

    config.languages.forEach(language => {
        const option = document.createElement("option");
        option.value = language.toLowerCase();
        option.textContent = language;
        dropdown.appendChild(option);
    });

    dropdown.addEventListener("blur", () => {
        if (dropdown.value) { // Update only if a value is selected
            selectedLanguage = dropdown.value;
        }
    });
}

// Attach event listeners
document.addEventListener("DOMContentLoaded", () => {
    populateLanguageDropdown();

    startButton.addEventListener("click", startRecording);
    stopButton.addEventListener("click", stopRecording);
    resetButton.addEventListener("click", resetRecording);
    saveButton.addEventListener("click", saveRecording);
    downloadButton.addEventListener("click", downloadRecording);

    // Initial button states
    startButton.disabled = false;
    stopButton.disabled = true;
});