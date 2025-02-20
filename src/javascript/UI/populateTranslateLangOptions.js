const dropdown = document.querySelector("#speechOptionLanguages");
const languages = [
  { code: "en", name: "English" },
  { code: "hi", name: "Hindi" }
];

let selectedLang = {
    languageCode: "hi",
    languageName: "Hindi"
};
function populateLanguages() {
    languages.forEach((lang) => {
      dropdown.value = "hi";
      const option = document.createElement("option");
      option.value = lang.code;
      option.textContent = lang.name;
      dropdown.appendChild(option);
    });
}
populateLanguages();

export function selectedLanguage() {
    dropdown.addEventListener("blur", (event) => {
        selectedLang.languageCode = event.target.value;
        selectedLang.languageName = event.target.options[event.target.selectedIndex].textContent;
    });

    return selectedLang;
}
