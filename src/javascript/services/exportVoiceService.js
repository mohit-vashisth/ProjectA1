const exportButton = document.querySelector('.export')
const exportDisplayContainer = document.querySelector('.exportOptionsPopup')

function exportOptions(button, displayContainer) {
    if(button && displayContainer){
        button.addEventListener('click', function(){
            displayContainer.style.display = "flex";
        });
        document.addEventListener('click', function(event){
            if(!displayContainer.contains(event.target) && event.target !== button){
            displayContainer.style.display = "none";
            }
        })
    }
}

export function exportVoiceEXP() {
    exportOptions(exportButton, exportDisplayContainer);
}

// this export functionality we will do it later 