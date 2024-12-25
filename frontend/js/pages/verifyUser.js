function refreshCaptcha() {
    fetch('/refresh_captcha')
        .then(response => response.json())
        .then(data => {
            document.getElementById('captchaCode').textContent = data.new_captcha;
        })
        .catch(error => console.error('Error refreshing CAPTCHA:', error));
}