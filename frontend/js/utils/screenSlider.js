const slideBar = document.querySelector('.slider');
const leftSection = document.querySelector('.leftMain');
const rightSection = document.querySelector('.rightMain');

function chatSlider(sliderIcon, leftElement, rightElement) {
  slideBar.addEventListener('click', function(){
    if(leftElement.style.width != '0%'){
      leftElement.style.width = '0%';
      rightElement.style.width = '100%';
    }
    else{
      leftElement.style.width = '13%';
      rightElement.style.width = '87%';
    }
  })
}

chatSlider(slideBar, leftSection, rightSection);