const slideBar = document.querySelector('.slider');
const leftSection = document.querySelector('.leftMain');
const rightSection = document.querySelector('.rightMain');

function slider() {
  if (slideBar && leftSection && rightSection) {
    slideBar.addEventListener('click', function () {
      if (window.matchMedia('(max-width: 768px)').matches) {
        if (leftSection.style.width !== "50%") {
          leftSection.style.width = "50%";
          rightSection.style.filter = "blur(5px)";
          rightSection.style.pointerEvents = "none";
        } else {
          leftSection.style.width = "0%";
          rightSection.style.filter = "blur(0px)";
          rightSection.style.pointerEvents = "auto";
        }
      }
    });

    document.addEventListener('click', function (event) {
      if (window.matchMedia('(max-width: 768px)').matches) {
        if (leftSection.style.width !== "0%" && 
            !leftSection.contains(event.target) && 
            event.target !== slideBar) {
          leftSection.style.width = "0%";
          rightSection.style.filter = "blur(0px)";
          rightSection.style.pointerEvents = "auto";
        }
      }
    });
  }
}

slider();
