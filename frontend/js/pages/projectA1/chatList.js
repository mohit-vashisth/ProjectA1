const recentChatsButton = document.querySelector('.recentChatsButton');
const chatsSection = document.querySelector('.chatsSection');
const iconRotate = document.querySelector('.dropdownRecentChats img');

function openCloseChatList(button, display, iconRotate) {
    if (button && display && iconRotate) {
        button.addEventListener('click', function () {
            if (!display.classList.contains('openChatListDisplay')) {
                button.classList.add('openChatList');
                display.classList.add('openChatListDisplay');
                iconRotate.style.transform = 'rotate(180deg)';
            } else {
                button.classList.remove('openChatList');
                display.classList.remove('openChatListDisplay');
                iconRotate.style.transform = 'rotate(0deg)';
            }
        });
    }
}

openCloseChatList(recentChatsButton, chatsSection, iconRotate);
