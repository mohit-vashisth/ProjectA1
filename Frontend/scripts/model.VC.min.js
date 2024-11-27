const getTextFromInput = document.querySelector('.askModel_response');
const sendResponseToModelButton = document.querySelector('.askModel_button');
const chatContainer = document.querySelector('.rightLowerSectionItemsHolderVoiceCloningButtonToChat');
const lines = 20;

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

function resetInputArea() {
  getTextFromInput.value = '';
  getTextFromInput.style.height = '7vmin';
}

function escapeHtml(text) {
  const element = document.createElement('div');
  if (text) {
    element.innerText = text;
    element.textContent = text;
  }
  return element.innerHTML;
}

function appendUserMessage(message) {
  const userChatContainer = document.createElement('article');
  userChatContainer.className = 'modelChat_responseContainerVoiceCloningButtonToChat';
  
  const escapedMessage = escapeHtml(message);

  userChatContainer.innerHTML = `<div class="userChat_HolderVoiceCloningButtonToChat">
    <div class="userChatMainImageHolderVoiceCloningButtonToChat">
      <div class="chatOfUserVoiceCloningButtonToChat">
        <div class="responseNowVoiceCloningButtonToChat">${escapedMessage}</div> <!-- Display escaped HTML here -->
      </div>
    </div>
  </div>`;
  
  chatContainer.appendChild(userChatContainer);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function appendModelMessage(message) {
  const modelChatContainer = document.createElement('article');
  modelChatContainer.className = 'modelChat_responseContainerVoiceCloningButtonToChat';

  modelChatContainer.innerHTML = `
    <div class="modelChat_HolderVoiceCloningButtonToChat">
      <div class="modelChatMainImageHolderVoiceCloningButtonToChat">
          <div class="imageOfModelVoiceCloningButtonToChat">
              <img src="/Frontend/images/svgs/voiceClone.svg" alt="model logo" />
          </div>
          <div class="chatOfModelVoiceCloningButtonToChat">
              <span class="modelChat_responseNowVoiceCloningButtonToChat">${message}</span>
              <div class="modelChatRegenerateLikeDislikeHolderVoiceCloningButtonToChat">
                  <div class="modelChatOptionsHolderVoiceCloningButtonToChat">
                      <div class="readTextHolderVoiceCloningButtonToChat">
                          <img src="/Frontend/images/svgs/volume.svg" title="Read Text" alt="">
                      </div>
                      <div class="thumbUpHolderVoiceCloningButtonToChat">
                          <img src="/Frontend/images/svgs/thumbup.svg" title="Like" alt="">
                      </div>
                      <div class="thumbDownHolderVoiceCloningButtonToChat">
                          <img src="/Frontend/images/svgs/thumbdown.svg" title="Dislike" alt="">
                      </div>
                      <div class="reGenerateHolderVoiceCloningButtonToChat">
                          <img src="/Frontend/images/svgs/reload.svg" title="Regenerate" alt="">
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>
  `;

  chatContainer.appendChild(modelChatContainer);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function sendMessage() {
  let message = getTextFromInput.value.trim();

  if (message) {
    appendUserMessage(message);
    getTextFromInput.value = "";
    sendButtonCheck();
    resetInputArea();
  }
}

getTextFromInput.addEventListener('input', sendButtonCheck);

sendResponseToModelButton.addEventListener('click', sendMessage);

function sendModelResponse(userMessage) {
  const simulatedModelResponse = `not able to fetch data: "${userMessage}"`;
  appendModelMessage(simulatedModelResponse);
}

getTextFromInput.addEventListener('input', function () {
  this.style.height = 'auto';
  const scrollHeightInVmin = (this.scrollHeight / window.innerHeight) * 100;
  this.style.height = `${scrollHeightInVmin}vmin`;

  if (this.value.trim() === "") {
    resetInputArea()
  }
});