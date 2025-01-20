// Selectors
const storageContainer = document.querySelector('.storagePopup');
const storageButton = document.querySelector('.storageAudios');
const selectAllCheckbox = document.querySelector('.checkboxSelect');
const deleteChatButton = document.querySelector('.deleteChatButton');
const chatList = document.querySelector('.chatList');

//--------------Open-Close Display---------------------
function openCloseStorage() {
    if (storageButton && storageContainer) {
        storageButton.addEventListener('click', function () {
            if (storageContainer.style.display === "flex") {
                storageContainer.style.display = "none";
                storageButton.classList.remove("storageActive");
            } else {
                storageContainer.style.display = "flex";
                storageButton.classList.add("storageActive");
            }
        });

        document.addEventListener('click', function (event) {
            if (!storageContainer.contains(event.target) && !storageButton.contains(event.target)) {
                storageContainer.style.display = "none";
                storageButton.classList.remove("storageActive");
            }
        });
    }
}

// --------------Filter Chats-----------------------

function filterChats() {
    const searchInput = document.querySelector('.searchInput');
    const chatListItems = document.querySelectorAll('#chatList li');

    searchInput.addEventListener('input', function () {
        const query = searchInput.value.toLowerCase();

        chatListItems.forEach(chat => {
            const chatName = chat.querySelector('.chatName').textContent.toLowerCase();
            if (chatName.includes(query)) {
                chat.style.display = "flex"; // Show the matching chat
            } else {
                chat.style.display = "none"; // Hide non-matching chats
            }
        });
    });
}

//--------------Select All Chats---------------------
function selectAllChats() {
    if (selectAllCheckbox && chatList) {
        selectAllCheckbox.addEventListener('change', function () {
            const chatCheckboxes = chatList.querySelectorAll('.chatCheckbox');
            chatCheckboxes.forEach(checkbox => {
                checkbox.checked = selectAllCheckbox.checked;
            });
        });
    }
}

//--------------Delete Selected Chats---------------------
function deleteChats() {
    if (deleteChatButton && chatList) {
        deleteChatButton.addEventListener('click', function () {
            const chatCheckboxes = chatList.querySelectorAll('.chatCheckbox:checked');
            chatCheckboxes.forEach(checkbox => {
                checkbox.closest('li').remove();
            });
            // Uncheck "Select All" if all chats are deleted
            if (chatList.querySelectorAll('li').length === 0) {
                selectAllCheckbox.checked = false;
            }
        });
    }
}

//--------------Rename a Single Chat---------------------
function renameChats() {
    if (chatList) {
        chatList.addEventListener('dblclick', function (event) {
            const chatNameSpan = event.target.closest('li')?.querySelector('.chatName');
            if (chatNameSpan) {
                const newName = prompt("Enter new name for the chat:", chatNameSpan.textContent);
                if (newName) {
                    chatNameSpan.textContent = newName;
                }
            }
        });
    }
}

//--------------Select a Single Chat---------------------
function selectChats() {
    if (chatList) {
        chatList.addEventListener('change', function (event) {
            if (event.target.classList.contains('chatCheckbox')) {
                // Uncheck "Select All" if any chat is unchecked
                if (!event.target.checked) {
                    selectAllCheckbox.checked = false;
                } else {
                    // Check "Select All" if all chats are selected
                    const chatCheckboxes = chatList.querySelectorAll('.chatCheckbox');
                    const allChecked = Array.from(chatCheckboxes).every(checkbox => checkbox.checked);
                    selectAllCheckbox.checked = allChecked;
                }
            }
        });
    }
}
// Initialize all functionalities
openCloseStorage();
filterChats();
selectAllChats();
deleteChats();
renameChats();
selectChats();
