/* Aureus Detailing: packages, booking, quote, hero rinse, workshop footage. No dependencies.
   Booking rules follow the bookingApp() script on carwashandpolish.com.au (see BUILD-PROMPT-V2.md). */
(function () {
  'use strict';

  // ---------- config ----------
  // Served by the existing Laravel app: the page carries a csrf-token meta tag and the forms post to its routes.
  // Otherwise set AUREUS.endpoint to a JSON form endpoint, or leave it empty to fall back to a prefilled email.
  // AUREUS.settings and AUREUS.dateLocks mirror the old site's siteSetting and activeDateLocks.
  var CFG = Object.assign({ endpoint: '', email: 'carwashandpolish.wa@gmail.com', phone: '0434 13 73 93', settings: null, dateLocks: [], turnstileSiteKey: '' }, window.AUREUS || {});
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var SET = Object.assign({ is_shop_open: true, shop_closed_notice: 'Online booking is closed right now. Please call us on ' + CFG.phone + '.', operating_days: DAYS.slice() }, CFG.settings || {});
  var csrfMeta = document.querySelector('meta[name="csrf-token"]');
  var MODE = csrfMeta ? 'laravel' : (CFG.endpoint ? 'endpoint' : 'email');

  var PACKS = [
    { id: 'silver', name: 'Silver', backend: 'Level 1: Express', price: 149, time: '1 h 30 min', tag: 'Fast and clean',
      slots: ['08:30 AM - 10:00 AM', '10:00 AM - 11:30 AM', '11:30 AM - 01:00 PM', '01:00 PM - 02:30 PM', '02:30 PM - 04:00 PM', '04:00 PM - 05:30 PM'],
      items: ['Exterior snow foam hand wash', 'Wheel and rim deep clean', 'Tyre dressing and gloss shine', 'Exterior windows and mirrors', 'Cabin vacuum: seats, carpet and boot', 'Dashboard, console and trim wipe', 'Door jambs wiped'] },
    { id: 'gold', name: 'Gold', backend: 'Level 2: Premium', price: 199, time: '2 h 30 min', tag: 'Most popular', popular: true,
      slots: ['08:30 AM - 11:00 AM', '11:00 AM - 01:30 PM', '01:30 PM - 04:00 PM', '04:00 PM - 06:30 PM'],
      items: ['Everything in Silver, plus polish', 'Wax paint sealant', 'Deep interior antibacterial steam clean', 'Full leather clean and condition', 'Air vent disinfection and deodoriser', 'AC vent brush detailing'] },
    { id: 'aureus', name: 'Aureus', backend: 'Level 3: Ultimate', price: 299, time: '4 hours', tag: 'Showroom finish',
      slots: ['08:30 AM - 12:30 PM', '01:00 PM - 05:00 PM'],
      items: ['Everything in Gold, plus ceramic sealant', 'Clay bar paint decontamination', 'Hydrophobic 6-month ceramic shield', 'Deep leather protection treatment', 'Hot water extraction shampoo: seats and mats', 'Headlight restoration and UV coat', 'High-gloss machine polish', 'Iron and tar removal'] }
  ];
  var VEHICLES = [
    { id: 'sedan', name: 'Sedan / Hatch', short: 'Sedan', backend: 'Sedan / Hatchback', add: 0, eg: 'Corolla, Civic, Camry, Model 3' },
    { id: 'suv', name: 'SUV / 4WD / Ute', short: 'SUV / Ute', backend: 'SUV / 4WD / Wagon', add: 20, eg: 'Prado, RAV4, Hilux, Ranger, CX-5' },
    { id: 'van', name: 'Van / Commercial', short: 'Van', backend: 'Van / Large Truck / Commercial', add: 40, eg: 'HiAce, Transit, LandCruiser 300, 7+ seats' }
  ];
  var ADDONS = [
    { id: 'headlights', name: 'Headlight restoration', backend: 'Headlights restore', price: 60, text: 'Multi-stage wet sanding and a UV sealant bring cloudy, yellowed headlights back to clear.' },
    { id: 'engine', name: 'Engine bay clean', backend: 'Engine Bay clean', price: 60, text: 'Gentle degreasing, steam cleaning and a satin dressing for engine bay plastics and hoses.' },
    { id: 'one-step', name: 'One-step paint correction', backend: 'One step paint correction', price: 120, text: 'A single-stage machine polish that removes 50 to 65% of light swirl marks, haze and oxidation.' },
    { id: 'two-step', name: 'Two-step paint correction', backend: 'Two step paint correction', price: 200, text: 'A heavy compound cut, then an ultrafine finishing polish, removing 85 to 95% of deeper scratches and swirls.' },
    { id: 'ceramic', name: 'Ceramic coating', backend: 'Ceramic coating', price: 699, from: true, text: 'Multi-year 9H nano-ceramic protection with a deep gloss finish. Priced per car after inspection.' }
  ];
  var WORKSHOP = '530 Albany Hwy, Victoria Park WA 6100';
  var WORKSHOP_BACKEND = '530, Albany Hwy, Victoria Park, WA-6100 (Physical Workshop)';
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  // Same starting point as the old site: popular package, sedan, workshop, today, first free time window.
  var S = { pack: 'gold', veh: 'sedan', loc: 'workshop', date: null, slot: null, addons: [], card: {}, openCard: null, addonsOpen: false, month: null, booked: [], locked: [], submitting: false };

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var money = function (n) { return '$' + n.toLocaleString('en-AU'); };
  var byId = function (list, id) { return list.filter(function (x) { return x.id === id; })[0]; };
  var icon = function (n) { return '<svg aria-hidden="true"><use href="#i-' + n + '"/></svg>'; };
  var noop = function () {};
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- prices ----------
  function surcharge() { return byId(VEHICLES, S.veh).add; }
  function sumAddons(ids) { return (ids || []).reduce(function (t, id) { return t + byId(ADDONS, id).price; }, 0); }
  function cardPrice(p) { return p.price + surcharge() + sumAddons(S.card[p.id]); }          // package card: base + vehicle + that card's extras
  function total() { return byId(PACKS, S.pack).price + surcharge() + sumAddons(S.addons); }   // booking: base + vehicle + chosen extras
  function hasFrom(ids) { return (ids || []).indexOf('ceramic') >= 0; }
  function priceText(n, ids) { return (hasFrom(ids) ? 'from ' : '') + money(n); }

  // ---------- render once ----------
  function renderDock() {
    $('#dock-veh').innerHTML = VEHICLES.map(function (v) {
      return '<label><input type="radio" name="veh-dock" value="' + v.id + '"><span>' + esc(v.short) + (v.add ? '<small>+' + money(v.add) + '</small>' : '') + '</span></label>';
    }).join('');
    $('#dock-pack').innerHTML = PACKS.map(function (p) {
      return '<label><input type="radio" name="pack-dock" value="' + p.id + '"><span>' + p.name + '</span></label>';
    }).join('');
  }
  function renderVehSeg() {
    $('#veh-seg').innerHTML = VEHICLES.map(function (v) {
      return '<label><input type="radio" name="veh-top" value="' + v.id + '"><span><i class="l">' + esc(v.name) + '</i><i class="s" aria-hidden="true">' + esc(v.short) + '</i>' + (v.add ? '<small>+' + money(v.add) + '</small>' : '') + '</span></label>';
    }).join('');
  }
  function renderPacks() {
    $('#packs').innerHTML = PACKS.map(function (p) {
      return '<article class="pack" data-id="' + p.id + '">' +
        '<div class="pack-head"><h3>' + p.name + '</h3><span class="pack-tag">' + esc(p.tag) + '</span></div>' +
        '<p class="pack-price"><b data-card-price="' + p.id + '"></b><span>' + p.time + '</span></p>' +
        '<ul class="pack-list">' + p.items.map(function (i) { return '<li>' + icon('check') + '<span>' + esc(i) + '</span></li>'; }).join('') + '</ul>' +
        '<div class="pack-extras">' +
          '<button class="pack-extras-btn" type="button" data-extras="' + p.id + '" aria-expanded="false" aria-controls="px-' + p.id + '"><span data-extras-label="' + p.id + '">Add extras</span>' + icon('plus') + '</button>' +
          '<div class="pack-extras-list" id="px-' + p.id + '" hidden>' + ADDONS.map(function (a) {
            return '<label class="xtra"><input type="checkbox" data-card-addon="' + a.id + '" data-pack="' + p.id + '"><span>' + esc(a.name) + '</span><em>' + (a.from ? 'from ' : '+') + money(a.price) + '</em></label>';
          }).join('') + '</div>' +
        '</div>' +
        '<a class="btn ' + (p.popular ? 'btn-pink' : 'btn-navy') + '" href="#booking" data-book="' + p.id + '">Book ' + p.name + ' ' + icon('arrow') + '</a>' +
      '</article>';
    }).join('');
  }
  function renderBookingOptions() {
    $('#f-pack').innerHTML = PACKS.map(function (p) { return '<option value="' + p.id + '"></option>'; }).join('');
    $('#f-veh').innerHTML = VEHICLES.map(function (v) { return '<option value="' + v.id + '">' + esc(v.name) + (v.add ? ' (+' + money(v.add) + ')' : '') + '</option>'; }).join('');
    $('#bk-addons').innerHTML = ADDONS.map(function (a) {
      return '<label class="opt"><input type="checkbox" name="addon" value="' + a.id + '"><span><span class="ck-text"><b>' + esc(a.name) + '</b><small>' + esc(a.text) + '</small></span><em>' + (a.from ? 'from ' : '+') + money(a.price) + '</em></span></label>';
    }).join('');
  }

  // ---------- keep every control in step with the state ----------
  function syncAll() {
    var p = byId(PACKS, S.pack);
    $('#dock-price').textContent = money(p.price + surcharge());
    $('#dock-time').textContent = p.time;
    $$('input[name="veh-dock"], input[name="veh-top"]').forEach(function (i) { i.checked = i.value === S.veh; });
    $$('input[name="pack-dock"]').forEach(function (i) { i.checked = i.value === S.pack; });
    $('#f-veh').value = S.veh;
    $$('#f-pack option').forEach(function (o) { var q = byId(PACKS, o.value); o.textContent = q.name + ' · ' + money(q.price + surcharge()) + ' · ' + q.time; });
    $('#f-pack').value = S.pack;

    $$('.pack').forEach(function (el) {
      var id = el.dataset.id, q = byId(PACKS, id), picked = S.card[id] || [], open = S.openCard === id;
      el.dataset.selected = id === S.pack;
      $('[data-card-price]', el).textContent = priceText(cardPrice(q), picked);
      $('[data-extras-label]', el).textContent = picked.length ? 'Extras: ' + picked.length + ' added, +' + money(sumAddons(picked)) : 'Add extras';
      $('.pack-extras-btn', el).setAttribute('aria-expanded', open);
      $('.pack-extras-list', el).hidden = !open;
      $$('[data-card-addon]', el).forEach(function (c) { c.checked = picked.indexOf(c.dataset.cardAddon) >= 0; });
    });

    $$('input[name="addon"]').forEach(function (i) { i.checked = S.addons.indexOf(i.value) >= 0; });
    $('#xtras-label').textContent = S.addons.length ? 'Extras: ' + S.addons.length + ' added, +' + money(sumAddons(S.addons)) : 'Add extras';
    $('#xtras-toggle').setAttribute('aria-expanded', S.addonsOpen);
    $('#bk-addons').hidden = !S.addonsOpen;
    $('#xtras-clear').hidden = !S.addons.length;
    $$('input[name="loc"]').forEach(function (i) { i.checked = i.value === S.loc; });
    $('#addr-field').hidden = S.loc !== 'mobile';
    renderSummary();
  }

  // ---------- calendar and time windows ----------
  var today = new Date(); today.setHours(0, 0, 0, 0);
  S.month = new Date(today.getFullYear(), today.getMonth(), 1);
  S.date = new Date(today);
  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function niceDate(d) { return d.toLocaleDateString('en-AU', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }); }
  function slotStart(slot, d) {
    var m = /^(\d{2}):(\d{2}) (AM|PM)/.exec(slot); var h = +m[1] % 12 + (m[3] === 'PM' ? 12 : 0);
    var t = new Date(d); t.setHours(h, +m[2], 0, 0); return t;
  }
  function slotLabel(slot) { return slot.replace(/(^|\s)0(\d:)/g, '$1$2').replace(/ AM/g, ' am').replace(/ PM/g, ' pm').replace(' - ', ' to '); }
  function slots() { return byId(PACKS, S.pack).slots; }
  // "Locked" and "Booked" come from the server. "Passed" is checked here for today (the old site leaves that to the server).
  function slotStatus(slot) {
    if (S.locked.indexOf(slot) >= 0) return 'Locked';
    if (S.booked.indexOf(slot) >= 0) return 'Booked';
    if (S.date && slotStart(slot, S.date) <= new Date()) return 'Passed';
    return '';
  }
  // If the chosen window is not offered by this package, or is taken, move to the first free one.
  function ensureSlot() {
    var all = slots();
    if (!S.slot || all.indexOf(S.slot) < 0 || slotStatus(S.slot)) S.slot = all.filter(function (s) { return !slotStatus(s); })[0] || null;
  }
  function fullLock(isoDate) {
    return (CFG.dateLocks || []).filter(function (l) {
      if (!l.is_active || l.scope !== 'full_day') return false;
      if (l.service_type !== 'all' && l.service_type !== S.loc) return false;
      return isoDate >= l.lock_date && isoDate <= (l.end_date || l.lock_date);
    })[0] || null;
  }
  function dayBlock(dt) {
    if (!SET.is_shop_open) return 'bookings are closed';
    if (dt < today) return 'past date';
    if (SET.operating_days.indexOf(DAYS[dt.getDay()]) < 0) return 'closed on ' + DAYS[dt.getDay()] + 's';
    var lock = fullLock(iso(dt));
    if (lock) return lock.reason ? 'unavailable: ' + lock.reason : 'unavailable';
    return '';
  }
  function renderCal() {
    var y = S.month.getFullYear(), m = S.month.getMonth(), days = new Date(y, m + 1, 0).getDate(), d, dt;
    $('#cal-title').textContent = MONTHS[m] + ' ' + y;
    $('#cal-prev').disabled = S.month <= new Date(today.getFullYear(), today.getMonth(), 1);
    // As on the old site: if the chosen date is not an open day in the month on screen, pick that month's first open day.
    var selOk = false, firstOk = null, moved = false;
    for (d = 1; d <= days; d++) {
      dt = new Date(y, m, d);
      if (dayBlock(dt)) continue;
      if (!firstOk) firstOk = dt;
      if (S.date && iso(S.date) === iso(dt)) selOk = true;
    }
    if (!selOk && firstOk) { S.date = firstOk; moved = true; }
    var html = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map(function (n) { return '<div class="cal-dow" aria-hidden="true">' + n + '</div>'; }).join('');
    for (var i = 0, lead = new Date(y, m, 1).getDay(); i < lead; i++) html += '<span></span>';
    for (d = 1; d <= days; d++) {
      dt = new Date(y, m, d);
      var why = dayBlock(dt), sel = S.date && iso(S.date) === iso(dt);
      html += '<button type="button" class="day" data-date="' + iso(dt) + '"' + (why ? ' disabled' : '') + ' aria-pressed="' + !!sel + '"' +
        (iso(dt) === iso(today) ? ' data-today="true"' : '') + ' aria-label="' + esc(niceDate(dt) + (why ? ', ' + why : '')) + '">' + d + '</button>';
    }
    $('#cal-grid').innerHTML = html;
    return moved;
  }
  function renderSlots() {
    var box = $('#slots');
    $('#slots-label').textContent = S.date ? 'Time windows on ' + niceDate(S.date) : 'Choose a time window';
    var all = slots(), free = 0;
    var html = all.map(function (s) {
      var st = slotStatus(s); if (!st) free++;
      return '<button type="button" class="slot" data-slot="' + s + '"' + (st ? ' disabled' : '') + ' aria-pressed="' + (S.slot === s) + '"' +
        ' aria-label="' + slotLabel(s) + (st ? ', ' + st.toLowerCase() : '') + '"><span>' + slotLabel(s) + '</span>' + (st ? '<small>' + st + '</small>' : '') + '</button>';
    }).join('');
    if (!free) html += '<p class="slots-empty">No time windows left on this day. Please pick another date.</p>';
    box.innerHTML = html;
  }
  var fetchSeq = 0;
  function fetchBooked() {
    var done = function () { ensureSlot(); renderSlots(); renderSummary(); };
    if (!S.date) return Promise.resolve();
    if (MODE !== 'laravel') { S.booked = []; S.locked = []; done(); return Promise.resolve(); }
    var my = ++fetchSeq; $('#slots-loading').hidden = false;
    return fetch('/booking/booked-slots?date=' + iso(S.date) + '&location_type=' + S.loc, { headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (my !== fetchSeq) return;
        if (d && d.success && Array.isArray(d.booked_slots)) { S.booked = d.booked_slots; S.locked = Array.isArray(d.locked_slots) ? d.locked_slots : []; }
      })
      .catch(noop)
      .then(function () { if (my !== fetchSeq) return; $('#slots-loading').hidden = true; done(); });
  }
  function selectDate(d) { S.date = d; $('#e-when').textContent = ''; renderCal(); return fetchBooked(); }
  function showMonth(step) { S.month = new Date(S.month.getFullYear(), S.month.getMonth() + step, 1); renderCal(); fetchBooked(); }

  // ---------- packages and extras (same hand-offs as the old site) ----------
  function changePack(id) {             // package picked from a list: keep the booking's extras and note them on that card
    S.pack = id; ensureSlot(); S.card[id] = S.addons.slice();
    syncAll(); renderSlots(); $('#e-when').textContent = '';
  }
  function choosePack(id) {             // "Book" on a package card: that card's extras become the booking's extras
    if (S.card[id]) { S.addons = S.card[id].slice(); if (S.addons.length) S.addonsOpen = true; }
    changePack(id);
  }
  function toggle(list, id) { var i = list.indexOf(id); if (i > -1) list.splice(i, 1); else list.push(id); }
  function toggleCardAddon(pack, id) {
    if (!S.card[pack]) S.card[pack] = [];
    toggle(S.card[pack], id);
    if (S.pack === pack) S.addons = S.card[pack].slice();
    syncAll();
  }
  function toggleBookingAddon(id) { toggle(S.addons, id); S.card[S.pack] = S.addons.slice(); syncAll(); }
  function setLoc(type) { S.loc = type; syncAll(); renderCal(); fetchBooked(); }

  // ---------- summary ----------
  function summaryRows() {
    var p = byId(PACKS, S.pack), v = byId(VEHICLES, S.veh);
    var rows = [
      ['Package', p.name + ' · ' + p.time],
      ['Vehicle', v.name],
      ['Where', S.loc === 'mobile' ? 'We come to you' : 'Workshop drop-off'],
      ['When', S.date ? niceDate(S.date) + (S.slot ? ', ' + slotLabel(S.slot) : ', no time chosen') : 'Not chosen yet']
    ];
    if (S.addons.length) rows.splice(2, 0, ['Extras', S.addons.map(function (id) { return byId(ADDONS, id).name; }).join(', ')]);
    return rows;
  }
  function rowsHtml(rows) { return rows.map(function (r) { return '<div class="sum-row"><dt>' + esc(r[0]) + '</dt><dd>' + esc(r[1]) + '</dd></div>'; }).join(''); }
  function renderSummary() {
    $('#sum-list').innerHTML = rowsHtml(summaryRows());
    $('#sum-total').textContent = priceText(total(), S.addons);
    $('#sum-total').style.fontSize = hasFrom(S.addons) ? '1.6rem' : '';
  }

  // ---------- validation (same rules as the old site, shown next to the field) ----------
  var THROWAWAY = ['tempmail.com', 'temp-mail.org', '10minutemail.com', 'mailinator.com', 'guerrillamail.com', 'yopmail.com', 'trashmail.com'];
  function phoneOk(v) {
    var c = (v || '').replace(/[\s\-\(\)\.]/g, '');
    return /^(?:\+?61|0)[2-478]\d{8}$/.test(c) || /^(?:1300\d{6}|1800\d{6}|13\d{4})$/.test(c);
  }
  // Space out mobile numbers as they are typed: 0412 345 678 or +61 4 12 345 678.
  function formatPhone(el) {
    var c = (el.value || '').replace(/[^\d+]/g, ''), parts;
    if (c.indexOf('04') === 0 && c.length <= 10) {
      parts = [c.substring(0, 4)]; if (c.length > 4) parts.push(c.substring(4, 7)); if (c.length > 7) parts.push(c.substring(7, 10));
      el.value = parts.join(' ');
    } else if (c.indexOf('+614') === 0 && c.length <= 12) {
      parts = ['+61 4']; if (c.length > 4) parts.push(c.substring(4, 6)); if (c.length > 6) parts.push(c.substring(6, 9)); if (c.length > 9) parts.push(c.substring(9, 12));
      el.value = parts.join(' ');
    }
  }
  function setErr(input, errEl, msg) {
    errEl.textContent = msg || '';
    if (input) { if (msg) input.setAttribute('aria-invalid', 'true'); else input.removeAttribute('aria-invalid'); }
    return !msg;
  }
  function checkEmail(v, el) {
    v = v.trim().toLowerCase();
    if (!v) return 'Enter your email so we can send the confirmation.';
    if ((el && el.validity && el.validity.typeMismatch) || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return 'That email doesn\'t look right. Check for typos, e.g. you@example.com.';
    if (THROWAWAY.some(function (d) { return v.endsWith('@' + d); })) return 'Temporary email addresses can\'t be used. Please use your regular email.';
    return '';
  }
  function checkPhone(v) {
    if (!v.trim()) return 'Enter a phone number so we can confirm your booking.';
    if (!phoneOk(v)) return 'Enter an Australian number, e.g. 0412 345 678 or (08) 9362 1234.';
    return '';
  }
  var BOOK_RULES = [
    ['#f-car', '#e-car', function (v) { return v.trim() ? '' : 'Tell us the make, model and year, e.g. Toyota Hilux 2023.'; }],
    ['#f-name', '#e-name', function (v) { return v.trim() ? '' : 'Enter your full name.'; }],
    ['#f-phone', '#e-phone', checkPhone],
    ['#f-email', '#e-email', checkEmail],
    ['#f-addr', '#e-addr', function (v) { return S.loc === 'mobile' && !v.trim() ? 'Enter the address where we should come.' : ''; }]
  ];
  function validateBooking() {
    var first = null;
    var whenMsg = !S.slot || slotStatus(S.slot) ? 'That time window isn\'t available. Please choose another time or date.' : '';
    if (!setErr(null, $('#e-when'), whenMsg)) first = $('.slot:not([disabled])') || $('#cal-next');
    BOOK_RULES.forEach(function (r) {
      var el = $(r[0]);
      if (!setErr(el, $(r[1]), r[2](el.value, el)) && !first) first = el;
    });
    return first;
  }

  // ---------- submit ----------
  var turnstile = { booking: '', quote: '' };
  function initTurnstile() {
    if (!CFG.turnstileSiteKey) return;
    (function tryRender() {
      if (!window.turnstile) { setTimeout(tryRender, 400); return; }
      [['booking', '#cf-turnstile-booking'], ['quote', '#cf-turnstile-quote']].forEach(function (x) {
        var el = $(x[1]);
        if (el && !el.hasChildNodes()) window.turnstile.render(x[1], { sitekey: CFG.turnstileSiteKey, callback: function (t) { turnstile[x[0]] = t; } });
      });
    })();
  }
  function reference() {
    var d = new Date();
    return 'AUR-' + String(d.getFullYear()).slice(2) + String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0') + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();
  }
  function bookingPayload() {
    var p = byId(PACKS, S.pack), v = byId(VEHICLES, S.veh);
    return {
      package_name: p.backend, vehicle_type: v.backend,
      vehicle_make_model: $('#f-car').value.trim(), vehicle_plate: $('#f-plate').value.trim().toUpperCase(),
      booking_date: iso(S.date), booking_time: S.slot,
      customer_name: $('#f-name').value.trim(), customer_email: $('#f-email').value.trim(), customer_phone: $('#f-phone').value.trim(),
      service_location_type: S.loc,
      service_address: S.loc === 'mobile' ? $('#f-addr').value.trim() : WORKSHOP_BACKEND,
      special_notes: $('#f-notes').value.trim(), total_price: total(),
      addons: S.addons.map(function (id) { return byId(ADDONS, id).backend; }),
      _hp_company_website: $('#f-hp').value,
      'cf-turnstile-response': turnstile.booking
    };
  }
  function post(url, data) {
    var headers = { 'Content-Type': 'application/json', Accept: 'application/json' };
    if (csrfMeta) headers['X-CSRF-TOKEN'] = csrfMeta.getAttribute('content');
    return fetch(url, { method: 'POST', headers: headers, body: JSON.stringify(data) }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok, data: d }; });
    });
  }
  function mailto(subject, lines) {
    var a = document.createElement('a');
    a.href = 'mailto:' + CFG.email + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
    a.hidden = true; document.body.appendChild(a); a.click(); a.remove();
  }
  var invoiceUrl = '';
  function showDone(ref, sent, booking) {
    var rows = summaryRows(), first = $('#f-name').value.trim().split(' ')[0];
    rows.push(['Total', priceText(total(), S.addons) + ', pay on completion']);
    rows.push(['Address', S.loc === 'mobile' ? $('#f-addr').value.trim() : WORKSHOP]);
    $('#done-h').textContent = sent ? 'Booking request received.' : 'One more step: send the email.';
    $('#done-p').textContent = sent
      ? 'Thanks, ' + first + '. We\'ll contact you shortly to confirm your time. A copy is on its way to your email.'
      : 'Your email app has opened with your booking details filled in. Press send and we\'ll confirm your time. If nothing opened, call us on ' + CFG.phone + ' and quote the reference below.';
    $('#done-ref').textContent = 'Reference ' + ref;
    $('#done-list').innerHTML = rowsHtml(rows);
    invoiceUrl = booking && booking.reference ? (booking.invoice_url || '/booking/' + booking.reference + '/invoice?print=1') : '';
    $('#done-print').hidden = !invoiceUrl;
    // As on the old site: clear the car, plate, notes and address, and check the day's windows again.
    ['#f-car', '#f-plate', '#f-notes', '#f-addr'].forEach(function (s) { $(s).value = ''; });
    $('#book-form').hidden = true; $('#bk-done').hidden = false; $('#bk-done').focus({ preventScroll: true });
    $('#bk-done').scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
    fetchBooked();
  }
  function submitBooking(e) {
    e.preventDefault();
    if (S.submitting) return;
    var alertEl = $('#bk-alert'); alertEl.textContent = '';
    if (!SET.is_shop_open) { alertEl.textContent = SET.shop_closed_notice; return; }
    var bad = validateBooking();
    if (bad) {
      alertEl.textContent = 'A few details need attention. Check the highlighted fields.';
      bad.focus({ preventScroll: true }); bad.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
      return;
    }
    var data = bookingPayload();
    if (data._hp_company_website) return; // bot
    var btn = $('#bk-submit'), ref = reference();
    if (MODE === 'email') {
      mailto('Booking request ' + ref + ': ' + byId(PACKS, S.pack).name + ', ' + niceDate(S.date), [
        'Booking request ' + ref, ''
      ].concat(summaryRows().map(function (x) { return x[0] + ': ' + x[1]; }), [
        'Total: ' + priceText(total(), S.addons) + ' (pay on completion)',
        'Address: ' + (S.loc === 'mobile' ? data.service_address : WORKSHOP), '',
        'Car: ' + data.vehicle_make_model + (data.vehicle_plate ? ' (' + data.vehicle_plate + ')' : ''),
        'Name: ' + data.customer_name, 'Phone: ' + data.customer_phone, 'Email: ' + data.customer_email,
        'Notes: ' + (data.special_notes || 'none')
      ]));
      showDone(ref, false);
      return;
    }
    var label = btn.textContent;
    S.submitting = true; btn.disabled = true; btn.textContent = 'Sending…';
    post(MODE === 'laravel' ? '/booking' : CFG.endpoint, MODE === 'laravel' ? data : Object.assign({ form: 'booking', reference: ref }, data)).then(function (res) {
      if (res.ok && (MODE !== 'laravel' || res.data.success)) {
        showDone((res.data.booking && res.data.booking.reference) || ref, true, res.data.booking);
      } else {
        alertEl.textContent = (res.data && res.data.message) || 'Please check your details and try again, or call ' + CFG.phone + '.';
        fetchBooked();
      }
    }).catch(function () {
      alertEl.textContent = 'We couldn\'t send your booking. Check your connection and try again, or call ' + CFG.phone + '.';
    }).then(function () { S.submitting = false; btn.disabled = false; btn.textContent = label; });
  }

  function submitQuote(e) {
    e.preventDefault();
    var f = { name: $('#q-name'), phone: $('#q-phone'), email: $('#q-email'), msg: $('#q-msg') };
    var first = null;
    [[f.name, '#eq-name', function (v) { return v.trim() ? '' : 'Enter your name.'; }],
     [f.phone, '#eq-phone', function (v) { return v.trim() && !phoneOk(v) ? 'Enter an Australian number, e.g. 0412 345 678.' : ''; }],   // optional, checked only if filled in
     [f.email, '#eq-email', checkEmail],
     [f.msg, '#eq-msg', function (v) { return v.trim() ? '' : 'Tell us about the vehicles and what you need.'; }]
    ].forEach(function (r) { if (!setErr(r[0], $(r[1]), r[2](r[0].value, r[0])) && !first) first = r[0]; });
    $('#qt-alert').textContent = '';
    if (first) { first.focus(); return; }
    if ($('#q-hp').value) return;
    var data = { name: f.name.value.trim(), phone: f.phone.value.trim(), email: f.email.value.trim(), message: f.msg.value.trim(), _hp_company_website: '', 'cf-turnstile-response': turnstile.quote };
    if (MODE === 'email') {
      mailto('Quote request from ' + data.name, ['Quote request', '', 'Name: ' + data.name, 'Phone: ' + (data.phone || 'not given'), 'Email: ' + data.email, '', data.message]);
      $('#quote-ok-h').textContent = 'One more step: send the email.';
      $('#quote-ok-p').textContent = 'Your email app has opened with your request filled in. Press send and we\'ll reply with a price. If nothing opened, call ' + CFG.phone + '.';
      $('#quote-form').hidden = true; $('#quote-ok').hidden = false; $('#quote-ok').focus();
      return;
    }
    var btn = $('#qt-submit'); btn.disabled = true;
    post(MODE === 'laravel' ? '/quote' : CFG.endpoint, MODE === 'laravel' ? data : Object.assign({ form: 'quote' }, data)).then(function (res) {
      if (res.ok && (MODE !== 'laravel' || res.data.success)) {
        toast(res.data.message || 'Quote request sent. We\'ll reply with a price.', 4000);
        [f.name, f.phone, f.email, f.msg].forEach(function (el) { el.value = ''; });
      } else $('#qt-alert').textContent = (res.data && res.data.message) || 'Please complete all required fields, or call ' + CFG.phone + '.';
    }).catch(function () { $('#qt-alert').textContent = 'We couldn\'t send your request. Please call ' + CFG.phone + '.'; })
      .then(function () { btn.disabled = false; });
  }

  // ---------- events ----------
  function toast(msg, ms) {
    var t = $('#toast'); t.textContent = msg; t.dataset.show = 'true';
    clearTimeout(toast.t); toast.t = setTimeout(function () { t.dataset.show = 'false'; }, ms || 2400);
  }
  function bind() {
    document.addEventListener('change', function (e) {
      var t = e.target;
      if (t.name === 'veh-dock' || t.name === 'veh-top') { S.veh = t.value; syncAll(); }
      else if (t.id === 'f-veh') { S.veh = t.value; syncAll(); }
      else if (t.name === 'pack-dock' || t.id === 'f-pack') changePack(t.value);
      else if (t.dataset.cardAddon) toggleCardAddon(t.dataset.pack, t.dataset.cardAddon);
      else if (t.name === 'addon') toggleBookingAddon(t.value);
      else if (t.name === 'loc') setLoc(t.value);
    });
    document.addEventListener('click', function (e) {
      var t = e.target.closest('button, a'); if (!t) return;
      if (t.dataset.book) choosePack(t.dataset.book);
      else if (t.id === 'dock-book') choosePack(S.pack);
      else if (t.dataset.extras) { S.openCard = S.openCard === t.dataset.extras ? null : t.dataset.extras; syncAll(); }   // one card's extras open at a time
      else if (t.id === 'xtras-toggle') { S.addonsOpen = !S.addonsOpen; syncAll(); }
      else if (t.id === 'xtras-clear') { S.addons = []; S.card[S.pack] = []; syncAll(); $('#xtras-toggle').focus(); }
      else if (t.classList.contains('day')) { var p = t.dataset.date.split('-'); selectDate(new Date(+p[0], +p[1] - 1, +p[2])); var again = $('.day[aria-pressed="true"]'); if (again) again.focus(); }
      else if (t.classList.contains('slot')) { S.slot = t.dataset.slot; renderSlots(); renderSummary(); $('#e-when').textContent = ''; var s = $('.slot[aria-pressed="true"]'); if (s) s.focus(); }
      else if (t.id === 'cal-prev') showMonth(-1);
      else if (t.id === 'cal-next') showMonth(1);
      else if (t.id === 'copy-addr') {
        var done = function () { toast('Address copied'); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(WORKSHOP).then(done, function () { toast(WORKSHOP); }); else toast(WORKSHOP);
      }
      else if (t.id === 'done-print') { if (invoiceUrl) window.open(invoiceUrl, '_blank', 'noopener'); }
      else if (t.id === 'done-again') {
        $('#bk-done').hidden = true; $('#book-form').hidden = false;
        $('#booking').scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
      }
    });
    $('#book-form').addEventListener('submit', submitBooking);
    $('#quote-form').addEventListener('submit', submitQuote);
    BOOK_RULES.forEach(function (r) {
      var el = $(r[0]);
      el.addEventListener('blur', function () { if (el.value) setErr(el, $(r[1]), r[2](el.value, el)); });
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid')) setErr(el, $(r[1]), r[2](el.value, el)); });
    });
    ['#f-phone', '#q-phone'].forEach(function (s) { $(s).addEventListener('input', function () { formatPhone(this); }); });

    // nav
    var nav = $('#nav'), tog = $('.nav-toggle');
    tog.addEventListener('click', function () { var o = nav.dataset.open !== 'true'; nav.dataset.open = o; tog.setAttribute('aria-expanded', o); });
    $$('.nav-links a').forEach(function (a) { a.addEventListener('click', function () { nav.dataset.open = 'false'; tog.setAttribute('aria-expanded', 'false'); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.dataset.open === 'true') { nav.dataset.open = 'false'; tog.setAttribute('aria-expanded', 'false'); tog.focus(); } });
    if ('IntersectionObserver' in window) {
      var links = {}; $$('.nav-links a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) { if (en.isIntersecting) { $$('.nav-links a').forEach(function (a) { a.removeAttribute('aria-current'); }); if (links[en.target.id]) links[en.target.id].setAttribute('aria-current', 'true'); } });
      }, { rootMargin: '-45% 0px -50% 0px' });
      Object.keys(links).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
      var bar = $('#bar');
      new IntersectionObserver(function (es) { bar.dataset.hide = es[0].isIntersecting; }, { rootMargin: '-20% 0px -20% 0px' }).observe($('#booking'));
    }
  }

  // ---------- hero: rinse the foam off the car ----------
  // The clean car is an <img>. The foam-covered car is painted on a canvas above it and erased where the
  // pointer sprays. Runs of water keep sliding down after each pass, and spray droplets fly on a second canvas.
  function wash() {
    var hero = $('#hero'), box = $('#wash'), foamCv = $('#foam'), fx = $('#spray'), img = $('#foam-img');
    var ui = $('#rinse'), btn = $('#rinse-btn'), label = $('#rinse-label'), bar = $('#rinse-bar');
    if (!box || !foamCv.getContext) return;
    var fctx = foamCv.getContext('2d'), sctx = fx.getContext('2d');
    var probe = document.createElement('canvas'); probe.width = 48; probe.height = 27;
    var pctx = probe.getContext('2d', { willReadFrequently: true });
    var CAR = { x0: 0.27, x1: 0.97, y0: 0.2, y1: 0.82 }, DONE_AT = 0.6;
    var W = 0, H = 0, dpr = 1, ready = false, state = 'foam', visible = true, touched = false;
    var drips = [], drops = [], raf = 0, last = null, demo = null, sheet = null, fade = null, demoTimer = 0, probeAt = 0;
    var ptr = { x: 0, y: 0, on: false };

    function size() {
      var r = box.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      W = Math.max(1, Math.round(r.width * dpr)); H = Math.max(1, Math.round(r.height * dpr));
      foamCv.width = fx.width = W; foamCv.height = fx.height = H;
    }
    function paintFoam(alpha) {
      fctx.globalCompositeOperation = 'source-over'; fctx.clearRect(0, 0, W, H);
      fctx.globalAlpha = alpha; fctx.drawImage(img, 0, 0, W, H); fctx.globalAlpha = 1;
    }
    function erase(x, y, r, strength) {
      var g = fctx.createRadialGradient(x, y, r * 0.2, x, y, r);
      g.addColorStop(0, 'rgba(0,0,0,' + strength + ')'); g.addColorStop(1, 'rgba(0,0,0,0)');
      fctx.globalCompositeOperation = 'destination-out'; fctx.fillStyle = g;
      fctx.beginPath(); fctx.arc(x, y, r, 0, 6.2832); fctx.fill();
    }
    function brush() { return Math.max(44 * dpr, W * 0.07) * (demo ? 0.62 : 1); }
    function spray(x, y, n) {
      for (var k = 0; k < n; k++) {
        var a = Math.random() * 6.2832, sp = (1 + Math.random() * 4.5) * dpr, life = 16 + Math.random() * 24;
        drops.push({ x: x, y: y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 1.6 * dpr, life: life, max: life, s: (0.7 + Math.random() * 1.7) * dpr });
      }
      if (drops.length > 420) drops.splice(0, drops.length - 420);
    }
    function stroke(x0, y0, x1, y1) {
      var r = brush(), n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / (r * 0.3)));
      for (var i = 1; i <= n; i++) {
        var t = i / n, x = x0 + (x1 - x0) * t, y = y0 + (y1 - y0) * t;
        erase(x, y, r, 0.85);
        if (reduced) continue;
        if (Math.random() < (demo ? 0.22 : 0.38)) drips.push({ x: x + (Math.random() - 0.5) * r * 1.3, y: y + r * 0.3, vy: (2 + Math.random() * 3.5) * dpr, r: (4 + Math.random() * 7) * dpr, life: (demo ? 26 : 40) + Math.random() * (demo ? 36 : 70) });
        spray(x, y, 3);
      }
      if (drips.length > 170) drips.splice(0, drips.length - 170);
      kick();
    }
    function setProgress(p) { bar.style.setProperty('--p', Math.max(0, Math.min(1, p)).toFixed(3)); }
    function setState(s) {
      state = s; ui.dataset.state = s === 'clean' ? 'clean' : 'foam';
      label.textContent = s === 'clean' ? 'Foam it again' : 'Rinse the car';
      if (s === 'clean') setProgress(1);
    }
    function measure() {
      pctx.clearRect(0, 0, 48, 27); pctx.drawImage(foamCv, 0, 0, 48, 27);
      var x = Math.round(CAR.x0 * 48), y = Math.round(CAR.y0 * 27), w = Math.round((CAR.x1 - CAR.x0) * 48), h = Math.round((CAR.y1 - CAR.y0) * 27);
      var d = pctx.getImageData(x, y, w, h).data, sum = 0;
      for (var i = 3; i < d.length; i += 4) sum += d[i];
      var cleared = 1 - sum / (d.length / 4 * 255);
      setProgress(cleared / DONE_AT);
      if (cleared >= DONE_AT && !demo && touched) finish();
    }
    // A sheet of water runs across and takes the rest of the foam with it.
    function finish() {
      if (state !== 'foam') return;
      demo = null; clearTimeout(demoTimer);
      if (reduced) { fctx.clearRect(0, 0, W, H); drips = []; setState('clean'); return; }
      state = 'sheet'; sheet = { t0: performance.now(), dur: 800 }; kick();
    }
    function refoam() {
      drips = []; drops = []; setProgress(0); touched = true;
      if (reduced) { paintFoam(1); setState('foam'); return; }
      state = 'fade'; ui.dataset.state = 'foam'; label.textContent = 'Rinse the car';
      fade = { t0: performance.now(), dur: 650 }; kick();
    }
    function armDemo() {
      clearTimeout(demoTimer);
      if (reduced) return;
      demoTimer = setTimeout(function () {
        if (touched || state !== 'foam' || !visible) return;
        demo = { t0: performance.now(), dur: 2200, last: null }; kick();
      }, 1300);
    }
    function demoPoint(t) {
      var e = t * t * (3 - 2 * t);
      return { x: (0.41 + 0.36 * e) * W, y: (0.47 + 0.035 * Math.sin(t * Math.PI * 2)) * H };
    }
    function kick() { if (!raf) raf = requestAnimationFrame(frame); }
    function frame(now) {
      raf = 0;
      var busy = false, i, d, t, x;
      if (demo) {
        t = (now - demo.t0) / demo.dur;
        if (t >= 1 || state !== 'foam') { demo = null; ptr.on = false; }
        else { var p = demoPoint(t); if (demo.last) stroke(demo.last.x, demo.last.y, p.x, p.y); demo.last = p; ptr.x = p.x; ptr.y = p.y; ptr.on = true; busy = true; }
      }
      if (sheet) {
        t = Math.min(1, (now - sheet.t0) / sheet.dur); x = (-0.05 + 1.35 * t) * W;
        var band = W * 0.28, g = fctx.createLinearGradient(x - band, 0, x, 0);
        g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)');
        fctx.globalCompositeOperation = 'destination-out';
        fctx.fillStyle = '#000'; fctx.fillRect(0, 0, Math.max(0, x - band), H);
        fctx.fillStyle = g; fctx.fillRect(x - band, 0, band, H);
        for (i = 0; i < 5; i++) spray(x - band * 0.4, (CAR.y0 + Math.random() * (CAR.y1 - CAR.y0)) * H, 2);
        if (t >= 1) { sheet = null; drips = []; fctx.clearRect(0, 0, W, H); setState('clean'); }
        busy = true;
      }
      if (fade) {
        t = Math.min(1, (now - fade.t0) / fade.dur); paintFoam(t);
        if (t >= 1) { fade = null; setState('foam'); touched = false; armDemo(); }
        busy = true;
      }
      for (i = drips.length - 1; i >= 0; i--) {
        d = drips[i]; d.y += d.vy; d.vy *= 0.975; d.r *= 0.993; d.life--;
        if (state === 'foam') erase(d.x, d.y, d.r, 0.9);
        if (d.life <= 0 || d.y > H) drips.splice(i, 1);
      }
      sctx.clearRect(0, 0, W, H);
      for (i = drops.length - 1; i >= 0; i--) {
        d = drops[i]; d.x += d.vx; d.y += d.vy; d.vy += 0.2 * dpr; d.life--;
        if (d.life <= 0) { drops.splice(i, 1); continue; }
        sctx.fillStyle = 'rgba(220,248,252,' + (d.life / d.max * 0.9).toFixed(3) + ')';
        sctx.beginPath(); sctx.arc(d.x, d.y, d.s, 0, 6.2832); sctx.fill();
      }
      if (ptr.on && state === 'foam') {         // the lance: a soft fan of water where the pointer is
        var r = brush() * 0.5, fan = sctx.createRadialGradient(ptr.x, ptr.y, 0, ptr.x, ptr.y, r);
        fan.addColorStop(0, 'rgba(220,248,252,0.20)'); fan.addColorStop(1, 'rgba(220,248,252,0)');
        sctx.fillStyle = fan; sctx.beginPath(); sctx.arc(ptr.x, ptr.y, r, 0, 6.2832); sctx.fill();
        sctx.strokeStyle = 'rgba(220,248,252,0.7)'; sctx.lineWidth = 1.5 * dpr;
        sctx.beginPath(); sctx.arc(ptr.x, ptr.y, r * 0.8, 0, 6.2832); sctx.stroke();
      }
      if (state === 'foam' && now - probeAt > 260 && (drips.length || demo || touched)) { probeAt = now; measure(); }
      if ((busy || drips.length || drops.length) && !raf) raf = requestAnimationFrame(frame);
    }

    function pos(e) { var r = box.getBoundingClientRect(); return { x: (e.clientX - r.left) * dpr, y: (e.clientY - r.top) * dpr }; }
    function lift() { last = null; if (ptr.on) { ptr.on = false; kick(); } }
    function onMove(e) {
      if (!ready || state !== 'foam' || !e.isPrimary) return;
      if (e.target.closest && e.target.closest('.dock, .rinse-btn, a')) { lift(); return; }   // using the controls should not spray
      var p = pos(e);
      demo = null; clearTimeout(demoTimer); touched = true;
      if (last && Math.hypot(p.x - last.x, p.y - last.y) < W * 0.4) stroke(last.x, last.y, p.x, p.y); else stroke(p.x, p.y, p.x, p.y);
      last = p; ptr.x = p.x; ptr.y = p.y; ptr.on = true; kick();
    }
    hero.addEventListener('pointermove', onMove);
    hero.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') { last = null; onMove(e); } });
    ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (n) { hero.addEventListener(n, lift); });
    btn.addEventListener('click', function () { if (!ready) return; if (state === 'clean') refoam(); else if (state === 'foam') { touched = true; finish(); } });

    var resizeT = 0;
    window.addEventListener('resize', function () {
      clearTimeout(resizeT);
      resizeT = setTimeout(function () {
        if (!ready) return;
        var w = W; size(); if (W === w) return;
        drips = []; drops = []; sheet = null; fade = null;
        if (state === 'clean') fctx.clearRect(0, 0, W, H); else { paintFoam(1); setState('foam'); setProgress(0); }
      }, 150);
    });
    function start() {
      size(); paintFoam(1); box.dataset.ready = 'true'; ready = true;
      if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(hero);
      armDemo();
    }
    if (img.complete && img.naturalWidth) start(); else img.addEventListener('load', start, { once: true });
  }

  // ---------- our work: four short clips, one screen, plays on its own ----------
  function work() {
    var v = $('#work-video'); if (!v) return;
    var tabs = $$('.work-tab'), play = $('#work-play'), cue = $('#work-cue'), desc = $('#work-desc'), panel = $('#work-panel');
    var i = 0, loops = 0, LOOPS = 2, auto = !reduced, visible = false;
    function playUI() { play.dataset.playing = auto; play.setAttribute('aria-label', auto ? 'Pause footage' : 'Play footage'); }
    function go() { if (auto && visible) { var p = v.play(); if (p && p.catch) p.catch(noop); } else v.pause(); }
    function show(k) {
      i = k; loops = 0;
      tabs.forEach(function (t, j) { t.setAttribute('aria-selected', j === k); t.tabIndex = j === k ? 0 : -1; });
      panel.setAttribute('aria-labelledby', tabs[k].id);
      desc.textContent = $('span', tabs[k]).textContent;
      cue.style.setProperty('--p', 0);
      v.poster = 'assets/video/work-' + (k + 1) + '.jpg'; v.src = 'assets/video/work-' + (k + 1) + '.mp4';
      go();
    }
    v.addEventListener('ended', function () {
      if (!auto) return;
      loops++;
      if (loops < LOOPS) { v.currentTime = 0; go(); } else show((i + 1) % tabs.length);
    });
    v.addEventListener('timeupdate', function () { cue.style.setProperty('--p', ((loops + v.currentTime / (v.duration || 1)) / LOOPS).toFixed(3)); });
    tabs.forEach(function (t, j) {
      t.addEventListener('click', function () { show(j); });
      t.addEventListener('keydown', function (e) {
        var step = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (!step) return;
        e.preventDefault(); var n = (j + step + tabs.length) % tabs.length; show(n); tabs[n].focus();
      });
    });
    play.addEventListener('click', function () { auto = !auto; playUI(); if (auto && v.ended) { v.currentTime = 0; } go(); });
    desc.textContent = $('span', tabs[0]).textContent; playUI();
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; go(); }, { threshold: 0.35 }).observe(panel);
    else { visible = true; go(); }
  }

  // ---------- init ----------
  if ($('#packs')) {
    renderDock(); renderVehSeg(); renderPacks(); renderBookingOptions();
    renderCal(); syncAll(); fetchBooked(); bind(); initTurnstile();
    if (!SET.is_shop_open) { var sc = $('#shop-closed'); sc.textContent = SET.shop_closed_notice; sc.hidden = false; $('#bk-submit').disabled = true; }
    if (MODE === 'email') $('#bk-submit').textContent = 'Send booking request';
    wash(); work();
  }
})();
