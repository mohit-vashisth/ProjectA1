const websiteHolderIcon = document.querySelector('.aboutWebsite_toolkitHolder');
const websiteInfoDisplayPopup = document.querySelector('.aboutWebsiteToolKitContainer');

websiteHolderIcon.addEventListener('click', function (event) {
  event.stopPropagation();
  websiteInfoDisplayPopup.classList.toggle('activeWebsiteInfo');
});

document.addEventListener('click', function () {
  websiteInfoDisplayPopup.classList.remove('activeWebsiteInfo');
});

websiteInfoDisplayPopup.addEventListener('click', function (event) {
  event.stopPropagation();
});
