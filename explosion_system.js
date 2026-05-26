
  // ─── Explosions ───────────────────────────────────────────────────────────
  let particles = [], shockwaves = [];

  function triggerExplosion(x, y, intensity) {
    shockwaves.push({ x, y, r: 5, maxR: 65 + intensity * 185, life: 1 });
    if (intensity > 0.5)
      shockwaves.push({ x, y, r: 5, maxR: 105 + intensity * 225, life: 0.7 });

    const nDebris = Math.floor(28 + intensity * 85);
    for (let i = 0; i < nDebris; i++) {
      const ang = Math.random() * Math.PI * 2;
      const spd = (1 + Math.random() * 5) * (0.4 + intensity * 1.9);
      particles.push({
        x, y,
        vx: Math.cos(ang) * spd, vy: Math.sin(ang) * spd - Math.random() * 1.5,
        life: 1, decay: 0.012 + Math.random() * 0.026,
        sz: (1.5 + Math.random() * 4) * (0.5 + intensity * 0.8),
        hue: Math.random() < 0.6 ? 30 + Math.random() * 40 : 200 + Math.random() * 80,
        type: 'dot',
      });
    }
    const nSparks = Math.floor(14 + intensity * 38);
    for (let i = 0; i < nSparks; i++) {
      const ang = Math.random() * Math.PI * 2;
      const spd = (3 + Math.random() * 9) * (0.5 + intensity * 1.2);
      particles.push({
        x, y, vx: Math.cos(ang) * spd, vy: Math.sin(ang) * spd,
        life: 1, decay: 0.018 + Math.random() * 0.04,
        sz: 1.2 + intensity, hue: 45 + Math.random() * 25,
        type: 'spark', trail: [],
      });
    }
    particles.push({ x, y, vx: 0, vy: 0, life: 1, decay: 0.12,
      sz: 22 + intensity * 65, hue: 50, type: 'flash' });

    if (intensity > 0.65 && isPlaying
        && star.motionTime - star.lastModeSwitch > 200
        && Math.random() < 0.38) {
      const others = MODES.filter(m => m !== star.motionMode);
      setMode(others[Math.floor(Math.random() * others.length)]);
    }
  }

  function updateExplosions() {
    shockwaves = shockwaves.filter(s => s.life > 0);
    shockwaves.forEach(s => { s.r += (s.maxR - s.r) * 0.12; s.life -= 0.035; });

    particles = particles.filter(p => p.life > 0);
    particles.forEach(p => {
      if (p.type === 'spark' && p.trail) {
        p.trail.push({ x: p.x, y: p.y });
        if (p.trail.length > 7) p.trail.shift();
      }
      p.x  += p.vx; p.y += p.vy;
      p.vy += 0.07;
      p.vx *= 0.975; p.vy *= 0.975;
      p.life -= p.decay;
    });
  }

  function drawExplosions() {
    shockwaves.forEach(s => {
      ctx.save();
      const g = ctx.createRadialGradient(s.x, s.y, s.r * 0.8, s.x, s.y, s.r);
      g.addColorStop(0,   'rgba(255,180,30,0)');
      g.addColorStop(0.5, `rgba(255,200,60,${s.life * 0.4})`);
      g.addColorStop(1,   'rgba(255,100,0,0)');
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(255,210,80,${s.life * 0.7})`;
      ctx.lineWidth   = 2.5 * s.life;
      ctx.shadowBlur  = 15;
      ctx.shadowColor = '#FF8800';
      ctx.stroke();
      ctx.restore();
    });

    particles.forEach(p => {
      ctx.save();
      ctx.globalAlpha = p.life;
      ctx.shadowBlur  = 8;
      ctx.shadowColor = `hsl(${p.hue},100%,60%)`;

      if (p.type === 'flash') {
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.sz);
        g.addColorStop(0,   `rgba(255,255,220,${p.life})`);
        g.addColorStop(0.4, `rgba(255,200,50,${p.life * 0.6})`);
        g.addColorStop(1,   'rgba(255,100,0,0)');
        ctx.fillStyle = g; ctx.shadowBlur = 40; ctx.shadowColor = '#FFFFFF';
        ctx.beginPath(); ctx.arc(p.x, p.y, p.sz, 0, Math.PI * 2); ctx.fill();

      } else if (p.type === 'spark' && p.trail && p.trail.length > 1) {
        ctx.strokeStyle = `hsl(${p.hue},100%,75%)`;
        ctx.lineWidth   = p.sz; ctx.lineCap = 'round';
        ctx.beginPath();
        p.trail.forEach((pt, i) => {
          ctx.globalAlpha = p.life * (i / p.trail.length) * 0.8;
          i === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y);
        });
        ctx.lineTo(p.x, p.y); ctx.stroke();

      } else {
        ctx.fillStyle = `hsl(${p.hue},100%,70%)`;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.sz, 0, Math.PI * 2); ctx.fill();
      }
      ctx.restore();
    });
  }
