/* Aureus scroll film: the visitor's scroll plays one continuous film (Higgsfield scroll-scrub method, vanilla JS).
   Chapters are normal HTML that scroll over a sticky stage. No autoplay, no manual interaction. */
(function () {
  'use strict';
  var film = document.querySelector('.film');
  if (!film) return;
  var stage = film.querySelector('.film-stage'), video = film.querySelector('.film-video'), poster = film.querySelector('.film-poster');
  var chapters = Array.prototype.slice.call(film.querySelectorAll('.chapter'));
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // chapters: mark the one in view (drives the copy fade), works with or without video
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle('in', e.isIntersecting); });
    }, { rootMargin: '-35% 0px -35% 0px' });
    chapters.forEach(function (c) { io.observe(c); });
  } else chapters.forEach(function (c) { c.classList.add('in'); });

  if (reduced || !video || !window.fetch) return; // still poster + readable chapters

  var mobile = window.matchMedia('(max-width: 760px), (pointer: coarse)').matches;
  var src = (mobile && video.dataset.srcMobile) || video.dataset.src;
  var ctrl = 'AbortController' in window ? new AbortController() : null;
  var blobUrl = null, ready = false, target = 0, seeking = false, raf = 0, duration = 0;

  function progress() {
    var r = film.getBoundingClientRect(), total = film.offsetHeight - window.innerHeight;
    return total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
  }
  function tick() {
    raf = 0;
    if (!ready) return;
    target = progress() * Math.max(0, duration - 0.05);
    if (!seeking && Math.abs(video.currentTime - target) > 0.012) { seeking = true; video.currentTime = target; }
  }
  function onScroll() { if (!raf) raf = requestAnimationFrame(tick); }
  video.addEventListener('seeked', function () {
    seeking = false;
    if (!stage.classList.contains('live')) stage.classList.add('live'); // swap poster for real frames
    if (Math.abs(video.currentTime - target) > 0.03) onScroll();
  });

  // fetch to a Blob so currentTime is always seekable, then start once the film is near
  function load() {
    fetch(src, ctrl ? { signal: ctrl.signal } : undefined)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.blob(); })
      .then(function (b) {
        blobUrl = URL.createObjectURL(b);
        video.src = blobUrl; video.load();
        video.addEventListener('loadeddata', function () {
          duration = video.duration || 0; ready = duration > 0; video.pause(); onScroll();
        }, { once: true });
      })
      .catch(function () { /* stay on the poster */ });
  }
  if ('IntersectionObserver' in window) {
    var near = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { near.disconnect(); load(); } }, { rootMargin: '200px 0px' });
    near.observe(film);
  } else load();

  // iOS: prime the muted video on the first touch so it will paint frames
  window.addEventListener('touchstart', function prime() {
    var p = video.play(); if (p && p.then) p.then(function () { video.pause(); onScroll(); }).catch(function () {});
  }, { once: true, passive: true });

  window.addEventListener('scroll', onScroll, { passive: true });
  var lastW = window.innerWidth;
  window.addEventListener('resize', function () { if (window.innerWidth !== lastW) { lastW = window.innerWidth; onScroll(); } });
  window.addEventListener('pagehide', function () { if (ctrl) ctrl.abort(); if (blobUrl) URL.revokeObjectURL(blobUrl); });
})();
