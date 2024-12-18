function slider() {
    const leftSection = document.querySelector('.leftSection');
    const slideToLeft = document.querySelector('.slideBarIcon');
    const slideToRight = document.querySelector('.slideToRightBack');

  slideToLeft.addEventListener('click', function() {
    leftSection.style.width = '0';
    slideToRight.style.display = 'flex';
  });

  slideToRight.addEventListener('click', function() {
    leftSection.style.width = '20%';
    slideToRight.style.display = 'none';
  });

}

slider();
