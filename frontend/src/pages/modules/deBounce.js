export function debounce(func, delay = 10) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => func(...args), delay);
    };
}