const microphoneHolder = document.querySelector(".microphoneHolder");
const rotatingBackground = document.querySelector(".rotatingBackground");

let rotation = 0;  // Rotation angle for background
let rotationSpeed = 360;  // Initial rotation speed
let isAnimating = false;
let speedChangeTimeout = null;

// Start the animation of rotating background
function animateRotation() {
  const currentTime = Date.now();
  let lastTime = currentTime;
  isAnimating = true;

  function update() {
    if (!isAnimating) return;

    const now = Date.now();
    const deltaTime = (now - lastTime) / 1000;
    lastTime = now;

    rotation += rotationSpeed * deltaTime;
    rotatingBackground.style.transform = `rotate(${rotation % 360}deg)`; // Continuous rotation

    requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

// Stop the background rotation animation
function stopAnimation() {
  isAnimating = false;
}

// Gradually change the rotation speed over a given duration
function graduallyChangeSpeed(targetSpeed, duration) {
  if (speedChangeTimeout) clearTimeout(speedChangeTimeout);

  const steps = 5;
  const stepDuration = duration / steps;
  const speedStep = (targetSpeed - rotationSpeed) / steps;
  let currentStep = 0;

  function step() {
    if (currentStep < steps) {
      rotationSpeed += speedStep;
      currentStep++;
      speedChangeTimeout = setTimeout(step, stepDuration);
    } else {
      rotationSpeed = targetSpeed; // Reached target speed
    }
  }

  step();
}

// Function to open the microphone, change animation speed, and start rotating
function openMicrophone() {
  microphoneHolder.style.transform = "translateY(-30vmin) scale(2.5)";
  graduallyChangeSpeed(60, 5000); // Gradually slow down the rotation speed to 60 over 5 seconds
  if (!isAnimating) animateRotation();
}

// Function to close the microphone, keep the rotation running, but reset scale and position
function closeMicrophone() {
  microphoneHolder.style.transform = "translateY(0) scale(1)";
  graduallyChangeSpeed(360, 2000); // Gradually reset speed back to 360 over 2 seconds
  // Don't stop the animation, so rotation continues running
}

// Event listener to open the microphone when clicked
microphoneHolder.addEventListener("click", function (event) {
  event.stopPropagation(); // Prevent the event from propagating to the document
  openMicrophone();
});

// Event listener to close the microphone when clicked outside
document.addEventListener("click", function (event) {
  if (!microphoneHolder.contains(event.target)) {
    closeMicrophone();
  }
});

// Start the rotation animation immediately when the page loads
window.addEventListener("load", function () {
  if (!isAnimating) animateRotation(); // Start the rotation on page load
});
