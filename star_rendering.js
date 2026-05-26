
  // ─── Stellar Point Rendering ──────────────────────────────────────────────
  function drawStellarPoint(cx, cy) {
    const t      = performance.now() * 0.001;
    const scale  = 1 + star.recoil * 0.55;
    const baseR  = star.baseR * scale;
    const glow   = star.glow;

    // ── Diffuse halo ──────────────────────────────────────────────────────
    {
      const haloR = baseR * 9 + glow * 45;
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, haloR);
      g.addColorStop(0,   `rgba(255,245,190,${0.55 + glow * 0.35})`);
      g.addColorStop(0.18,`rgba(255,210,100,${0.22 + glow * 0.18})`);
      g.addColorStop(0.5, `rgba(255,170, 50,${0.06 + glow * 0.08})`);
      g.addColorStop(1,   'rgba(255,120, 20,0)');
      ctx.save();
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(cx, cy, haloR, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // ── Diffraction spikes ────────────────────────────────────────────────
    const spikes = [
      { angle: 0,            baseLen: 34, w: 2.0, primary: true  },
      { angle: Math.PI * .5, baseLen: 31, w: 2.0, primary: true  },
      { angle: Math.PI * .25,baseLen: 17, w: 1.1, primary: false },
      { angle:-Math.PI * .25,baseLen: 17, w: 1.1, primary: false },
    ];

    spikes.forEach((sp, i) => {
      const flicker   = 0.65 + 0.35 * Math.sin(t * (1.0 + i * 0.45) + sp.angle * 2.7 + i);
      const beatBoost = 1 + glow * 2.8;
      const len       = (sp.baseLen + star.recoil * 28) * flicker * beatBoost * scale;
      const alpha     = (sp.primary ? 0.88 : 0.42) * flicker;

      const grad = ctx.createLinearGradient(
        cx - Math.cos(sp.angle) * len, cy - Math.sin(sp.angle) * len,
        cx + Math.cos(sp.angle) * len, cy + Math.sin(sp.angle) * len
      );
      grad.addColorStop(0,    'rgba(255,220,120,0)');
      grad.addColorStop(0.28, `rgba(255,238,165,${alpha * 0.4})`);
      grad.addColorStop(0.44, `rgba(255,250,215,${alpha * 0.88})`);
      grad.addColorStop(0.5,  `rgba(255,255,255,${alpha})`);
      grad.addColorStop(0.56, `rgba(255,250,215,${alpha * 0.88})`);
      grad.addColorStop(0.72, `rgba(255,238,165,${alpha * 0.4})`);
      grad.addColorStop(1,    'rgba(255,220,120,0)');

      ctx.save();
      ctx.strokeStyle = grad;
      ctx.lineWidth   = sp.w * flicker * scale;
      ctx.shadowBlur  = sp.primary ? 12 : 5;
      ctx.shadowColor = '#FFD060';
      ctx.lineCap     = 'round';
      ctx.beginPath();
      ctx.moveTo(cx - Math.cos(sp.angle) * len, cy - Math.sin(sp.angle) * len);
      ctx.lineTo(cx + Math.cos(sp.angle) * len, cy + Math.sin(sp.angle) * len);
      ctx.stroke();
      ctx.restore();
    });

    // ── Airy disk (bright core) ───────────────────────────────────────────
    ctx.save();
    const coreG = ctx.createRadialGradient(cx, cy, 0, cx, cy, baseR * 2.8);
    coreG.addColorStop(0,   'rgba(255,255,255,1)');
    coreG.addColorStop(0.28,'rgba(255,248,208,0.92)');
    coreG.addColorStop(0.65,'rgba(255,218,130,0.45)');
    coreG.addColorStop(1,   'rgba(255,185, 60,0)');
    ctx.fillStyle  = coreG;
    ctx.shadowBlur = 22 + glow * 42;
    ctx.shadowColor= '#FFFAE0';
    ctx.beginPath();
    ctx.arc(cx, cy, baseR * 2.8, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // ── Innermost bright point ────────────────────────────────────────────
    ctx.save();
    ctx.fillStyle  = '#FFFFFF';
    ctx.shadowBlur = 14 + glow * 22;
    ctx.shadowColor= '#FFFFFF';
    ctx.beginPath();
    ctx.arc(cx, cy, baseR * 0.55, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }
