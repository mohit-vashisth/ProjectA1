import { selectedLanguage } from "../UI/populateTranslateLangOptions"
import { displayError } from "../utils/errorDisplay"
import { userFinalSpeech } from "./generateSpeechService"

const translateButton = document.querySelector(".translateSpeechBtn")
const inputArea = document.querySelector("#inputText")
const translateBtn = document.querySelector(".translateSpeechBtn")
const generateBtn = document.querySelector(".generateSpeechBtn")
const translateURL = import.meta.env.VITE_TRANSLATE_SPEECH_EP

let currentController = null
let translateSpeechOb = {
    languageCode: null,
    userSpeech: null
}

async function translateHandle() {

    translateBtn.disabled = true
    generateBtn.disabled = true
    if(currentController){
        currentController.abort()
        currentController = null
    }
    
    translateSpeechOb.languageCode = selectedLanguage()
    translateSpeechOb.userSpeech = userFinalSpeech()

    currentController = new AbortController()
    let timeout;
    try {
        timeout = setTimeout(()=>{
            currentController.abort()
            currentController = null
            displayError("Request Aborted")
        })
        const response = await fetch(translateURL, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            credentials: "include",
            body: JSON.stringify(translateSpeechOb),
            signal: currentController.signal,
        })
        clearTimeout(timeout)

        translateBtn.disabled = false
        generateBtn.disabled = false

        const data = await response.json();
        if (!response.ok) {
            const errorDetails = data?.detail || "Something went wrong. Try again.";
            switch (response.status) {
                case 400:
                    displayError(errorDetails || "Invalid input. Please check your text or voice selection.");
                    break;
                case 401:
                    displayError(errorDetails || "You are not logged in. Please log in and try again.");
                    break;
                case 404:
                    displayError(errorDetails || "The requested resource was not found.");
                    break;
                case 500:
                    displayError(errorDetails || "A server error occurred. Please try again later.");
                    break;
                default:
                    displayError(errorDetails);
            }
            return;
        }

        if(data){
            inputArea.value = ""
            inputArea.value = data.userSpeech
        }
        else{
            displayError("Unable to translate speech")
        }

    } catch (error) {
        clearTimeout(timeout)
        if(error.message === "AbortError"){
            displayError("Request Aborted")
        }
        else{
            displayError("Something went wrong. Try again.")
        }
    }
    finally{
        clearTimeout(timeout)
        translateBtn.disabled = false
        generateBtn.disabled = false
    }

}

export function translateServiceEXP() {
    translateButton.addEventListener("click", translateHandle)
}
