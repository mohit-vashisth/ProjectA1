const aboutWebsitePopupContainer = document.querySelector('.aboutWebsitePopupContainer');
const about = document.querySelector('.about');
const aboutLinksContainer = document.querySelector('.aboutWItems'); // Parent container for delegation
const legalURL = import.meta.env.VITE_LEGAL_3RMINDS_PAGE;

// Generic popup handler
function handlePopup(trigger, popup) {
  if (!trigger || !popup) return;

  // Toggle popup
  const togglePopup = (show) => popup.classList.toggle('active', show);

  trigger.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent immediate document click handler
    togglePopup(true);
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!popup.contains(e.target) && e.target !== trigger) {
      togglePopup(false);
    }
  });

  // Close on ESC key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') togglePopup(false);
  });
}

// Event delegation for links
function handleLegalLinks(e) {
  const target = e.target.closest('li');
  if (!target) return;
  
  e.preventDefault();
  window.location.assign(legalURL); // Better than href assignment
}

export function aboutWWebsiteEXP() {
  handlePopup(about, aboutWebsitePopupContainer);
  
  if (aboutLinksContainer) {
    aboutLinksContainer.addEventListener('click', handleLegalLinks);
  }
}

document.addEventListener('DOMContentLoaded', aboutWWebsiteEXP);