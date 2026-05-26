  const canvas = document.getElementById('canvas');
  const ctx    = canvas.getContext('2d');
  let W, H;

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
    star.orbitCX = W / 2;
    star.orbitCY = H / 2;
    star.orbitRX = Math.min(W, H) * 0.32;
    star.orbitRY = Math.min(W, H) * 0.20;
  }
  window.addEventListener('resize', resize);
