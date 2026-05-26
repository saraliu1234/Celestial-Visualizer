# Star Motion Visualizer

## How it works

Each Python file is a **JS module** — it just holds its JavaScript as a string:

```python
# e.g. background.py
JS = r"""
  // ─── Background Stars ──────────────────
  const BG = Array.from({ length: 220 }, ...
  function drawBackground(beatInt) { ... }
"""
```

`main.py` is the **assembler** — it imports all five JS strings and stitches them together with the HTML shell:

```python
import audio_engine, background, travelling_star, star_rendering, explosion_system

html = (
    HTML_HEAD            # <!DOCTYPE>, <style>, <canvas>, <script>, canvas setup
    + audio_engine.JS    # Web Audio API beat detection
    + background.JS      # Twinkling stars + meteors
    + travelling_star.JS # Motion modes + comet trail
    + star_rendering.JS  # Halo, spikes, Airy disk, core
    + explosion_system.JS# Shockwaves, particles, sparks, flash
    + JS_MAIN_LOOP       # animate(), keyboard, file input, init
    + HTML_TAIL          # </script></body></html>
)
```

Run `python3 main.py` → it writes `star-visualizer.html` → open in browser.

## Why this is better than a pure Python approach

| | Pure Python (pygame) | Python → HTML |
|---|---|---|
| Rendering | CPU-bound, slow | GPU-accelerated canvas |
| Gradients | Manual numpy simulation | Native `createRadialGradient` |
| Beat detection | librosa pre-analysis (offline) | Real-time Web Audio API |
| Dependencies | pygame, librosa, numpy | Just Python stdlib |
| Output | Requires Python to run | Standalone `.html` file anyone can open |

Python is used purely as a **build tool** — it organizes, owns, and assembles the code. The browser does all the heavy work.
