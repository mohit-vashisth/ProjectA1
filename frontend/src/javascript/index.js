const exploreProjectA1 = document.getElementById("exploreProjectA1");

exploreProjectA1.addEventListener("click", () => {
    window.location.href = "src/pages/signup.html";
});

// model
// Get elements
const openChatbotBtn = document.getElementById("openChatbot");
const chatbotModal = document.getElementById("chatbotModal");
const closeBtn = document.getElementsByClassName("closeBtn")[0];
const sendMessageBtn = document.getElementById("sendMessage");
const chatInput = document.getElementById("chatInput");
const chatbotMessages = document.querySelector(".chatbot-messages");

// Predefined questions for quick replies
const predefinedQuestions = [
    "What is Project A1?",
    "Tell me about 3R Minds.",
    "How can I get started?",
    "Do you provide customer support?",
    "What technologies are used in Project A1?",
    "Can I use Project A1 for free?",
    "How do I contact customer support?",
    "Can I collaborate with 3R Minds?",
    "What are the system requirements?",
    "How secure is Project A1?"
];

// Open the chatbot modal when "Contact Us" button is clicked
openChatbotBtn.addEventListener("click", () => {
    chatbotModal.style.display = "flex";  // Show the modal
});

// Close the chatbot modal
closeBtn.addEventListener("click", () => {
    chatbotModal.style.display = "none";  // Hide the modal
});

// Display the preloaded questions when user clicks a button
const questionButtons = document.querySelectorAll(".user-message");
questionButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const userMessage = button.textContent;
        addMessage(userMessage, "user");  // Display user message
        chatInput.value = "";  // Clear input box

        // Simulate bot response (can later be replaced with actual AI logic)
        setTimeout(() => {
            const botResponse = `You asked about: ${userMessage}`;
            addMessage(botResponse, "bot");  // Display bot message
        }, 1000);  // Simulate delay
    });
});

// Function to add message to chat
function addMessage(message, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", `${sender}-message`);
    messageDiv.textContent = message;
    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;  // Scroll to bottom
}

// Send button functionality for custom messages
sendMessageBtn.addEventListener("click", () => {
    const userMessage = chatInput.value.trim();
    if (userMessage !== "") {
        addMessage(userMessage, "user");  // Display user message
        chatInput.value = "";  // Clear input box

        // Simulate bot response (can later be replaced with actual AI logic)
        setTimeout(() => {
            const botResponse = `You said: ${userMessage}`;
            addMessage(botResponse, "bot");  // Display bot message
        }, 1000);  // Simulate delay
    }
});

// Close modal on clicking outside
window.onclick = (event) => {
    if (event.target === chatbotModal) {
        chatbotModal.style.display = "none";  // Hide the modal
    }
};
