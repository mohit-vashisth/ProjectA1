const animationTexts = document.querySelectorAll(".loadingText");
const animationContainer = document.querySelector(".loadingAssets");
let currentIndex = 0;

function showAndHideTexts() {
    // Disable interaction with the page by setting pointer-events to 'none' on the html element
    document.querySelector("html").style.pointerEvents = "none";

    animationTexts.forEach((text) => {
        text.style.opacity = "0";
        text.style.transition = "opacity 0.5s";
    });

    animationTexts[currentIndex].style.opacity = "1";

    setTimeout(() => {
        if (currentIndex === animationTexts.length - 1) {
            setTimeout(() => {
                // Hide the animation container and re-enable interaction
                animationContainer.style.display = "none";
                localStorage.setItem("animationPlayed", "true");

                // Re-enable pointer events (allow interaction)
                document.querySelector("html").style.pointerEvents = "auto";
            }, 2000); // Hide the animation container after 2 seconds
        } else {
            currentIndex++;
            showAndHideTexts();
        }
    }, 3000); // Wait 3 seconds before showing the next text
}

export function assetsLoadingEXP() {
    if (localStorage.getItem("animationPlayed") === "true") {
        showAndHideTexts();
    } else {
        animationContainer.style.display = "none";
    }
}