const svgImages = document.querySelectorAll('img, svg');

export function dragDisabledEXP(params) {
  svgImages.forEach((img) => {
    img.addEventListener('dragstart', (event) => {
      event.preventDefault();
    });
  });
}