const profileImg = document.querySelector('.img')
const userName = document.querySelector('.userName span')
const logout = document.querySelector('#logout')

function main() {
    nameOfUser = localStorage.getItem("userName");
    emailOfUser = localStorage.getItem("userEmail");
    userName.textContent = nameOfUser
    profileImg.textContent = emailOfUser[0].toLowerCase();
}