function generateRGB(progress) {
  let b = Math.floor((progress + 255) % 255); // Start from 255 for red
  let r = Math.floor((progress + 255 + 85) % 255); // Start from 255 for green
  let g = Math.floor((progress + 255 + 170) % 255); // Start from 255 for blue

  return `rgb(${r}, ${g}, ${b})`;
}

let progress = 0;
const colorTransitionSpeed = 20;
let interval;

function animateColors() {
  interval = setInterval(() => {
      progress = (progress + 0.5) % 255;
      const color = generateRGB(progress);
      
      document.querySelectorAll('.logo3Website, .logoNameWebsite, .websiteTagLine').forEach(element => {
          element.style.backgroundImage = `linear-gradient(90deg, ${color}, ${color})`; // Create the gradient
      });
  }, colorTransitionSpeed);
}

animateColors();
