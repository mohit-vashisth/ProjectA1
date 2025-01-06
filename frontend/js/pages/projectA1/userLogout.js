const logoutPopupContainer = document.querySelector('.logoutPopupContainer');
const logoutIcon = document.querySelector('.logoutIcon');
const yesButton = document.querySelector('.yesButton');
const noButton = document.querySelector('.noButton');

function logoutDisplay(logoutButton, popupContainer) {
    if (logoutButton && popupContainer) {
        logoutButton.addEventListener('click', function () {
            popupContainer.style.display = "flex";
        });

        document.addEventListener('click', function (event) {
            if (!popupContainer.contains(event.target) && event.target !== logoutButton) {
                popupContainer.style.display = "none";
            }
        });
    }
}

function confirmLogout(yesButton, noButton) {
    if(yesButton && noButton){
        if(yesButton){
            yesButton.addEventListener('click', function(){
                window.location.href = "/frontend/pages/auth/login.html";
            })
            
            noButton.addEventListener('click', function(){
                logoutPopupContainer.style.display = "none"
            })
        }
    }
}

logoutDisplay(logoutIcon, logoutPopupContainer);
confirmLogout(yesButton, noButton)