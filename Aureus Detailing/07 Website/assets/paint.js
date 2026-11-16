/* Aureus v3 "Into the Paint": hero lens, paint dive, polish arc, odometer price, heading polish.
   Independent of app.js (booking engine). Respects prefers-reduced-motion. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hero = $('#hero'), stage = $('#stage'), paint = $('#paint'), lens = $('#lens'), lensCv = $('#lens-cv');
  var btn = $('#dive-btn'), sub = $('#hero-sub'), hint = $('#hero-hint'), car = $('#car');
  if (!hero || !paint || !paint.getContext) return;

  var NAVY = [7, 26, 51], AQUA = '0,168,168', AQUA_HI = '95,240,230';
  var rand = mulberry(7);
  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

  // ---------- micro-paint textures (scratched and polished), built once per size ----------
  function makeCanvas(w, h) { var c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
  function baseCoat(ctx, w, h, sheen) {
    var g = ctx.createRadialGradient(w * 0.7, h * 0.35, 0, w * 0.6, h * 0.5, Math.max(w, h) * 0.9);
    g.addColorStop(0, 'rgb(16,44,82)'); g.addColorStop(0.55, 'rgb(' + NAVY + ')'); g.addColorStop(1, 'rgb(2,8,18)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    var r = mulberry(11), n = Math.round(w * h / 260);
    for (var i = 0; i < n; i++) {
      var x = r() * w, y = r() * h, s = r(), a = 0.18 + s * 0.6;
      ctx.fillStyle = s > 0.92 ? 'rgba(' + AQUA_HI + ',' + a + ')' : 'rgba(205,225,250,' + (a * 0.7) + ')';
      var d = s > 0.97 ? 2.2 : s > 0.8 ? 1.4 : 0.9;
      ctx.fillRect(x, y, d, d);
    }
    if (sheen) {
      var s2 = ctx.createLinearGradient(w * 0.3, 0, w, h * 0.8);
      s2.addColorStop(0, 'rgba(' + AQUA + ',0.04)'); s2.addColorStop(0.5, 'rgba(' + AQUA_HI + ',0.34)'); s2.addColorStop(1, 'rgba(' + AQUA + ',0.12)');
      ctx.fillStyle = s2; ctx.fillRect(0, 0, w, h);
    }
  }
  function scratches(ctx, w, h) {
    var r = mulberry(29), centres = 7 + Math.round(w / 260);
    ctx.lineCap = 'round';
    for (var c = 0; c < centres; c++) {
      var cx = r() * w, cy = r() * h, rings = 10 + Math.round(r() * 16);
      for (var k = 0; k < rings; k++) {
        var rad = 20 + r() * Math.max(w, h) * 0.32, a0 = r() * Math.PI * 2, len = 0.25 + r() * 0.9;
        ctx.strokeStyle = 'rgba(214,230,248,' + (0.14 + r() * 0.3) + ')';
        ctx.lineWidth = 0.9 + r() * 2.2;
        ctx.beginPath(); ctx.arc(cx, cy, rad, a0, a0 + len); ctx.stroke();
      }
    }
    var haze = ctx.createLinearGradient(0, 0, w, h);
    haze.addColorStop(0, 'rgba(180,200,225,0.12)'); haze.addColorStop(1, 'rgba(180,200,225,0.04)');
    ctx.fillStyle = haze; ctx.fillRect(0, 0, w, h);
  }
  var tex = { w: 0, h: 0, rough: null, smooth: null };
  function buildTextures(w, h) {
    if (tex.w === w && tex.h === h) return;
    tex.w = w; tex.h = h;
    tex.rough = makeCanvas(w, h); tex.smooth = makeCanvas(w, h);
    var a = tex.rough.getContext('2d'), b = tex.smooth.getContext('2d');
    baseCoat(a, w, h, false); scratches(a, w, h);
    baseCoat(b, w, h, true);
    if (!tex.macro) tex.macro = macroTexture(900);
  }
  // close-up paint for the lens: big glittering flakes under bold silver swirl canyons
  function macroTexture(n) {
    var c = makeCanvas(n, n), x = c.getContext('2d'), r = mulberry(41);
    var g = x.createRadialGradient(n * 0.4, n * 0.35, 0, n / 2, n / 2, n * 0.75);
    g.addColorStop(0, '#163A6A'); g.addColorStop(0.6, '#0A2142'); g.addColorStop(1, '#040F20');
    x.fillStyle = g; x.fillRect(0, 0, n, n);
    for (var i = 0; i < 2600; i++) {
      var s = r(), d = 1 + s * 3.2, px = r() * n, py = r() * n;
      x.fillStyle = s > 0.9 ? 'rgba(95,240,230,' + (0.5 + s * 0.5) + ')' : 'rgba(215,232,252,' + (0.25 + s * 0.6) + ')';
      x.beginPath(); x.arc(px, py, d / 2, 0, Math.PI * 2); x.fill();
      if (s > 0.985) { x.fillStyle = 'rgba(235,248,255,0.85)'; x.fillRect(px - d * 2.5, py - 0.6, d * 5, 1.2); x.fillRect(px - 0.6, py - d * 2.5, 1.2, d * 5); }
    }
    x.lineCap = 'round';
    for (var c2 = 0; c2 < 6; c2++) {
      var cx = r() * n, cy = r() * n;
      for (var k = 0; k < 14; k++) {
        var rad = 40 + r() * n * 0.6, a0 = r() * 6.28, len = 0.2 + r() * 0.7, wdt = 1.2 + r() * 2.6;
        x.strokeStyle = 'rgba(10,20,40,0.55)'; x.lineWidth = wdt + 1.5; x.beginPath(); x.arc(cx, cy, rad, a0, a0 + len); x.stroke();
        x.strokeStyle = 'rgba(220,235,252,' + (0.25 + r() * 0.4) + ')'; x.lineWidth = wdt; x.beginPath(); x.arc(cx, cy, rad - 1, a0, a0 + len); x.stroke();
      }
    }
    return c;
  }

  // ---------- hero paint world ----------
  var ctx = paint.getContext('2d'), W = 0, H = 0, dpr = 1;
  var mask = makeCanvas(1, 1), mctx = mask.getContext('2d');
  var comp = makeCanvas(1, 1), cctx = comp.getContext('2d');
  var stars = [], sweep = 1, sweeping = false, visible = true, raf = 0, dirty = true, t0 = 0;
  var ARC = function () { return { cx: -W * 0.55, cy: H * 1.45 }; };
  var R_START = function () { return Math.hypot(W * 1.6, H * 1.5); }, R_END = function () { return Math.hypot(W * 1.12, H * 1.2); };

  function size() {
    var r = stage.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    W = Math.max(1, Math.round(r.width * dpr)); H = Math.max(1, Math.round(r.height * dpr));
    paint.width = mask.width = comp.width = W; paint.height = mask.height = comp.height = H;
    buildTextures(Math.round(W / 1), Math.round(H / 1));
    mctx.clearRect(0, 0, W, H);
    stars = [];
    var r2 = mulberry(3), n = Math.round(W * H / 9000);
    for (var i = 0; i < n; i++) stars.push({ x: r2() * W, y: r2() * H, p: r2() * 6.28, s: 0.6 + r2() * 1.8, hi: r2() > 0.8 });
    applyArc(); dirty = true;
  }
  function applyArc() {
    var a = ARC(), rad = R_START() + (R_END() - R_START()) * ease(sweep);
    mctx.save(); mctx.globalCompositeOperation = 'source-over';
    // polished = everything outside the circle
    mctx.fillStyle = '#000'; mctx.beginPath(); mctx.rect(0, 0, W, H); mctx.arc(a.cx, a.cy, rad, 0, Math.PI * 2, true); mctx.fill('evenodd');
    mctx.restore();
    return rad;
  }
  function ease(t) { return 1 - Math.pow(1 - t, 3); }
  function polishAt(x, y, r) {
    var g = mctx.createRadialGradient(x, y, r * 0.15, x, y, r);
    g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)');
    mctx.fillStyle = g; mctx.beginPath(); mctx.arc(x, y, r, 0, Math.PI * 2); mctx.fill();
    dirty = true;
  }
  function composite() {
    cctx.globalCompositeOperation = 'source-over';
    cctx.clearRect(0, 0, W, H); cctx.drawImage(tex.smooth, 0, 0, W, H);
    cctx.globalCompositeOperation = 'destination-in'; cctx.drawImage(mask, 0, 0);
    cctx.globalCompositeOperation = 'destination-over'; cctx.drawImage(tex.rough, 0, 0, W, H);
    cctx.globalCompositeOperation = 'source-over';
    dirty = false;
  }
  var pad = { x: 0, y: 0, on: false, a: 0 };
  function draw(now) {
    raf = 0;
    if (!visible || hero.dataset.stage !== 'paint') return;
    if (!t0) t0 = now;
    if (sweeping) {
      sweep = Math.min(1, (now - sweepStart) / 1700);
      var rad = applyArc(); dirty = true;
      if (sweep >= 1) sweeping = false;
    }
    if (dirty) composite();
    ctx.clearRect(0, 0, W, H); ctx.drawImage(comp, 0, 0);
    // glowing polish arc at the edge of the polished area
    var a = ARC(), rr = R_START() + (R_END() - R_START()) * ease(sweep);
    ctx.save(); ctx.lineWidth = 3 * dpr; ctx.strokeStyle = 'rgba(' + AQUA_HI + ',0.9)';
    ctx.shadowColor = 'rgba(' + AQUA_HI + ',0.9)'; ctx.shadowBlur = 28 * dpr;
    ctx.beginPath(); ctx.arc(a.cx, a.cy, rr, -Math.PI / 2, 0); ctx.stroke(); ctx.restore();
    // twinkling flakes
    if (!reduced) {
      var t = (now - t0) / 1000;
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i], k = 0.5 + 0.5 * Math.sin(t * 1.6 + s.p);
        if (k < 0.82) continue;
        var al = (k - 0.82) / 0.18;
        ctx.fillStyle = s.hi ? 'rgba(' + AQUA_HI + ',' + al + ')' : 'rgba(235,245,255,' + (al * 0.85) + ')';
        var d = s.s * dpr * (0.6 + al);
        ctx.fillRect(s.x - d / 2, s.y - d * 2, d, d * 4); ctx.fillRect(s.x - d * 2, s.y - d / 2, d * 4, d);
      }
    }
    // polishing pad ring under the pointer
    if (pad.on) {
      ctx.save(); ctx.strokeStyle = 'rgba(' + AQUA_HI + ',0.55)'; ctx.lineWidth = 1.5 * dpr;
      ctx.beginPath(); ctx.arc(pad.x, pad.y, 46 * dpr, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
    }
    loop();
  }
  function loop() { if (!raf && !reduced) raf = requestAnimationFrame(draw); }
  var sweepStart = 0;

  // ---------- the lens over the car ----------
  var lctx = lensCv.getContext('2d'), L = { x: 0.62, y: 0.52, tx: 0.62, ty: 0.52, size: 0 }, idle = true, lensRaf = 0, lensT = 0;
  function lensSize() {
    var r = lens.getBoundingClientRect(); L.size = r.width;
    var d = Math.min(window.devicePixelRatio || 1, 2);
    lensCv.width = Math.round(r.width * d); lensCv.height = Math.round(r.height * d);
  }
  function placeLens() {
    var hr = stage.getBoundingClientRect();
    lens.style.transform = 'translate(' + (L.x * hr.width - L.size / 2) + 'px,' + (L.y * hr.height - L.size / 2) + 'px)';
    // magnified micro-paint: the scratched texture, shifted by lens position
    if (!tex.macro) return;
    var w = lensCv.width, h = lensCv.height, m = tex.macro.width, view = m * 0.55;
    var sx = Math.max(0, Math.min(m - view, (L.x - 0.35) / 0.57 * (m - view))), sy = Math.max(0, Math.min(m - view, (L.y - 0.25) / 0.6 * (m - view)));
    lctx.drawImage(tex.macro, sx, sy, view, view, 0, 0, w, h);
    var g = lctx.createRadialGradient(w * 0.35, h * 0.3, 0, w / 2, h / 2, w / 2);
    g.addColorStop(0, 'rgba(255,255,255,0.10)'); g.addColorStop(0.7, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0.45)');
    lctx.fillStyle = g; lctx.fillRect(0, 0, w, h);
  }
  function lensLoop(now) {
    lensRaf = 0;
    if (hero.dataset.stage !== 'car' || !visible) return;
    if (idle && !reduced) { // slow drift along the bonnet
      lensT = now / 1000;
      L.tx = 0.6 + Math.sin(lensT * 0.45) * 0.07; L.ty = 0.53 + Math.sin(lensT * 0.8) * 0.035;
    }
    L.x += (L.tx - L.x) * (reduced ? 1 : 0.12); L.y += (L.ty - L.y) * (reduced ? 1 : 0.12);
    placeLens();
    if (!reduced) lensRaf = requestAnimationFrame(lensLoop);
  }
  function startLens() { if (!lensRaf) lensRaf = requestAnimationFrame(lensLoop); }

  // ---------- stages ----------
  function setStage(next) {
    hero.dataset.stage = next;
    if (next === 'paint') {
      sub.textContent = 'Mobile and workshop car detailing, Victoria Park, Perth.';
      btn.textContent = 'Back to the car';
      hint.textContent = 'Drag across the scratches to polish them out.';
      sweep = reduced ? 1 : 0; sweeping = !reduced; sweepStart = performance.now();
      mctx.clearRect(0, 0, W, H); applyArc(); dirty = true;
      if (reduced) { composite(); draw(performance.now()); } else loop();
    } else {
      sub.textContent = 'See what we do to your paint.';
      btn.textContent = 'Look closer';
      hint.textContent = 'Move the lens across the bonnet.';
      startLens();
    }
  }
  function dive() {
    if (hero.dataset.stage === 'paint') { setStage('car'); return; }
    if (reduced) { setStage('paint'); return; }
    hero.classList.add('diving');
    setTimeout(function () { setStage('paint'); hero.classList.remove('diving'); }, 900);
  }

  // ---------- pointer ----------
  function local(e) { var r = stage.getBoundingClientRect(); return { x: (e.clientX - r.left) / r.width, y: (e.clientY - r.top) / r.height }; }
  hero.addEventListener('pointermove', function (e) {
    if (e.target.closest('.dock, .hero-copy, .nav')) { pad.on = false; return; }
    var p = local(e);
    if (hero.dataset.stage === 'car') { idle = false; L.tx = Math.min(0.92, Math.max(0.35, p.x)); L.ty = Math.min(0.85, Math.max(0.25, p.y)); startLens(); }
    else { pad.on = true; pad.x = p.x * W; pad.y = p.y * H; polishAt(pad.x, pad.y, 60 * dpr); loop(); }
  });
  hero.addEventListener('pointerleave', function () { idle = true; pad.on = false; });
  stage.addEventListener('click', function () { if (hero.dataset.stage === 'car') dive(); });
  btn.addEventListener('click', dive);

  // ---------- visibility, resize, start ----------
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) {
    visible = es[0].isIntersecting;
    if (visible) { if (hero.dataset.stage === 'paint') loop(); else startLens(); }
  }, { threshold: 0.05 }).observe(hero);
  var rt = 0;
  window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { size(); lensSize(); placeLens(); if (hero.dataset.stage === 'paint') { dirty = true; loop(); } }, 150); });
  size(); lensSize(); placeLens(); setStage('car');
  requestAnimationFrame(function () { hero.classList.add('lit'); });

  // ---------- odometer price ----------
  var price = $('#dock-price');
  if (price && 'MutationObserver' in window && !reduced) {
    var last = price.textContent;
    new MutationObserver(function () {
      if (price.textContent === last) return;
      var up = parseInt(price.textContent.replace(/\D/g, ''), 10) >= parseInt(last.replace(/\D/g, ''), 10);
      last = price.textContent;
      price.classList.remove('roll-up', 'roll-down'); void price.offsetWidth;
      price.classList.add(up ? 'roll-up' : 'roll-down');
    }).observe(price, { childList: true, characterData: true, subtree: true });
  }

  // ---------- section headings get one polish sweep as they arrive ----------
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('polished'); io.unobserve(e.target); } });
    }, { threshold: 0.6 });
    document.querySelectorAll('.section .h2').forEach(function (h) { h.classList.add('to-polish'); io.observe(h); });
  }
})();
