const chatMenuIcon = document.querySelector('.chatMenuImageHolder img');
const chatMenuOptionsVisibility = document.querySelector('.chatMenuOptions');
const backgroundBlueOfChatHistory = document.querySelector('.chatDetailsHolder');

chatMenuIcon.addEventListener('click', function(event) {
    event.stopPropagation(); 
    chatMenuOptionsVisibility.style.visibility = 
        chatMenuOptionsVisibility.style.visibility === 'visible' ? 'hidden' : 'visible';

    backgroundBlueOfChatHistory.style.filter = 
        backgroundBlueOfChatHistory.style.filter === 'blur(4px)' ? 'none' : 'blur(4px)';
});

document.addEventListener('click', function(event) {
    if (!chatMenuOptionsVisibility.contains(event.target) && !chatMenuIcon.contains(event.target)) {
        chatMenuOptionsVisibility.style.visibility = 'hidden';
        backgroundBlueOfChatHistory.style.filter = 'none';
    }
});
