const fileName = document.querySelector('.fileName');
const fileNameEdit = document.querySelector('.fileNameEdit');
const inputField = fileNameEdit.querySelector('input');
const exportButton = document.querySelector('.export')
const exportDisplayContainer = document.querySelector('.exportOptionsPopup')

fileName.addEventListener('dblclick', function () {
    fileName.style.display = 'none';
    fileNameEdit.style.display = 'flex';
    inputField.value = fileName.querySelector('span').textContent;
    inputField.focus();
});

inputField.addEventListener('blur', updateFileName);
inputField.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        updateFileName();
    }
});

function updateFileName() {
    const newValue = inputField.value.trim();
    if (newValue) {
        fileName.querySelector('span').textContent = newValue;
    }
    fileName.style.display = 'flex';
    fileNameEdit.style.display = 'none';
}


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

exportOptions(exportButton, exportDisplayContainer);