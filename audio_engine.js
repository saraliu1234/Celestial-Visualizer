
  // ─── Audio Engine ─────────────────────────────────────────────────────────
  let audioCtx = null, analyser = null, freqData = null, isPlaying = false;
  const HIST = 50;
  const energyBuf = new Float32Array(HIST);
  let histIdx = 0, lastBeatAt = 0;
  const MIN_BEAT_GAP = 0.12;

  function getSensitivity() { return parseFloat(document.getElementById('sens').value); }

  function detectBeat() {
    if (!analyser || !isPlaying) return { beat: false, intensity: 0 };
    analyser.getByteFrequencyData(freqData);
    const nyquist = audioCtx.sampleRate / 2;
    const binHz   = nyquist / analyser.frequencyBinCount;
    const lo = Math.max(0, Math.floor(30   / binHz));
    const hi = Math.min(freqData.length - 1, Math.floor(3000 / binHz));
    let energy = 0;
    for (let i = lo; i <= hi; i++) energy += freqData[i] * freqData[i];
    energy /= (hi - lo + 1);
    let avg = 0;
    for (let i = 0; i < HIST; i++) avg += energyBuf[i];
    avg /= HIST;
    energyBuf[histIdx] = energy;
    histIdx = (histIdx + 1) % HIST;
    const sens      = getSensitivity();
    const threshold = avg * (1.5 - sens * 0.04);
    const now       = audioCtx.currentTime;
    const isBeat    = energy > threshold && energy > 200 && (now - lastBeatAt) > MIN_BEAT_GAP;
    if (isBeat) lastBeatAt = now;
    return { beat: isBeat, intensity: Math.max(0, Math.min(1, (energy - avg) / (avg * 2 + 1))) };
  }

  async function loadAudio(file) {
    if (audioCtx) audioCtx.close();
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = 2048;
    analyser.smoothingTimeConstant = 0.25;
    freqData = new Uint8Array(analyser.frequencyBinCount);
    const decoded = await audioCtx.decodeAudioData(await file.arrayBuffer());
    const src = audioCtx.createBufferSource();
    src.buffer = decoded;
    src.connect(analyser);
    analyser.connect(audioCtx.destination);
    src.start(0);
    isPlaying = true;
    src.onended = () => { isPlaying = false; };
  }
