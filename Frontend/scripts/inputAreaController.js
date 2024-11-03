const inputArea = document.querySelector('.input-area');
inputArea.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});
