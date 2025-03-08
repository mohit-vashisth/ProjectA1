import { userCurrentChatEXP } from "./chatListService";
import { displayError } from "../utils/errorDisplay";

const fileName = document.querySelector(".fileName");
const fileNameEdit = document.querySelector(".fileNameEdit");
const inputField = fileNameEdit.querySelector("input");

const renameURL = import.meta.env.VITE_RENAME_EP;

let currentController = null;

function setCurrentFileName() {
  const currentName = userCurrentChatEXP();
  fileName.textContent = currentName.name ? currentName.name : "untitled";
}

function openInputField() {
  fileName.style.display = "none";
  fileNameEdit.style.display = "flex";
  inputField.value = fileName.querySelector("span").textContent;
  inputField.focus();
}

async function updateName() {
  if (currentController) {
    currentController.abort();
    currentController = null;
  }
  currentController = new AbortController();

  const payload = { newName: inputField.value.trim() };
  if (!payload.newName) {
    displayError("Name cannot be empty!");
    return;
  }

  try {
    const timeout = setTimeout(() => {
      currentController.abort();
      displayError("Request Aborted!");
    }, 8000);

    const response = await fetch(renameURL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      signal: currentController.signal,
      body: JSON.stringify(payload),
    });
    clearTimeout(timeout);

    const data = await response.json();
      if (!response.ok) {
        const errorDetails = data?.detail;
        displayError(errorDetails);
      }

    if (data?.success && data.newName) {
      fileName.querySelector("span").textContent = data.newName;
      fileName.style.display = "block";
      fileNameEdit.style.display = "none";
    } else {
      displayError("Unable to change name, try again later.");
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

function handleNameChange() {
  inputField.addEventListener("blur", updateName);
  inputField.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      updateName();
    }
  });
}

fileName.addEventListener("dblclick", openInputField);
export function handleCurrentFileNameEXP() {
  handleNameChange();
  setCurrentFileName();
}