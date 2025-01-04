const slideBar = document.querySelector('.slider');
const leftSection = document.querySelector('.leftMain');
const rightSection = document.querySelector('.rightMain');
const upperRight = document.querySelector('.upperRight');

function chatSlider(sliderIcon, leftElement, rightElement, navBar) {
  slideBar.addEventListener('click', function(){
    if(leftElement.style.width != '0%'){
      leftElement.style.width = '0%';
      rightElement.style.width = '100%';
      navBar.style.width = '100%';
    }
    else{
      leftElement.style.width = '13%';
      rightElement.style.width = '87%';
      navBar.style.width = '87%';
    }
  })
}

chatSlider(slideBar, leftSection, rightSection, upperRight);