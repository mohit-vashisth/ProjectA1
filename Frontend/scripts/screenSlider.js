function slider() {
  document.querySelector('.slideBarIcon').addEventListener('click', function() {
    const slideToLeft = document.querySelector('.leftSection');
    slideToLeft.classList.add('hidden');

    const sliderToRight = document.querySelector('.sliderHolder');
    sliderToRight.classList.add('show');
  });

  document.querySelector('.slideToRightBack').addEventListener('click', function() {
    const slideToLeft = document.querySelector('.leftSection');
    slideToLeft.classList.remove('hidden');

    const sliderToRight = document.querySelector('.sliderHolder');
    sliderToRight.classList.remove('show');
  });
}

slider();