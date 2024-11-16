const dayNightModeHolder = document.querySelector('.dayNightModeHolder');
const darkModeOffIcon = document.querySelector('.darkModeOff');
const darkModeOnIcon = document.querySelector('.darkModeOn');

function toggleDarkMode() {
    const isDarkMode = document.body.classList.toggle('dark-mode');

    document.querySelectorAll('.sections, .filter1, .toolkit_websiteInfo, .renameChat, .deleteChat, .chatMenuOptions, .horizontalBar, .toolkit_websiteInfo, .closeNowIcon, .googleLoginTemplate, .horizontalBarLoginGoogle, .userPasswordInput, .userConfirmPasswordInput, .existingUser, .loginInformationHolder, .userNameSignUp, .userEmailInput, .thumbUpHolder, .readTextHolder, .thumbDownHolder, .reGenerateHolder, .sliderHolder, .imageOfModel img, .models_ img, .slideToRightBack, .reEditUserMessageHolder, .reEditUserMessage, .websiteInfo, .microphoneHolder, .askModel_responseHolder, .askModel_response, .models_, .chatDetails, .chatMenuIcon, .chatOfUser, .userLoginNow, .darkModeOn, .shareChat, .slideBarIcon, .newChatLink img, .leftSection, .rightSection, .models_, .chatHistory')
        .forEach(element => element.classList.toggle('dark-mode', isDarkMode));

    darkModeOffIcon.style.display = isDarkMode ? 'none' : 'block';
    darkModeOnIcon.style.display = isDarkMode ? 'block' : 'none';
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    const isDarkMode = savedTheme === 'dark';

    document.body.classList.toggle('dark-mode', isDarkMode);
    document.querySelectorAll('.sections, .filter1, .toolkit_websiteInfo, .renameChat, .deleteChat, .chatMenuOptions, .horizontalBar, .toolkit_websiteInfo, .closeNowIcon, .googleLoginTemplate, .horizontalBarLoginGoogle, .userPasswordInput, .userConfirmPasswordInput, .existingUser, .loginInformationHolder, .userNameSignUp, .userEmailInput, .thumbUpHolder, .readTextHolder, .thumbDownHolder, .reGenerateHolder, .sliderHolder, .imageOfModel img, .models_ img, .slideToRightBack, .reEditUserMessageHolder, .reEditUserMessage, .websiteInfo, .microphoneHolder, .askModel_responseHolder, .askModel_response, .models_, .chatDetails, .chatMenuIcon, .chatOfUser, .userLoginNow, .darkModeOn, .shareChat, .slideBarIcon, .newChatLink img, .leftSection, .rightSection, .models_, .chatHistory')
        .forEach(element => element.classList.toggle('dark-mode', isDarkMode));

    darkModeOffIcon.style.display = isDarkMode ? 'none' : 'block';
    darkModeOnIcon.style.display = isDarkMode ? 'block' : 'none';
}

dayNightModeHolder.addEventListener('click', toggleDarkMode);
window.onload = loadTheme;
