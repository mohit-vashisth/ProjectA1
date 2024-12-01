const chatLoader = document.getElementById("chatLoader");
const leftSectionChatLoaderAnimation = document.querySelector(".leftSectionChatLoaderAnimation");

function showLoader() {
  chatLoader.style.display = "block";
  leftSectionChatLoaderAnimation.style.display = "flex";
}
function hideLoader() {
  chatLoader.style.display = "none";
  leftSectionChatLoaderAnimation.style.display = "none";
}
function loadChats() {
  showLoader();

  setTimeout(() => {
    hideLoader();
  }, 1500);
}

loadChats();
