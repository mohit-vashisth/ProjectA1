const microphoneHolder = document.querySelector(".microphoneHolder");
const rotatingBackground = document.querySelector(".rotatingBackground");
const microphone = document.querySelector('.microphoneHere');
const microPhoneToolkitHolder = document.querySelector('.microPhoneToolkitHolder');
const microPhoneActivateSound = document.querySelector('.microPhoneActivateSound');
const microPhoneDeactivateSound = document.querySelector('.microPhoneDeactivateSound');
let isMicrophoneActive = false;
let rotation = 0;
let rotationSpeed = 360;
let isAnimating = false;
let speedChangeTimeout = null;
let openMicrophoneTimeout = null;
microPhoneActivateSound.volume = 0.3;
microPhoneDeactivateSound.volume = 0.3;

function animateRotation() {
  const currentTime = Date.now();
  let lastTime = currentTime;
  isAnimating = true;

  function update() {
    if (!isAnimating) return;

    const now = Date.now();
    const deltaTime = (now - lastTime) / 3000;
    lastTime = now;

    rotation += rotationSpeed * deltaTime;
    rotatingBackground.style.transform = `rotate(${rotation % 360}deg)`;

    requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

function stopAnimation() {
  isAnimating = false;
}

function graduallyChangeSpeed(targetSpeed, duration) {
  if (speedChangeTimeout) clearTimeout(speedChangeTimeout);

  const steps = 10;
  const stepDuration = duration / steps;
  const speedStep = (targetSpeed - rotationSpeed) / steps;
  let currentStep = 0;

  function step() {
    if (currentStep < steps) {
      rotationSpeed += speedStep;
      currentStep++;
      speedChangeTimeout = setTimeout(step, stepDuration);
    } else {
      rotationSpeed = targetSpeed;
    }
  }

  step();
}

function playSound(audioElement) {
  if (audioElement) {
    if (!audioElement.paused) {
      audioElement.pause();
      audioElement.currentTime = 0;
    }
    audioElement.play();
  }
}

function openMicrophone() {
  microphoneHolder.style.transform = "translateY(-30vmin) scale(2.5)";
  graduallyChangeSpeed(60, 5000);
  if (!isAnimating) animateRotation();

  if (openMicrophoneTimeout) clearTimeout(openMicrophoneTimeout);

  openMicrophoneTimeout = setTimeout(() => {
    microphone.classList.add("vibrating");
    microPhoneToolkitHolder.style.display = 'flex';

    if (!isMicrophoneActive) {
      isMicrophoneActive = true;
      playSound(microPhoneActivateSound);
    }
  }, 1500);
}

function closeMicrophone() {
  microphoneHolder.style.transform = "translateY(0) scale(1)";
  graduallyChangeSpeed(360, 2000);
  microphone.classList.remove("vibrating");
  microPhoneToolkitHolder.style.display = 'none';

  if (openMicrophoneTimeout) clearTimeout(openMicrophoneTimeout);

  if (isMicrophoneActive) {
    isMicrophoneActive = false;
    setTimeout(() => {
      playSound(microPhoneDeactivateSound);
    }, 500);
  }
}

microphoneHolder.addEventListener("click", function (event) {
  event.stopPropagation();
  openMicrophone();
});

document.addEventListener("click", function (event) {
  if (!microphoneHolder.contains(event.target)) {
    closeMicrophone();
  }
});

window.addEventListener("load", function () {
  if (!isAnimating) animateRotation();
});
