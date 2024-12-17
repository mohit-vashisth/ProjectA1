const closeAnimationHolder = document.querySelector(".CloseAnimationHolder");
const openAnimationHolder = document.querySelector(".openAnimationHolder");
const gs = document.querySelectorAll(".g1, .g2, .g3, .g4, .g5, .interactiveCircle");

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


closeAnimationHolder.addEventListener("click", () => {
    gs.forEach(g => {
        g.style.visibility = "hidden";
    });
    openAnimationHolder.style.visibility = "visible";
    closeAnimationHolder.style.visibility = "hidden";
});

openAnimationHolder.addEventListener("click", () => {
    gs.forEach(g => {
        g.style.visibility = "visible";
    });
    openAnimationHolder.style.visibility = "hidden";
    closeAnimationHolder.style.visibility = "visible";
});