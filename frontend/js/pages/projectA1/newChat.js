document.addEventListener('DOMContentLoaded', () => {
    const newChat = document.querySelector(".newChat");

    // Access baseURL dynamically from environment variables
    const baseURL = window.location.origin.includes('localhost') 
        ? import.meta.env.VITE_PROJECTA1_URL // Local environment URL
        : import.meta.env.VITE_PROJECTA1_URL; // Production URL

    newChat.addEventListener('click', () => {
        window.location.href = baseURL; // Redirect to the ProjectA1 URL
    });
});
