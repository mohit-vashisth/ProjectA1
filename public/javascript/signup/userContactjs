const contactNumber = document.querySelector("#contactNumber");
const countryCode = document.querySelector("#countryCode");
let countryData = [];

async function populateCountryCodes() {
  try {
    const response = await fetch("/public/data/countryCodes.json");
    if (!response.ok) throw new Error("Failed to load country codes");

    countryData = await response.json();

    countryData.forEach(country => {
      const option = document.createElement("option");
      option.value = country.dial_code;
      option.textContent = `${country.name} (${country.dial_code})`;
      countryCode.appendChild(option);
    });

    if (countryData.length > 0) {
      countryCode.value = countryData[0].dial_code;
    }

    countryCode.addEventListener("change", function () {
      contactNumber.value = this.value + " ";
    });

    contactNumber.addEventListener("input", function () {
      syncDropdownWithInput();
    });

    return `${countryCode.value} ${contactNumber.value.trim().replace(/\s+/g, " ")}`;

  } catch (error) {
    console.error("Error loading country codes:", error);
    return null;
  }
}

function syncDropdownWithInput() {
  let inputValue = contactNumber.value.trim();

  for (const country of countryData) {
    if (inputValue.startsWith(country.dial_code)) {
      countryCode.value = country.dial_code;
      inputValue = country.dial_code + " " + inputValue.slice(country.dial_code.length).trim();
      contactNumber.value = inputValue;
      return;
    }
  }
}

export async function initializePhoneInput() {
  return await populateCountryCodes();
}