const exportButton = document.querySelector('.export');
const exportDisplayContainer = document.querySelector('.exportOptionsPopup');

function exportOptions(button, displayContainer) {
    if (button && displayContainer) {
        button.addEventListener('click', function (event) {
            event.stopPropagation();
            displayContainer.style.display = displayContainer.style.display === "flex" ? "none" : "flex";
        });

        document.addEventListener('click', function (event) {
            if (!displayContainer.contains(event.target) && event.target !== button) {
                displayContainer.style.display = "none";
            }
        });

        displayContainer.addEventListener('click', (event) => event.stopPropagation());
    }
}

export function exportVoiceEXP() {
    exportOptions(exportButton, exportDisplayContainer);
}
