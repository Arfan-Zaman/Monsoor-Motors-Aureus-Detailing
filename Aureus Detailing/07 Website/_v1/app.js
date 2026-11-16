/* Aureus Detailing: packages, booking, quote, hero tunnel, scroll footage. No dependencies. */
(function () {
  'use strict';

  // ---------- config ----------
  // When this site is served by the existing Laravel app, the page carries a csrf-token meta tag
  // and the forms post to its routes. Otherwise set AUREUS.endpoint to a JSON form endpoint,
  // or leave it empty to fall back to a prefilled email.
  var CFG = Object.assign({ endpoint: '', email: 'carwashandpolish.wa@gmail.com', phone: '0434 13 73 93' }, window.AUREUS || {});
  var csrfMeta = document.querySelector('meta[name="csrf-token"]');
  var MODE = csrfMeta ? 'laravel' : (CFG.endpoint ? 'endpoint' : 'email');

  var PACKS = [
    { id: 'silver', name: 'Silver', backend: 'Level 1: Express', price: 149, time: '1 h 30 min', tag: 'Fast and clean',
      slots: ['08:30 AM - 10:00 AM', '10:00 AM - 11:30 AM', '11:30 AM - 01:00 PM', '01:00 PM - 02:30 PM', '02:30 PM - 04:00 PM', '04:00 PM - 05:30 PM'],
      items: ['Exterior snow foam hand wash', 'Wheel and rim deep clean', 'Tyre dressing and gloss shine', 'Exterior windows and mirrors', 'Cabin vacuum: seats, carpet and boot', 'Dashboard, console and trim wipe', 'Door jambs wiped'] },
    { id: 'gold', name: 'Gold', backend: 'Level 2: Premium', price: 199, time: '2 h 30 min', tag: 'Most popular',
      slots: ['08:30 AM - 11:00 AM', '11:00 AM - 01:30 PM', '01:30 PM - 04:00 PM', '04:00 PM - 06:30 PM'],
      items: ['Everything in Silver, plus polish', 'Wax paint sealant', 'Deep interior antibacterial steam clean', 'Full leather clean and condition', 'Air vent disinfection and deodoriser', 'AC vent brush detailing'] },
    { id: 'aureus', name: 'Aureus', backend: 'Level 3: Ultimate', price: 299, time: '4 hours', tag: 'Showroom finish',
      slots: ['08:30 AM - 12:30 PM', '01:00 PM - 05:00 PM'],
      items: ['Everything in Gold, plus ceramic sealant', 'Clay bar paint decontamination', 'Hydrophobic 6-month ceramic shield', 'Deep leather protection treatment', 'Hot water extraction shampoo: seats and mats', 'Headlight restoration and UV coat', 'High-gloss machine polish', 'Iron and tar removal'] }
  ];
  var VEHICLES = [
    { id: 'sedan', name: 'Sedan / Hatch', backend: 'Sedan / Hatchback', add: 0, eg: 'Corolla, Civic, Camry, Model 3' },
    { id: 'suv', name: 'SUV / 4WD / Ute', backend: 'SUV / 4WD / Wagon', add: 20, eg: 'Prado, RAV4, Hilux, Ranger, CX-5' },
    { id: 'van', name: 'Van / Commercial', backend: 'Van / Large Truck / Commercial', add: 40, eg: 'HiAce, Transit, LandCruiser 300, 7+ seats' }
  ];
  var ADDONS = [
    { id: 'headlights', name: 'Headlight restoration', price: 60, text: 'Multi-stage wet sanding and a UV sealant bring cloudy, yellowed headlights back to clear.' },
    { id: 'engine', name: 'Engine bay clean', price: 60, text: 'Gentle degreasing, steam cleaning and a satin dressing for engine bay plastics and hoses.' },
    { id: 'one-step', name: 'One-step paint correction', price: 120, text: 'A single-stage machine polish that removes 50 to 65% of light swirl marks, haze and oxidation.' },
    { id: 'two-step', name: 'Two-step paint correction', price: 200, text: 'A heavy compound cut, then an ultrafine finishing polish, removing 85 to 95% of deeper scratches and swirls.' },
    { id: 'ceramic', name: 'Ceramic coating', price: 699, from: true, text: 'Multi-year 9H nano-ceramic protection with a deep gloss finish. Priced per car after inspection.' }
  ];
  var WORKSHOP = '530 Albany Hwy, Victoria Park WA 6100';
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  var S = { pack: 'gold', veh: 'sedan', loc: 'mobile', date: null, slot: null, addons: {}, month: null, booked: [], submitting: false };

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var money = function (n) { return '$' + n.toLocaleString('en-AU'); };
  var byId = function (list, id) { return list.filter(function (x) { return x.id === id; })[0]; };
  var icon = function (n) { return '<svg aria-hidden="true"><use href="#i-' + n + '"/></svg>'; };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function packPrice(p) { return p.price + byId(VEHICLES, S.veh).add; }
  function addonTotal() { return ADDONS.reduce(function (t, a) { return t + (S.addons[a.id] ? a.price : 0); }, 0); }
  function total() { return packPrice(byId(PACKS, S.pack)) + addonTotal(); }
  function hasFrom() { return !!S.addons.ceramic; }

  // ---------- render: packages section ----------
  function renderVehSeg() {
    $('#veh-seg').innerHTML = VEHICLES.map(function (v) {
      return '<label><input type="radio" name="veh-top" value="' + v.id + '"' + (v.id === S.veh ? ' checked' : '') + '><span>' + esc(v.name) + (v.add ? '<small>+' + money(v.add) + '</small>' : '') + '</span></label>';
    }).join('');
  }
  function renderPacks() {
    $('#packs').innerHTML = PACKS.map(function (p) {
      var open = p.id === S.pack;
      return '<article class="pack" data-id="' + p.id + '" data-open="' + open + '">' +
        '<button class="pack-top" type="button" aria-expanded="' + open + '" aria-controls="pb-' + p.id + '">' +
          '<span class="pack-name"><h3>' + p.name + '</h3><span class="pack-tag">' + esc(p.tag) + '</span></span>' +
          '<span class="pack-price"><b data-price="' + p.id + '">' + money(packPrice(p)) + '</b><span>' + p.time + '</span></span>' +
        '</button>' +
        '<div class="pack-body" id="pb-' + p.id + '"><div>' +
          '<ul class="pack-list">' + p.items.map(function (i) { return '<li>' + icon('check') + '<span>' + esc(i) + '</span></li>'; }).join('') + '</ul>' +
          '<div class="pack-actions"><a class="btn btn-pink" href="#booking" data-book="' + p.id + '">Book ' + p.name + ' ' + icon('arrow') + '</a></div>' +
        '</div></div>' +
        '<p class="pack-hint" aria-hidden="true">' + icon('plus') + ' See what\'s included</p>' +
      '</article>';
    }).join('');
  }
  function renderAddonList() {
    $('#addon-list').innerHTML = ADDONS.map(function (a) {
      return '<li class="addon"><div><h4>' + esc(a.name) + '</h4><p>' + esc(a.text) + '</p></div>' +
        '<div class="addon-price">' + (a.from ? '<small>from</small>' : '') + money(a.price) + '</div>' +
        '<button class="chip" type="button" data-addon="' + a.id + '" aria-pressed="' + !!S.addons[a.id] + '">' +
          '<span class="off" style="display:contents">' + icon('plus') + '</span><svg class="on" aria-hidden="true"><use href="#i-check"/></svg>' +
          '<span data-chip-label>' + (S.addons[a.id] ? 'Added' : 'Add to booking') + '</span></button></li>';
    }).join('');
    syncChips();
  }
  function syncChips() {
    $$('[data-addon]').forEach(function (b) {
      var on = !!S.addons[b.dataset.addon];
      b.setAttribute('aria-pressed', on);
      $('[data-chip-label]', b).textContent = on ? 'Added' : 'Add to booking';
      var off = $('.off', b); if (off) off.style.display = on ? 'none' : 'contents';
    });
  }

  // ---------- render: booking options ----------
  function renderBookingOptions() {
    $('#bk-packs').innerHTML = PACKS.map(function (p) {
      return '<label class="opt"><input type="radio" name="pack" value="' + p.id + '"' + (p.id === S.pack ? ' checked' : '') + '><span><b>' + p.name + ' <span data-price="' + p.id + '">' + money(packPrice(p)) + '</span></b><small>' + p.time + ' · ' + esc(p.tag) + '</small></span></label>';
    }).join('');
    $('#bk-veh').innerHTML = VEHICLES.map(function (v) {
      return '<label class="opt"><input type="radio" name="veh" value="' + v.id + '"' + (v.id === S.veh ? ' checked' : '') + '><span><b>' + esc(v.name) + (v.add ? ' +' + money(v.add) : '') + '</b><small>' + esc(v.eg) + '</small></span></label>';
    }).join('');
    $('#bk-addons').innerHTML = ADDONS.map(function (a) {
      return '<label class="opt"><input type="checkbox" name="addon" value="' + a.id + '"' + (S.addons[a.id] ? ' checked' : '') + '><span><b>' + esc(a.name) + '</b><em>' + (a.from ? 'from ' : '+') + money(a.price) + '</em></span></label>';
    }).join('');
  }

  function syncAll() {
    $$('[data-price]').forEach(function (el) { el.textContent = money(packPrice(byId(PACKS, el.dataset.price))); });
    $$('.pack').forEach(function (el) {
      var open = el.dataset.id === S.pack;
      el.dataset.open = open; $('.pack-top', el).setAttribute('aria-expanded', open);
    });
    $$('input[name="veh-top"], input[name="veh"]').forEach(function (i) { i.checked = i.value === S.veh; });
    $$('input[name="pack"]').forEach(function (i) { i.checked = i.value === S.pack; });
    $$('input[name="addon"]').forEach(function (i) { i.checked = !!S.addons[i.value]; });
    $$('input[name="loc"]').forEach(function (i) { i.checked = i.value === S.loc; });
    $('#addr-field').hidden = S.loc !== 'mobile';
    syncChips();
    renderSummary();
  }

  // ---------- calendar and slots ----------
  var today = new Date(); today.setHours(0, 0, 0, 0);
  var lastDay = new Date(today.getFullYear(), today.getMonth() + 3, today.getDate());
  S.month = new Date(today.getFullYear(), today.getMonth(), 1);
  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function niceDate(d) { return d.toLocaleDateString('en-AU', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }); }
  function slotStart(slot, d) {
    var m = /^(\d{2}):(\d{2}) (AM|PM)/.exec(slot); var h = +m[1] % 12 + (m[3] === 'PM' ? 12 : 0);
    var t = new Date(d); t.setHours(h, +m[2], 0, 0); return t;
  }
  function slotLabel(slot) { return slot.replace(/(^|\s)0(\d:)/g, '$1$2').replace(/ AM/g, ' am').replace(/ PM/g, ' pm').replace(' - ', ' to '); }
  function openSlots(d) {
    var now = new Date();
    return byId(PACKS, S.pack).slots.filter(function (s) { return slotStart(s, d) > now && S.booked.indexOf(s) < 0; });
  }
  function dayHasSlots(d) {
    var now = new Date();
    return byId(PACKS, S.pack).slots.some(function (s) { return slotStart(s, d) > now; });
  }

  function renderCal() {
    var y = S.month.getFullYear(), m = S.month.getMonth();
    $('#cal-title').textContent = MONTHS[m] + ' ' + y;
    $('#cal-prev').disabled = S.month <= new Date(today.getFullYear(), today.getMonth(), 1);
    $('#cal-next').disabled = new Date(y, m + 1, 1) > lastDay;
    var html = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'].map(function (d) { return '<div class="cal-dow" aria-hidden="true">' + d + '</div>'; }).join('');
    var lead = (new Date(y, m, 1).getDay() + 6) % 7;
    for (var i = 0; i < lead; i++) html += '<span></span>';
    var days = new Date(y, m + 1, 0).getDate();
    for (var d = 1; d <= days; d++) {
      var dt = new Date(y, m, d);
      var off = dt < today || dt > lastDay || !dayHasSlots(dt);
      var sel = S.date && iso(S.date) === iso(dt);
      html += '<button type="button" class="day" data-date="' + iso(dt) + '"' + (off ? ' disabled' : '') + ' aria-pressed="' + !!sel + '"' +
        (iso(dt) === iso(today) ? ' data-today="true"' : '') + ' aria-label="' + niceDate(dt) + (off ? ', unavailable' : '') + '">' + d + '</button>';
    }
    $('#cal-grid').innerHTML = html;
  }
  function renderSlots() {
    var box = $('#slots'), label = $('#slots-label');
    if (!S.date) { label.textContent = 'Choose a date to see times'; box.innerHTML = ''; return; }
    label.textContent = 'Times on ' + niceDate(S.date);
    var now = new Date(), all = byId(PACKS, S.pack).slots;
    var free = openSlots(S.date);
    if (S.slot && free.indexOf(S.slot) < 0) S.slot = null;
    if (!free.length) { box.innerHTML = '<p class="slots-empty">No times left on this day. Please pick another date.</p>'; return; }
    box.innerHTML = all.map(function (s) {
      var gone = slotStart(s, S.date) <= now || S.booked.indexOf(s) >= 0;
      return '<button type="button" class="slot" data-slot="' + s + '"' + (gone ? ' disabled aria-label="' + slotLabel(s) + ', unavailable"' : '') + ' aria-pressed="' + (S.slot === s) + '">' + slotLabel(s) + '</button>';
    }).join('');
  }
  function loadBooked() {
    S.booked = [];
    if (MODE !== 'laravel' || !S.date) return Promise.resolve();
    return fetch('/booking/booked-slots?date=' + iso(S.date) + '&location_type=' + S.loc, { headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (d) { if (d && d.success) S.booked = [].concat(d.booked_slots || [], d.locked_slots || []); })
      .catch(function () { /* availability check failed: the team confirms by phone */ });
  }
  function pickDate(d) {
    S.date = d; S.slot = null; renderCal(); renderSlots(); renderSummary();
    loadBooked().then(function () { renderSlots(); renderSummary(); });
    $('#e-when').textContent = '';
  }

  // ---------- summary ----------
  function summaryRows() {
    var p = byId(PACKS, S.pack), v = byId(VEHICLES, S.veh);
    var adds = ADDONS.filter(function (a) { return S.addons[a.id]; });
    var rows = [
      ['Package', p.name + ' · ' + p.time],
      ['Vehicle', v.name],
      ['Where', S.loc === 'mobile' ? 'We come to you' : 'Workshop drop-off'],
      ['When', S.date ? niceDate(S.date) + (S.slot ? ', ' + slotLabel(S.slot) : '') : 'Not chosen yet']
    ];
    if (adds.length) rows.splice(2, 0, ['Add-ons', adds.map(function (a) { return a.name; }).join(', ')]);
    return rows;
  }
  function rowsHtml(rows) { return rows.map(function (r) { return '<div class="sum-row"><dt>' + esc(r[0]) + '</dt><dd>' + esc(r[1]) + '</dd></div>'; }).join(''); }
  function renderSummary() {
    $('#sum-list').innerHTML = rowsHtml(summaryRows());
    $('#sum-total').textContent = (hasFrom() ? 'from ' : '') + money(total());
    $('#sum-total').style.fontSize = hasFrom() ? '1.6rem' : '';
  }

  // ---------- validation ----------
  var RE_EMAIL = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;
  var RE_PHONE = /^(?:\+?61|0)[2-478](?:[ -]?\d){8}$/;
  var THROWAWAY = ['tempmail.com', 'temp-mail.org', '10minutemail.com', 'mailinator.com', 'guerrillamail.com', 'yopmail.com', 'trashmail.com'];
  function setErr(input, errEl, msg) {
    errEl.textContent = msg || '';
    if (input) { if (msg) input.setAttribute('aria-invalid', 'true'); else input.removeAttribute('aria-invalid'); }
    return !msg;
  }
  function checkEmail(v) {
    v = v.trim().toLowerCase();
    if (!v) return 'Enter your email so we can send the confirmation.';
    if (!RE_EMAIL.test(v)) return 'That email doesn\'t look right. Check for typos, e.g. you@example.com.';
    if (THROWAWAY.some(function (d) { return v.endsWith('@' + d); })) return 'Temporary email addresses can\'t be used. Please use your regular email.';
    return '';
  }
  function checkPhone(v) {
    v = v.trim();
    if (!v) return 'Enter a phone number so we can confirm your booking.';
    if (!RE_PHONE.test(v)) return 'Enter an Australian number, e.g. 0412 345 678.';
    return '';
  }
  var BOOK_RULES = [
    ['#f-addr', '#e-addr', function (v) { return S.loc === 'mobile' && v.trim().length < 6 ? 'Enter the address where we should come.' : ''; }],
    ['#f-car', '#e-car', function (v) { return v.trim().length < 3 ? 'Tell us the make and model, e.g. Toyota RAV4 2019.' : ''; }],
    ['#f-name', '#e-name', function (v) { return v.trim().length < 2 ? 'Enter your name.' : ''; }],
    ['#f-phone', '#e-phone', checkPhone],
    ['#f-email', '#e-email', checkEmail]
  ];
  function validateBooking() {
    var first = null;
    var whenOk = setErr(null, $('#e-when'), !S.date ? 'Choose a date.' : (!S.slot ? 'Choose a time.' : ''));
    BOOK_RULES.forEach(function (r) {
      var el = $(r[0]);
      if (!setErr(el, $(r[1]), r[2](el.value)) && !first) first = el;
    });
    if (!whenOk) { var w = $('#cal'); if (!first || (w.compareDocumentPosition(first) & Node.DOCUMENT_POSITION_FOLLOWING)) first = S.date ? $('.slot:not([disabled])') || w : $('.day:not([disabled])') || w; }
    return first;
  }

  // ---------- submit ----------
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
      service_address: S.loc === 'mobile' ? $('#f-addr').value.trim() : WORKSHOP + ' (Physical Workshop)',
      special_notes: $('#f-notes').value.trim(), total_price: total(),
      addons: ADDONS.filter(function (a) { return S.addons[a.id]; }).map(function (a) { return a.name; }),
      _hp_company_website: $('#f-hp').value
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
  function showDone(ref, sent) {
    var rows = summaryRows();
    rows.push(['Total', (hasFrom() ? 'from ' : '') + money(total()) + ', pay on completion']);
    if (S.loc === 'mobile') rows.push(['Address', $('#f-addr').value.trim()]);
    $('#done-h').textContent = sent ? 'Booking request received.' : 'One more step: send the email.';
    $('#done-p').textContent = sent
      ? 'Thanks, ' + $('#f-name').value.trim().split(' ')[0] + '. We\'ll contact you shortly to confirm your time. A copy is on its way to your email.'
      : 'Your email app has opened with your booking details filled in. Press send and we\'ll confirm your time. If nothing opened, call us on ' + CFG.phone + ' and quote the reference below.';
    $('#done-ref').textContent = 'Reference ' + ref;
    $('#done-list').innerHTML = rowsHtml(rows);
    $('#book-form').hidden = true; $('#bk-done').hidden = false; $('#bk-done').focus({ preventScroll: true });
    $('#bk-done').scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
  }
  function submitBooking(e) {
    e.preventDefault();
    if (S.submitting) return;
    $('#bk-alert').textContent = '';
    var bad = validateBooking();
    if (bad) {
      $('#bk-alert').textContent = 'A few details are missing. Check the highlighted fields.';
      bad.focus({ preventScroll: true }); bad.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
      return;
    }
    var data = bookingPayload();
    if (data._hp_company_website) return; // bot
    var btn = $('#bk-submit'), ref = reference();
    if (MODE === 'email') {
      var r = summaryRows();
      mailto('Booking request ' + ref + ': ' + byId(PACKS, S.pack).name + ', ' + niceDate(S.date), [
        'Booking request ' + ref, ''
      ].concat(r.map(function (x) { return x[0] + ': ' + x[1]; }), [
        'Total: ' + (hasFrom() ? 'from ' : '') + money(total()) + ' (pay on completion)',
        'Address: ' + data.service_address, '',
        'Car: ' + data.vehicle_make_model + (data.vehicle_plate ? ' (' + data.vehicle_plate + ')' : ''),
        'Name: ' + data.customer_name, 'Phone: ' + data.customer_phone, 'Email: ' + data.customer_email,
        'Notes: ' + (data.special_notes || 'none')
      ]));
      showDone(ref, false);
      return;
    }
    S.submitting = true; btn.disabled = true; btn.textContent = 'Sending…';
    post(MODE === 'laravel' ? '/booking' : CFG.endpoint, Object.assign({ form: 'booking', reference: ref }, data)).then(function (res) {
      if (res.ok && (MODE !== 'laravel' || res.data.success)) {
        showDone((res.data.booking && res.data.booking.reference) || ref, true);
      } else {
        $('#bk-alert').textContent = (res.data && res.data.message) || 'We couldn\'t send your booking. Try again, or call ' + CFG.phone + '.';
        loadBooked().then(renderSlots);
      }
    }).catch(function () {
      $('#bk-alert').textContent = 'No connection. Check your internet and try again, or call ' + CFG.phone + '.';
    }).then(function () { S.submitting = false; btn.disabled = false; btn.textContent = 'Confirm booking'; });
  }

  function submitQuote(e) {
    e.preventDefault();
    var f = { name: $('#q-name'), phone: $('#q-phone'), email: $('#q-email'), msg: $('#q-msg') };
    var first = null;
    [[f.name, '#eq-name', function (v) { return v.trim().length < 2 ? 'Enter your name.' : ''; }],
     [f.phone, '#eq-phone', checkPhone], [f.email, '#eq-email', checkEmail],
     [f.msg, '#eq-msg', function (v) { return v.trim().length < 10 ? 'Tell us a little about the vehicles and what you need.' : ''; }]
    ].forEach(function (r) { if (!setErr(r[0], $(r[1]), r[2](r[0].value)) && !first) first = r[0]; });
    $('#qt-alert').textContent = '';
    if (first) { first.focus(); return; }
    if ($('#q-hp').value) return;
    var data = { name: f.name.value.trim(), phone: f.phone.value.trim(), email: f.email.value.trim(), message: f.msg.value.trim(), _hp_company_website: '' };
    var ok = function (sent) {
      $('#quote-ok-h').textContent = sent ? 'Quote request sent.' : 'One more step: send the email.';
      $('#quote-ok-p').textContent = sent ? 'Thanks, ' + data.name.split(' ')[0] + '. We\'ll reply with a price as soon as we can.'
        : 'Your email app has opened with your request filled in. Press send and we\'ll reply with a price. If nothing opened, call ' + CFG.phone + '.';
      $('#quote-form').hidden = true; $('#quote-ok').hidden = false; $('#quote-ok').focus();
    };
    if (MODE === 'email') {
      mailto('Quote request from ' + data.name, ['Quote request', '', 'Name: ' + data.name, 'Phone: ' + data.phone, 'Email: ' + data.email, '', data.message]);
      ok(false); return;
    }
    var btn = $('#qt-submit'); btn.disabled = true;
    post(MODE === 'laravel' ? '/quote' : CFG.endpoint, Object.assign({ form: 'quote' }, data)).then(function (res) {
      if (res.ok && (MODE !== 'laravel' || res.data.success !== false)) ok(true);
      else $('#qt-alert').textContent = (res.data && res.data.message) || 'We couldn\'t send your request. Try again, or call ' + CFG.phone + '.';
    }).catch(function () { $('#qt-alert').textContent = 'No connection. Check your internet and try again, or call ' + CFG.phone + '.'; })
      .then(function () { btn.disabled = false; });
  }

  // ---------- events ----------
  function toast(msg) {
    var t = $('#toast'); t.textContent = msg; t.dataset.show = 'true';
    clearTimeout(toast.t); toast.t = setTimeout(function () { t.dataset.show = 'false'; }, 2400);
  }
  function setPack(id) { S.pack = id; S.slot = null; syncAll(); renderCal(); renderSlots(); renderSummary(); }
  function bind() {
    document.addEventListener('change', function (e) {
      var t = e.target;
      if (t.name === 'veh-top' || t.name === 'veh') { S.veh = t.value; syncAll(); }
      else if (t.name === 'pack') setPack(t.value);
      else if (t.name === 'addon') { S.addons[t.value] = t.checked; syncAll(); }
      else if (t.name === 'loc') { S.loc = t.value; syncAll(); if (S.date) loadBooked().then(renderSlots); }
    });
    document.addEventListener('click', function (e) {
      var t = e.target.closest('button, a'); if (!t) return;
      if (t.classList.contains('pack-top')) setPack(t.closest('.pack').dataset.id);
      else if (t.dataset.book) setPack(t.dataset.book);
      else if (t.dataset.addon) { var id = t.dataset.addon; S.addons[id] = !S.addons[id]; syncAll(); toast(S.addons[id] ? byId(ADDONS, id).name + ' added to your booking' : byId(ADDONS, id).name + ' removed'); }
      else if (t.classList.contains('day')) { var p = t.dataset.date.split('-'); pickDate(new Date(+p[0], +p[1] - 1, +p[2])); var again = $('.day[aria-pressed="true"]'); if (again) again.focus(); }
      else if (t.classList.contains('slot')) { S.slot = t.dataset.slot; renderSlots(); renderSummary(); $('#e-when').textContent = ''; var s = $('.slot[aria-pressed="true"]'); if (s) s.focus(); }
      else if (t.id === 'cal-prev') { S.month = new Date(S.month.getFullYear(), S.month.getMonth() - 1, 1); renderCal(); }
      else if (t.id === 'cal-next') { S.month = new Date(S.month.getFullYear(), S.month.getMonth() + 1, 1); renderCal(); }
      else if (t.id === 'copy-addr') {
        var done = function () { toast('Address copied'); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(WORKSHOP).then(done, function () { toast(WORKSHOP); }); else toast(WORKSHOP);
      }
      else if (t.id === 'done-again') {
        $('#bk-done').hidden = true; $('#book-form').hidden = false;
        ['#f-car', '#f-plate', '#f-notes'].forEach(function (s) { $(s).value = ''; });
        S.date = null; S.slot = null; renderCal(); renderSlots(); renderSummary();
        $('#booking').scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
      }
    });
    $('#book-form').addEventListener('submit', submitBooking);
    $('#quote-form').addEventListener('submit', submitQuote);
    BOOK_RULES.forEach(function (r) {
      var el = $(r[0]);
      el.addEventListener('blur', function () { if (el.value) setErr(el, $(r[1]), r[2](el.value)); });
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid')) setErr(el, $(r[1]), r[2](el.value)); });
    });

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

  // ---------- hero: light tunnel ----------
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function smooth(v, a, b) { v = clamp((v - a) / (b - a)); return v * v * (3 - 2 * v); }
  function tunnel() {
    var hero = $('#hero'), stage = $('.hero-stage'), cv = $('#tunnel'), ctx = cv.getContext('2d');
    var W = 0, H = 0, dpr = 1, visible = true, N = 15, t0 = performance.now();
    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 2); W = stage.clientWidth; H = stage.clientHeight;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function progress() { return clamp(window.scrollY / Math.max(1, hero.offsetHeight - window.innerHeight)); }
    function draw(now) {
      var p = progress(), narrow = W <= 760;
      var vx = W * (narrow ? 0.5 : 0.68), vy = H * (narrow ? 0.25 : 0.52);
      var off = (reduced ? 0 : (now - t0) / 1000 * 0.035) + p * 1.35;
      ctx.fillStyle = '#04101F'; ctx.fillRect(0, 0, W, H);
      var g = ctx.createRadialGradient(vx, vy, 0, vx, vy, Math.max(W, H) * 0.55);
      g.addColorStop(0, 'rgba(0,168,168,0.30)'); g.addColorStop(0.35, 'rgba(12,37,71,0.55)'); g.addColorStop(1, 'rgba(4,16,31,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      var span = Math.max(W, H) * 0.95;
      ctx.lineCap = 'round';
      for (var i = 0; i < N; i++) {
        var t = (i / N + off) % 1;
        var s = 0.035 + Math.pow(t, 2.5) * 2.1;
        var hw = span * s, hh = hw * 0.6;
        var a = smooth(t, 0, 0.14) * (1 - smooth(t, 0.8, 1));
        if (a <= 0.01) continue;
        var lw = 0.6 + t * t * 9;
        var x0 = vx - hw, x1 = vx + hw, y0 = vy - hh, y1 = vy + hh * 0.62;
        var col = t > 0.55 ? '220,250,250' : '95,240,230';
        for (var pass = 0; pass < 2; pass++) {
          ctx.lineWidth = pass ? lw : lw * 3.4;
          ctx.strokeStyle = 'rgba(' + col + ',' + (pass ? a * 0.92 : a * 0.14) + ')';
          ctx.beginPath(); ctx.moveTo(x0, y1); ctx.lineTo(x0, y0); ctx.lineTo(x1, y0); ctx.lineTo(x1, y1); ctx.stroke();
        }
        // mirror floor: faint continuation of the uprights below the floor line
        var fl = ctx.createLinearGradient(0, y1, 0, y1 + hh * 0.7);
        fl.addColorStop(0, 'rgba(0,168,168,' + a * 0.45 + ')'); fl.addColorStop(1, 'rgba(0,168,168,0)');
        ctx.strokeStyle = fl; ctx.lineWidth = lw;
        ctx.beginPath(); ctx.moveTo(x0, y1); ctx.lineTo(x0, y1 + hh * 0.7); ctx.moveTo(x1, y1); ctx.lineTo(x1, y1 + hh * 0.7); ctx.stroke();
      }
      stage.style.setProperty('--logo-scale', (1 + p * 0.5).toFixed(3));
      stage.style.setProperty('--logo-o', (1 - smooth(p, 0.72, 1)).toFixed(3));
      stage.style.setProperty('--copy-o', (1 - smooth(p, 0.12, 0.55)).toFixed(3));
      stage.style.setProperty('--copy-y', (-p * 70).toFixed(1) + 'px');
      $('.hero-copy').style.pointerEvents = p > 0.5 ? 'none' : '';
    }
    function loop(now) { if (visible) draw(now); if (!reduced) requestAnimationFrame(loop); }
    size(); window.addEventListener('resize', function () { size(); draw(performance.now()); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(hero);
    if (reduced) { draw(t0); window.addEventListener('scroll', function () { if (visible) draw(t0); }, { passive: true }); }
    else requestAnimationFrame(loop);
  }

  // ---------- real work: scroll-scrubbed frames ----------
  function sequence() {
    var sec = $('#work'), cv = $('#seq'), ctx = cv.getContext('2d'), steps = $$('.work-step'), cue = $('#seq-cue');
    var COUNT = 72, imgs = new Array(COUNT), started = false, shown = -1, ticking = false;
    function src(i) { return 'assets/img/seq/f' + String(i + 1).padStart(3, '0') + '.webp'; }
    function load(i) { if (imgs[i]) return; var im = new Image(); im.decoding = 'async'; im.onload = function () { im.ready = true; if (shown === -1 || i === want()) render(); }; im.src = src(i); imgs[i] = im; }
    function prog() { return clamp(-sec.getBoundingClientRect().top / Math.max(1, sec.offsetHeight - window.innerHeight)); }
    function want() { return Math.round(prog() * (COUNT - 1)); }
    function render() {
      ticking = false;
      var q = prog(), i = Math.round(q * (COUNT - 1)), j = i;
      while (j >= 0 && !(imgs[j] && imgs[j].ready)) j--;       // nearest loaded frame at or before the target
      if (j < 0) { j = i; while (j < COUNT && !(imgs[j] && imgs[j].ready)) j++; }
      if (j >= 0 && j < COUNT && j !== shown) { ctx.drawImage(imgs[j], 0, 0, cv.width, cv.height); shown = j; }
      var active = Math.min(steps.length - 1, Math.floor(q * steps.length));
      steps.forEach(function (s, k) { s.dataset.active = k === active; });
      cue.style.setProperty('--p', q.toFixed(4));
    }
    function start() { if (started) return; started = true; for (var i = 0; i < COUNT; i++) load(i); }
    load(0);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { if (es[0].isIntersecting) start(); }, { rootMargin: '150% 0px' }).observe(sec); else start();
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(render); } }, { passive: true });
    window.addEventListener('resize', render);
  }

  // ---------- init ----------
  if ($('#packs')) {
    renderVehSeg(); renderPacks(); renderAddonList(); renderBookingOptions();
    renderCal(); renderSlots(); syncAll(); bind();
    if (MODE === 'email') $('#bk-submit').textContent = 'Send booking request';
    tunnel(); sequence();
  }
})();
