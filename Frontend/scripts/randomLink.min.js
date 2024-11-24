function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
  });
}

function createRandomLink() {
  const baseURL = "http://127.0.0.1:3000/Frontend/homepage.html/c/";
  const uniqueID = generateUUID();
  const fullLink = baseURL + uniqueID;

  const linkContainer = document.querySelector(".modelChat_responseNow");
  linkContainer.innerHTML = fullLink;
}

document.addEventListener("DOMContentLoaded", createRandomLink);
