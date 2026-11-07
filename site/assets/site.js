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

  // Google Analytics, only after the visitor allows it. The ID comes from <meta name="ga-id">,
  // which pages.py writes only when GA_ID is set. Nothing loads before consent.
  var gaMeta = document.querySelector('meta[name="ga-id"]');
  var GA = gaMeta && gaMeta.content;
  if (GA) {
    var KEY = 'st-analytics';
    var store = {
      get: function () { try { return localStorage.getItem(KEY); } catch (e) { return null; } },
      set: function (v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
    };
    var loaded = false;
    window.dataLayer = window.dataLayer || [];
    var gtag = function () { window.dataLayer.push(arguments); };
    var track = function (name, params) { if (loaded) gtag('event', name, params || {}); };
    var loadGA = function () {
      if (loaded) return;
      loaded = true;
      var sc = document.createElement('script');
      sc.async = true;
      sc.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA);
      document.head.appendChild(sc);
      gtag('js', new Date());
      gtag('config', GA, { allow_google_signals: false, allow_ad_personalization_signals: false });
    };
    var clearGA = function () {
      document.cookie.split(';').forEach(function (c) {
        var n = c.split('=')[0].trim();
        if (/^_ga/.test(n)) {
          document.cookie = n + '=; Max-Age=0; path=/';
          document.cookie = n + '=; Max-Age=0; path=/; domain=.' + location.hostname.replace(/^www\./, '');
        }
      });
    };
    var banner = null;
    var showBanner = function () {
      if (banner) return;
      banner = document.createElement('div');
      banner.className = 'cookie';
      banner.setAttribute('role', 'dialog');
      banner.setAttribute('aria-label', 'Cookie choice');
      banner.innerHTML = '<p>We would like to use Google Analytics cookies to count visits and improve this website. ' +
        'No advertising. Please allow only if you are 18 or older. <a href="privacy.html">Privacy Notice</a></p>' +
        '<div class="btns"><button type="button" class="btn btn-red" data-c="yes">Allow</button>' +
        '<button type="button" class="btn btn-ghost" data-c="no">Decline</button></div>';
      banner.addEventListener('click', function (e) {
        var c = e.target.getAttribute('data-c');
        if (!c) return;
        store.set(c);
        if (c === 'yes') loadGA();
        else if (loaded) { clearGA(); location.reload(); return; }
        else clearGA();
        banner.remove();
        banner = null;
      });
      document.body.appendChild(banner);
    };
    var choice = store.get();
    if (choice === 'yes') loadGA();
    else if (choice !== 'no') showBanner();
    var cs = $('cookieSettings');
    if (cs) cs.addEventListener('click', showBanner);

    // Enquiry events: calls, WhatsApp, email and Instagram clicks
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (!a) return;
      var h = a.getAttribute('href');
      if (h.indexOf('tel:') === 0) track('click_call');
      else if (h.indexOf('wa.me') !== -1) track('click_whatsapp');
      else if (h.indexOf('mailto:') === 0) track('click_email');
      else if (h.indexOf('instagram.com') !== -1) track('click_instagram');
    });
    window.stTrack = track;
  }

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
    if (window.stTrack) window.stTrack('generate_lead', { method: 'whatsapp_form' });
    window.open(url, '_blank', 'noopener');
  });
})();
