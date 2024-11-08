document.querySelector('.dayNightModeHolder').addEventListener('click', function() {
  document.body.classList.toggle('dark-mode');
  
  // Toggle class on each container that requires the dark mode effect
  document.querySelectorAll('.sections, .imageOfModel img, .models_ img, .slideToRightBack, .reEditUserMessageHolder, .reEditUserMessage, .websiteInfo, .microphoneHolder, .askModel_responseHolder, .askModel_response, .models_, .chatDetails, .chatMenuIcon, .chatOfUser, .userLoginNow, .darkModeOn, .shareChat, .slideBarIcon, .newChatLink img, .leftSection, .rightSection, .models_, .chatHistory').forEach(element => {
      element.classList.toggle('dark-mode');
  });

  // Swap dark mode icons (optional)
  document.querySelector('.darkModeOff').style.display = 
      document.body.classList.contains('dark-mode') ? 'none' : 'block';
  document.querySelector('.darkModeOn').style.display = 
      document.body.classList.contains('dark-mode') ? 'block' : 'none';
});
