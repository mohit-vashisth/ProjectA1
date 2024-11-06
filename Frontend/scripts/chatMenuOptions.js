document.querySelector('.chatMenuHolder img').addEventListener('click', function(){
  this.style.visibility = 'visible';
  document.querySelector('.chatHistory').style.pointerEvents = 'none';
  document.querySelector('.chatMenuOptions').style.visibility = 'visible';
  document.querySelector('.chatDetails').style.filter = 'blur(.5vmin)'; 
});