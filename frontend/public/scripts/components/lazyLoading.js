document.addEventListener("DOMContentLoaded", function () {
    const lazyGradient = document.getElementById("lazyGradient");
    const lazyLoadContent = document.querySelectorAll(".lazy-load-content");

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                lazyLoadContent.forEach(el => {
                    el.style.display = "block"; // Show content
                    el.classList.add("lazy-loaded");
                });
                observer.unobserve(entry.target); // Stop observing after loading
            }
        });
    });

    observer.observe(lazyGradient);
});