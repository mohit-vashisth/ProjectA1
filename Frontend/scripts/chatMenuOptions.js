const chatMenuIcon = document.querySelector('.chatMenuIcon');
const chatMenuOptions = document.querySelector('.chatMenuOptions');

chatMenuOptions.classList.add('hideChatMenu');
chatMenuOptions.style.visibility = 'hidden';
chatMenuOptions.style.opacity = '0';

function showChatMenu(event) {
    chatMenuOptions.classList.remove('hideChatMenu');
    chatMenuOptions.style.left = `${event.clientX}px`;
    chatMenuOptions.style.top = `${event.clientY + 20}px`;
    chatMenuOptions.style.visibility = 'visible';
    chatMenuOptions.style.opacity = '1';
}

function hideChatMenu() {
    chatMenuOptions.classList.add('hideChatMenu');
    chatMenuOptions.style.visibility = 'hidden';
    chatMenuOptions.style.opacity = '0';
}

chatMenuIcon.addEventListener('click', function (event) {
    event.preventDefault();
    if (chatMenuOptions.classList.contains('hideChatMenu')) {
        showChatMenu(event);
    } else {
        hideChatMenu();
    }
});

document.addEventListener('click', function (e) {
    if (!chatMenuOptions.contains(e.target) && !chatMenuIcon.contains(e.target)) {
        hideChatMenu();
    }
});