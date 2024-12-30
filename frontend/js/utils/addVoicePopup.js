const closeVoicePopup = document.querySelector('.closeVoicePopup');
const addVoiceButton = document.querySelector('.addVoice');
const addVoicePopupDisplay = document.querySelector('.addVoicePopup100VH');
const addVoicePopup = document.querySelector('.addvoicePopup');
const voiceBox1 = document.querySelector('.voiceBox1');
const voiceBox2 = document.querySelector('.voiceBox2');
const addInputLanguage = document.querySelector('.addInputLanguage');
const voicePopup = document.querySelector('.voicePopup');
const backVoiceIcon = document.querySelector('.backVoicePopup');
const continueButton = document.querySelector('.nextButtonV');
const recordHereDisplay = document.querySelector('.recordHere');


document.addEventListener("DOMContentLoaded", () => {
    const startButton = document.querySelector(".startButton");
    const stopButton = document.querySelector(".stopButton");
    const resetButton = document.querySelector(".resetButton");
    const saveButton = document.querySelector(".saveButton");
    const downloadButton = document.querySelector(".downloadButton");
    const audioPlayer = document.querySelector(".audio-player");
    const recordingTime = document.querySelector(".recordingTime");
    const recordingAnimation = document.querySelector(".recordingAnimation");

    let mediaRecorder;
    let audioChunks = [];
    let recordingInterval;
    let seconds = 0;

    const updateRecordingTime = () => {
        seconds++;
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        recordingTime.textContent = `${minutes}:${remainingSeconds < 10 ? "0" : ""}${remainingSeconds}`;
    };

    startButton.addEventListener("click", async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                const audioURL = URL.createObjectURL(audioBlob);
                audioPlayer.src = audioURL;
                audioPlayer.style.display = "flex";
                audioPlayer.controls = true;

                saveButton.disabled = false;
                downloadButton.disabled = false;

                saveButton.addEventListener("click", () => {
                    console.log("Audio saved: ", audioBlob); // Replace with actual save functionality
                    alert("Audio saved successfully!");
                });

                downloadButton.addEventListener("click", () => {
                    const link = document.createElement("a");
                    link.href = audioURL;
                    link.download = "recording.wav";
                    link.click();
                });
            };

            mediaRecorder.start();
            startButton.disabled = true;
            stopButton.disabled = false;
            resetButton.disabled = false;
            recordingAnimation.style.display = "flex";

            seconds = 0;
            recordingInterval = setInterval(updateRecordingTime, 1000);
        } catch (err) {
            console.error("Error accessing microphone: ", err);
            alert("Microphone access is required to record audio.");
        }
    });

    stopButton.addEventListener("click", () => {
        mediaRecorder.stop();
        stopButton.disabled = true;
        recordingAnimation.style.display = "none";
        clearInterval(recordingInterval);
    });

    resetButton.addEventListener("click", () => {
        audioChunks = [];
        seconds = 0;
        recordingTime.textContent = "0:00";
        audioPlayer.style.display = "none";
        startButton.disabled = false;
        stopButton.disabled = true;
        resetButton.disabled = true;
        saveButton.disabled = true;
        downloadButton.disabled = true;
    });
});

// --------------------------open-close-popup--------------------------
function openPopup(clickable, displayElement) {
    if (clickable && displayElement) {
        clickable.addEventListener('click', function () {
            displayElement.style.display = "flex";
            displayElement.style.pointerEvents = "auto";
        });
    } 
}

function reset() {
    
}

function closePopup(clickable, displayElement, popup) {
    if (clickable && displayElement && popup) {

        displayElement.addEventListener('click', function (event) {
            if (!popup.contains(event.target)) {
                displayElement.style.display = "none";
            }
        });

        clickable.addEventListener('click', function () {
            displayElement.style.display = "none";
        });
    } 
}

// --------------------------open-instant-voice-add-popup--------------------------

function instantVoiceAdd(clickable, instantVoiceElement, inputLanguage, previousState, continueButtonElement, nextDisplay) {
    if (clickable && instantVoiceElement && inputLanguage && previousState) {
        clickable.addEventListener('click', function () {
            instantVoiceElement.style.display = "none";
            inputLanguage.style.display = "flex";
            backVoiceIcon.style.display = 'flex';

            if (backVoiceIcon.style.display === 'flex') {
                previousState.addEventListener('click', function () {
                    instantVoiceElement.style.display = "flex";
                    inputLanguage.style.display = "none";
                    previousState.style.display = 'none';
                });
            } else {
                previousState.style.display = 'flex';
            }
        });
    }

    if (continueButtonElement) {
        continueButtonElement.addEventListener('click', function () {
            instantVoiceElement.style.display = "none";
            nextDisplay.style.display = 'flex'
        });
    }
}

// ---------------------------------add language-------------------------------

const languages = ["English", "Hindi"];
function populateLanguageDropdown() {
    const dropdown = document.getElementById("languageDropdown");
    languages.forEach((language) => {
        const option = document.createElement("option");
        option.value = language.toLowerCase();
        option.textContent = language;
        dropdown.appendChild(option);
    });
}

function main() {
    document.addEventListener("DOMContentLoaded", populateLanguageDropdown);
    openPopup(addVoiceButton, addVoicePopupDisplay);
    closePopup(closeVoicePopup, addVoicePopupDisplay, addVoicePopup);
    instantVoiceAdd(voiceBox1, voicePopup, addInputLanguage, backVoiceIcon, continueButton, recordHereDisplay)
}

main()