const shareChat = document.querySelector(".shareChat");
const shareChatPopupHolder = document.querySelector(".shareChatPopupHolder");

shareChat.addEventListener("click", function (event) {
  event.stopPropagation();
  if (shareChatPopupHolder.style.display === "flex") {
    shareChatPopupHolder.style.display = "none";
  } else {
    shareChatPopupHolder.style.display = "flex";
  }
});

document.addEventListener("click", function (event) {
  if (!shareChat.contains(event.target) && !shareChatPopupHolder.contains(event.target)) {
    shareChatPopupHolder.style.display = "none";
  }
});

shareChatPopupHolder.style.display = "none";
