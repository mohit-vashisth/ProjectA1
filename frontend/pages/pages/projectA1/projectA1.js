document.addEventListener("DOMContentLoaded", ()=>{

    const newChatButton = document.querySelector('.newChat');
    function openNewChat(button) {
        try{
            button.addEventListener('click', ()=>{
                window.location.href = '/frontend/pages/projectA1.html';
            })
        }
        catch{
            window.location.href = "";
        }
    }

    openNewChat(newChatButton)



























})