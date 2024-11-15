const getTextFromInput = document.querySelector('.askModel_response');
const sendResponseToModelButton = document.querySelector('.askModel_button');
const chatContainer = document.querySelector('.rightLowerSectionItemsHolder');

// Function to check if the message is empty and enable/disable the send button
function sendButtonCheck() {
  if (getTextFromInput.value.trim() !== "") {
    sendResponseToModelButton.disabled = false;
    sendResponseToModelButton.style.cursor = 'pointer';
    sendResponseToModelButton.style.opacity = '1';
  } else {
    sendResponseToModelButton.disabled = true;
    sendResponseToModelButton.style.cursor = 'not-allowed';
    sendResponseToModelButton.style.opacity = '0.5';
  }
}

// Function to reset the input area after sending a message
function resetInputArea() {
  getTextFromInput.value = ''; // Clear the text
  getTextFromInput.style.height = '40px'; // Reset height to default (adjust if needed)
}

// Function to escape HTML tags to display them as plain text
function escapeHtml(text) {
  const element = document.createElement('div');
  if (text) {
    element.innerText = text;
    element.textContent = text;
  }
  return element.innerHTML;
}

// Function to append the user's message
function appendUserMessage(message) {
  const userChatContainer = document.createElement('article');
  userChatContainer.className = 'userChat_responseContainer';
  
  const escapedMessage = escapeHtml(message); // Escape HTML tags

  userChatContainer.innerHTML = `<div class="userChat_Holder">
    <div class="userChatMainImageHolder">
      <div class="chatOfUser">
        <div class="responseNow">${escapedMessage}</div> <!-- Display escaped HTML here -->
      </div>
    </div>
  </div>`;
  
  chatContainer.appendChild(userChatContainer);
  chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the latest message
}

// Function to append the model's response
function appendModelMessage(message) {
  const modelChatContainer = document.createElement('article');
  modelChatContainer.className = 'modelChat_responseContainer';

  modelChatContainer.innerHTML = `
    <div class="modelChat_Holder">
      <div class="modelChatMainImageHolder">
        <div class="imageOfModel">
          <img src="images/svgs/voiceClone.svg" alt="model logo" />
        </div>
        <div class="chatOfModel">
          <span>${message}</span>
          <div class="modelChatRegenerateLikeDislikeHolder">
            <div class="modelChatOptionsHolder">
              <div class="readTextHolder">
                <img src="images/svgs/volume.svg" title="Read Text" alt="">
              </div>
              <div class="thumbUpHolder">
                <img src="images/svgs/thumbup.svg" title="Like" alt="">
              </div>
              <div class="thumbDownHolder">
                <img src="images/svgs/thumbdown.svg" title="Dislike" alt="">
              </div>
              <div class="reGenerateHolder">
                <img src="images/svgs/reload.svg" title="Regenerate" alt="">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  chatContainer.appendChild(modelChatContainer);
  chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the latest message
}

// Function to send the message
function sendMessage() {
  let message = getTextFromInput.value.trim(); // Trim leading and trailing spaces only

  if (message) {
    appendUserMessage(message);
    getTextFromInput.value = "";
    sendButtonCheck();
    // Now only send model response when explicitly triggered, not automatically
    // Commenting out automatic model response
    // sendModelResponse(message);
    resetInputArea(); // Reset the input area after sending
  }
}

// Handle input event to enable/disable the send button
getTextFromInput.addEventListener('input', sendButtonCheck);

// Handle 'Enter' key event to send the message or add a newline
getTextFromInput.addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    if (event.shiftKey) {
      getTextFromInput.value += "\n"; // Add a newline if Shift + Enter is pressed
    } else {
      event.preventDefault(); // Prevent default behavior (form submit)
      sendMessage();
    }
  }
});

// Send button click event to trigger message sending
sendResponseToModelButton.addEventListener('click', sendMessage);

// Simulate the model response (replace this with actual API logic)
function sendModelResponse(userMessage) {
  const simulatedModelResponse = `not able to fetch data: "${userMessage}"`;
  appendModelMessage(simulatedModelResponse);
}

// Auto resize the input area based on content
getTextFromInput.addEventListener('input', function () {
  this.style.height = 'auto'; // Reset height to auto
  this.style.height = this.scrollHeight + 'px'; // Set height based on content
});
