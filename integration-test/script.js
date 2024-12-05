// Get the sign-up form element
const signupForm = document.getElementById('signup-form');

// Add event listener to handle form submission
signupForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Get the values from the input fields
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Save the data to localStorage
    localStorage.setItem('username', username);
    localStorage.setItem('password', password);

    // Redirect to the home page
    window.location.href = 'home.html';  // Redirect to home page
});
