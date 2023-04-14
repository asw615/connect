document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();
  
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    // Replace these lines with your own authentication method (e.g., call to an API)
    if (username === 'user' && password === 'password') {
      localStorage.setItem('isLoggedIn', 'true');
      window.location.href = 'sociogram.html';
    } else {
      alert('Invalid credentials');
    }
  });
  