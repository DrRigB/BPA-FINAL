// Get the username from localStorage
const username = localStorage.getItem('username');

// Display the username in the home page
document.getElementById('profile-name').textContent = username;
