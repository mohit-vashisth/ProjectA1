const taglineElement = document.querySelector(".websiteTagLine");
const texts = [
  "Innovating AI, Fueling Imagination",
  "Read Privacy & Policy before using.",
  "This Website is for everyone.",
];

let text = texts[Math.floor(Math.random() * texts.length)];
let index = 0;
let isAdding = true;
let position = 0;

function updateText() {
    if (isAdding) {
        if (index < text.length) {
            taglineElement.textContent += text.charAt(index);
            index++;

            if (taglineElement.scrollWidth > taglineElement.parentElement.clientWidth) {
                position -= 1; // Slide the text left
                taglineElement.style.transform = `translateX(${position}px)`;
                taglineElement.style.transition = "transform 0.05s linear";
            }
        } else {
            isAdding = false;
            setTimeout(updateText, 2000);
            return;
        }
    } else {
        if (index > 0) {
            taglineElement.textContent = taglineElement.textContent.slice(0, -1);
            index--;

            if (position < 0) {
                position += 1;
                taglineElement.style.transform = `translateX(${position}px)`;
                taglineElement.style.transition = "transform 0.05s linear";
            }
        } else {
            isAdding = true;
            text = texts[Math.floor(Math.random() * texts.length)];
            setTimeout(updateText, 800);
            return;
        }
    }

    setTimeout(updateText, 30);
}

updateText();
