import { userCurrentChatEXP } from "./chatListService";
import { displayError } from "../utils/errorDisplay";

const fileName = document.querySelector(".fileName");
const fileNameEdit = document.querySelector(".fileNameEdit");
const inputField = fileNameEdit?.querySelector("input");

const renameURL = import.meta.env.VITE_RENAME_EP;
let currentController = null;
let previousFileName = ""; // Store previous name to restore in case of failure

function setCurrentFileName() {
  const currentName = userCurrentChatEXP();
  if (fileName) {
    fileName.textContent = currentName?.name || "untitled";
    previousFileName = fileName.textContent; // Store the initial file name
  }
}

function openInputField() {
  if (!fileName || !fileNameEdit || !inputField) return;

  fileName.style.display = "none";
  fileNameEdit.style.display = "flex";
  inputField.value = fileName.textContent;
  inputField.focus();
}

async function updateName() {
  if (!inputField || !fileName || !fileNameEdit) return;

  const newName = inputField.value.trim();
  if (!newName) {
    displayError("Name cannot be empty!");
    return;
  }

  if (currentController) {
    currentController.abort();
    currentController = null;
  }

  currentController = new AbortController();

  try {
    const timeout = setTimeout(() => {
      currentController.abort();
      displayError("Request Timeout!");
    }, 8000);

    const response = await fetch(renameURL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      signal: currentController.signal,
      body: JSON.stringify({ newName }),
    });

    clearTimeout(timeout);

    const data = await response.json();

    if (!response.ok || !data?.success || !data.newName) {
      throw new Error(data?.detail || "Failed to rename file.");
    }

    fileName.textContent = data.newName;
    previousFileName = data.newName; // Update previous name only on success
    fileName.style.display = "flex";
    fileNameEdit.style.display = "none";
  } catch (error) {
    displayError(error.message || "An unexpected error occurred.");
    fileName.textContent = previousFileName; // Restore previous name on failure
  } finally {
    fileName.style.display = "flex";
    fileNameEdit.style.display = "none";
    inputField.value = previousFileName; // Ensure the input field resets
  }
}

function handleNameChange() {
  if (!inputField) return;

  inputField.addEventListener("blur", updateName);
  inputField.addEventListener("keypress", (event) => {
    if (event.key === "Enter") updateName();
  });
}

if (fileName) fileName.addEventListener("dblclick", openInputField);

export function handleCurrentFileNameEXP() {
  handleNameChange();
  setCurrentFileName();
}
