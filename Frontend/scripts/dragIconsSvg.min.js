const svgImages = document.querySelectorAll('img, svg');

svgImages.forEach((img) => {
  img.addEventListener('dragstart', (event) => {
    event.preventDefault();
  });
});
