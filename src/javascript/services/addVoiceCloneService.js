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
    recordLimit: 30,
    languages: ["English", "Hindi"]
};

const today = new Date();
const payload = {
    language: "English",
    audio: null,
    date: `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
};

let previousCount = 0;
let currentController = null;
let timerInterval;
let userSeconds = 0;
let downloadButton = null;
let stream, recorder, audioChunks = [];
let recordingFormat = {
    extension: "mp3",
    mimeType: "audio/mpeg"
};

function detectOptimalFormat() {
    const formats = [
        { mimeType: "audio/mp3", extension: "mp3" },
        { mimeType: "audio/mpeg", extension: "mp3" },
        { mimeType: "audio/wav", extension: "wav" },
        { mimeType: "audio/webm;codecs=pcm", extension: "webm" },
        { mimeType: "audio/webm", extension: "webm" }
    ];
    
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
        card.style.height = "400px"
        card.style.width = "350px"
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
        card.style.width = "300px"
        card.style.height = "600px"
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
    if (!downloadButton) {
        downloadButton = document.createElement("button");
        downloadButton.className = "downloadButton";
        downloadButton.textContent = "Download Recording";
        saveRecButton.parentNode.insertBefore(downloadButton, saveRecButton.nextSibling);
    }
    return downloadButton;
}

function createAudioFileForDownload(audioBlob, format) {
    const outputType = format || recordingFormat.mimeType || "audio/webm";
    const extension = recordingFormat.extension;
    const downloadBtn = createDownloadButton();
    downloadBtn.style.display = "flex";
    
    const downloadUrl = URL.createObjectURL(audioBlob);
    
    downloadBtn.onclick = () => {
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = `voice-recording-${new Date().toISOString().slice(0,10)}.${extension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
    };
}

async function convertToWav(audioBlob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = async function() {
            try {
                const arrayBuffer = this.result;
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
                const wavBuffer = audioBufferToWav(audioBuffer);
                const wavBlob = new Blob([new DataView(wavBuffer)], { type: "audio/wav" });
                resolve(wavBlob);
            } catch (e) {
                reject(e);
            }
        };
        reader.onerror = reject;
        reader.readAsArrayBuffer(audioBlob);
    });
}

function audioBufferToWav(buffer, opt) {
    opt = opt || {}
    let numChannels = buffer.numberOfChannels;
    let sampleRate = buffer.sampleRate;
    let format = opt.float32 ? 3 : 1;
    let bitDepth = format === 3 ? 32 : 16;
    
    let result;
    if (numChannels === 2) {
        result = interleave(buffer.getChannelData(0), buffer.getChannelData(1));
    } else {
        result = buffer.getChannelData(0);
    }
    return encodeWAV(result, numChannels, sampleRate, bitDepth);
}

function encodeWAV(samples, numChannels, sampleRate, bitDepth) {
    let bytesPerSample = bitDepth / 8;
    let blockAlign = numChannels * bytesPerSample;
    let buffer = new ArrayBuffer(44 + samples.length * bytesPerSample);
    let view = new DataView(buffer);
    
    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + samples.length * bytesPerSample, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * blockAlign, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, bitDepth, true);
    writeString(view, 36, 'data');
    view.setUint32(40, samples.length * bytesPerSample, true);
    
    if (bitDepth === 16) {
        floatTo16BitPCM(view, 44, samples);
    } else {
        writeFloat32(view, 44, samples);
    }
    return buffer;
}

function floatTo16BitPCM(output, offset, input) {
    for (let i = 0; i < input.length; i++, offset += 2) {
        let s = Math.max(-1, Math.min(1, input[i]));
        output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
}

function writeFloat32(output, offset, input) {
    for (let i = 0; i < input.length; i++, offset += 4) {
        output.setFloat32(offset, input[i], true);
    }
}

function writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
    }
}

function interleave(leftChannel, rightChannel) {
    let length = leftChannel.length + rightChannel.length;
    let result = new Float32Array(length);
    let index = 0, inputIndex = 0;
    while (index < length) {
        result[index++] = leftChannel[inputIndex];
        result[index++] = rightChannel[inputIndex];
        inputIndex++;
    }
    return result;
}

async function startRecording() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true,
                channelCount: 1,
                sampleRate: 44100
            } 
        });
        
        const options = {};
        if (recordingFormat.mimeType) {
            options.mimeType = recordingFormat.mimeType;
        }
        
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
            if (downloadButton) {
                downloadButton.style.display = "none";
            }
        };
        
        recorder.onstop = async () => {
            const blobType = recorder.mimeType || recordingFormat.mimeType || "audio/webm";
            let audioBlob = new Blob(audioChunks, { type: blobType });
            
            if (recordingFormat.extension !== "wav") {
                try {
                    audioBlob = await convertToWav(audioBlob);
                    recordingFormat = { mimeType: "audio/wav", extension: "wav" };
                } catch (e) {
                    console.error("Conversion to WAV failed:", e);
                }
            }
            
            const playableURL = URL.createObjectURL(audioBlob);
            player.src = playableURL;
            player.style.display = "flex";
            animation.style.display = "none";
            player.controls = true;
            player.setAttribute('controlsList', 'nodownload');
            saveRecButton.dataset.blobUrl = playableURL;
            payload.audio = audioBlob;
            createAudioFileForDownload(audioBlob, blobType);
            startRecButton.disabled = false;
            stopRecButton.disabled = true;
            resetRecButton.disabled = false;
            saveRecButton.disabled = false;
        };

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
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    }
}

function resetRecording() {
    stopRecording();
    player.src = "";
    player.style.display = "none";
    audioChunks = [];
    payload.audio = null;
    resetRecButton.disabled = true;
    saveRecButton.disabled = true;
    recordingTime.textContent = "0:00";
    userSeconds = 0;
    if (downloadButton) {
        downloadButton.style.display = "none";
    }
}

function startTimer() {
    userSeconds = 0;
    recordingTime.textContent = "0:00";
    clearInterval(timerInterval);
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
    previousCount = 0;
    card.style.width = "300px"
    card.style.height = "600px"
    display1.style.display = "flex";
    display2.style.display = "none";
    display3.style.display = "none";
    previous.style.display = "none";
    player.src = "";
    player.style.display = "none";
    audioChunks = [];
    payload.audio = null;
    if (recorder && recorder.state !== "inactive") {
        stopRecording();
    }
    clearInterval(timerInterval);
    userSeconds = 0;
    recordingTime.textContent = "0:00";
    startRecButton.disabled = false;
    stopRecButton.disabled = true;
    resetRecButton.disabled = true;
    saveRecButton.disabled = true;
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
    // openDisplayButtonText.style.display = "none";
    
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
    formData.append("language", payload.language || "English");
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

        const data = await response.json();
        if (!response.ok) {
            const errorDetails = data?.detail;
            displayError(errorDetails);
        }

        if (data && data.success) {
            openDisplayButtonText.textContent = "1 Voice Added";
            popupDisplay.style.display = "none";
            resetDisplays();
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
        currentController = null;
    }
}

export function addVoiceServiceEXP() {
    detectOptimalFormat();
    
    createDownloadButton();
    
    startRecButton.disabled = false;
    stopRecButton.disabled = true;
    resetRecButton.disabled = true;
    saveRecButton.disabled = true;

    payload.language = "English";

    toggleDisplay();
    selectLanguages();

    startRecButton.addEventListener("click", startRecording);
    stopRecButton.addEventListener("click", stopRecording);
    resetRecButton.addEventListener("click", resetRecording);
    saveRecButton.addEventListener("click", saveRecording);
}