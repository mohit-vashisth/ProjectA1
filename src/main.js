const openChatbotBtn = document.getElementById("openChatbot");
const chatbotModal = document.getElementById("chatbotModal");
const closeBtn = document.getElementsByClassName("closeBtn")[0];
const sendMessageBtn = document.getElementById("sendMessage");
const chatInput = document.getElementById("chatInput");
const chatbotMessages = document.querySelector(".botResponses");

const exploreProjectA1 = document.getElementById("exploreProjectA1");

exploreProjectA1.addEventListener("click", () => {
    window.location.href = "/frontend/pages/signup.html";
});

const predefinedQuestions = [
    "how can i get started with project a1?",
    "what is 3r minds, and what does it do?",
    "is project a1 available for free?",
    "what are the benefits of the paid version of project a1?",
    "does project a1 offer customer support?",
    "can i request a refund for the paid version of project a1?",
    "how secure is project a1?",
    "what career opportunities are available at 3r minds?",
];

const predefinedAnswers = [
    "You can get started by signing up with your Gmail account or logging in if you already have an account. Our website provides step-by-step guidance for a smooth onboarding process.",
    "3R Minds is an emerging company founded with a vision to create innovative AI-driven solutions that are practical, engaging, and fun to use.",
    "Yes, Project A1 is currently free for all users. You also get access to the latest AI models and updates at no additional cost.",
    "The paid version of Project A1 includes advanced voice features, additional customization options, and enhanced access to premium AI functionalities.",
    "At the moment, we provide static customer support via email and FAQs. However, we plan to introduce live customer support in the near future.",
    "3R Minds values its customers and guarantees a 100% refund if you are unsatisfied with the paid version of Project A1.",
    "Project A1 prioritizes user data security. We do not sell or share any user data. For more information, please refer to our Privacy Policy.",
    "3R Minds is a newly established company founded by three college friends. It offers open career opportunities for talented individuals passionate about AI and technology.",
];

openChatbotBtn.addEventListener("click", () => {
    chatbotModal.style.display = "flex";
});

closeBtn.addEventListener("click", () => {
    chatbotModal.style.display = "none";
});

function findQuestionIndex(userMessage) {
    const formattedMessage = userMessage.trim().toLowerCase();
    return predefinedQuestions.findIndex(
        (question) => question === formattedMessage
    );
}

document.querySelectorAll(".user-message").forEach((button) => {
    button.addEventListener("click", () => {
        const userMessage = button.textContent.trim();
        addMessage(userMessage, "user");

        setTimeout(() => {
            const questionIndex = findQuestionIndex(userMessage);
            const botResponse =
                questionIndex >= 0
                    ? predefinedAnswers[questionIndex]
                    : "Sorry, I don't have an answer for that question.";
            addMessage(botResponse, "bot");
        }, 1000);
    });
});

sendMessageBtn.addEventListener("click", () => {
    const userMessage = chatInput.value.trim();
    if (userMessage !== "") {
        addMessage(userMessage, "user");
        chatInput.value = "";

        setTimeout(() => {
            const questionIndex = findQuestionIndex(userMessage);
            const botResponse =
                questionIndex >= 0
                    ? predefinedAnswers[questionIndex]
                    : "Sorry, I don't have an answer for that. Could you rephrase?";
            addMessage(botResponse, "bot");
        }, 1000);
    }
});

function addMessage(message, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", `${sender}-message`);
    messageDiv.textContent = message;
    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

window.onclick = (event) => {
    if (event.target === chatbotModal) {
        chatbotModal.style.display = "none";
    }
};
