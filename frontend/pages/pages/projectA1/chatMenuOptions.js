const chatMenuIcon = document.querySelector('.chatMenuIcon');
const chatMenuOptions = document.querySelector('.chatMenuOptions');

chatMenuOptions.classList.add('hideChatMenu');
chatMenuOptions.style.visibility = 'hidden';
chatMenuOptions.style.opacity = '0';

function convertPxToVmin(pxValue) {
    const vmin = Math.min(window.innerWidth, window.innerHeight);
    return (pxValue / vmin) * 100; 
}

function showChatMenu(event) {
    chatMenuOptions.classList.remove('hideChatMenu');
    const leftInVmin = convertPxToVmin(event.clientX);
    const topInVmin = convertPxToVmin(event.clientY + 20);
    
    chatMenuOptions.style.left = `${leftInVmin}vmin`;
    chatMenuOptions.style.top = `${topInVmin}vmin`;
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
