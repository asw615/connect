function openLoginIframe() {
    const iframeContainer = document.getElementById('login-iframe-container');
    iframeContainer.style.display = 'block';
  
    const iframe = document.createElement('iframe');
    iframe.src = 'login.html';
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = 'none';
  
    iframeContainer.appendChild(iframe);
  }
  
  function closeLoginIframe() {
    const iframeContainer = document.getElementById('login-iframe-container');
    iframeContainer.style.display = 'none';
    iframeContainer.innerHTML = '';
  }
  