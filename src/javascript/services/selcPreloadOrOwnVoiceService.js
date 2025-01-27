document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById("inputText");
  
    // Add an input event listener
    textarea.addEventListener("input", function () {
        this.style.height = "auto"; // Reset height to auto for recalculation
        this.style.height = this.scrollHeight + "px"; // Set height based on scrollHeight
    });
  });
  
  document.addEventListener("DOMContentLoaded", function () {
      const preAvailableRadio = document.getElementById("preAvailable");
      const useOwnVoiceRadio = document.getElementById("useOwnVoice");
      const preAvailableDropdown = document.getElementById("preAvailableDropdown");
      const useOwnVoiceDropdown = document.getElementById("useOwnVoiceDropdown");
      // Enable/disable dropdown based on selected radio button
      preAvailableRadio.addEventListener("change", function () {
        if (preAvailableRadio.checked) {
          preAvailableDropdown.disabled = false;
          useOwnVoiceDropdown.disabled = true;
        }
      });
    
      useOwnVoiceRadio.addEventListener("change", function () {
        if (useOwnVoiceRadio.checked) {
          useOwnVoiceDropdown.disabled = false;
          preAvailableDropdown.disabled = true;
        }
      });
    });
  
  