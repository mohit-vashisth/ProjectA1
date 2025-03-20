const slideBar = document.querySelector('.slider');
const leftSection = document.querySelector('.leftMain');
const rightSection = document.querySelector('.rightMain');
const closeCross = document.querySelector('.closeLeftMainContainer img');

function updateLeftSectionSize() {
    if (window.matchMedia("(max-width: 760px)").matches) {
        // Mobile (phones)
        leftSection.style.width = "0%"; // Initially hidden
        leftSection.style.position = "absolute";
        slideBar.style.display = "flex"; // Show hamburger menu
    } else if (window.matchMedia("(max-width: 1024px)").matches) {
        // Tablets
        leftSection.style.width = "0%"; // Initially hidden
        leftSection.style.position = "absolute";
        slideBar.style.display = "flex"; // Show hamburger menu
    } else if (window.matchMedia("(max-width: 1440px)").matches) {
        // Laptops
        leftSection.style.width = "0%"; // Initially hidden
        leftSection.style.position = "relative";
        slideBar.style.display = "flex"; // Show hamburger menu
    } else {
        // Desktops (larger screens)
        leftSection.style.width = "30%"; // Always visible on desktops
        leftSection.style.position = "relative";
        slideBar.style.display = "none"; // Hide hamburger menu
        rightSection.style.opacity = "1"; // Reset opacity
        rightSection.style.pointerEvents = "auto"; // Allow interactions
    }
}

function toggleLeftSection() {
    if (leftSection.style.width === "0%" || leftSection.style.width === "") {
        // Open sidebar based on screen size
        if (window.matchMedia("(max-width: 760px)").matches) {
            leftSection.style.width = "100%";
        } else if (window.matchMedia("(max-width: 1024px)").matches) {
            leftSection.style.width = "40%";
        } else {
            leftSection.style.width = "30%";
        }
        rightSection.style.pointerEvents = "none"; 
        rightSection.style.opacity = 0.1;
    } else {
        leftSection.style.width = "0%"; // Close sidebar
        rightSection.style.pointerEvents = "auto"; 
        rightSection.style.opacity = 1;
    }
}

export function slideMobileEXP() {
    updateLeftSectionSize(); // Set initial size on page load

    slideBar.addEventListener("click", (e) => {
        e.stopPropagation();
        toggleLeftSection();
    });

    closeCross.addEventListener("click", toggleLeftSection);

    document.addEventListener("click", (e) => {
        if (!leftSection.contains(e.target) && !slideBar.contains(e.target)) {
            leftSection.style.width = "0%";
            rightSection.style.pointerEvents = "auto"; 
            rightSection.style.opacity = 1;
        }
    });

    leftSection.addEventListener("click", (e) => {
        e.stopPropagation();
    });

    // Update layout dynamically when resizing the screen
    window.addEventListener("resize", updateLeftSectionSize);
}
