const voiceCloningButton = document.querySelector('.voiceCloningButton');
const voiceToTeXTButton = document.querySelector('.voiceToTeXTButton');
const realTimeTranslatorButton = document.querySelector('.realTimeTranslatorButton');
const shareChat = document.querySelector('.shareChat');
const inputVoiceMicrophoneNoticeHolder = document.querySelector('.inputVoiceMicrophoneNoticeHolder');
const leftSectionChatLoaderAnimation = document.querySelector(".leftSectionChatLoaderAnimation");
const buttonsContainer = document.querySelector('.checkAndValidateChatOptionsToStart');
const chatContainerVoiceCloning = document.querySelector('.rightLowerSectionItemsHolderVoiceCloningButtonToChat');
const chatContainerVoiceToText = document.querySelector('.rightLowerSectionItemsHolderVoiceToTeXTButtonToChat');
const chatContainerRealTimeTranslator = document.querySelector('.rightLowerSectionItemsHolderRealTimeTranslatorButtonToChat');
const chatContainerTemplateParent = document.querySelector('.userChatHolder');

function chatTemplate(message = 'Default message') {
  const chatItem = document.createElement('div');
  chatItem.classList.add('userChatItemsContainer');

  chatItem.innerHTML = `
    <div class="userChatHere">
      <div class="vcChatHolder"><span>VC</span></div>
      <span>${message}</span>
    </div>
    <div class="userChatRenameDeleteToolKit">
      <img class="chatMenuOptionIcon" src="/Frontend/public/images/svgs/dot3Menu.svg" alt="">
    </div>
  `;

  chatContainerTemplateParent.appendChild(chatItem);
}
function chats3ButtonsDisplay() {
  buttonsContainer.style.display = 'none';
}
function shareChatDisplay() {
  shareChat.style.display = 'flex';
}
function microPhoneDisplay() {
  inputVoiceMicrophoneNoticeHolder.style.display = 'flex';
}
voiceCloningButton.addEventListener('click', function () {
  chats3ButtonsDisplay();
  chatContainerVoiceCloning.style.display = 'flex';
  shareChatDisplay();
  microPhoneDisplay();
  chatTemplate('Voice Cloning activated');
});

voiceToTeXTButton.addEventListener('click', function () {
  chats3ButtonsDisplay();
  chatContainerVoiceToText.style.display = 'flex';
  shareChatDisplay();
  microPhoneDisplay()
  chatTemplate('Voice-to-Text activated');
});

realTimeTranslatorButton.addEventListener('click', function () {
  chats3ButtonsDisplay();
  chatContainerRealTimeTranslator.style.display = 'flex';
  shareChatDisplay();
  microPhoneDisplay();
  chatTemplate('Real-Time Translator activated');
});
