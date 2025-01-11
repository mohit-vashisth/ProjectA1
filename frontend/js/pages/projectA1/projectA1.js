const profileImg = document.querySelector('.img')
const userName = document.querySelector('.userName span')
const logout = document.querySelector('#logout')

async function validateUserCred() {
  try {
      const response = await fetch("http://127.0.0.1:3000/api/verify", {
          method: "GET",
          credentials: "include",
      });

      if (!response.ok) {
          if (response.status === 401) {
              console.log("Access token expired. Attempting to refresh...");
              const refreshResponse = await fetch("http://127.0.0.1:3000/api/refresh-token", {
                  method: "POST",
                  credentials: "include",
              });

              if (refreshResponse.ok) {
                  return await validateUserCred();
              } else {
                  window.location.href = "/frontend/pages/auth/login.html";
              }
          } else {
              window.location.href = "/frontend/pages/auth/login.html";
          }
          return;
      }
      const data = await response.json();

      if (data && data.status && data.userInfo) {
          localStorage.setItem("userName", data.userName);
          localStorage.setItem("userEmail", data.userEmail);
      }
  }
  catch (error) {
      console.error("Error verifying token:", error);
      window.location.href = "/frontend/pages/auth/login.html";
  }
}

function setUser() {
  nameOfUser = localStorage.getItem("userName");
  emailOfUser = localStorage.getItem("userEmail");
  userName.textContent = nameOfUser;
  profileImg.textContent = emailOfUser[0].toLowerCase();
}

async function logoutUser() {
    const response = await fetch("http://localhost:3000/logout", {
      method: "POST",
      credentials: "include",
    });
    if (response.ok) {
      window.location.href = "/frontend/pages/auth/login.html";
    } else {
      alert("Unable to logout");
    }

    const data = await response.json();

    if (data.status) {
      localStorage.removeItem("access_token");
    }
}

logout.addEventListener('click', logoutUser);
// document.addEventListener("DOMContentLoaded", async () => {
//   try {
//       await validateUserCred();
//   } catch (error) {
//       console.error("Error during user validation:", error);
//   }
// });