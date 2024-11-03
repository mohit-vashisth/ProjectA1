document.querySelectorAll('.models_').forEach((model) => {
    model.addEventListener('click', function (e) {
        // Create the ripple container if it doesn’t exist
        let rippleContainer = this.querySelector('.ripple-container');
        if (!rippleContainer) {
            rippleContainer = document.createElement('div');
            rippleContainer.classList.add('ripple-container');
            this.appendChild(rippleContainer);
        }

        // Create the ripple element
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');

        // Set the size of the ripple
        const size = Math.max(this.clientWidth, this.clientHeight);
        ripple.style.width = ripple.style.height = `${size}px`;

        // Set the position of the ripple
        const rect = this.getBoundingClientRect();
        ripple.style.left = `${e.clientX - rect.left - size / 2}px`;
        ripple.style.top = `${e.clientY - rect.top - size / 2}px`;

        // Append the ripple to the container and remove it after animation
        rippleContainer.appendChild(ripple);
        ripple.addEventListener('animationend', () => ripple.remove());
    });
});
