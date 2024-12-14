let curX = 0;
let curY = 0;
let tgX = 0;
let tgY = 0;

document.addEventListener('DOMContentLoaded', () => {
    const interBubble = document.querySelector('.interactiveCircle');

    function move() {
        const vmin = Math.min(window.innerWidth, window.innerHeight) / 100;
    
        curX += (tgX - curX) / 20;
        curY += (tgY - curY) / 20;
    
        const curXvmin = curX / vmin;
        const curYvmin = curY / vmin;
    
        interBubble.style.transform = `translate(${curXvmin}vmin, ${curYvmin}vmin)`;
    
        requestAnimationFrame(move);
    }
    

    window.addEventListener('mousemove', (event) => {
        tgX = event.clientX;
        tgY = event.clientY;
    });

    move();
});
