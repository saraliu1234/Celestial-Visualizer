  const beatDot = document.getElementById('beat-indicator');

  function animate() {
    requestAnimationFrame(animate);
    let beatInt = 0, isBeat = false;
    if (isPlaying) {
      const r = detectBeat();
      isBeat = r.beat; beatInt = r.intensity;
      if (isBeat) {
        triggerExplosion(star.x, star.y, beatInt);
        star.recoil = 1; star.glow = 1;
        beatDot.style.opacity = '1';
        setTimeout(() => beatDot.style.opacity = '0', 80);
      }
    }
    drawBackground(beatInt);
    updateStar(beatInt);
    updateExplosions();
    drawExplosions();
    drawTravelStar();
  }

  window.addEventListener('keydown', e => {
    const map = { '1': 'linear', '2': 'circular', '3': 'lissajous', '4': 'figure8', '5': 'random' };
    if (map[e.key]) setMode(map[e.key]);
  });

  document.getElementById('file-input').addEventListener('change', async e => {
    const file = e.target.files[0]; if (!file) return;
    document.getElementById('upload-area').style.display = 'none';
    document.getElementById('hud').style.display         = 'flex';
    document.getElementById('mode-hint').style.display   = 'block';
    document.getElementById('track-name').textContent    = file.name;
    try { await loadAudio(file); }
    catch (err) {
      console.error(err);
      document.getElementById('track-name').textContent = 'Error — try a different format';
    }
  });

  resize();
  star.x = W / 2; star.y = H / 2;
  animate();
