import { userCurrentChatEXP } from "./chatListService";
import { displayError } from "../utils/errorDisplay";

const fileName = document.querySelector(".fileName");
const fileNameEdit = document.querySelector(".fileNameEdit");
const inputField = fileNameEdit.querySelector("input");

const baseURL = import.meta.env.VITE_BASE_URL;

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

    const response = await fetch(baseURL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      signal: currentController.signal,
      body: JSON.stringify(payload),
    });
    clearTimeout(timeout);

    if (!response.ok) {
      displayError("Something went wrong, Try Again.");
      return;
    }

    const data = await response.json();

    if (data?.success && data.newName) {
      fileName.querySelector("span").textContent = data.newName;
      fileName.style.display = "block";
      fileNameEdit.style.display = "none";
    } else {
      displayError("Unable to change name, try again later.");
    }
  } catch (error) {
    if (error.name === "AbortError") {
      displayError("Request timeout");
    } else {
      displayError("Unexpected error occurred.");
    }
  } finally {
    clearTimeout(timeout);
    currentController = null;
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

export function handleCurrentFileNameEXP() {
  fileName.addEventListener("dblclick", openInputField);
  handleNameChange();
  setCurrentFileName();
}
