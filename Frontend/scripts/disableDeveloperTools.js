document.addEventListener("keydown", function (event) {
  if (event.key === "F12" || event.keyCode === 123) {
    event.preventDefault();
  }

  if (
    ((event.ctrlKey || event.metaKey) &&
      event.shiftKey &&
      (event.key === "I" ||
        event.key === "J" ||
        event.key === "C" ||
        event.key === "K")) ||
    ((event.ctrlKey || event.metaKey) && event.key === "U")
  ) {
    event.preventDefault();
  }
});

document.addEventListener("contextmenu", function (event) {
  event.preventDefault();
});

document.addEventListener("dragstart", function (event) {
  event.preventDefault();
});
document.addEventListener("drop", function (event) {
  event.preventDefault();
});

let devtoolsOpen = false;
const element = new Image();
Object.defineProperty(element, "id", {
  get: function () {
    devtoolsOpen = true;
    console.warn("Developer tools are detected.");
    alert("Developer tools are restricted on this website.");
  },
});

requestAnimationFrame(function check() {
  console.log(element);
  if (devtoolsOpen) {
    devtoolsOpen = false;
  }
  requestAnimationFrame(check);
});

let devToolsDetectionTimer;
let resizingTriggered = false;

window.addEventListener("resize", function () {
  clearTimeout(devToolsDetectionTimer);
  devToolsDetectionTimer = setTimeout(function () {
    if (!resizingTriggered) {
      if (
        Math.abs(window.innerWidth - previousWidth) > 300 ||
        Math.abs(window.innerHeight - previousHeight) > 300
      ) {
        location.reload();
      }
    }
    resizingTriggered = false;
  }, 500);
  resizingTriggered = true;
});

setInterval(function () {
  const devtoolsCheck = /./;
  devtoolsCheck.toString = function () {
    console.warn("Developer tools detected.");
  };
  console.log(devtoolsCheck);
}, 2000);