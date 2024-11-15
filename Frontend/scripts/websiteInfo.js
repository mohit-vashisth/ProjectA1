document.querySelector('.websiteInfo').addEventListener('mouseenter', () => {
  const toolkit = document.querySelector('.toolkit_websiteInfo');
  toolkit.querySelector('li:nth-child(1)').textContent = "Release Notes: v1.0";
  toolkit.querySelector('li:nth-child(2)').textContent = "Credits: John Doe";
  toolkit.querySelector('li:nth-child(3)').textContent = "Version: 1.0";
});
