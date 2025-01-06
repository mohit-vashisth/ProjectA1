const closeVoicePopup = document.querySelector('.closeVoicePopup');
const addVoiceButton = document.querySelector('.addVoice');
const addVoicePopupDisplay = document.querySelector('.addVoicePopup100VH');
const addVoicePopup = document.querySelector('.addvoicePopup');
const voiceBox2 = document.querySelector('.voiceBox2');
const voiceBox1 = document.querySelector('.voiceBox1');
const addInputLanguage = document.querySelector('.addInputLanguage');
const backVoiceIcon = document.querySelector('.backVoicePopup');
const continueButton = document.querySelector('.nextButtonV');
const recordHereDisplay = document.querySelector('.recordHere');
const voicePopup = document.querySelector('.voicePopup');
const voiceText = document.querySelector('.voiceText');
const config = {
    recordingLimit: 30,
    languages: ["English", "Hindi"]
};

// --------------------------------Recorder-------------------------------------
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
                    resetFun();
                    addVoicePopupDisplay.style.display = "none";
                    voiceText.innerHTML = "1 Voice Added";
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
            recordingInterval = setInterval(() => {
                updateRecordingTime();
    
                // Stop recording if seconds exceed 30
                if (seconds >= config.recordingLimit) {
                    mediaRecorder.stop();
                    clearInterval(recordingInterval);
                    recordingAnimation.style.display = "none";
                    stopButton.disabled = true;
                    alert("Recording stopped automatically after 30 seconds.");
                }
            }, 1000);
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

    const resetFun = function() {
        audioChunks = [];
        seconds = 0;
        recordingTime.textContent = "0:00";
        audioPlayer.style.display = "none";
        startButton.disabled = false;
        stopButton.disabled = true;
        resetButton.disabled = true;
        saveButton.disabled = true;
        downloadButton.disabled = true;
    };
    
    resetButton.addEventListener("click", resetFun);
    
});

// ---------------------------------add language-------------------------------
function populateLanguageDropdown() {
    const dropdown = document.getElementById("languageDropdown");

    config.languages.forEach((language="English") => {
        const option = document.createElement("option");
        option.value = language.toLowerCase();
        option.textContent = language;
        dropdown.appendChild(option);
    });
}

// --------------------------open-close-popup--------------------------
function resetVoiceOptions() {
    voicePopup.style.display = "flex";
    recordHereDisplay.style.display = "none";
    addInputLanguage.style.display = "none";
    backVoiceIcon.style.display = "none";
}

function openPopup(clickable, displayElement) {
    if (clickable && displayElement) {
        clickable.addEventListener('click', function () {
            resetVoiceOptions();
            displayElement.style.display = "flex";
            displayElement.style.pointerEvents = "auto";
        });
    } 
}

function closePopup(clickable, displayElement, popup) {
    if (clickable && displayElement && popup) {

        displayElement.addEventListener('click', function (event) {
            if (!popup.contains(event.target)) {
                displayElement.style.display = "none";
                resetFun(); // Recorder reset kare
            }
        });

        clickable.addEventListener('click', function () {
            displayElement.style.display = "none";
            resetFun(); // Recorder reset kare
            resetVoiceOptions(); // Existing functionality
        });
    } 
}


// --------------------------open-instant-voice-add-popup--------------------------

function instantVoiceAdd() {
    if (voiceBox1 && addInputLanguage && backVoiceIcon && continueButton && recordHereDisplay) {
        
        voiceBox1.addEventListener('click', function () {
            voicePopup.style.display = "none"; 
            addInputLanguage.style.display = "flex";
            backVoiceIcon.style.display = "flex";
        });

        continueButton.addEventListener('click', function () {
            addInputLanguage.style.display = "none";
            recordHereDisplay.style.display = "flex";
        });

        backVoiceIcon.addEventListener('click', function () {
            if (recordHereDisplay.style.display === "flex") {
                recordHereDisplay.style.display = "none";
                addInputLanguage.style.display = "flex";
            } else if (addInputLanguage.style.display === "flex") {
                addInputLanguage.style.display = "none";
                voicePopup.style.display = "flex";
                backVoiceIcon.style.display = "none";
            }
        });
    }
}



function main() {
    openPopup(addVoiceButton, addVoicePopupDisplay);
    closePopup(closeVoicePopup, addVoicePopupDisplay, addVoicePopup);
    instantVoiceAdd()
    document.addEventListener("DOMContentLoaded", populateLanguageDropdown);
}

document.addEventListener("DOMContentLoaded", () => {
    populateLanguageDropdown();
    main();
});
