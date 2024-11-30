const shareChat = document.querySelector(".shareChat");
const shareChatPopupHolder = document.querySelector(".shareChatPopupHolder");

shareChat.addEventListener("click", function (event) {
  event.stopPropagation();

  if (shareChatPopupHolder.style.display === 'none' || !shareChatPopupHolder.style.display) {
    shareChatPopupHolder.style.display = 'flex';
  } else {
    shareChatPopupHolder.style.display = 'none';
  }
});

document.addEventListener("click", function (event) {
  if (!shareChat.contains(event.target) && !shareChatPopupHolder.contains(event.target)) {
    shareChatPopupHolder.style.display = 'none';
  }
});
