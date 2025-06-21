const dropdown = document.querySelector("#speechOptionLanguages");
const languages = [
  { code: "hi", name: "Hindi" },
  { code: "en", name: "English" }
];

let selectedLangCode = "en"; // Default to Hindi

function populateLanguages() {
    dropdown.innerHTML = ""; // Clear any existing options
    languages.forEach((lang) => {
      const option = document.createElement("option");
      option.value = lang.code;
      option.textContent = lang.name;
      dropdown.appendChild(option);
    });
    dropdown.value = selectedLangCode; // Set default value
}

populateLanguages();

dropdown.addEventListener("input", (event) => {
    selectedLangCode = event.target.value;
});

// Function to get the latest selected language
export function selectedLanguage() {
    return selectedLangCode;
}
