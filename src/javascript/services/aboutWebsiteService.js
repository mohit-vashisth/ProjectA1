const aboutWebsitePopupContainer = document.querySelector('.aboutWebsitePopupContainer');
const about = document.querySelector('.about');
const aboutLinks = document.querySelectorAll('.aboutWItems li');
const legalURL = import.meta.env.VITE_LEGAL_3RMINDS_PAGE;


function aboutWebsiteDisplay(aboutButton, popupContainer) {
    if (aboutButton && popupContainer) {
        aboutButton.addEventListener('click', function () {
            popupContainer.style.display = "flex";
        });

        document.addEventListener('click', function (event) {
            if (!popupContainer.contains(event.target) && event.target !== aboutButton) {
                popupContainer.style.display = "none";
            }
        });
    }
}

export function aboutWWebsiteEXP() {
    
aboutWebsiteDisplay(about, aboutWebsitePopupContainer);


aboutLinks.forEach(element => {
    element.addEventListener("click", (e)=>{
        e.preventDefault()
        window.location.href = legalURL;
    })
});
}