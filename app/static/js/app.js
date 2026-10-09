/**
 * app/static/js/app.js
 * Interactive Real-Time Prediction, Gauge Animation, Sliders & Presets,
 * Chart.js configurations, and Drag-and-Drop Batch File Ingestion.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Theme Switcher (Bright / Dark mode)
  initThemeSwitcher();

  // Initialize Real-Time Predictor if on home page
  if (document.getElementById('predictor-section')) {
    initPredictor();
  }

  // Initialize Batch Uploader if on batch page
  if (document.getElementById('batch-dropzone')) {
    initBatchUploader();
  }

  // Initialize Model Retraining handler if present
  const retrainBtn = document.getElementById('btn-retrain-models');
  if (retrainBtn) {
    initRetrainer(retrainBtn);
  }

  // Initialize Font Size Controller
  initFontResizer();

  // Initialize Produce Intelligence Atmosphere Engine
  initProduceThemeEngine();

  // Modal Lightbox for images
  initImageLightbox();
});

/* ==========================================================================
   Theme Switcher (Bright vs Dark Modes)
   ========================================================================== */
function initThemeSwitcher() {
  const themeToggle = document.getElementById('theme-toggle');
  const cornerThemeToggle = document.getElementById('corner-theme-toggle');
  const themeModeText = document.getElementById('theme-mode-text');

  function updateThemeUI(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('freshIQ_theme', theme);
    if (themeModeText) {
      themeModeText.textContent = theme === 'light' ? 'Bright' : 'Dark';
    }
  }

  const currentTheme = localStorage.getItem('freshIQ_theme') || 'dark';
  updateThemeUI(currentTheme);

  const handleToggle = () => {
    const activeTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const nextTheme = activeTheme === 'dark' ? 'light' : 'dark';
    updateThemeUI(nextTheme);
  };

  if (themeToggle) themeToggle.addEventListener('click', handleToggle);
  if (cornerThemeToggle) cornerThemeToggle.addEventListener('click', handleToggle);
}

/* ==========================================================================
   Font Size Resizer Controller
   ========================================================================== */
function initFontResizer() {
  const fontDecrease = document.getElementById('font-decrease');
  const fontReset = document.getElementById('font-reset');
  const fontIncrease = document.getElementById('font-increase');

  const FONT_SIZES = ['13px', '14.5px', '16px', '18px', '20px'];
  let currentIndex = parseInt(localStorage.getItem('freshIQ_font_index') || '2', 10);
  if (isNaN(currentIndex) || currentIndex < 0 || currentIndex >= FONT_SIZES.length) {
    currentIndex = 2; // Default 16px
  }

  function applyFontSize(idx) {
    currentIndex = Math.max(0, Math.min(FONT_SIZES.length - 1, idx));
    document.documentElement.style.setProperty('--base-font-size', FONT_SIZES[currentIndex]);
    localStorage.setItem('freshIQ_font_index', currentIndex.toString());
  }

  // Initial apply
  applyFontSize(currentIndex);

  if (fontDecrease) {
    fontDecrease.addEventListener('click', () => applyFontSize(currentIndex - 1));
  }
  if (fontReset) {
    fontReset.addEventListener('click', () => applyFontSize(2));
  }
  if (fontIncrease) {
    fontIncrease.addEventListener('click', () => applyFontSize(currentIndex + 1));
  }
}

/* ==========================================================================
   Produce Intelligence Professional Atmosphere & Theme Engine
   Replaces literal floating fruits with dynamic, executive produce themes
   ========================================================================== */
function initProduceThemeEngine() {
  const canvas = document.getElementById('produce-ambient-canvas') || document.getElementById('funky-fruits-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  // Fruit theme definitions with professional color palettes & physics
  const PRODUCE_THEMES = [
    {
      id: 'spectrum',
      name: 'FreshIQ Spectrum',
      label: 'Multi-Produce Harmonic',
      palette: [
        [16, 185, 129],   // Emerald
        [6, 182, 212],    // Cyan
        [245, 158, 11],   // Amber
        [244, 63, 94]     // Rose
      ]
    },
    {
      id: 'citrus',
      name: 'Citrus Aura',
      label: 'Orange & Tangerine',
      palette: [
        [249, 115, 22],   // Tangerine
        [245, 158, 11],   // Warm Amber
        [251, 191, 36],   // Sunny Gold
        [234, 88, 12]     // Deep Citrus
      ]
    },
    {
      id: 'orchard',
      name: 'Crisp Orchard',
      label: 'Fresh Produce & Flora',
      palette: [
        [16, 185, 129],   // Emerald
        [5, 150, 105],    // Jade
        [52, 211, 153],   // Mint
        [20, 184, 166]    // Teal
      ]
    },
    {
      id: 'berry',
      name: 'Ruby Berry',
      label: 'Berry & Vine Tomato',
      palette: [
        [244, 63, 94],    // Ruby Rose
        [225, 29, 72],    // Crimson
        [190, 18, 60],    // Deep Berry
        [251, 113, 133]   // Coral Rose
      ]
    },
    {
      id: 'tropical',
      name: 'Solar Tropical',
      label: 'Pineapple & Banana',
      palette: [
        [234, 179, 8],    // Golden Mango
        [245, 158, 11],   // Warm Apricot
        [253, 224, 71],   // Radiant Sun
        [217, 119, 6]     // Amber Honey
      ]
    }
  ];

  // Retrieve or default theme
  let savedId = localStorage.getItem('freshIQ_fruit_theme') || 'spectrum';
  let currentThemeIndex = PRODUCE_THEMES.findIndex(t => t.id === savedId);
  if (currentThemeIndex === -1) currentThemeIndex = 0;

  const cycleBtn = document.getElementById('fruit-bg-cycle');
  const tooltipLabel = document.getElementById('bg-fruit-label');

  function applyFruitTheme(themeIndex, save = true) {
    currentThemeIndex = themeIndex;
    const theme = PRODUCE_THEMES[currentThemeIndex];

    document.documentElement.setAttribute('data-fruit-theme', theme.id);
    if (document.body) {
      document.body.setAttribute('data-fruit-theme', theme.id);
    }

    if (tooltipLabel) {
      tooltipLabel.textContent = `Fruit Theme: ${theme.name}`;
    }

    if (save) {
      localStorage.setItem('freshIQ_fruit_theme', theme.id);
    }

    // Trigger smooth color transition on all active particles
    if (particles && particles.length > 0) {
      particles.forEach(p => p.transitionToTheme(theme.palette));
    }
  }

  // Bind dock button
  if (cycleBtn) {
    cycleBtn.addEventListener('click', () => {
      const nextIndex = (currentThemeIndex + 1) % PRODUCE_THEMES.length;
      applyFruitTheme(nextIndex, true);
    });
  }

  // Professional Telemetry Ambient Node Simulation
  const NUM_PARTICLES = window.innerWidth < 768 ? 32 : 55;
  const MAX_CONNECT_DIST = 110;

  class TelemetryNode {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.radius = Math.random() * 2.6 + 1.4; // 1.4px - 4.0px
      this.vx = (Math.random() - 0.5) * 0.4;
      this.vy = (Math.random() - 0.5) * 0.4;
      this.baseAlpha = Math.random() * 0.22 + 0.18; // 0.18 - 0.40 subtle
      this.alpha = this.baseAlpha;
      this.pulseSpeed = Math.random() * 0.02 + 0.01;
      this.pulseAngle = Math.random() * Math.PI * 2;

      // Color interpolation
      const initialPalette = PRODUCE_THEMES[currentThemeIndex].palette;
      const initialColor = initialPalette[Math.floor(Math.random() * initialPalette.length)];
      this.color = [...initialColor];
      this.targetColor = [...initialColor];
    }

    transitionToTheme(palette) {
      this.targetColor = [...palette[Math.floor(Math.random() * palette.length)]];
    }

    update(mouseX, mouseY) {
      // Smooth color lerp towards target theme color
      for (let i = 0; i < 3; i++) {
        this.color[i] += (this.targetColor[i] - this.color[i]) * 0.06;
      }

      // Breathing luminescence
      this.pulseAngle += this.pulseSpeed;
      this.alpha = this.baseAlpha + Math.sin(this.pulseAngle) * 0.1;

      this.x += this.vx;
      this.y += this.vy;

      // Wrap around bounds
      if (this.x < -20) this.x = width + 20;
      if (this.x > width + 20) this.x = -20;
      if (this.y < -20) this.y = height + 20;
      if (this.y > height + 20) this.y = -20;

      // Cursor gentle interaction
      if (mouseX !== null && mouseY !== null) {
        const dx = this.x - mouseX;
        const dy = this.y - mouseY;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 130) {
          const force = (130 - dist) / 130;
          this.x += (dx / dist) * force * 1.6;
          this.y += (dy / dist) * force * 1.6;
          this.alpha = Math.min(0.8, this.alpha + force * 0.3);
        }
      }
    }

    draw() {
      const [r, g, b] = this.color.map(Math.round);
      const glowRadius = this.radius * 3.6;

      // Soft ambient radial glow
      const grad = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, glowRadius);
      grad.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${this.alpha})`);
      grad.addColorStop(0.4, `rgba(${r}, ${g}, ${b}, ${this.alpha * 0.4})`);
      grad.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0)`);

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(this.x, this.y, glowRadius, 0, Math.PI * 2);
      ctx.fill();

      // Sharp central luminous nucleus
      ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${Math.min(1, this.alpha + 0.35)})`;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius * 0.75, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  const particles = Array.from({ length: NUM_PARTICLES }, () => new TelemetryNode());

  let mouseX = null;
  let mouseY = null;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  window.addEventListener('mouseleave', () => {
    mouseX = null;
    mouseY = null;
  });

  // Render Loop
  function animate() {
    ctx.clearRect(0, 0, width, height);

    // Subtle IoT sensor telemetry connection filaments
    for (let i = 0; i < particles.length; i++) {
      const p1 = particles[i];
      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < MAX_CONNECT_DIST) {
          const lineAlpha = (1 - dist / MAX_CONNECT_DIST) * 0.15 * ((p1.alpha + p2.alpha) / 2);
          const [r, g, b] = p1.color.map(Math.round);
          ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, ${lineAlpha})`;
          ctx.lineWidth = 0.85;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
    }

    // Update and draw nodes
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(mouseX, mouseY);
      particles[i].draw();
    }

    requestAnimationFrame(animate);
  }

  // Initial theme application & start animation
  applyFruitTheme(currentThemeIndex, false);
  animate();

  // Expose global helper for synchronizing theme with produce variety
  window.setProduceFruitTheme = function(fruitName) {
    const mapping = {
      'Orange': 'citrus',
      'Tomato': 'berry',
      'Banana': 'tropical',
      'Pineapple': 'tropical'
    };
    const targetId = mapping[fruitName] || 'spectrum';
    const targetIdx = PRODUCE_THEMES.findIndex(t => t.id === targetId);
    if (targetIdx !== -1) {
      applyFruitTheme(targetIdx, true);
    }
  };
}

/* ==========================================================================
   Real-Time Predictor Engine
   ========================================================================== */
function initPredictor() {
  let selectedFruit = 'Orange';
  let debounceTimer = null;

  const tempSlider = document.getElementById('slider-temp');
  const tempVal = document.getElementById('val-temp');

  const humSlider = document.getElementById('slider-humidity');
  const humVal = document.getElementById('val-humidity');

  const lightSlider = document.getElementById('slider-light');
  const lightVal = document.getElementById('val-light');

  const co2Slider = document.getElementById('slider-co2');
  const co2Val = document.getElementById('val-co2');

  const fruitChips = document.querySelectorAll('.fruit-chip');
  const presetBtns = document.querySelectorAll('.preset-btn');

  // SVG Gauge elements
  const gaugeProgress = document.getElementById('gauge-progress');
  const gaugeValue = document.getElementById('gauge-value');
  const gaugeLabel = document.getElementById('gauge-label');
  const statusBadge = document.getElementById('status-badge');
  const statusCard = document.getElementById('status-card');
  const advisoryText = document.getElementById('advisory-text');
  const diagnosticsList = document.getElementById('diagnostics-list');
  const probGood = document.getElementById('prob-good');
  const probBad = document.getElementById('prob-bad');

  // Circle circumference is 2 * PI * r = 2 * 3.14159 * 75 ≈ 471
  const CIRCUMFERENCE = 471;

  // Real-time HUD elements
  const qualityGradeBadge = document.getElementById('quality-grade-badge');
  const shelfLifePill = document.getElementById('shelf-life-pill');
  const hudDewPoint = document.getElementById('hud-dew-point');
  const hudDewMargin = document.getElementById('hud-dew-margin');
  const hudVpd = document.getElementById('hud-vpd');
  const hudVpdStatus = document.getElementById('hud-vpd-status');
  const hudHaccp = document.getElementById('hud-haccp');
  const hudHaccpSpec = document.getElementById('hud-haccp-spec');
  const hudPathogen = document.getElementById('hud-pathogen');
  const hudRespiration = document.getElementById('hud-respiration');
  const chartTimestamp = document.getElementById('chart-timestamp');

  // Live Microclimate Waveform Chart.js instance
  let liveChart = null;
  const chartCanvas = document.getElementById('live-telemetry-chart');
  const MAX_HISTORY = 18;
  const historyLabels = [];
  const historyTemp = [];
  const historyHum = [];
  const historyCo2 = [];

  function initLiveWaveformChart() {
    if (!chartCanvas || typeof Chart === 'undefined') return;
    const ctx = chartCanvas.getContext('2d');
    liveChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: historyLabels,
        datasets: [
          {
            label: 'Temp (°C)',
            data: historyTemp,
            borderColor: '#f59e0b',
            backgroundColor: 'rgba(245, 158, 11, 0.1)',
            borderWidth: 2,
            tension: 0.35,
            pointRadius: 0,
            yAxisID: 'yTemp'
          },
          {
            label: 'Humidity (%)',
            data: historyHum,
            borderColor: '#06b6d4',
            backgroundColor: 'rgba(6, 182, 212, 0.1)',
            borderWidth: 2,
            tension: 0.35,
            pointRadius: 0,
            yAxisID: 'yHum'
          },
          {
            label: 'CO2 / 10',
            data: historyCo2,
            borderColor: '#10b981',
            backgroundColor: 'transparent',
            borderWidth: 1.5,
            borderDash: [4, 4],
            tension: 0.35,
            pointRadius: 0,
            yAxisID: 'yTemp'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 300 },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              boxWidth: 8,
              font: { size: 9, family: 'JetBrains Mono' },
              color: '#94a3b8'
            }
          },
          tooltip: { enabled: true }
        },
        scales: {
          x: { display: false },
          yTemp: {
            type: 'linear',
            position: 'left',
            min: 19,
            max: 29,
            ticks: {
              font: { size: 9, family: 'JetBrains Mono' },
              color: '#94a3b8',
              callback: (v) => `${v}°`
            },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          },
          yHum: {
            type: 'linear',
            position: 'right',
            min: 82,
            max: 99,
            grid: { display: false },
            ticks: {
              font: { size: 9, family: 'JetBrains Mono' },
              color: '#06b6d4',
              callback: (v) => `${v}%`
            }
          }
        }
      }
    });

    // Populate initial points
    for (let i = 0; i < 6; i++) {
      pushTelemetryData(24.0, 93.0, 330.0);
    }
  }

  function pushTelemetryData(t, h, c) {
    const timeStr = new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
    historyLabels.push(timeStr);
    historyTemp.push(t);
    historyHum.push(h);
    historyCo2.push(c / 10.0);

    if (historyLabels.length > MAX_HISTORY) {
      historyLabels.shift();
      historyTemp.shift();
      historyHum.shift();
      historyCo2.shift();
    }
    if (liveChart) liveChart.update('none');
    if (chartTimestamp) chartTimestamp.textContent = `Last Packet: ${timeStr} • LoRaWAN`;
  }

  initLiveWaveformChart();

  function updateGauge(confidence, isFresh) {
    const offset = CIRCUMFERENCE - (confidence / 100) * CIRCUMFERENCE;
    gaugeProgress.style.strokeDashoffset = offset;
    gaugeProgress.style.stroke = isFresh ? '#10b981' : '#f43f5e';
    gaugeValue.textContent = `${confidence.toFixed(1)}%`;
    gaugeValue.style.color = isFresh ? '#10b981' : '#f43f5e';
    gaugeLabel.textContent = isFresh ? 'Freshness Confidence' : 'Spoilage Probability';
  }

  function runPrediction() {
    const payload = {
      temp: parseFloat(tempSlider.value),
      humidity: parseFloat(humSlider.value),
      light: parseFloat(lightSlider.value),
      co2: parseFloat(co2Slider.value),
      fruit: selectedFruit
    };

    pushTelemetryData(payload.temp, payload.humidity, payload.co2);

    fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(res => {
      if (!res.success) throw new Error(res.error || 'Prediction failed');
      const data = res.data;
      const isFresh = data.prediction === 'Good';

      // Update Gauge
      updateGauge(data.confidence, isFresh);

      // Update Status Hero
      if (isFresh) {
        statusCard.className = 'status-hero state-fresh';
        statusBadge.className = 'status-badge-lg badge-fresh';
        statusBadge.innerHTML = `<span class="icon">🌿</span> Fresh & Marketable`;
      } else {
        statusCard.className = 'status-hero state-spoiled';
        statusBadge.className = 'status-badge-lg badge-spoiled';
        statusBadge.innerHTML = `<span class="icon">⚠️</span> Spoiled / Degraded`;
      }

      // Update Probabilities
      if (probGood && probBad) {
        probGood.textContent = `${data.probabilities['Good']}%`;
        probBad.textContent = `${data.probabilities['Bad']}%`;
      }

      // Update Physical Cold-Chain Telemetry HUD
      const pt = data.physical_telemetry;
      if (pt) {
        if (qualityGradeBadge) {
          qualityGradeBadge.textContent = pt.quality_grade;
          qualityGradeBadge.className = isFresh ? 'badge-pill badge-good' : 'badge-pill badge-bad';
        }
        if (shelfLifePill) {
          shelfLifePill.textContent = `⏱️ Est. Shelf Life: ${pt.shelf_life_display} (${pt.shelf_life_urgency})`;
          shelfLifePill.style.color = pt.shelf_life_urgency === 'CRITICAL' ? '#f43f5e' : pt.shelf_life_urgency === 'OPTIMAL' ? '#10b981' : '#f59e0b';
          shelfLifePill.style.borderColor = pt.shelf_life_urgency === 'CRITICAL' ? 'rgba(244,63,94,0.4)' : 'rgba(16,185,129,0.4)';
        }
        if (hudDewPoint) hudDewPoint.textContent = `${pt.dew_point}°C`;
        if (hudDewMargin) {
          const margin = (payload.temp - pt.dew_point).toFixed(1);
          hudDewMargin.textContent = margin <= 1.0 ? `Margin: ${margin}°C (CONDENSATION RISK)` : `Margin: +${margin}°C (Safe)`;
          hudDewMargin.style.color = margin <= 1.0 ? '#f43f5e' : '#94a3b8';
        }
        if (hudVpd) hudVpd.textContent = `${pt.vpd} kPa`;
        if (hudVpdStatus) {
          hudVpdStatus.textContent = pt.vpd < 0.12 ? 'Low: Mold Risk' : pt.vpd > 0.45 ? 'High: Shrivel Risk' : 'Optimal Storage Range';
          hudVpdStatus.style.color = (pt.vpd < 0.12 || pt.vpd > 0.45) ? '#f59e0b' : '#94a3b8';
        }
        if (hudHaccp) {
          hudHaccp.textContent = pt.haccp_status;
          hudHaccp.style.color = pt.haccp_status === 'HACCP COMPLIANT' ? '#10b981' : '#f43f5e';
        }
        if (hudHaccpSpec) hudHaccpSpec.textContent = pt.haccp_standard;
        if (hudPathogen) hudPathogen.textContent = pt.primary_pathogen.split('(')[0].trim();
        if (hudRespiration) hudRespiration.textContent = `Resp: ${pt.respiration_rate.split('(')[0].trim()}`;
      }

      // Update Advisory text
      advisoryText.textContent = data.action_advice;

      // Update Diagnostics
      if (diagnosticsList && data.diagnostics) {
        diagnosticsList.innerHTML = data.diagnostics.map(d => `
          <div class="diag-item diag-${d.type}">
            <span>${d.type === 'success' ? '✓' : d.type === 'warning' ? '⚠' : d.type === 'danger' ? '✕' : 'ℹ'}</span>
            <div><strong>${d.param}:</strong> ${d.message}</div>
          </div>
        `).join('');
      }
    })
    .catch(err => {
      console.error('Inference error:', err);
    });
  }

  function queuePrediction() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(runPrediction, 100);
  }

  // Slider events
  tempSlider.addEventListener('input', (e) => {
    tempVal.textContent = `${parseFloat(e.target.value).toFixed(1)}°C`;
    queuePrediction();
  });
  humSlider.addEventListener('input', (e) => {
    humVal.textContent = `${parseFloat(e.target.value).toFixed(0)}%`;
    queuePrediction();
  });
  lightSlider.addEventListener('input', (e) => {
    lightVal.textContent = `${parseFloat(e.target.value).toFixed(1)} Lux`;
    queuePrediction();
  });
  co2Slider.addEventListener('input', (e) => {
    co2Val.textContent = `${parseFloat(e.target.value).toFixed(0)} ppm`;
    queuePrediction();
  });

  // Fruit Selection
  fruitChips.forEach(chip => {
    chip.addEventListener('click', () => {
      fruitChips.forEach(c => c.classList.remove('selected'));
      chip.classList.add('selected');
      selectedFruit = chip.dataset.fruit;
      if (typeof window.setProduceFruitTheme === 'function') {
        window.setProduceFruitTheme(selectedFruit);
      }
      queuePrediction();
    });
  });

  // Presets Selection
  presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const pFruit = btn.dataset.fruit;
      const pTemp = btn.dataset.temp;
      const pHum = btn.dataset.hum;
      const pLight = btn.dataset.light;
      const pCo2 = btn.dataset.co2;

      // Set fruit
      selectedFruit = pFruit;
      fruitChips.forEach(c => {
        if (c.dataset.fruit === pFruit) c.classList.add('selected');
        else c.classList.remove('selected');
      });
      if (typeof window.setProduceFruitTheme === 'function') {
        window.setProduceFruitTheme(pFruit);
      }

      // Set sliders
      tempSlider.value = pTemp;
      tempVal.textContent = `${parseFloat(pTemp).toFixed(1)}°C`;

      humSlider.value = pHum;
      humVal.textContent = `${parseFloat(pHum).toFixed(0)}%`;

      lightSlider.value = pLight;
      lightVal.textContent = `${parseFloat(pLight).toFixed(1)} Lux`;

      co2Slider.value = pCo2;
      co2Val.textContent = `${parseFloat(pCo2).toFixed(0)} ppm`;

      queuePrediction();
    });
  });

  // Live IoT Telemetry Streaming Simulation
  let isStreaming = false;
  let streamInterval = null;
  const streamToggleBtn = document.getElementById('btn-toggle-stream');

  if (streamToggleBtn) {
    streamToggleBtn.addEventListener('click', () => {
      isStreaming = !isStreaming;
      if (isStreaming) {
        streamToggleBtn.classList.add('btn-emerald');
        streamToggleBtn.classList.remove('btn-secondary');
        streamToggleBtn.innerHTML = `<span class="live-stream-dot"></span> Live Telemetry Active`;

        streamInterval = setInterval(() => {
          // Slight natural physical micro-variations
          const tempDelta = (Math.random() - 0.48) * 0.35;
          const humDelta = (Math.random() - 0.5) * 0.9;
          const lightDelta = (Math.random() - 0.5) * 0.7;
          const co2Delta = (Math.random() - 0.46) * 5.5;

          let newTemp = Math.min(27.5, Math.max(20.5, parseFloat(tempSlider.value) + tempDelta));
          let newHum = Math.min(97.0, Math.max(86.0, parseFloat(humSlider.value) + humDelta));
          let newLight = Math.min(24.0, Math.max(4.0, parseFloat(lightSlider.value) + lightDelta));
          let newCo2 = Math.min(460.0, Math.max(190.0, parseFloat(co2Slider.value) + co2Delta));

          tempSlider.value = newTemp.toFixed(1);
          tempVal.textContent = `${newTemp.toFixed(1)}°C`;

          humSlider.value = newHum.toFixed(0);
          humVal.textContent = `${newHum.toFixed(0)}%`;

          lightSlider.value = newLight.toFixed(1);
          lightVal.textContent = `${newLight.toFixed(1)} Lux`;

          co2Slider.value = newCo2.toFixed(0);
          co2Val.textContent = `${newCo2.toFixed(0)} ppm`;

          queuePrediction();
        }, 1800);
      } else {
        clearInterval(streamInterval);
        streamToggleBtn.classList.remove('btn-emerald');
        streamToggleBtn.classList.add('btn-secondary');
        streamToggleBtn.innerHTML = `<span>📡</span> Stream Live IoT`;
      }
    });
  }

  // Real Canvas Computer Vision Pixel Analysis
  function performOpticalCVScan(img) {
    const cvCanvas = document.getElementById('optical-cv-canvas');
    if (!cvCanvas) return;
    const ctx = cvCanvas.getContext('2d');
    const W = 140;
    const H = 140;
    cvCanvas.width = W;
    cvCanvas.height = H;
    ctx.drawImage(img, 0, 0, W, H);

    const imgData = ctx.getImageData(0, 0, W, H);
    const data = imgData.data;
    let totalPixels = 0;
    let decayPixels = 0;
    let hueSum = 0;
    const hues = [];

    for (let i = 0; i < data.length; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];
      const a = data[i + 3];

      if (a < 60) continue;

      const max = Math.max(r, g, b) / 255;
      const min = Math.min(r, g, b) / 255;
      const d = max - min;
      let h = 0;
      const l = (max + min) / 2;
      const s = d === 0 ? 0 : d / (1 - Math.abs(2 * l - 1));

      if (d !== 0) {
        if (max === r / 255) h = ((g / 255 - b / 255) / d) % 6;
        else if (max === g / 255) h = (b / 255 - r / 255) / d + 2;
        else h = (r / 255 - g / 255) / d + 4;
        h = Math.round(h * 60);
        if (h < 0) h += 360;
      }

      totalPixels++;
      hueSum += h;
      hues.push(h);

      // Detection of necrotic browning & lesions
      const isBrownNecrosis = (h >= 14 && h <= 46 && s > 0.18 && l < 0.42 && r > b * 1.35);
      const isDarkMold = (l < 0.22 && max < 0.35);
      if (isBrownNecrosis || isDarkMold) {
        decayPixels++;
      }
    }

    if (totalPixels === 0) return;

    const avgHue = Math.round(hueSum / totalPixels);
    const necrosisRatio = Math.min(100, Math.max(0, (decayPixels / totalPixels) * 100));

    let varianceSum = 0;
    for (let i = 0; i < hues.length; i++) {
      const diff = hues[i] - avgHue;
      varianceSum += diff * diff;
    }
    const stdDev = Math.sqrt(varianceSum / totalPixels);
    const uniformity = Math.max(10, Math.min(99.2, 100 - (stdDev * 0.75)));

    // Update Optical UI
    const hueValEl = document.getElementById('optical-hue-val');
    const necrosisValEl = document.getElementById('optical-necrosis-val');
    const necrosisBarEl = document.getElementById('optical-necrosis-bar');
    const uniformityValEl = document.getElementById('optical-uniformity-val');
    const uniformityBarEl = document.getElementById('optical-uniformity-bar');
    const resultBadge = document.getElementById('photo-result-badge');
    const summaryText = document.getElementById('optical-summary-text');

    if (hueValEl) hueValEl.textContent = `${avgHue}°`;
    if (necrosisValEl) {
      necrosisValEl.textContent = `${necrosisRatio.toFixed(1)}%`;
      necrosisValEl.style.color = necrosisRatio > 10.0 ? '#f43f5e' : necrosisRatio > 4.5 ? '#f59e0b' : '#10b981';
    }
    if (necrosisBarEl) {
      necrosisBarEl.style.width = `${Math.max(4, necrosisRatio)}%`;
      necrosisBarEl.style.background = necrosisRatio > 10.0 ? '#f43f5e' : necrosisRatio > 4.5 ? '#f59e0b' : '#10b981';
    }
    if (uniformityValEl) uniformityValEl.textContent = `${uniformity.toFixed(1)}%`;
    if (uniformityBarEl) uniformityBarEl.style.width = `${uniformity.toFixed(1)}%`;

    if (resultBadge && summaryText) {
      if (necrosisRatio > 12.0) {
        resultBadge.className = 'badge-pill badge-bad';
        resultBadge.textContent = `⚠️ High Necrosis Detected (${necrosisRatio.toFixed(1)}%)`;
        summaryText.textContent = `Optical analysis reveals localized fungal lesioning and cuticle breakdown. Correlates with sensor microbial decay risk.`;
      } else if (necrosisRatio > 4.5) {
        resultBadge.className = 'badge-pill';
        resultBadge.style.background = 'rgba(245, 158, 11, 0.2)';
        resultBadge.style.color = '#f59e0b';
        resultBadge.textContent = `⚠️ Moderate Oxidation (${necrosisRatio.toFixed(1)}%)`;
        summaryText.textContent = `Minor surface browning detected on produce peel. Storage humidity and temperature require stabilization.`;
      } else {
        resultBadge.className = 'badge-pill badge-good';
        resultBadge.textContent = `✓ Intact Cuticle Integrity (${(100 - necrosisRatio).toFixed(1)}%)`;
        summaryText.textContent = `Peel pigments reflect uniform cellular health with minimal oxidative darkening.`;
      }
    }
  }

  // Visual Produce Inspection Handler
  const photoInput = document.getElementById('produce-photo-input');
  const photoPreview = document.getElementById('photo-preview-wrap');
  const photoImg = document.getElementById('photo-preview-img');
  const photoResultBadge = document.getElementById('photo-result-badge');

  if (photoInput) {
    photoInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (evt) => {
        if (photoPreview && photoImg) {
          photoImg.src = evt.target.result;
          photoPreview.style.display = 'block';
          if (photoResultBadge) {
            photoResultBadge.textContent = 'Optical Spectrum Analysis: Processing Pixels...';
          }
          photoImg.onload = () => {
            performOpticalCVScan(photoImg);
          };
        }
      };
      reader.readAsDataURL(file);
    });
  }

  // Initial trigger
  runPrediction();
}

/* ==========================================================================
   Batch Uploader Engine
   ========================================================================== */
function initBatchUploader() {
  const dropzone = document.getElementById('batch-dropzone');
  const fileInput = document.getElementById('file-input');
  const uploadPrompt = document.getElementById('upload-prompt');
  const resultsArea = document.getElementById('batch-results-area');
  const downloadBtn = document.getElementById('btn-download-enriched');
  const printAuditBtn = document.getElementById('btn-print-audit');
  const filterBtns = document.querySelectorAll('.batch-filter-btn');

  let currentEnrichedCsv = null;
  let allBatchRecords = [];

  ['dragenter', 'dragover'].forEach(name => {
    dropzone.addEventListener(name, (e) => {
      e.preventDefault();
      dropzone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(name => {
    dropzone.addEventListener(name, (e) => {
      e.preventDefault();
      dropzone.classList.remove('dragover');
    });
  });

  dropzone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFile(files[0]);
  });

  dropzone.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) handleFile(e.target.files[0]);
  });

  function renderBatchTable(filter = 'all') {
    const tableBody = document.getElementById('batch-table-body');
    if (!tableBody) return;

    let filtered = allBatchRecords;
    if (filter === 'good') filtered = allBatchRecords.filter(r => r.Predicted_Class === 'Good');
    if (filter === 'bad') filtered = allBatchRecords.filter(r => r.Predicted_Class === 'Bad');

    tableBody.innerHTML = filtered.map((row, idx) => {
      const isGood = row.Predicted_Class === 'Good';
      const badge = isGood
        ? `<span class="badge-pill badge-good">✓ Fresh</span>`
        : `<span class="badge-pill badge-bad">⚠️ Spoiled</span>`;
      const dewVal = row['Dew_Point (°C)'] !== undefined ? row['Dew_Point (°C)'] : (row['Dew_Point (C)'] !== undefined ? row['Dew_Point (C)'] : '—');
      const vpdVal = row['VPD (kPa)'] !== undefined ? row['VPD (kPa)'] : (row['VPD'] !== undefined ? row['VPD'] : '—');
      return `
        <tr>
          <td>${idx + 1}</td>
          <td><strong>${row.Fruit || 'N/A'}</strong></td>
          <td>${row.Temp}°C</td>
          <td>${row['Humidity (%)']}%</td>
          <td>${dewVal !== '—' ? dewVal + '°C' : '—'}</td>
          <td>${vpdVal !== '—' ? vpdVal + ' kPa' : '—'}</td>
          <td>${row['CO2 (ppm)']} ppm</td>
          <td>${badge}</td>
          <td><strong>${row['Freshness_Score (%)'] || row.Confidence || '—'}%</strong></td>
          <td><span style="font-size: 0.76rem; font-weight: 700; color: ${isGood ? 'var(--emerald-glow)' : 'var(--rose-glow)'};">${row.Market_Grade || 'Grade A'}</span></td>
          <td><span style="font-family: 'JetBrains Mono'; font-size: 0.8rem;">${row.Estimated_Shelf_Life || '—'}</span></td>
        </tr>
      `;
    }).join('');
  }

  // Filter click handlers
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderBatchTable(btn.dataset.filter);
    });
  });

  // Print QA Audit handler
  if (printAuditBtn) {
    printAuditBtn.addEventListener('click', () => {
      window.print();
    });
  }

  function handleFile(file) {
    if (!file.name.endsWith('.csv')) {
      alert('Please upload a valid .csv file.');
      return;
    }

    uploadPrompt.innerHTML = `<span class="spinner"></span> Running Batch Cold-Chain Telemetry on <strong>${file.name}</strong>...`;

    const formData = new FormData();
    formData.append('file', file);

    fetch('/api/batch-predict', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(res => {
      uploadPrompt.innerHTML = `<span>✓ Completed: <strong>${file.name}</strong> (${res.total_records} records processed)</span>`;
      if (!res.success) throw new Error(res.error || 'Batch evaluation failed');

      // Populate summary counters
      document.getElementById('b-total').textContent = res.total_records;
      document.getElementById('b-good').textContent = res.good_count;
      document.getElementById('b-bad').textContent = res.bad_count;
      document.getElementById('b-rate').textContent = `${res.freshness_rate}%`;
      document.getElementById('b-conf').textContent = `${res.avg_confidence}%`;

      currentEnrichedCsv = res.csv_content;
      allBatchRecords = res.preview_data;

      downloadBtn.style.display = 'inline-flex';
      if (printAuditBtn) printAuditBtn.style.display = 'inline-flex';

      renderBatchTable('all');

      resultsArea.style.display = 'block';
      resultsArea.scrollIntoView({ behavior: 'smooth' });
    })
    .catch(err => {
      uploadPrompt.innerHTML = `<span style="color: #f43f5e">✕ Error: ${err.message}</span>`;
    });
  }

  downloadBtn.addEventListener('click', () => {
    if (!currentEnrichedCsv) return;
    const blob = new Blob([currentEnrichedCsv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'classified_produce_batch_enriched.csv';
    link.click();
  });
}

/* ==========================================================================
   Model Retrainer Trigger
   ========================================================================== */
function initRetrainer(button) {
  button.addEventListener('click', () => {
    if (!confirm('Retrain all 5 machine learning models and recalculate 5-fold cross validation benchmarks?')) return;

    const originalContent = button.innerHTML;
    button.disabled = true;
    button.innerHTML = `<span class="spinner"></span> Benchmarking Models...`;

    fetch('/api/retrain', {
      method: 'POST'
    })
    .then(res => res.json())
    .then(res => {
      if (res.success) {
        alert('Models retrained and benchmarked successfully! Reloading page...');
        window.location.reload();
      } else {
        alert('Error: ' + res.error);
        button.disabled = false;
        button.innerHTML = originalContent;
      }
    })
    .catch(err => {
      alert('Error: ' + err.message);
      button.disabled = false;
      button.innerHTML = originalContent;
    });
  });
}

/* ==========================================================================
   Lightbox Zoom for Saved Plots
   ========================================================================== */
function initImageLightbox() {
  const modal = document.getElementById('image-modal');
  const modalImg = document.getElementById('modal-img');
  const modalTitle = document.getElementById('modal-title');
  const closeBtn = document.getElementById('modal-close');

  if (!modal) return;

  document.querySelectorAll('.btn-zoom-plot').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const src = btn.dataset.img;
      const title = btn.dataset.title;
      modalImg.src = src;
      modalTitle.textContent = title;
      modal.classList.add('active');
    });
  });

  const closeModal = () => modal.classList.remove('active');
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });
}
