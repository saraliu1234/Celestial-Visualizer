"""
main.py
Imports each JS block from its Python module, assembles them with the HTML
shell + CSS, and writes the final star-visualizer.html webpage.

Run:  python3 main.py
Then open star-visualizer.html in a browser.
"""

import os
import audio_engine
import background
import travelling_star
import star_rendering
import explosion_system

# ─── HTML shell (everything that isn't JS logic) ──────────────────────────────
HTML_HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Star Motion Visualizer</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #000; overflow: hidden; font-family: 'Arial', sans-serif; }
    canvas { display: block; position: fixed; top: 0; left: 0; }

    #ui {
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      pointer-events: none; z-index: 10;
    }
    #upload-area {
      pointer-events: all; text-align: center;
      padding: 40px 50px;
      border: 2px dashed rgba(255, 200, 50, 0.4);
      border-radius: 20px;
      background: rgba(0, 0, 10, 0.85);
      color: #FFD700;
      cursor: pointer;
      transition: all 0.3s;
      backdrop-filter: blur(10px);
    }
    #upload-area:hover {
      border-color: #FFD700;
      background: rgba(255, 200, 50, 0.08);
      box-shadow: 0 0 40px rgba(255, 200, 50, 0.2);
    }
    #upload-area h2 { font-size: 1.8em; margin-bottom: 12px; letter-spacing: 2px; }
    #upload-area p { opacity: 0.6; font-size: 0.9em; line-height: 1.6; }
    #upload-area .hint { margin-top: 12px; font-size: 0.75em; opacity: 0.4; }
    #file-input { display: none; }

    #hud {
      position: fixed; bottom: 0; left: 0; right: 0;
      padding: 16px 24px;
      display: none;
      align-items: center; justify-content: space-between;
      background: linear-gradient(transparent, rgba(0,0,0,0.6));
      color: rgba(255, 200, 50, 0.7);
      font-size: 13px;
      z-index: 10;
    }
    #hud-left { display: flex; flex-direction: column; gap: 4px; }
    #track-name { max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    #mode-display { font-size: 11px; opacity: 0.6; letter-spacing: 1px; }
    #controls-right { display: flex; align-items: center; gap: 20px; }
    label[for="sens"] { opacity: 0.7; }
    #sens { width: 90px; accent-color: #FFD700; cursor: pointer; }
    #beat-indicator {
      width: 10px; height: 10px; border-radius: 50%;
      background: #FFD700; opacity: 0;
      transition: opacity 0.05s;
      box-shadow: 0 0 8px #FFD700;
    }
    #mode-hint {
      position: fixed; top: 16px; right: 16px;
      color: rgba(255, 200, 50, 0.4); font-size: 11px;
      display: none; z-index: 10;
      text-align: right; line-height: 1.9;
    }
  </style>
</head>
<body>
  <canvas id="canvas"></canvas>

  <div id="ui">
    <div id="upload-area" onclick="document.getElementById('file-input').click()">
      <h2>✦ Star Motion Visualizer</h2>
      <p>Load your audio file to begin<br>Stars react to every beat — diffraction spikes & orbital dynamics</p>
      <p class="hint">Supports MP3 · WAV · AAC · OGG · FLAC</p>
    </div>
    <input type="file" id="file-input" accept="audio/*">
  </div>

  <div id="hud">
    <div id="hud-left">
      <div>Now playing: <span id="track-name"></span></div>
      <div id="mode-display">MODE: CIRCULAR ORBIT</div>
    </div>
    <div id="controls-right">
      <label for="sens">Sensitivity</label>
      <input type="range" id="sens" min="1" max="10" value="5" step="0.5">
      <div id="beat-indicator"></div>
    </div>
  </div>

  <div id="mode-hint">
    Keys 1–5 · switch motion mode<br>
    1: Linear  ·  2: Circular Orbit<br>
    3: Lissajous  ·  4: Figure-8<br>
    5: Random Walk
  </div>

  <script>
  // ─── Canvas Setup ─────────────────────────────────────────────────────────
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
"""

JS_MAIN_LOOP = """
  // ─── Main Loop ────────────────────────────────────────────────────────────
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

  // ─── Keyboard: manual mode switch ─────────────────────────────────────────
  window.addEventListener('keydown', e => {
    const map = { '1': 'linear', '2': 'circular', '3': 'lissajous', '4': 'figure8', '5': 'random' };
    if (map[e.key]) setMode(map[e.key]);
  });

  // ─── File Input ───────────────────────────────────────────────────────────
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

  // ─── Init ─────────────────────────────────────────────────────────────────
  resize();
  star.x = W / 2; star.y = H / 2;
  animate();
"""

HTML_TAIL = """\
  </script>
</body>
</html>
"""

# ─── Assemble ─────────────────────────────────────────────────────────────────
def build():
    html = (
        HTML_HEAD
        + audio_engine.JS       # Web Audio API beat detection
        + background.JS         # Twinkling stars + meteors
        + travelling_star.JS    # Motion system + comet trail
        + star_rendering.JS     # Halo, spikes, Airy disk, core
        + explosion_system.JS   # Shockwaves, particles, sparks, flash
        + JS_MAIN_LOOP          # animate(), keyboard, file input, init
        + HTML_TAIL
    )

    out = os.path.join(os.path.dirname(__file__), "star-visualizer.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Built → {out}")
    print("Open that file in a browser to run the visualizer.")

if __name__ == "__main__":
    build()
