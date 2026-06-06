/* ===== Grace Distribution — interactions ===== */
document.addEventListener('DOMContentLoaded', function () {

  /* Year in footer */
  var yEl = document.getElementById('year');
  if (yEl) yEl.textContent = new Date().getFullYear();

  /* Mobile menu toggle */
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
      toggle.classList.toggle('open');
    });
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('open');
        toggle.classList.remove('open');
      });
    });
  }

  /* Header shadow on scroll */
  var header = document.getElementById('header');
  window.addEventListener('scroll', function () {
    if (header) header.classList.toggle('scrolled', window.scrollY > 20);
  });

  /* ===== Scroll animations (AOS) — same style as the Fuelup template ===== */
  // Auto-assign animation types to .reveal elements so each one animates in.
  document.querySelectorAll('.reveal').forEach(function (el) {
    if (el.hasAttribute('data-aos')) return;
    var anim = 'fade-up';
    if (el.classList.contains('about__media') || el.classList.contains('faq__media')) anim = 'fade-right';
    else if (el.classList.contains('contact__form-wrap')) anim = 'fade-left';
    el.setAttribute('data-aos', anim);
    var siblings = Array.prototype.slice.call(el.parentNode.children);
    var idx = siblings.indexOf(el);
    if (idx > 0) el.setAttribute('data-aos-delay', String((idx % 4) * 120));
  });

  if (window.AOS) {
    AOS.init({ duration: 800, easing: 'ease-out-cubic', once: true, offset: 80 });
  } else {
    document.documentElement.classList.add('no-aos');
  }

  /* ===== Hero slider ===== */
  (function () {
    var slides = document.querySelectorAll('.hero__slide');
    if (slides.length < 2) return;
    var cur = 0, timer;
    function show(n) {
      slides[cur].classList.remove('active');
      cur = (n + slides.length) % slides.length;
      slides[cur].classList.add('active');
    }
    function next() { show(cur + 1); }
    function prev() { show(cur - 1); }
    function auto() { timer = setInterval(next, 5000); }
    function reset() { clearInterval(timer); auto(); }
    var nb = document.getElementById('heroNext');
    var pb = document.getElementById('heroPrev');
    if (nb) nb.addEventListener('click', function () { next(); reset(); });
    if (pb) pb.addEventListener('click', function () { prev(); reset(); });
    auto();
  })();

  /* Animated stat counters */
  var counters = document.querySelectorAll('.counter__num');
  var counted = false;
  function runCounters() {
    if (counted) return;
    var statsSection = document.querySelector('.counters');
    if (!statsSection) return;
    var rect = statsSection.getBoundingClientRect();
    if (rect.top < window.innerHeight - 60) {
      counted = true;
      counters.forEach(function (c) {
        var target = parseInt(c.getAttribute('data-count'), 10) || 0;
        var current = 0;
        var step = Math.max(1, Math.ceil(target / 40));
        var timer = setInterval(function () {
          current += step;
          if (current >= target) { current = target; clearInterval(timer); }
          c.textContent = current;
        }, 30);
      });
    }
  }
  window.addEventListener('scroll', runCounters);
  runCounters();

  /* FAQ accordion */
  document.querySelectorAll('.acc__item').forEach(function (item) {
    var q = item.querySelector('.acc__q');
    q.addEventListener('click', function () {
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.acc__item').forEach(function (i) { i.classList.remove('open'); });
      if (!isOpen) item.classList.add('open');
    });
  });

  /* Clients logo marquee */
  (function () {
    var t1 = document.getElementById('clientTrack1');
    var t2 = document.getElementById('clientTrack2');
    if (!t1 || !t2) return;
    var TOTAL = 26;
    function pad(i) { return (i < 10 ? '0' : '') + i; }
    function tile(i) {
      var d = document.createElement('div');
      d.className = 'marquee__item';
      var img = document.createElement('img');
      img.src = 'images/clients/client-' + pad(i) + '.jpg';
      img.alt = 'Valued customer logo';
      img.loading = 'lazy';
      d.appendChild(img);
      return d;
    }
    function fill(track, from, to) {
      var arr = [];
      for (var i = from; i <= to; i++) arr.push(i);
      // duplicate the set so the loop is seamless
      arr.concat(arr).forEach(function (i) { track.appendChild(tile(i)); });
    }
    var mid = Math.ceil(TOTAL / 2);
    fill(t1, 1, mid);
    fill(t2, mid + 1, TOTAL);
  })();

  /* Newsletter subscribe -> WhatsApp */
  var subForm = document.getElementById('subForm');
  if (subForm) {
    subForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = subForm.email.value.trim();
      var text = 'Hello, I would like to subscribe for updates. My email: ' + encodeURIComponent(email);
      window.open('https://wa.me/923005895573?text=' + text, '_blank');
      subForm.reset();
    });
  }

  /* Contact form -> WhatsApp */
  var form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.name.value.trim();
      var phone = form.phone.value.trim();
      var qty = form.qty.value.trim();
      var message = form.message.value.trim();
      var text =
        '*New Enquiry — Grace Distribution*%0A' +
        '%0A*Name:* ' + encodeURIComponent(name) +
        '%0A*Phone:* ' + encodeURIComponent(phone) +
        (qty ? '%0A*Requirement:* ' + encodeURIComponent(qty) : '') +
        (message ? '%0A*Message:* ' + encodeURIComponent(message) : '');
      window.open('https://wa.me/923005895573?text=' + text, '_blank');
      form.reset();
    });
  }

});
