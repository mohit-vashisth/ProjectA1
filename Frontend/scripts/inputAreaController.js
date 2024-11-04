const inputArea = document.querySelector('.askModel_response');
inputArea.style.overflow = 'auto'; // Set overflow to auto

inputArea.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});
