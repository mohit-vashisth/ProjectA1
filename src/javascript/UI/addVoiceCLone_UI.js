const close = document.querySelector('.closeVoicePopup');
const back = document.querySelector('.backVoicePopup');
const addVoiceButton = document.querySelector('.addVoice');
const addVoiceMainContainer = document.querySelector('.addVoicePopup100VH');
const addvoiceItemsContainer = document.querySelector('.addvoicePopup');
const voiceBox1 = document.querySelector('.voiceBox1');
const voiceBox2 = document.querySelector('.voiceBox2');
const selectLanguage = document.querySelector('.addInputLanguage');
const continueButton = document.querySelector('.nextButtonV');
const recordNowContainer = document.querySelector('.recordHere');
const voicePopup = document.querySelector('.voicePopup');
const voiceText = document.querySelector('.voiceText');

let backCount = 0;

// Open and close popup
function toggleVoiceContainer() {
    addVoiceButton.addEventListener('click', () => {
        addVoiceMainContainer.style.display = "flex";
    });
    addVoiceMainContainer.addEventListener('click', (event) => {
        if (!addvoiceItemsContainer.contains(event.target)) {
            addVoiceMainContainer.style.display = "none";
            resetDisplay()
        }
    });
    
    close.addEventListener('click', () => {
        addVoiceMainContainer.style.display = "none";
    });
}

function resetDisplay() {
    const isHidden = window.getComputedStyle(addVoiceMainContainer).display === "none";
    if(isHidden){
        backCount = 0
        voicePopup.style.display = "flex";
        selectLanguage.style.display = "none";
        recordNowContainer.style.display = "none";
        back.style.display = "none";
    }
}

// Function to update displays based on `backCount`
function updateDisplays() {
    if (backCount === 0) {
        voicePopup.style.display = "flex";
        selectLanguage.style.display = "none";
        recordNowContainer.style.display = "none";
    } else if (backCount === 1) {
        voicePopup.style.display = "none";
        selectLanguage.style.display = "flex";
        recordNowContainer.style.display = "none";
        back.style.display = "flex";
    } else if (backCount === 2) {
        voicePopup.style.display = "none";
        selectLanguage.style.display = "none";
        recordNowContainer.style.display = "flex";
        back.style.display = "flex";
    }
}

// Navigation logic for continue and back buttons
function setupNavigation() {
    continueButton.addEventListener('click', () => {
        if (backCount < 2) {
            backCount += 1;
            updateDisplays();
        }
    });
    back.addEventListener('click', () => {
        if (backCount > 0) {
            backCount -= 1;
            updateDisplays();
        }
    });
    voiceBox1.addEventListener('click', () => {
        if (backCount < 2) {
            backCount += 1;
            updateDisplays();
        }
    });
}

// main function call
document.addEventListener("DOMContentLoaded", () => {
    toggleVoiceContainer();
    setupNavigation();
    updateDisplays();
});
