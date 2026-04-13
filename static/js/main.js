/**
 * Ma Mangala Travels — Main JavaScript
 * Handles: Navbar scroll, particles, AOS, price calculator, mobile menu, forms
 */

/* ============================================================
   NAVBAR — scroll shrink + mobile toggle
   ============================================================ */
document.addEventListener('DOMContentLoaded', function () {

  const navbar = document.querySelector('.navbar');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  // ── Scroll effect ──
  window.addEventListener('scroll', () => {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  // ── Mobile toggle ──
  if (navToggle) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }

  // ── Close on link click ──
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });

  // ── Active nav link ──
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ── Init AOS ──
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 700,
      once: true,
      easing: 'ease-out-cubic',
      offset: 60,
    });
  }

  // ── Generate particles ──
  generateParticles();

  // ── Hero bg parallax ──
  heroParallax();

  // ── Init price calculator ──
  initPriceCalculator();

  // ── Counter animation ──
  initCounters();

  // ── Gallery lightbox ──
  initGalleryLightbox();

});


/* ============================================================
   FLOATING PARTICLES
   ============================================================ */
function generateParticles() {
  const container = document.querySelector('.hero-particles');
  if (!container) return;

  const count = 30;
  for (let i = 0; i < count; i++) {
    const p = document.createElement('div');
    p.classList.add('particle');
    p.style.cssText = `
      left: ${Math.random() * 100}%;
      top: ${60 + Math.random() * 40}%;
      animation-delay: ${Math.random() * 6}s;
      animation-duration: ${4 + Math.random() * 4}s;
      width: ${2 + Math.random() * 3}px;
      height: ${2 + Math.random() * 3}px;
      opacity: ${0.3 + Math.random() * 0.7};
    `;
    container.appendChild(p);
  }
}


/* ============================================================
   HERO PARALLAX
   ============================================================ */
function heroParallax() {
  const heroBg = document.querySelector('.hero-bg');
  if (!heroBg) return;

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    heroBg.style.transform = `scale(1.05) translateY(${scrollY * 0.3}px)`;
  }, { passive: true });
}


/* ============================================================
   PRICE CALCULATOR
   ============================================================ */
// Pricing rates (mirrored from views.py — kept in sync)
const PRICE_TABLE = {
  hatchback: { per_km: 12, per_day: 300 },
  sedan:     { per_km: 16, per_day: 400 },
  suv:       { per_km: 22, per_day: 500 },
};

const DESTINATION_DISTANCES = {
  'puri': 60,
  'chilika lake': 110,
  'chilika': 110,
  'bhubaneswar': 10,
  'konark': 65,
};

function getEstimatedDistance(dest) {
  if (!dest) return 60;
  const lower = dest.toLowerCase().trim();
  for (const key in DESTINATION_DISTANCES) {
    if (lower.includes(key)) return DESTINATION_DISTANCES[key];
  }
  return 60; // default
}

function calculatePrice(carType, days, destination) {
  const rates = PRICE_TABLE[carType] || PRICE_TABLE.hatchback;
  const distance = getEstimatedDistance(destination);
  const distanceCharge = distance * rates.per_km;
  const dayCharge = days * rates.per_day;
  const total = distanceCharge + dayCharge;
  return { total, distanceCharge, dayCharge, distance, rates };
}

function formatINR(amount) {
  return '₹' + Math.round(amount).toLocaleString('en-IN');
}

function updatePriceDisplay() {
  const carTypeEl = document.getElementById('id_car_type');
  const daysEl = document.getElementById('id_days');
  const destEl = document.getElementById('id_destination');
  const priceEl = document.getElementById('id_estimated_price');
  const displayEl = document.getElementById('priceDisplay');
  const breakdownEl = document.getElementById('priceBreakdown');

  if (!carTypeEl || !daysEl || !displayEl) return;

  const carType = carTypeEl.value || 'hatchback';
  const days = parseInt(daysEl.value) || 1;
  const destination = destEl ? destEl.value : '';

  const result = calculatePrice(carType, days, destination);

  // Update display
  displayEl.textContent = formatINR(result.total);

  // Update hidden field for form submission
  if (priceEl) priceEl.value = result.total;

  // Update breakdown
  if (breakdownEl) {
    breakdownEl.innerHTML = `
      <span>📍 Distance: ~${result.distance} km × ${formatINR(result.rates.per_km)}/km = <strong>${formatINR(result.distanceCharge)}</strong></span><br>
      <span>📅 ${days} day(s) × ${formatINR(result.rates.per_day)}/day = <strong>${formatINR(result.dayCharge)}</strong></span>
    `;
    breakdownEl.classList.add('visible');
  }
}

function initPriceCalculator() {
  const fields = ['id_car_type', 'id_days', 'id_destination'];
  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('change', updatePriceDisplay);
      el.addEventListener('input', updatePriceDisplay);
      el.addEventListener('keyup', updatePriceDisplay);
    }
  });

  // Initial calculation
  updatePriceDisplay();
}


/* ============================================================
   COUNTER ANIMATION
   ============================================================ */
function initCounters() {
  const counters = document.querySelectorAll('.stat-number[data-target]');
  if (!counters.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 }); // lowered from 0.5 for better mobile triggering

  counters.forEach(counter => {
    // If element is already in viewport (above-fold), run immediately
    const rect = counter.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      setTimeout(() => animateCounter(counter), 400);
    } else {
      observer.observe(counter);
    }
  });
}

function animateCounter(el) {
  const target = parseInt(el.getAttribute('data-target'));
  const suffix = el.getAttribute('data-suffix') || '';
  const duration = 1500;
  const step = target / (duration / 16);
  let current = 0;

  const timer = setInterval(() => {
    current += step;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = Math.floor(current) + suffix;
  }, 16);
}


/* ============================================================
   GALLERY LIGHTBOX
   ============================================================ */
function initGalleryLightbox() {
  const galleryItems = document.querySelectorAll('.gallery-item');
  if (!galleryItems.length) return;

  // Create lightbox
  const lb = document.createElement('div');
  lb.id = 'lightbox';
  lb.style.cssText = `
    display:none; position:fixed; inset:0; z-index:9999;
    background:rgba(0,0,0,0.92); align-items:center;
    justify-content:center; cursor:pointer;
    backdrop-filter: blur(12px);
  `;
  lb.innerHTML = `
    <button id="lbClose" style="position:absolute;top:1.5rem;right:1.5rem;background:rgba(212,175,55,0.2);border:1px solid rgba(212,175,55,0.4);color:#D4AF37;width:44px;height:44px;border-radius:50%;cursor:pointer;font-size:1.25rem;">✕</button>
    <img id="lbImg" style="max-width:90%;max-height:85vh;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,0.8);" />
    <p id="lbCaption" style="position:absolute;bottom:2rem;color:#ccc;font-size:0.9rem;text-align:center;"></p>
  `;
  document.body.appendChild(lb);

  galleryItems.forEach(item => {
    item.addEventListener('click', () => {
      const img = item.querySelector('img');
      const caption = item.querySelector('.gallery-caption');
      document.getElementById('lbImg').src = img.src;
      document.getElementById('lbCaption').textContent = caption ? caption.textContent : '';
      lb.style.display = 'flex';
    });
  });

  lb.addEventListener('click', (e) => {
    if (e.target === lb || e.target.id === 'lbClose') {
      lb.style.display = 'none';
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') lb.style.display = 'none';
  });
}


/* ============================================================
   BOOKING FORM — auto-dismiss messages
   ============================================================ */
setTimeout(() => {
  document.querySelectorAll('.alert').forEach(alert => {
    alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-10px)';
    setTimeout(() => alert.remove(), 600);
  });
}, 5000);


/* ============================================================
   SMOOTH REVEAL on scroll (fallback if AOS not loaded)
   ============================================================ */
if (typeof AOS === 'undefined') {
  const style = document.createElement('style');
  style.textContent = `.reveal { opacity:0; transform:translateY(30px); transition:opacity 0.7s ease, transform 0.7s ease; } .reveal.visible { opacity:1; transform:none; }`;
  document.head.appendChild(style);

  document.querySelectorAll('[data-aos]').forEach(el => el.classList.add('reveal'));

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObserver.unobserve(e.target); }});
  }, { threshold: 0.1 });

  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
}
