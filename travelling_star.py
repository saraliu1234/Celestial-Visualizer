"""
travelling_star.py
JavaScript block: traveling star motion system (5 modes) + comet trail.
Imported by main.py to assemble the final HTML file.
"""

JS = r"""
  // ─── Traveling Star — Motion System ───────────────────────────────────────
  const MODES       = ['circular', 'lissajous', 'figure8', 'random', 'linear'];
  const MODE_LABELS = {
    circular:  'CIRCULAR ORBIT',
    lissajous: 'LISSAJOUS',
    figure8:   'FIGURE-8 (LEMNISCATE)',
    random:    'RANDOM WALK',
    linear:    'LINEAR',
  };

  const star = {
    x: 200, y: 300,
    vx: 0, vy: 0,
    motionMode: 'circular',
    motionTime: 0,
    lastModeSwitch: 0,
    orbitCX: 0, orbitCY: 0,
    orbitRX: 250, orbitRY: 160,
    orbitAngle: 0,
    orbitSpeed: 0.013,
    trail: [], TRAIL_LEN: 130,
    recoil: 0, glow: 0,
    baseR: 5,
  };

  function setMode(mode) {
    star.motionMode = mode;
    star.lastModeSwitch = star.motionTime;
    const el = document.getElementById('mode-display');
    if (el) el.textContent = 'MODE: ' + MODE_LABELS[mode];
  }

  function stepPosition() {
    const T = star.motionTime;
    switch (star.motionMode) {
      case 'linear':
        star.x += 2.6;
        if (star.x > W + 80) {
          star.x = -60;
          star.y  = H * (0.2 + Math.random() * 0.6);
          star.trail = [];
        }
        break;

      case 'circular':
        star.orbitAngle += star.orbitSpeed;
        star.x = star.orbitCX + star.orbitRX * Math.cos(star.orbitAngle);
        star.y = star.orbitCY + star.orbitRY * Math.sin(star.orbitAngle);
        break;

      case 'lissajous': {
        const A  = Math.min(W, H) * 0.36;
        const B  = Math.min(W, H) * 0.26;
        const ks = T * 0.0055;
        star.x   = W / 2 + A * Math.cos(3 * ks + Math.PI / 4);
        star.y   = H / 2 + B * Math.sin(5 * ks);
        break;
      }

      case 'figure8': {
        const scale = Math.min(W, H) * 0.30;
        const ks    = T * 0.0042;
        const cosK  = Math.cos(ks);
        const sinK  = Math.sin(ks);
        const den   = 1 + sinK * sinK;
        star.x = W / 2 + scale * cosK / den;
        star.y = H / 2 + scale * 0.65 * cosK * sinK / den;
        break;
      }

      case 'random': {
        star.vx += (Math.random() - 0.5) * 0.8 - star.vx * 0.04;
        star.vy += (Math.random() - 0.5) * 0.6 - star.vy * 0.04;
        const spd = Math.sqrt(star.vx * star.vx + star.vy * star.vy);
        if (spd > 4.5) { star.vx *= 4.5 / spd; star.vy *= 4.5 / spd; }
        const m = 70;
        if (star.x < m)     star.vx += 0.4;
        if (star.x > W - m) star.vx -= 0.4;
        if (star.y < m)     star.vy += 0.4;
        if (star.y > H - m) star.vy -= 0.4;
        star.x += star.vx;
        star.y += star.vy;
        break;
      }
    }
  }

  function updateStar(beatInt) {
    stepPosition();
    star.motionTime++;
    star.trail.push({ x: star.x, y: star.y });
    if (star.trail.length > star.TRAIL_LEN) star.trail.shift();
    star.recoil *= 0.84;
    star.glow   *= 0.87;

    if (isPlaying
        && star.motionTime - star.lastModeSwitch > 420
        && Math.random() < 0.004) {
      const next = MODES[(MODES.indexOf(star.motionMode) + 1) % MODES.length];
      setMode(next);
    }
  }

  function drawTravelStar() {
    const len = star.trail.length;
    if (len < 2) return;

    for (let i = 1; i < len; i++) {
      const t1  = i / len;
      ctx.save();
      ctx.globalAlpha = t1 * t1 * 0.52;
      ctx.strokeStyle = `hsl(${20 + t1 * 35}, 100%, ${45 + t1 * 32}%)`;
      ctx.lineWidth   = t1 * 5;
      ctx.lineCap     = 'round';
      ctx.shadowBlur  = 10;
      ctx.shadowColor = '#FF9900';
      ctx.beginPath();
      ctx.moveTo(star.trail[i - 1].x, star.trail[i - 1].y);
      ctx.lineTo(star.trail[i].x,     star.trail[i].y);
      ctx.stroke();
      ctx.restore();
    }

    drawStellarPoint(star.x, star.y);
  }
"""
