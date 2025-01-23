const animationTexts = document.querySelectorAll(".loadingText");
const animationContainer = document.querySelector(".loadingAssets");
let currentIndex = 0;

function showAndHideTexts() {
    animationTexts.forEach((text) => {
        text.style.opacity = "0";
        text.style.transition = "opacity 0.5s";
    });

    animationTexts[currentIndex].style.opacity = "1";

    setTimeout(() => {
        if (currentIndex === animationTexts.length - 1) {
            setTimeout(() => {
                animationContainer.style.display = "none";
                localStorage.setItem("animationPlayed", "true");
            }, 2000);
        } else {
            currentIndex++;
            showAndHideTexts();
        }
    }, 3000);
}

export function assetsLoadingEXP() {
    if (localStorage.getItem("animationPlayed") !== "true") {
        showAndHideTexts();
    } else {
        animationContainer.style.display = "none";
    }
}