(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Banner slider: changes on its own every few seconds. It holds still only while a keyboard
  // user is tabbing through it. Reduced-motion users get instant swaps.
  var slidesBox = $('slides');
  if (slidesBox) {
    var slides = slidesBox.querySelectorAll('.slide');
    var cur = 0, timer = null, DELAY = 5000, held = false;
    var stop = function () { clearInterval(timer); };
    var start = function () {
      stop();
      if (held || document.hidden) return;
      timer = setInterval(function () { go(cur + 1); }, DELAY);
    };
    var go = function (n) {
      slidesBox.parentNode.classList.add('moved');
      slides[cur].classList.remove('active');
      cur = (n + slides.length) % slides.length;
      slides[cur].classList.add('active');
      start();
    };
    $('slNext').addEventListener('click', function () { go(cur + 1); });
    $('slPrev').addEventListener('click', function () { go(cur - 1); });
    var box = slidesBox.parentNode;
    // Only keyboard focus holds the slider; a mouse click on an arrow keeps it moving
    box.addEventListener('focusin', function (e) {
      if (e.target.matches && e.target.matches(':focus-visible')) { held = true; stop(); }
    });
    box.addEventListener('focusout', function () { if (held) { held = false; start(); } });
    document.addEventListener('visibilitychange', start);
    var x0 = null;
    slidesBox.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    slidesBox.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) go(cur + (dx < 0 ? 1 : -1));
      x0 = null;
    });
    if (document.readyState === 'complete') start();
    else window.addEventListener('load', start);
  }

  // Gentle fade-in; content stays visible if this is unsupported
  // Only items below the first screen fade in, so nothing visible on load is restyled
  var fades = document.querySelectorAll('.fade-in');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('fade');
        e.target.style.transitionDelay = '60ms';
        requestAnimationFrame(function () { requestAnimationFrame(function () { e.target.classList.add('in'); }); });
        io.unobserve(e.target);
      });
    }, { threshold: 0.05, rootMargin: '0px 0px -40px 0px' });
    fades.forEach(function (el) { io.observe(el); });
  }

  var yr = $('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // Header shadow and back-to-top
  var hdr = $('hdr'), toTop = $('toTop');
  window.addEventListener('scroll', function () {
    hdr.classList.toggle('shadow', window.scrollY > 10);
    if (toTop) toTop.classList.toggle('show', window.scrollY > 600);
  }, { passive: true });

  // Mobile menu
  var mnav = $('mnav'), burger = $('burger');
  var setMenu = function (open) {
    mnav.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
  };
  burger.addEventListener('click', function () { setMenu(!mnav.classList.contains('open')); });
  mnav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && mnav.classList.contains('open')) { setMenu(false); burger.focus(); }
  });

  // Active nav link on the home page
  var links = document.querySelectorAll('nav.main a:not(.btn)');
  var secs = ['home', 'about', 'courses', 'gallery', 'reviews', 'faq', 'contact'].map($).filter(Boolean);
  if (secs.length) window.addEventListener('scroll', function () {
    var c = 'home';
    secs.forEach(function (s) { if (s.getBoundingClientRect().top < 120) c = s.id; });
    links.forEach(function (l) {
      var on = l.getAttribute('href') === '#' + c;
      l.classList.toggle('active', on);
      if (on) l.setAttribute('aria-current', 'true'); else l.removeAttribute('aria-current');
    });
  }, { passive: true });

  // Google Map loads only when the visitor asks for it
  var mapBtn = $('mapLoad');
  if (mapBtn) mapBtn.addEventListener('click', function () {
    var f = document.createElement('iframe');
    f.title = 'Smart Tutorials location on Google Maps';
    f.loading = 'lazy';
    f.referrerPolicy = 'no-referrer-when-downgrade';
    f.src = mapBtn.getAttribute('data-src');
    var box = $('mapBox');
    box.innerHTML = '';
    box.appendChild(f);
  });

  // Enquiry form: builds a WhatsApp message. Nothing is stored or sent by this website.
  var form = $('enqForm');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var val = function (id) { return $(id).value.trim(); };
    var mark = function (id, bad) {
      var el = $(id), msg = $(id + 'Err');
      el.classList.toggle('err', bad);
      el.setAttribute('aria-invalid', String(bad));
      msg.classList.toggle('show', bad);
      return !bad;
    };
    var phone = val('fPhone').replace(/[\s-]/g, '').replace(/^(\+?91|0)/, '');
    var ok = [
      mark('fName', val('fName').length < 2),
      mark('fPhone', !/^[6-9]\d{9}$/.test(phone)),
      mark('fConsent', !$('fConsent').checked)
    ];
    if (ok.indexOf(false) !== -1) {
      form.querySelector('[aria-invalid="true"]').focus();
      return;
    }
    var msg = 'Hi Smart Tutorials, I would like to book a free demo class.\n' +
      'Parent/guardian: ' + val('fName') + '\nPhone: ' + phone +
      (val('fClass') ? '\nClass: ' + val('fClass') : '') +
      (val('fBoard') ? '\nBoard: ' + val('fBoard') : '') +
      (val('fMsg') ? '\nMessage: ' + val('fMsg') : '');
    var url = 'https://wa.me/919731045709?text=' + encodeURIComponent(msg);
    $('waSend').href = url;
    form.hidden = true;
    var done = $('formOk');
    done.classList.add('show');
    done.focus();
    window.open(url, '_blank', 'noopener');
  });
})();
