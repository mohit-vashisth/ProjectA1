document.addEventListener('DOMContentLoaded', ()=>{

    const newChatButton = document.querySelector('.newChat');

    function openNewChat(button) {
        const projectA1Path = "/frontend/pages/projectA1.html";
        try{
            if(projectA1Path.trim() !== ""){
                    window.location.href = projectA1Path.trim();
            } else{
                setTimeout(() => {
                    window.location.href = "/frontend/pages/error/404.html";
                }, 5000);
            }
        }
        catch{
        }
    }

    newChatButton.addEventListener('click', openNewChat)

















})