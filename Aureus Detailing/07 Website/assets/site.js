/* Aureus v4 "The Reveal": film controller, hero HUD, section motion, package and reel enhancements.
   Replaces scrub.js. Runs after app.js (which renders the packages and owns the booking engine).
   Nothing here needs a click, drag or hover to play: the reveal plays once on its own, then scroll drives the film. */
(function () {
  'use strict';

  var REVEAL_END = 4.9, INTRO_RATE = 1.75, HUD_AT = 3.4, HUD_FAILSAFE_MS = 2600, SMOOTH_TAU = 0.09, COMPACT_AT = 0.10;
  var FILM_SPAN = 10.09;                    // seconds of film covered by the pinned scroll (4.9 s to 14.99 s)
  var CH2_AT = 0.20, CH3_AT = 0.62;         // chapter counter switches
  var SESSION_KEY = 'aureus-intro';

  var html = document.documentElement, win = window;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var conn = navigator.connection || {};
  var gsap = win.gsap, ScrollTrigger = win.ScrollTrigger;

  var isStatic = html.classList.contains('static') || !!conn.saveData || /2g/.test(conn.effectiveType || '') || !gsap || !ScrollTrigger;
  if (isStatic) { html.classList.remove('motion', 'pre', 'seen'); html.classList.add('static'); }

  var hero = $('#hero'), nav = $('#nav'), navLinks = $('#nav-links'), navToggle = $('.nav-toggle');
  if (!hero || !nav) { win.__aureusReady = true; return; }
  var phoneMq = win.matchMedia('(max-width: 860px)');

  // cubic-bezier eases, the same curves as the CSS tokens
  function bez(x1, y1, x2, y2) {
    function f(a, b, u) { var v = 1 - u; return 3 * v * v * u * a + 3 * v * u * u * b + u * u * u; }
    function df(a, b, u) { var v = 1 - u; return 3 * v * v * a + 6 * v * u * (b - a) + 3 * u * u * (1 - b); }
    return function (t) {
      if (t <= 0) return 0; if (t >= 1) return 1;
      var u = t, i, d;
      for (i = 0; i < 6; i++) { d = df(x1, x2, u); if (Math.abs(d) < 1e-6) break; u = clamp(u - (f(x1, x2, u) - t) / d, 0, 1); }
      return f(y1, y2, u);
    };
  }
  var E_OUT = bez(0.16, 1, 0.3, 1), E_INOUT = bez(0.65, 0, 0.35, 1), E_IN = bez(0.5, 0, 0.75, 0);

  // ---------- packages: whole-card selection and the accordion wrapper ----------
  function enhancePacks() {
    var phonePk = win.matchMedia('(max-width: 900px)');
    var cards = $$('#packs .pack');
    function sync(card, pick) {
      var on = card.dataset.selected === 'true';
      pick.setAttribute('aria-pressed', on);
      if (phonePk.matches) pick.setAttribute('aria-expanded', on); else pick.removeAttribute('aria-expanded');
    }
    cards.forEach(function (card) {
      if ($('.pack-pick', card)) return;
      var id = card.dataset.id, name = ($('h3', card) || {}).textContent || id;
      var body = document.createElement('div'), inner = document.createElement('div');
      body.className = 'pack-body'; body.appendChild(inner);
      [$('.pack-list', card), $('.pack-extras', card), $('[data-book]', card)].forEach(function (el) { if (el) inner.appendChild(el); });
      card.appendChild(body);
      var pick = document.createElement('button');
      pick.type = 'button'; pick.className = 'pack-pick'; pick.setAttribute('aria-label', 'Select ' + name + ' package');
      card.insertBefore(pick, card.firstChild);
      pick.addEventListener('click', function () {
        var radio = $('input[name="pack-dock"][value="' + id + '"]');
        if (!radio) return;
        radio.checked = true;
        radio.dispatchEvent(new Event('change', { bubbles: true }));   // app.js listens on document
      });
      sync(card, pick);
      new MutationObserver(function () { sync(card, pick); }).observe(card, { attributes: true, attributeFilter: ['data-selected'] });
    });
    var onMq = function () { cards.forEach(function (c) { var p = $('.pack-pick', c); if (p) sync(c, p); }); };
    if (phonePk.addEventListener) phonePk.addEventListener('change', onMq);
  }

  // ---------- V06: prices roll when they change ----------
  function priceRolls() {
    $$('[data-card-price], #dock-price, #sum-total').forEach(function (el) {
      var num = function () { return parseInt(el.textContent.replace(/[^\d]/g, ''), 10) || 0; };
      var last = num();
      el.addEventListener('animationend', function () { el.classList.remove('roll-up', 'roll-down'); });
      new MutationObserver(function () {
        var now = num(); if (now === last) return;
        var up = now > last; last = now;
        if (isStatic) return;
        el.classList.remove('roll-up', 'roll-down'); void el.offsetWidth;
        el.classList.add(up ? 'roll-up' : 'roll-down');
      }).observe(el, { childList: true, characterData: true, subtree: true });
    });
  }

  // ---------- V11: team reel ----------
  function reel() {
    var fig = $('#reel'); if (!fig) return;
    var vids = $$('video', fig), ticks = $$('.reel-ticks i', fig), btn = $('.reel-toggle', fig), nameEl = $('#reel-name'), idxEl = $('#reel-idx');
    var i = 0, auto = !isStatic, visible = false, raf = 0;
    function poster(k) { var v = vids[k]; if (v && !v.poster && v.dataset.poster) v.poster = v.dataset.poster; }
    function ui() { fig.dataset.playing = auto; btn.setAttribute('aria-label', auto ? 'Pause team footage' : 'Play team footage'); }
    function paint() {
      raf = 0; var v = vids[i];
      ticks[i].style.setProperty('--p', v.duration ? clamp(v.currentTime / v.duration, 0, 1).toFixed(3) : 0);
      if (!v.paused && !v.ended) raf = requestAnimationFrame(paint);
    }
    function show(k) {
      i = k; poster(k); poster((k + 1) % vids.length);
      vids.forEach(function (v, j) { v.classList.toggle('on', j === k); if (j !== k) v.pause(); });
      ticks.forEach(function (t, j) { t.style.setProperty('--p', j < k ? 1 : 0); });
      nameEl.textContent = vids[k].dataset.name; idxEl.textContent = '0' + (k + 1);
    }
    function go() {
      var v = vids[i];
      if (auto && visible) { var p = v.play(); if (p && p.catch) p.catch(function () { auto = false; ui(); }); }
      else v.pause();
      ui();
    }
    vids.forEach(function (v, j) {
      v.addEventListener('ended', function () {
        if (j !== i) return;
        var n = (i + 1) % vids.length;
        try { vids[n].currentTime = 0; } catch (e) {}
        show(n); go();
      });
      v.addEventListener('playing', function () { if (j === i && !raf) raf = requestAnimationFrame(paint); });
    });
    btn.addEventListener('click', function () { auto = !auto; go(); });
    ui();
    if ('IntersectionObserver' in win) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; go(); }, { threshold: 0.5 }).observe(fig);
    else { visible = true; go(); }
  }

  // ---------- nav: expanded tiles (A) or compact disc with a menu panel (B) ----------
  var compact = nav.dataset.compact === 'true', compTl = null, hudTl = null;
  var navTiles = $$('.tile', navLinks), navCall = $('.nav-call', nav);
  function closeMenu() { if (nav.dataset.open === 'true') { nav.dataset.open = 'false'; navToggle.setAttribute('aria-expanded', 'false'); } }
  function setCompact(on) {
    if (phoneMq.matches) on = true;
    if (on === compact) return;
    if (on && navLinks.contains(document.activeElement)) return;      // never pull the links from under the keyboard
    compact = on;
    var els = navTiles.concat(navCall);
    if (isStatic || phoneMq.matches) { if (!on) closeMenu(); nav.dataset.compact = on; return; }
    if (compTl) compTl.kill();
    if (hudTl && hudTl.isActive()) hudTl.progress(1);
    if (on) {
      compTl = gsap.to(els, { opacity: 0, y: -12, duration: 0.22, stagger: 0.04, ease: E_IN, overwrite: true, onComplete: function () {
        nav.dataset.compact = 'true'; gsap.set(els, { clearProps: 'opacity,transform' });
      } });
    } else {
      closeMenu(); nav.dataset.compact = 'false';
      compTl = gsap.fromTo(els, { opacity: 0, y: -12 }, { opacity: 1, y: 0, duration: 0.32, stagger: 0.04, ease: E_OUT, overwrite: true, clearProps: 'opacity,transform' });
    }
  }
  document.addEventListener('pointerdown', function (e) { if (nav.dataset.open === 'true' && !nav.contains(e.target)) closeMenu(); });

  // ---------- shared, in both modes ----------
  enhancePacks(); priceRolls(); reel();

  // app.js marks the section in the middle band as current but never clears it, so a tile stayed lit on the hero.
  // Above the packages section nothing is current: drop the stale mark.
  var packsSec = $('#packages');
  function clearStaleCurrent() {
    if (!packsSec || packsSec.getBoundingClientRect().top <= win.innerHeight * 0.5) return;
    $$('a[aria-current]', navLinks).forEach(function (a) { a.removeAttribute('aria-current'); });
  }
  win.addEventListener('scroll', clearStaleCurrent, { passive: true });

  var heroTop = 0, heroTravel = 1;
  function measure() { heroTop = hero.getBoundingClientRect().top + win.scrollY; heroTravel = Math.max(1, hero.offsetHeight - win.innerHeight); }
  function heroP() { return clamp((win.scrollY - heroTop) / heroTravel, 0, 1); }

  if (isStatic) {
    // static page: the nav still compacts once the first screen has gone, with no transition
    var onStaticScroll = function () { setCompact(win.scrollY > win.innerHeight * 0.16); };
    win.addEventListener('scroll', onStaticScroll, { passive: true });
    win.addEventListener('resize', onStaticScroll);
    if (phoneMq.matches) { compact = true; nav.dataset.compact = 'true'; } else onStaticScroll();
    win.__aureusReady = true;
    return;
  }

  // =====================================================================================
  // motion mode
  // =====================================================================================
  gsap.registerPlugin(ScrollTrigger);
  ScrollTrigger.config({ ignoreMobileResize: true });

  var lenis = null;
  if (win.Lenis && win.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    lenis = new win.Lenis({ lerp: 0.11, smoothWheel: true, syncTouch: false, anchors: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
  }
  function scrollToY(y, immediate) {
    if (lenis) lenis.scrollTo(y, { immediate: !!immediate, duration: 1.4, easing: E_INOUT, force: true });
    else win.scrollTo({ top: y, behavior: immediate ? 'instant' : 'smooth' });
  }
  function heroY(p) { measure(); return heroTop + p * heroTravel; }

  var stage = $('.stage', hero), media = $('.stage-media', hero), video = $('.stage-film', hero);
  var chapters = $('.chapters', hero), chSvg = $('svg', chapters), chBase = $('.ch-base', chapters), chProg = $('.ch-prog', chapters);
  var chBtns = $$('.ch-btns button', chapters), chNum = $('.ch-num', chapters);
  var beats = $$('.beat', hero), hotspots = $$('.hotspot', hero);
  var seenAtInit = html.classList.contains('seen');
  if (!seenAtInit && win.scrollY >= 8) { html.classList.add('seen'); seenAtInit = true; }   // reloaded part-way down: no intro
  if (phoneMq.matches) { compact = true; nav.dataset.compact = 'true'; }

  // ---------- chapter dock: the loader line that sags into the cockpit curve ----------
  var sag = { v: seenAtInit ? 1 : 0 };
  function drawCurve() {
    var w = chapters.clientWidth, h = chapters.clientHeight; if (!w || !h) return;
    var X = function (n) { return (n * w / 1000).toFixed(1); }, lo = (64 * h / 80).toFixed(1), hi = ((64 - 56 * sag.v) * h / 80).toFixed(1);
    var d = 'M0,' + hi + ' C' + X(140) + ',' + hi + ' ' + X(190) + ',' + lo + ' ' + X(330) + ',' + lo + ' L' + X(670) + ',' + lo +
            ' C' + X(810) + ',' + lo + ' ' + X(860) + ',' + hi + ' ' + X(1000) + ',' + hi;
    chSvg.setAttribute('viewBox', '0 0 ' + w + ' ' + h); chSvg.removeAttribute('preserveAspectRatio');
    chBase.setAttribute('d', d); chProg.setAttribute('d', d);
  }
  drawCurve();

  var chapterIdx = 0;
  function setChapter(k) {
    if (k === chapterIdx) return;
    var up = k > chapterIdx; chapterIdx = k;
    chBtns.forEach(function (b, j) { if (j === k) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
    var gone = $$('b', chNum), now = document.createElement('b');
    now.textContent = '0' + (k + 1); chNum.appendChild(now);
    gsap.fromTo(now, { yPercent: up ? 100 : -100 }, { yPercent: 0, duration: 0.3, ease: E_OUT });
    gsap.to(gone, { yPercent: up ? -100 : 100, duration: 0.3, ease: E_OUT, overwrite: true, onComplete: function () {
      gone.forEach(function (b) { if (b.parentNode) b.parentNode.removeChild(b); });
    } });
  }
  chBtns.forEach(function (b) { b.addEventListener('click', function () { scrollToY(heroY(parseFloat(b.dataset.p) || 0)); }); });

  // ---------- hotspots: film-frame fractions to stage pixels (cover-fit maths) ----------
  function placeHotspots() {
    var W = media.clientWidth, H = media.clientHeight, vw = 1928, vh = 1072; if (!W || !H) return;
    var phone = phoneMq.matches, ox = phone ? 0.8 : 0.5, oy = 0.5;       // on phones the framing has panned to 80% by the time they show
    var s = Math.max(W / vw, H / vh);
    hotspots.forEach(function (li) {
      var x = (W - vw * s) * ox + parseFloat(li.dataset.x) * vw * s, y = (H - vh * s) * oy + parseFloat(li.dataset.y) * vh * s;
      li.style.setProperty('--x', x.toFixed(1) + 'px'); li.style.setProperty('--y', y.toFixed(1) + 'px');
      var lab = $('span', li), lw = phone ? 0 : lab.offsetWidth + 141, pad = 12, out;
      out = y < 70 || y > H - 20 || x < pad || x > W - pad || (li.dataset.side === 'right' ? x + lw > W - pad : x - lw < pad);
      li.hidden = out;
    });
  }

  // ---------- M03: the HUD arrives from all four edges ----------
  var hudShown = false;
  function showHud() {
    if (hudShown) return; hudShown = true;
    html.classList.remove('pre');
    var b1 = $('.beat-1', hero), tiles = $$('.hud-right > *', hero);
    if (seenAtInit || win.scrollY >= 8) {
      sag.v = 1; drawCurve(); html.classList.add('hud-in');
      gsap.from([navLinks, navCall, $('.hud', hero)], { opacity: 0, duration: 0.3, ease: E_OUT, clearProps: 'opacity' });
      return;
    }
    hudTl = gsap.timeline({ defaults: { ease: E_OUT }, onComplete: function () { hudTl = null; } });
    if (!compact) hudTl.fromTo(navTiles.concat(navCall), { y: -28, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, stagger: 0.05, clearProps: 'opacity,transform' }, 0);
    hudTl.fromTo($('.eyebrow', b1), { opacity: 0 }, { opacity: 1, duration: 0.3, ease: 'none', clearProps: 'opacity' }, 0)
      .fromTo($$('h1 .ln > span', b1), { yPercent: 135 }, { yPercent: 0, duration: 0.9, stagger: 0.09, clearProps: 'transform' }, 0)
      .fromTo($$('.beat-body, .beat-actions, .hero-facts', b1), { x: -24, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, stagger: 0.07, clearProps: 'opacity,transform' }, 0.25)
      .fromTo(tiles, { x: 40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, stagger: 0.09 }, 0.15)
      .fromTo([$('.ch-btns', chapters), $('.ch-count', chapters)], { y: 32, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: E_INOUT, clearProps: 'opacity,transform' }, 0.3)
      .to(sag, { v: 1, duration: 0.7, ease: E_INOUT, onUpdate: drawCurve }, 0.3)
      .add(function () { html.classList.add('hud-in'); }, 1.0);
  }

  // ---------- film controller ----------
  var film = { mode: 'idle', duration: 0, cur: REVEAL_END, seeking: false, seekAt: 0, loadFrac: 0, loading: false, interrupted: false, blobUrl: null, ctrl: null };
  var lineV = 0;
  function markLive() {
    if (stage.classList.contains('live')) return;
    if (video.requestVideoFrameCallback) video.requestVideoFrameCallback(function () { stage.classList.add('live'); });
    else stage.classList.add('live');
  }
  function remember() { try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (e) {} }
  function toScrub(from) {
    if (film.mode === 'scrub') return;
    film.mode = 'scrub'; film.seeking = false;
    film.cur = typeof from === 'number' ? from : (isFinite(video.currentTime) ? video.currentTime : REVEAL_END);
    remember(); showHud();
  }
  function filmFail() {
    film.mode = 'failed'; film.loading = false; chapters.classList.remove('pulse');
    hero.classList.add('film-failed'); showHud();
  }
  function startIntro() {
    film.mode = 'intro';
    try { video.currentTime = 0; video.playbackRate = INTRO_RATE; } catch (e) {}
    var p = video.play();
    markLive();
    if (p && p.catch) p.catch(function () {            // autoplay refused (for example iOS Low Power Mode): rest still, film scrubs from the first touch
      if (film.mode !== 'intro') return;
      html.classList.add('seen'); film.mode = 'idle'; toScrub(REVEAL_END + heroP() * FILM_SPAN);
    });
  }
  function onFilmReady() {
    film.duration = video.duration || 0; film.loading = false; chapters.classList.remove('pulse');
    if (!film.duration) { filmFail(); return; }
    video.pause();
    if (!seenAtInit && !film.interrupted && win.scrollY < 8 && document.visibilityState === 'visible') startIntro();
    else toScrub(REVEAL_END + heroP() * FILM_SPAN);     // repeat visit or already scrolled: the first seek lands on the right frame
  }
  function loadFilm() {
    if (film.mode !== 'idle' || film.loading || !win.fetch) { if (!win.fetch) filmFail(); return; }
    var mobile = win.matchMedia('(max-width: 860px), (pointer: coarse)').matches;
    var src = (mobile && video.dataset.srcMobile) || video.dataset.src;
    film.loading = true; film.ctrl = 'AbortController' in win ? new AbortController() : null;
    fetch(src, film.ctrl ? { signal: film.ctrl.signal } : undefined).then(function (r) {
      if (!r.ok) throw new Error('film ' + r.status);
      var total = parseInt(r.headers.get('Content-Length'), 10) || 0;
      if (!r.body || !r.body.getReader) { chapters.classList.add('pulse'); film.loadFrac = 1; return r.blob(); }
      if (!total) { chapters.classList.add('pulse'); film.loadFrac = 1; }
      var reader = r.body.getReader(), chunks = [], got = 0;
      return (function pump() {
        return reader.read().then(function (res) {
          if (res.done) return new Blob(chunks, { type: 'video/mp4' });
          chunks.push(res.value); got += res.value.length;
          if (total) film.loadFrac = Math.min(1, got / total);     // M01: the loader line follows bytes received
          return pump();
        });
      })();
    }).then(function (blob) {
      film.loadFrac = 1;
      film.blobUrl = URL.createObjectURL(blob);
      video.addEventListener('loadeddata', onFilmReady, { once: true });
      video.addEventListener('error', filmFail, { once: true });
      video.src = film.blobUrl; video.load();
    }).catch(function (err) { if (!err || err.name !== 'AbortError') filmFail(); });
  }
  video.addEventListener('seeked', function () { film.seeking = false; if (film.mode === 'scrub') markLive(); });
  function interrupt() {                                  // M06: any scroll intent ends the intro; smoothing carries the film to the scroll target
    film.interrupted = true;
    if (film.mode === 'intro') { video.pause(); toScrub(); }
    showHud();
  }
  win.addEventListener('wheel', interrupt, { passive: true, once: true });
  win.addEventListener('touchmove', interrupt, { passive: true, once: true });
  win.addEventListener('keydown', function onKey(e) {
    if (['ArrowDown', 'ArrowUp', 'PageDown', 'PageUp', 'End', 'Home', ' '].indexOf(e.key) < 0) return;
    win.removeEventListener('keydown', onKey); interrupt();
  });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden && film.mode === 'intro') { video.pause(); try { video.currentTime = REVEAL_END; } catch (e) {} toScrub(REVEAL_END); }
  });
  win.addEventListener('touchstart', function prime() {  // iOS: a muted video only paints frames after a user-initiated play
    if (film.mode !== 'scrub' || !video.paused) return;
    var p = video.play(); if (p && p.then) p.then(function () { if (film.mode === 'scrub') video.pause(); }).catch(function () {});
  }, { once: true, passive: true });
  win.addEventListener('pagehide', function () { if (film.ctrl) film.ctrl.abort(); if (film.blobUrl) URL.revokeObjectURL(film.blobUrl); });

  // one ticker for the film and the progress line
  gsap.ticker.add(function (time, dtMs) {
    var dt = Math.min(0.1, (dtMs || 16.7) / 1000), p = heroP();
    if (film.mode === 'intro') {
      var t = video.currentTime;
      if (win.scrollY >= 8) { interrupt(); }
      else {
        if (t >= HUD_AT) showHud();
        if (t >= REVEAL_END || video.ended) { video.pause(); toScrub(); }
      }
    } else if (film.mode === 'scrub' && film.duration) {
      var target = Math.min(REVEAL_END + p * FILM_SPAN, film.duration - 0.04);
      film.cur += (target - film.cur) * (1 - Math.exp(-dt / SMOOTH_TAU));
      if (film.seeking && time - film.seekAt > 0.6) film.seeking = false;          // a lost "seeked" must not freeze the film
      if (!film.seeking && Math.abs(video.currentTime - film.cur) > 1 / 60) {
        film.seeking = true; film.seekAt = time;
        try { video.currentTime = film.cur; } catch (e) { film.seeking = false; }
      }
    }
    // S03 / M01: one line. Bytes while the film loads on a first visit, scroll progress after that.
    var want = (!hudShown && !seenAtInit) ? film.loadFrac : p;
    lineV += (want - lineV) * (1 - Math.exp(-dt / 0.12));
    if (Math.abs(want - lineV) < 0.0005) lineV = want;
    chProg.style.strokeDashoffset = (1 - lineV).toFixed(4);
    chapters.style.setProperty('--p', lineV.toFixed(4));
  });

  // start loading when the stage is near the viewport (not when the visitor reloads far down the page)
  if ('IntersectionObserver' in win) {
    var near = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { near.disconnect(); loadFilm(); } }, { rootMargin: '300px 0px' });
    near.observe(hero);
  } else loadFilm();
  if (seenAtInit) showHud(); else setTimeout(showHud, HUD_FAILSAFE_MS);

  // ---------- S02 and first-scroll flags ----------
  function onScrollFlags() {
    var y = win.scrollY;
    html.classList.toggle('scrolled', y > 4);
    if (y > 4 && !html.classList.contains('scrolled-once')) { html.classList.add('scrolled-once'); showHud(); }
  }
  win.addEventListener('scroll', onScrollFlags, { passive: true });
  onScrollFlags();

  // ---------- hero timeline: one scrubbed timeline of duration 1 ----------
  function onHeroProgress(p) {
    if (hudTl && p > 0.03) hudTl.progress(1);
    setCompact(p >= COMPACT_AT);
    setChapter(p < CH2_AT ? 0 : p < CH3_AT ? 1 : 2);
    var act = [p < 0.14, p >= 0.20 && p < 0.60, p >= 0.60];
    beats.forEach(function (b, i) { if (act[i]) b.setAttribute('data-active', ''); else b.removeAttribute('data-active'); });
  }
  var mm = gsap.matchMedia();
  mm.add({ desk: '(min-width: 861px)', phone: '(max-width: 860px)' }, function (ctx) {
    var phone = ctx.conditions.phone;
    var b1 = $('.beat-1', hero), b2 = $('.beat-2', hero), b3 = $('.beat-3', hero);
    var tl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: {
      trigger: hero, start: 'top top', end: 'bottom bottom', scrub: 0.5,
      onUpdate: function (self) { onHeroProgress(self.progress); },
      onRefresh: function (self) { measure(); onHeroProgress(self.progress); }
    } });
    tl.to({}, { duration: 1 }, 0);

    // S04: the HUD retracts as the film starts to move
    if (!phone) $$('.hud-right > *', hero).forEach(function (t, i) {
      tl.fromTo(t, { xPercent: 0, autoAlpha: 1 }, { xPercent: 120, autoAlpha: 0, duration: 0.10, immediateRender: false }, 0.04 + i * 0.02);
    });
    tl.fromTo(b1, { opacity: 1 }, { opacity: 0, duration: 0.08, immediateRender: false }, 0.06);

    // S05, S06: beats cross-fade in place, line by line
    function beatIn(beat, at) {
      var parts = $$('.beat-copy > .eyebrow, .beat-copy > .beat-h, .beat-copy > .beat-body, .beat-copy > .ministats' + (phone ? ', .beat-copy > .beat-tags' : ''), beat);
      parts.forEach(function (el, i) { tl.fromTo(el, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.05 }, at + i * 0.015); });
      tl.fromTo($$('.ministats li', beat), { '--rule': 0 }, { '--rule': 1, duration: 0.06 }, at + 0.03);
    }
    beatIn(b2, 0.20);
    // 02 is still fading out while 03 fades in, so there is never an empty frame. On phones both sit in the same place: keep the overlap short.
    tl.to(b2, { opacity: 0, duration: phone ? 0.06 : 0.08 }, phone ? 0.555 : 0.54);
    beatIn(b3, 0.58);
    tl.fromTo($('.beat-actions', b3), { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.05 }, 0.86);   // S08 (ends before the Protect chapter stop at p 0.92)

    // S07: hotspots on the final hold
    [[0.72, 0.74, 0.78], [0.80, 0.82, 0.86]].forEach(function (at, i) {
      var li = hotspots[i]; if (!li) return;
      tl.fromTo($('.dot', li), { scale: 0 }, { scale: 1, duration: 0.03 }, at[0])
        .fromTo($('.leader', li), { scaleX: 0 }, { scaleX: 1, duration: 0.06 }, at[1])
        .fromTo($('span', li), { opacity: 0, x: 8 }, { opacity: 1, x: 0, duration: 0.05 }, at[2]);
    });

    // S09: side scrims follow the copy
    if (!phone) {
      tl.fromTo($('.scrim-l', hero), { opacity: 1 }, { opacity: 0, duration: 0.08, immediateRender: false }, 0.10)
        .to($('.scrim-l', hero), { opacity: 1, duration: 0.10 }, 0.56)
        .fromTo($('.scrim-r', hero), { opacity: 0 }, { opacity: 1, duration: 0.10 }, 0.18)
        .to($('.scrim-r', hero), { opacity: 0, duration: 0.10 }, 0.56);
    } else {
      tl.fromTo(stage, { '--film-x': '50%' }, { '--film-x': '80%', duration: 0.20 }, 0.55);                // S10: keep the wheel in the cropped panel
    }

    // S11: the stage leaves slower than the page and dims
    gsap.fromTo(media, { yPercent: 0 }, { yPercent: 10, ease: 'none', scrollTrigger: { trigger: hero, start: 'bottom bottom', end: 'bottom top', scrub: true } });
    gsap.fromTo($('.hotspots', hero), { y: 0 }, { y: function () { return media.offsetHeight * 0.1; }, ease: 'none', scrollTrigger: { trigger: hero, start: 'bottom bottom', end: 'bottom top', scrub: true, invalidateOnRefresh: true } });   // the dots ride with the film
    gsap.fromTo($('.scrim-dim', hero), { opacity: 0 }, { opacity: 0.4, ease: 'none', scrollTrigger: { trigger: hero, start: 'bottom bottom', end: 'bottom top', scrub: true } });

    if (phone) { compact = true; nav.dataset.compact = 'true'; }
    measure(); placeHotspots(); drawCurve(); onHeroProgress(heroP());
  });

  if ('ResizeObserver' in win) new ResizeObserver(function () { measure(); placeHotspots(); drawCurve(); }).observe(stage);
  else win.addEventListener('resize', function () { measure(); placeHotspots(); drawCurve(); });

  // keyboard: a control inside a beat that is not on screen brings its beat on screen
  hero.addEventListener('focusin', function (e) {
    var beat = e.target.closest && e.target.closest('.beat');
    if (beat && !beat.hasAttribute('data-active')) scrollToY(heroY(parseFloat(beat.dataset.p) || 0), true);
    else if (!beat && !phoneMq.matches && e.target.closest && e.target.closest('.hud-right') && heroP() > 0.02) scrollToY(heroY(0), true);   // the price dock lives on the rest frame
  });

  // ---------- section motion (each plays once) ----------
  function once(el, start, fn) { if (el) ScrollTrigger.create({ trigger: el, start: start, once: true, onEnter: fn }); }
  function mark(el) { return function () { el.classList.add('in'); }; }
  $$('.v4 .lightline').forEach(function (el) { once(el, 'top 85%', mark(el)); });                         // V01
  $$('main .h2').forEach(function (el) { once(el, 'top 80%', mark(el)); });                                // V02
  once($('.facts'), 'top 85%', mark($('.facts')));                                                         // V03
  var bento = $('.bento');
  once(bento, 'top 75%', function () {                                                                     // V04
    bento.classList.add('in');
    gsap.delayedCall(1.0, function () { bento.classList.add('settled'); });
  });
  $$('.info-row').forEach(function (el) { once(el, 'top 85%', mark(el)); });                               // V12

  var closing = $('.closing'), info = $('.info');
  if (closing) {
    var still = $('.closing-media img', closing), logo = $('.logo3d', closing), rot = $('.l3-rot', closing), closingH = $('.closing-h', closing);
    if (info) gsap.fromTo(info, { '--sag': '72px' }, { '--sag': '0px', ease: 'none', scrollTrigger: { trigger: closing, start: 'top bottom', end: 'top 55%', scrub: true } });   // V14
    gsap.fromTo(still, { scale: 1.10, filter: 'brightness(0.55)' }, { scale: 1, filter: 'brightness(1)', ease: 'none', scrollTrigger: { trigger: closing, start: 'top bottom', end: 'top 30%', scrub: true } });   // V15
    gsap.fromTo(still, { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: closing, start: 'top bottom', end: 'max', scrub: true } });
    once(closing, 'top 65%', function () {
      closing.classList.add('in'); closingH.classList.add('in'); logo.classList.add('sweep');
      gsap.delayedCall(1.2, function () { closing.classList.add('settled'); });
    });
    gsap.fromTo(rot, { '--ry': '-18deg', '--rx': '6deg' }, { '--ry': '18deg', '--rx': '-4deg', ease: 'none', scrollTrigger: {                                              // V16
      trigger: closing, start: 'top bottom', end: 'max', scrub: true,
      onToggle: function (self) { logo.classList.toggle('live', self.isActive); }
    } });
  }

  win.__aureusReady = true;
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
  win.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
