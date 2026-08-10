// ACBOSS — Flat Vector Graphic & Telemetry Logic with Interactive Motion & Auto Carousel

document.addEventListener('DOMContentLoaded', () => {
  initArchitectureInspector();
  initComfortSimulator();
  initProductGallery();
  initCard3DTiltEffects();
  initSleepCarousel();
});

/* -------------------------------------------------------------
 * 1. Auto-Playing Sleep Paradox Carousel
 * ------------------------------------------------------------- */
function initSleepCarousel() {
  const track = document.getElementById('carouselTrack');
  const slides = document.querySelectorAll('.carousel-slide');
  const dots = document.querySelectorAll('.carousel-dot');
  const prevBtn = document.getElementById('carouselPrev');
  const nextBtn = document.getElementById('carouselNext');
  const wrapper = document.querySelector('.carousel-wrapper');

  if (!track || !slides.length) return;

  let currentIndex = 0;
  let autoTimer = null;
  const slideCount = slides.length;

  function goToSlide(index) {
    if (index < 0) index = slideCount - 1;
    if (index >= slideCount) index = 0;

    currentIndex = index;
    track.style.transform = `translateX(-${currentIndex * 100}%)`;

    dots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx === currentIndex);
    });
  }

  function startAutoPlay() {
    stopAutoPlay();
    autoTimer = setInterval(() => {
      goToSlide(currentIndex + 1);
    }, 4000);
  }

  function stopAutoPlay() {
    if (autoTimer) {
      clearInterval(autoTimer);
      autoTimer = null;
    }
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      goToSlide(currentIndex - 1);
      startAutoPlay();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      goToSlide(currentIndex + 1);
      startAutoPlay();
    });
  }

  dots.forEach((dot, idx) => {
    dot.addEventListener('click', () => {
      goToSlide(idx);
      startAutoPlay();
    });
  });

  if (wrapper) {
    wrapper.addEventListener('mouseenter', stopAutoPlay);
    wrapper.addEventListener('mouseleave', startAutoPlay);
  }

  // Start auto-slide
  startAutoPlay();
}

/* -------------------------------------------------------------
 * 2. Architecture Component Inspector & Smooth Node Selection
 * ------------------------------------------------------------- */
const ARCH_DATA = {
  mcu: {
    title: "MCU",
    subtitle: "Dual-band Wi-Fi (5GHz & 2.4GHz) + Thread / Zigbee (802.15.4)",
    description: "The primary MCU executing local comfort algorithms. Runs deterministic real-time control loops without reliance on external cloud servers.",
    pinouts: [
      { pin: "GPIO 04", function: "IR_TX_PWM", status: "ACTIVE (38kHz Carrier)" },
      { pin: "GPIO 05", function: "IR_RX_LEARNER", status: "READY (Demodulated)" },
      { pin: "GPIO 08", function: "I2C_SDA (Climate Sensor)", status: "400 kHz Fast-Mode" },
      { pin: "GPIO 09", function: "I2C_SCL (Climate Sensor)", status: "Clock Synced" },
      { pin: "GPIO 18", function: "MMWAVE_RADAR_IN", status: "Interrupt Trigger" }
    ]
  },
  ble_proximity: {
    title: "BLE Mobile Proximity Sensing",
    subtitle: "Bluetooth Low Energy RSSI Beacon Engine",
    description: "Measures signal strength (RSSI) from your paired ACBOSS mobile app. Detects when you enter or leave the room, triggering instant personalized cooling presets.",
    pinouts: [
      { pin: "BLE_ANT", function: "2.4GHz Bluetooth Antenna", status: "SCANNING (-45 dBm)" },
      { pin: "BEACON_ID", function: "Encrypted Mobile UUID", status: "PAIRED (In Range)" },
      { pin: "RSSI_IN", function: "Proximity Distance Filter", status: "< 3.5 Meters" }
    ]
  },
  climate_sensor: {
    title: "Precision Climate Sensor",
    subtitle: "Ultra-High Precision Temp (±0.1°C) & Relative Humidity (±1.5% RH)",
    description: "Monitors microscopic shifts in thermal comfort, dew point, and heat index to compute the PMV (Predicted Mean Vote) comfort metric locally.",
    pinouts: [
      { pin: "VDD", function: "3.3V Power", status: "Regulated Low-Noise" },
      { pin: "SCL", function: "I2C Clock Line", status: "Hardware Pull-up" },
      { pin: "SDA", function: "I2C Data Line", status: "Bi-directional" },
      { pin: "ALERT", function: "Comfort Boundary Alert", status: "Edge Triggered" }
    ]
  },
  mmwave: {
    title: "Human Presence Radar",
    subtitle: "24GHz mmWave Radar Array",
    description: "Detects micro-movements such as breathing during sleep. Adjusts cooling profiles automatically when occupants enter or leave the room.",
    pinouts: [
      { pin: "OUT", function: "Presence Digital Signal", status: "HIGH (Occupied)" },
      { pin: "TX/RX", function: "24GHz Radar Transceiver", status: "Continuous Sensing" },
      { pin: "VCC", function: "5V Power", status: "Isolated Rail" }
    ]
  },
  ir_array: {
    title: "IR Transmitter & Receiver",
    subtitle: "Wide-Angle 360° IR Emitter Array + Signal Learning Demodulator",
    description: "Learns existing Split AC remote control protocols (Daikin, Voltas, LG, Mitsubishi, Panasonic) and transmits precise micro-adjustments.",
    pinouts: [
      { pin: "TX_1..4", function: "Quad IR LED Array", status: "Pulsing Carrier" },
      { pin: "RX_IN", function: "38kHz Phototransistor", status: "Listening Mode" },
      { pin: "MOD_EN", function: "Modulation Enable", status: "Hardware Gated" }
    ]
  }
};

function initArchitectureInspector() {
  const nodes = document.querySelectorAll('.arch-node');
  const inspectorPanel = document.querySelector('.arch-inspector');
  const titleEl = document.getElementById('inspectorTitle');
  const subEl = document.getElementById('inspectorSub');
  const descEl = document.getElementById('inspectorDesc');
  const tableBody = document.getElementById('inspectorPins');

  if (!nodes.length) return;

  function selectNode(key) {
    const data = ARCH_DATA[key];
    if (!data) return;

    nodes.forEach((node) => {
      const selected = node.dataset.node === key;
      node.classList.toggle('active', selected);
      node.setAttribute('aria-pressed', String(selected));
    });

    if (inspectorPanel) {
      inspectorPanel.style.transform = 'scale(0.98)';
      inspectorPanel.style.opacity = '0.8';
      setTimeout(() => {
        inspectorPanel.style.transform = 'scale(1)';
        inspectorPanel.style.opacity = '1';
      }, 100);
    }

    if (titleEl) titleEl.textContent = data.title;
    if (subEl) subEl.textContent = data.subtitle;
    if (descEl) descEl.textContent = data.description;

    if (tableBody) {
      tableBody.innerHTML = data.pinouts.map(p => `
        <tr style="transition: background 0.2s ease;">
          <td style="color: #b45309; font-weight: 800;">${p.pin}</td>
          <td>${p.function}</td>
          <td style="color: #2e7d32; font-weight: 800;">${p.status}</td>
        </tr>
      `).join('');
    }
  }

  nodes.forEach(node => {
    node.addEventListener('click', () => {
      selectNode(node.dataset.node);
    });
  });

  // Default selection
  selectNode('mcu');
}

/* -------------------------------------------------------------
 * 3. Autopilot vs Traditional AC Comfort Simulator (Animated Canvas with Flowing Particles)
 * ------------------------------------------------------------- */
function initComfortSimulator() {
  const canvas = document.getElementById('simCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const outsideSlider = document.getElementById('sliderOutside');
  const targetSlider = document.getElementById('sliderTarget');
  const outsideValEl = document.getElementById('valOutside');
  const targetValEl = document.getElementById('valTarget');

  let animationFrame;
  let phaseOffset = 0;
  let particles = [];

  for (let i = 0; i < 8; i++) {
    particles.push({
      x: Math.random() * 600,
      speed: 1.5 + Math.random() * 1.5
    });
  }

  function resizeCanvas() {
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * window.devicePixelRatio;
    canvas.height = rect.height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }

  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  function draw() {
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    
    const outsideTemp = parseFloat(outsideSlider ? outsideSlider.value : 34);
    const targetTemp = parseFloat(targetSlider ? targetSlider.value : 23.5);

    if (outsideValEl) outsideValEl.textContent = `${outsideTemp}°C`;
    if (targetValEl) targetValEl.textContent = `${targetTemp}°C`;

    ctx.clearRect(0, 0, width, height);

    // Draw Vector Light Grid
    ctx.strokeStyle = '#e0f2f1';
    ctx.lineWidth = 1.5;
    for (let x = 0; x < width; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y < height; y += 35) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Target Temperature Reference Line
    const targetY = height / 2;
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 2;
    ctx.setLineDash([8, 6]);
    ctx.beginPath();
    ctx.moveTo(0, targetY);
    ctx.lineTo(width, targetY);
    ctx.stroke();
    ctx.setLineDash([]);

    // Label Target
    ctx.fillStyle = '#b45309';
    ctx.font = 'bold 12px JetBrains Mono';
    ctx.fillText(`TARGET: ${targetTemp.toFixed(1)}°C`, 10, targetY - 8);

    if (!reduceMotion) phaseOffset += 0.03;

    // 1. Traditional AC Curve
    ctx.strokeStyle = '#ff6e40';
    ctx.lineWidth = 3;
    ctx.beginPath();
    for (let x = 0; x < width; x++) {
      const freq = 0.015;
      const amp = 45 + (outsideTemp - 30) * 3;
      const saw = Math.sin(x * freq + phaseOffset) + 0.3 * Math.sin(2 * (x * freq + phaseOffset));
      const y = targetY + saw * amp;
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // 2. ACBOSS Autopilot Curve
    ctx.strokeStyle = '#00897b';
    ctx.lineWidth = 4;
    ctx.beginPath();
    for (let x = 0; x < width; x++) {
      const freq = 0.02;
      const amp = 6 + (outsideTemp - 30) * 0.5;
      const smooth = Math.sin(x * freq + phaseOffset * 1.5) * amp;
      const y = targetY + smooth;
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // 3. Flowing Pulse Particles
    particles.forEach(p => {
      if (!reduceMotion) p.x += p.speed;
      if (p.x > width) p.x = 0;

      const freq = 0.02;
      const amp = 6 + (outsideTemp - 30) * 0.5;
      const smooth = Math.sin(p.x * freq + phaseOffset * 1.5) * amp;
      const pY = targetY + smooth;

      ctx.fillStyle = '#ff6e40';
      ctx.beginPath();
      ctx.arc(p.x, pY, 4, 0, Math.PI * 2);
      ctx.fill();
    });

    if (!reduceMotion) animationFrame = requestAnimationFrame(draw);
  }

  if (reduceMotion) {
    [outsideSlider, targetSlider].forEach((slider) => {
      if (slider) slider.addEventListener('input', draw);
    });
  }

  draw();
}

/* -------------------------------------------------------------
 * 4. Interactive Card Mouseover 3D Tilt / Parallax Effect
 * ------------------------------------------------------------- */
function initCard3DTiltEffects() {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  const cards = document.querySelectorAll('.hw-card, .vector-stage-card, .story-card-grid');

  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((y - centerY) / centerY) * -4;
      const rotateY = ((x - centerX) / centerX) * 4;

      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
    });
  });
}

function initProductGallery() {
  const image = document.getElementById('mainProductImg');
  const buttons = document.querySelectorAll('[data-product-src]');

  if (!image || !buttons.length) return;

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      image.src = button.dataset.productSrc;
      image.alt = button.dataset.productAlt;

      buttons.forEach((item) => {
        const selected = item === button;
        item.classList.toggle('active', selected);
        item.setAttribute('aria-pressed', String(selected));
      });
    });
  });
}
