// ═══════════════════════════════════════════════
// LUMIÈRE HOTEL — Main JavaScript
// ═══════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', function () {

  // ── Navbar scroll behavior
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    const updateNav = () => {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
        navbar.classList.remove('transparent');
      } else {
        navbar.classList.remove('scrolled');
        if (navbar.dataset.transparent === 'true') navbar.classList.add('transparent');
      }
    };
    window.addEventListener('scroll', updateNav, { passive: true });
    updateNav();
  }

  // ── Mobile menu
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
    });
  }

  // ── Scroll reveal
  const reveals = document.querySelectorAll('.reveal');
  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) {
        setTimeout(() => e.target.classList.add('visible'), i * 80);
        revealObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  reveals.forEach(el => revealObs.observe(el));

  // ── Auto-dismiss alerts
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 4500);
  });

  // ── Lightbox
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  if (lightbox) {
    document.querySelectorAll('[data-lightbox]').forEach(item => {
      item.addEventListener('click', () => {
        lightboxImg.src = item.dataset.src || item.querySelector('img')?.src;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    });
    document.querySelector('.lightbox-close')?.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(); });
  }
  function closeLightbox() {
    if (lightbox) { lightbox.classList.remove('active'); document.body.style.overflow = ''; }
  }

  // ── Booking bar date validation
  const checkIn = document.getElementById('id_check_in') || document.querySelector('[name="check_in"]');
  const checkOut = document.getElementById('id_check_out') || document.querySelector('[name="check_out"]');
  if (checkIn) {
    const today = new Date().toISOString().split('T')[0];
    checkIn.min = today;
    checkIn.addEventListener('change', () => {
      if (checkOut) {
        const nextDay = new Date(checkIn.value);
        nextDay.setDate(nextDay.getDate() + 1);
        checkOut.min = nextDay.toISOString().split('T')[0];
        if (checkOut.value && checkOut.value <= checkIn.value) {
          checkOut.value = nextDay.toISOString().split('T')[0];
        }
      }
    });
  }

  // ── Gallery filter chips
  document.querySelectorAll('.chip[data-filter]').forEach(chip => {
    chip.addEventListener('click', function () {
      document.querySelectorAll('.chip[data-filter]').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      const filter = this.dataset.filter;
      document.querySelectorAll('.gallery-item[data-category]').forEach(item => {
        if (filter === 'all' || item.dataset.category === filter) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  // ── Tab navigation
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const target = this.dataset.tab;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.style.display = 'none');
      this.classList.add('active');
      const pane = document.getElementById(target);
      if (pane) pane.style.display = 'block';
    });
  });

  // ── Payment card formatting
  const cardInput = document.querySelector('[name="card_number"]');
  if (cardInput) {
    cardInput.addEventListener('input', function () {
      let val = this.value.replace(/\D/g, '').substring(0, 16);
      this.value = val.replace(/(.{4})/g, '$1 ').trim();
    });
    const expiry = document.querySelector('[name="expiry"]');
    if (expiry) {
      expiry.addEventListener('input', function () {
        let val = this.value.replace(/\D/g, '').substring(0, 4);
        if (val.length > 2) val = val.substring(0, 2) + '/' + val.substring(2);
        this.value = val;
      });
    }
  }

  // ── Payment method selection
  document.querySelectorAll('.payment-method-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.payment-method-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const methodInput = document.querySelector('[name="method"]');
      if (methodInput) methodInput.value = this.dataset.method;
    });
  });

  // ── Booking price preview
  const bookingCheckIn = document.querySelector('input[name="check_in"]');
  const bookingCheckOut = document.querySelector('input[name="check_out"]');
  const pricePreview = document.getElementById('price-preview');
  const nightsDisplay = document.getElementById('nights-display');
  const pricePerNight = parseFloat(document.querySelector('[data-price]')?.dataset.price || 0);

  function updatePricePreview() {
    if (!bookingCheckIn || !bookingCheckOut || !pricePreview) return;
    const ci = new Date(bookingCheckIn.value);
    const co = new Date(bookingCheckOut.value);
    if (ci && co && co > ci) {
      const nights = Math.ceil((co - ci) / (1000 * 60 * 60 * 24));
      const subtotal = nights * pricePerNight;
      const taxes = subtotal * 0.15;
      const total = subtotal + taxes;
      if (nightsDisplay) nightsDisplay.textContent = nights + ' night' + (nights > 1 ? 's' : '');
      pricePreview.innerHTML = `
        <div class="booking-detail-row"><span class="label">Room (${nights} nights)</span><span class="value">$${subtotal.toFixed(2)}</span></div>
        <div class="booking-detail-row"><span class="label">Taxes & fees (15%)</span><span class="value">$${taxes.toFixed(2)}</span></div>
        <div class="booking-total-row"><span class="label">Total</span><span class="value">$${total.toFixed(2)}</span></div>`;
    }
  }

  if (bookingCheckIn) bookingCheckIn.addEventListener('change', updatePricePreview);
  if (bookingCheckOut) bookingCheckOut.addEventListener('change', updatePricePreview);

  // ── Image slider for room detail
  const sliderTrack = document.querySelector('.slider-track');
  if (sliderTrack) {
    const slides = sliderTrack.querySelectorAll('.slide');
    let current = 0;
    const go = (idx) => {
      current = (idx + slides.length) % slides.length;
      sliderTrack.style.transform = `translateX(-${current * 100}%)`;
      document.querySelectorAll('.slider-dot').forEach((d, i) => d.classList.toggle('active', i === current));
    };
    document.querySelector('.slider-prev')?.addEventListener('click', () => go(current - 1));
    document.querySelector('.slider-next')?.addEventListener('click', () => go(current + 1));
    document.querySelectorAll('.slider-dot').forEach((dot, i) => dot.addEventListener('click', () => go(i)));
  }

  // ── Counter animation
  document.querySelectorAll('.count-up').forEach(el => {
    const target = parseInt(el.dataset.target);
    const obs = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        let start = 0;
        const step = target / 60;
        const timer = setInterval(() => {
          start += step;
          if (start >= target) { el.textContent = target + (el.dataset.suffix || ''); clearInterval(timer); }
          else el.textContent = Math.floor(start) + (el.dataset.suffix || '');
        }, 25);
        obs.disconnect();
      }
    });
    obs.observe(el);
  });

});
