const recentChatsButton = document.querySelector('.recentChatsButton');
const chatsSection = document.querySelector('.chatsSection');

function openCloseChatList(button, display) {
    if (button && display) {
        button.addEventListener('click', function () {
            if (!display.classList.contains('openChatListDisplay')) {
                button.classList.add('openChatList');
                display.classList.add('openChatListDisplay');
            } else {
                button.classList.remove('openChatList');
                display.classList.remove('openChatListDisplay');
            }
        });
    }
}

openCloseChatList(recentChatsButton, chatsSection);
