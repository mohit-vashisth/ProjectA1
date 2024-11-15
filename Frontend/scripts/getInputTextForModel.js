const getTextFromInput = document.querySelector('.askModel_response');
const sendResponseToModelButton = document.querySelector('.askModel_button');
const chatContainer = document.querySelector('.rightLowerSectionItemsHolder');

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

function appendUserMessage(message) {
  const userChatContainer = document.createElement('article');
  userChatContainer.className = 'userChat_responseContainer';

  userChatContainer.innerHTML = `<div class="userChat_Holder">
      <div class="userChatMainImageHolder">
        <div class="reEditUserMessageHolder">
          <img class="reEditUserMessage" title="Edit" src="images/svgs/rename-black.svg" alt="">
        </div>
        <div class="chatOfUser">
          <span class="responseNow">${message}</span>
        </div>
      </div>
    </div>
  `;

  chatContainer.appendChild(userChatContainer);
  chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the latest message
}

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
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function sendMessage() {
  const message = getTextFromInput.value.trim();
  if (message) {
    appendUserMessage(message);
    getTextFromInput.value = "";
    sendButtonCheck();
    sendModelResponse(message);
  }
}

getTextFromInput.addEventListener('input', sendButtonCheck);

getTextFromInput.addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    if (event.shiftKey) {
      getTextFromInput.value += "\n";
    } else {
      event.preventDefault();
      sendMessage();
    }
  }
});

sendResponseToModelButton.addEventListener('click', sendMessage);

function sendModelResponse(userMessage) {
  const simulatedModelResponse = `not able to fetch data: "${userMessage}"`;
  appendModelMessage(simulatedModelResponse);
}