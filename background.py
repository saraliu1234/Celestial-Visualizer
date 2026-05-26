"""
background.py
JavaScript block: twinkling background stars + transient meteor streaks.
Imported by main.py to assemble the final HTML file.
"""

JS = r"""
  // ─── Background Stars ─────────────────────────────────────────────────────
  const BG = Array.from({ length: 220 }, () => ({
    x:          Math.random(),
    y:          Math.random(),
    r:          Math.random() * 1.4 + 0.25,
    phase:      Math.random() * Math.PI * 2,
    twinkleSpd: Math.random() * 0.6 + 0.15,
    spikeAngle: Math.random() * Math.PI,
    spikeLen:   Math.random() * 5 + 1.5,
    hasDiffrac: Math.random() < 0.28,
  }));

  let streaks = Array.from({ length: 7 }, makeStreak);
  function makeStreak() {
    return {
      x: Math.random(), y: Math.random(),
      angle:      Math.random() * Math.PI,
      speed:      0.0004 + Math.random() * 0.0015,
      trackLen:   0.04  + Math.random() * 0.09,
      life:       0,
      maxLife:    70 + Math.random() * 110,
      brightness: 0.5 + Math.random() * 0.5,
      delay:      Math.floor(Math.random() * 400),
    };
  }

  function drawBackground(beatInt) {
    ctx.fillStyle = 'rgba(0, 0, 8, 0.18)';
    ctx.fillRect(0, 0, W, H);

    const t = performance.now() * 0.001;

    BG.forEach(s => {
      const twk  = 0.3 + 0.55 * Math.sin(s.phase + t * s.twinkleSpd);
      const sx   = s.x * W, sy = s.y * H;

      ctx.save();
      ctx.globalAlpha = twk * 0.9;
      ctx.fillStyle   = `rgba(220, 230, 255, ${twk})`;
      ctx.shadowBlur  = 2;
      ctx.shadowColor = '#C0D0FF';
      ctx.beginPath();
      ctx.arc(sx, sy, s.r, 0, Math.PI * 2);
      ctx.fill();

      if (s.hasDiffrac && twk > 0.55) {
        const spikeA = (twk - 0.55) / 0.45;
        const len    = s.spikeLen * twk * (1 + beatInt * 1.8);
        for (let k = 0; k < 2; k++) {
          const ang = s.spikeAngle + k * Math.PI * 0.5;
          const grad = ctx.createLinearGradient(
            sx - Math.cos(ang) * len, sy - Math.sin(ang) * len,
            sx + Math.cos(ang) * len, sy + Math.sin(ang) * len
          );
          grad.addColorStop(0,   'rgba(200,215,255,0)');
          grad.addColorStop(0.4, `rgba(220,235,255,${spikeA * 0.5})`);
          grad.addColorStop(0.5, `rgba(255,255,255,${spikeA * 0.9})`);
          grad.addColorStop(0.6, `rgba(220,235,255,${spikeA * 0.5})`);
          grad.addColorStop(1,   'rgba(200,215,255,0)');
          ctx.strokeStyle = grad;
          ctx.lineWidth   = 0.7;
          ctx.beginPath();
          ctx.moveTo(sx - Math.cos(ang) * len, sy - Math.sin(ang) * len);
          ctx.lineTo(sx + Math.cos(ang) * len, sy + Math.sin(ang) * len);
          ctx.stroke();
        }
      }
      ctx.restore();
    });

    for (let i = 0; i < streaks.length; i++) {
      const s = streaks[i];
      if (s.delay > 0) { s.delay--; continue; }
      s.life++;
      const prog  = s.life / s.maxLife;
      const alpha = prog < 0.18 ? prog / 0.18 : prog > 0.82 ? (1 - prog) / 0.18 : 1;
      s.x += Math.cos(s.angle) * s.speed;
      s.y += Math.sin(s.angle) * s.speed;
      const x1 = s.x * W, y1 = s.y * H;
      const len = s.trackLen * Math.min(W, H);
      const x0  = x1 - Math.cos(s.angle) * len;
      const y0  = y1 - Math.sin(s.angle) * len;
      const g   = ctx.createLinearGradient(x0, y0, x1, y1);
      g.addColorStop(0,   'rgba(255,255,255,0)');
      g.addColorStop(0.6, `rgba(220,235,255,${alpha * s.brightness * 0.5})`);
      g.addColorStop(1,   `rgba(255,255,255,${alpha * s.brightness})`);
      ctx.save();
      ctx.strokeStyle = g;
      ctx.lineWidth   = 1.4;
      ctx.shadowBlur  = 5;
      ctx.shadowColor = 'rgba(200,220,255,0.9)';
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.stroke();
      ctx.restore();
      if (s.life >= s.maxLife) {
        streaks[i] = makeStreak();
        streaks[i].delay = 80 + Math.floor(Math.random() * 300);
      }
    }
  }
"""
