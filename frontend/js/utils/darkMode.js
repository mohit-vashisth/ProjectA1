const darkModeClasses = document.querySelectorAll(
    '.sections, .checkAndValidateChatOptionsToStart, .leftSectionChatLoaderAnimation, .filter1, .toolkit_websiteInfo, .labelShareRadio, .closeNowIcon, .googleLoginTemplate, .horizontalBarLoginGoogle, .userPasswordInput, .userConfirmPasswordInput, .existingUser, .loginInformationHolder, .shareChatPopupHolder, .shareChatLinkPopupHolder, .userNameSignUp, .userEmailInput, .thumbUpHolder, .readTextHolder, .thumbDownHolder, .reGenerateHolder, .sliderHolder, .imageOfModel img, .models_ img, .websiteInfo, .microphoneHolder, .askModel_responseHolder, .askModel_response, .models_, .chatDetails, .slideBar, .chatMenuIcon, .chatOfUser, .userLoginNow, .darkModeOn, .shareChat, .newChatLink img, .leftSection, .rightSection, .models_, .chatHistory'
  );
  
  const darkModeOffIcon = document.querySelector('.darkModeOff');
  const darkModeOnIcon = document.querySelector('.darkModeOn');
  const dayNightModeHolder = document.querySelector('.dayNightModeHolder');
  
  function applyDarkMode(isDarkMode) {
    document.body.classList.toggle('dark-mode', isDarkMode);
  
    darkModeClasses.forEach((element) => {
      if (element) {
        element.classList.toggle('dark-mode', isDarkMode);
      }
    });

    if (darkModeOffIcon && darkModeOnIcon) {
      darkModeOffIcon.style.display = isDarkMode ? 'none' : 'block';
      darkModeOnIcon.style.display = isDarkMode ? 'block' : 'none';
    }
  
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
  }
  
  function toggleDarkMode() {
    const isDarkMode = !document.body.classList.contains('dark-mode');
    applyDarkMode(isDarkMode);
  }
  
  function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    const isDarkMode = savedTheme === 'dark';
    applyDarkMode(isDarkMode);
  }
  
  if (dayNightModeHolder) {
    dayNightModeHolder.addEventListener('click', toggleDarkMode);
  }
  
  window.onload = loadTheme;
  