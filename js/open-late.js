/* ============================================================================
   BOBA NIGHT — /best/open-late/ interactive layer (open-late.js)
   Live-first, degrades gracefully. Baked seed renders instantly (SEO + no-JS);
   on load we refresh the full late set live from Supabase (niteboba_finder).
   Open-now math is Pacific-time from Google-shape hours. No framework.
   ============================================================================ */
(function () {
  'use strict';

  var SB  = 'https://hfvbeqlefwwjlrbyxpbj.supabase.co';
  var KEY = 'sb_publishable_wlfujszvn2logC3KNL3MsA_AW1F42kf';
  var D   = window.__OL__ || {};
  var DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  var ALL  = (D.seed || []).slice();   // working set of late shops
  var GEMS = (D.gems || []).slice();
  var live = false;
  var state = { bucket: 'now', slider: 1320, crawl: [], saved: loadSaved() };

  /* ------------------------------------------------------------- helpers */
  function el(id) { return document.getElementById(id); }
  function esc(s) { return (s == null ? '' : '' + s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function toMin(t) { if (t == null) return null; t = '' + t; if (t.length < 3) return null; return parseInt(t.slice(0, 2), 10) * 60 + parseInt(t.slice(2), 10); }
  function fmt(m) { if (m == null) return ''; m = ((m % 1440) + 1440) % 1440; var h = Math.floor(m / 60), mm = m % 60, ap = h < 12 ? 'AM' : 'PM', hh = h % 12; if (hh === 0) hh = 12; return hh + (mm ? ':' + (mm < 10 ? '0' : '') + mm : '') + ' ' + ap; }
  function pacific() {
    try {
      var p = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Los_Angeles', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
      var o = {}; p.forEach(function (x) { o[x.type] = x.value; });
      return { day: DAYS.indexOf(o.weekday), min: (parseInt(o.hour, 10) % 24) * 60 + parseInt(o.minute, 10) };
    } catch (e) { var d = new Date(); return { day: d.getDay(), min: d.getHours() * 60 + d.getMinutes() }; }
  }
  function miles(la1, lo1, la2, lo2) { var R = 3958.8, dLa = (la2 - la1) * Math.PI / 180, dLo = (lo2 - lo1) * Math.PI / 180, a = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(la1 * Math.PI / 180) * Math.cos(la2 * Math.PI / 180) * Math.sin(dLo / 2) * Math.sin(dLo / 2); return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)); }

  /* open-now state for right now (Pacific). Handles overnight + 24h. */
  function openState(per) {
    if (!per || !per.length) return { open: false, label: 'Hours vary', close: null };
    var t = pacific(), day = t.day, min = t.min, i, p, o, c;
    for (i = 0; i < per.length; i++) {
      p = per[i]; o = toMin(p.o); if (o == null) continue;
      if (p.c == null) { if (p.d === day) return { open: true, label: 'Open 24 hours', close: null }; continue; }
      c = toMin(p.c);
      if (c > o) { if (p.d === day && min >= o && min < c) return { open: true, label: 'Open · closes ' + fmt(c), close: c }; }
      else {
        if (p.d === day && min >= o) return { open: true, label: 'Open · closes ' + fmt(c), close: c + 1440 };
        if ((p.d + 1) % 7 === day && min < c) return { open: true, label: 'Open · closes ' + fmt(c), close: c };
      }
    }
    for (var k = 0; k < 8; k++) {
      var d = (day + k) % 7, best = null;
      for (var j = 0; j < per.length; j++) { var q = per[j]; if (q.d === d) { var oo = toMin(q.o); if (oo == null) continue; if (k === 0 && oo <= min) continue; if (best == null || oo < best) best = oo; } }
      if (best != null) return { open: false, label: 'Opens ' + (k === 0 ? '' : k === 1 ? 'tomorrow ' : DAYS[d] + ' ') + fmt(best), close: null };
    }
    return { open: false, label: 'Closed', close: null };
  }
  /* tonight's closing minute (absolute, +1440 if past midnight) regardless of open state */
  function closeTonight(per) {
    var t = pacific(), i, p, o, c;
    for (i = 0; i < per.length; i++) { p = per[i]; if (p.d === t.day) { o = toMin(p.o); c = toMin(p.c); if (o == null || c == null) return null; return c <= o ? c + 1440 : c; } }
    return null;
  }
  /* is the shop open at a given wall-clock (day, minute)? */
  function openAt(per, day, atMin) {
    for (var i = 0; i < per.length; i++) {
      var p = per[i], o = toMin(p.o); if (o == null) continue;
      if (p.c == null) { if (p.d === day) return true; continue; }
      var c = toMin(p.c);
      if (c > o) { if (p.d === day && atMin >= o && atMin < c) return true; }
      else { if (p.d === day && atMin >= o) return true; if ((p.d + 1) % 7 === day && atMin < c) return true; }
    }
    return false;
  }
  function openAtSlider(per, base, M) { var day = M < 1440 ? base : (base + 1) % 7; return openAt(per, day, M % 1440); }
  /* closing minute (abs, +1440 past midnight) of the period covering the slider time */
  function closeAtSlider(per, base, M) {
    var day = M < 1440 ? base : (base + 1) % 7, mm = M % 1440;
    for (var i = 0; i < per.length; i++) {
      var p = per[i], o = toMin(p.o); if (o == null) continue;
      if (p.c == null) { if (p.d === day) return null; continue; }
      var c = toMin(p.c);
      if (c > o) { if (p.d === day && mm >= o && mm < c) return c; }
      else { if (p.d === day && mm >= o) return c + 1440; if ((p.d + 1) % 7 === day && mm < c) return c; }
    }
    return null;
  }

  /* --------------------------------------------------------------- saved */
  function loadSaved() { try { return JSON.parse(localStorage.getItem('bn_saved') || '[]'); } catch (e) { return []; } }
  function isSaved(s) { return state.saved.indexOf(s) > -1; }
  function toggleSave(s) { var i = state.saved.indexOf(s); if (i > -1) state.saved.splice(i, 1); else state.saved.push(s); try { localStorage.setItem('bn_saved', JSON.stringify(state.saved)); } catch (e) {} paintStars(); renderSticky(); }
  function paintStars() { Array.prototype.forEach.call(document.querySelectorAll('[data-save]'), function (b) { b.classList.toggle('on', isSaved(b.getAttribute('data-save'))); }); }

  /* ---------------------------------------------------------- shop cards */
  function dir(sh) { return 'https://www.google.com/maps/dir/?api=1&destination=' + sh.la + ',' + sh.lo; }
  function starBtn(sh) { return '<button class="ol-star' + (isSaved(sh.s) ? ' on' : '') + '" data-save="' + esc(sh.s) + '" aria-label="Save ' + esc(sh.nm) + '" title="Save to your black book"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-9.2-8.4A5 5 0 0 1 12 6a5 5 0 0 1 9.2 5.6C19 15.6 12 20 12 20z"/></svg></button>'; }
  function ratLine(sh) { return sh.r ? '<span class="rat">★ ' + (Math.round(sh.r * 10) / 10).toFixed(1) + '</span> <span>' + (sh.rv || 0) + ' on Google</span>' : ''; }
  function pill(sh) { var st = openState(sh.per); var cls = st.open ? 'open' : 'closed'; return '<span class="ol-pill ' + cls + '"><span class="led"></span>' + esc(st.label) + '</span>'; }
  function shopCard(sh, pillHtml) {
    var url = sh.url || ('/boba/ca/' + sh.cs + '/');
    return '<article class="ol-card" data-slug="' + esc(sh.s) + '">' +
      '<div class="ol-card-top"><a class="nm" href="' + url + '">' + esc(sh.nm) + '</a>' + starBtn(sh) + '</div>' +
      '<div class="meta"><a href="/boba/ca/' + sh.cs + '/">' + esc(sh.ci) + '</a>' + (ratLine(sh) ? '<span>·</span> ' + ratLine(sh) : '') + '</div>' +
      (pillHtml || pill(sh)) +
      '<div class="ol-actions"><a class="ol-mini pri" href="' + dir(sh) + '" target="_blank" rel="nofollow noopener">Directions</a>' +
      '<button class="ol-mini" data-crawl="' + esc(sh.s) + '">+ Add to crawl</button></div>' +
      '</article>';
  }
  function grid(list, emptyMsg) { if (!list.length) return '<p class="ol-empty">' + esc(emptyMsg || 'Nothing here right now. Try the time slider or check back tonight.') + '</p>'; return '<div class="ol-grid">' + list.map(shopCard).join('') + '</div>'; }
  function bySlug(s) { for (var i = 0; i < ALL.length; i++) if (ALL[i].s === s) return ALL[i]; for (var j = 0; j < GEMS.length; j++) if (GEMS[j].s === s) return GEMS[j]; return null; }

  /* ------------------------------------------------------- LIVE bucket cards */
  var BUCKETS = [
    { k: 'now',  cls: 'now',  lbl: 'Open right now',       test: function (e) { return e.open; }, sub: 'pouring this minute' },
    { k: 'p10',  cls: 'late', lbl: 'Open past 10 PM',      test: function (e) { return e.open && e.close != null && e.close >= 1320; }, sub: 'still going at 10' },
    { k: 'p11',  cls: 'late', lbl: 'Open past 11 PM',      test: function (e) { return e.open && e.close != null && e.close >= 1380; }, sub: 'late-night milk tea' },
    { k: 'mid',  cls: 'mid',  lbl: 'Open past midnight',   test: function (e) { return e.open && e.close != null && e.close >= 1440; }, sub: 'the after-midnight few' },
    { k: 'p1',   cls: 'mid',  lbl: 'Open past 1 AM',       test: function (e) { return e.open && e.close != null && e.close >= 1500; }, sub: 'rare and precious' }
  ];
  function evalAll() { return ALL.map(function (sh) { var st = openState(sh.per); return { sh: sh, open: st.open, close: st.open ? st.close : closeTonight(sh.per) }; }); }
  function renderLive() {
    var box = el('ol-live'); if (!box) return;
    var ev = evalAll();
    box.innerHTML = BUCKETS.map(function (b) {
      var n = ev.filter(b.test).length;
      if (b.k !== 'now' && n === 0) return '';
      return '<button class="ol-livecard ' + b.cls + (state.bucket === b.k ? ' is-on' : '') + '" data-bucket="' + b.k + '">' +
        '<span class="top"><span class="led"></span></span>' +
        '<span class="n">' + n + '</span><span class="lbl">' + b.lbl + '</span><span class="sub">' + b.sub + '</span>' +
        '<span class="cta">' + (state.bucket === b.k ? 'Showing' : 'See these') + '</span></button>';
    }).join('');
    renderLiveList();
  }
  function renderLiveList() {
    var out = el('ol-live-list'); if (!out) return;
    var b = BUCKETS.filter(function (x) { return x.k === state.bucket; })[0] || BUCKETS[0];
    var ev = evalAll().filter(b.test).map(function (x) { return x.sh; });
    ev.sort(function (a, c) { return (closeTonight(c.per) || 0) - (closeTonight(a.per) || 0) || (c.r || 0) - (a.r || 0); });
    out.innerHTML = '<p class="ol-count">' + ev.length + ' ' + (b.lbl.toLowerCase()) + (live ? '' : ' · refreshing…') + '</p>' + grid(ev.slice(0, 24), 'None in this window right now.');
    paintStars();
  }

  /* --------------------------------------------------------- TIME slider */
  function renderSliderStatic() {
    var ticks = el('ol-slider-ticks'); if (ticks) { ticks.innerHTML = ['8 PM', '9', '10', '11', '12', '1', '2 AM'].map(function (t) { return '<span>' + t + '</span>'; }).join(''); }
    var r = el('ol-slider'); if (r) { r.value = state.slider; }
    renderSlider();
  }
  function renderSlider() {
    var r = el('ol-slider'); if (!r) return;
    var M = +r.value, base = pacific().day;
    var pct = ((M - 1200) / (1560 - 1200)) * 100; r.style.setProperty('--fill', pct + '%');
    var open = ALL.filter(function (sh) { return openAtSlider(sh.per, base, M); });
    open.sort(function (a, c) { return (c.r || 0) - (a.r || 0); });
    var read = el('ol-slider-read'); if (read) read.innerHTML = '<span class="big">' + fmt(M) + '</span><span class="cnt"><b>' + open.length + '</b> shops still open at ' + fmt(M) + '</span>';
    var lst = el('ol-slider-list');
    if (lst) {
      lst.innerHTML = open.length
        ? '<div class="ol-grid">' + open.slice(0, 18).map(function (sh) {
            var c = closeAtSlider(sh.per, base, M);
            var ph = '<span class="ol-pill open"><span class="led"></span>' + (c ? 'Open till ' + fmt(c) : 'Open') + '</span>';
            return shopCard(sh, ph);
          }).join('') + '</div>'
        : '<p class="ol-empty">Nothing open that late in the set yet. The live refresh may add more.</p>';
      paintStars();
    }
    // reflect tick highlight
    var idx = Math.round((M - 1200) / 60);
    Array.prototype.forEach.call(document.querySelectorAll('#ol-slider-ticks span'), function (s, i) { s.classList.toggle('on', i === idx); });
    if (window.__olMap) mapHighlight(open);
  }

  /* --------------------------------------------------------------- gems */
  function renderGems() { var box = el('ol-gems'); if (!box) return; box.innerHTML = '<div class="ol-grid">' + GEMS.map(function (sh) { return shopCard(sh).replace('ol-card"', 'ol-card ol-card--gem"'); }).join('') + '</div>'; paintStars(); }

  /* ------------------------------------------------------------ shuffle */
  function renderShuffle() {
    var open = ALL.filter(function (sh) { return openState(sh.per).open; });
    var pool = open.length ? open : ALL; if (!pool.length) return;
    var sh = pool[Math.floor(Math.random() * pool.length)];
    var st = openState(sh.per), out = el('ol-shuffle-out');
    if (!out) return;
    out.className = 'ol-shuffle-out show';
    out.innerHTML = '<p class="rnm">' + esc(sh.nm) + '</p>' +
      '<p class="rwhy">' + esc(sh.ci) + (sh.r ? ' · ★ ' + sh.r.toFixed(1) + ' on Google' : '') + ' · ' + esc(st.label) + '</p>' +
      '<div class="ol-actions"><a class="ol-mini pri" href="' + dir(sh) + '" target="_blank" rel="nofollow noopener">Directions</a>' +
      '<button class="ol-mini" data-crawl="' + esc(sh.s) + '">+ Add to crawl</button>' +
      '<a class="ol-mini" href="' + (sh.url || '/boba/ca/' + sh.cs + '/') + '">See the shop</a></div>';
  }

  /* -------------------------------------------------------------- crawl */
  function addCrawl(s) { if (state.crawl.indexOf(s) > -1 || state.crawl.length >= 5) return; state.crawl.push(s); renderCrawl(); var c = el('ol-crawl'); if (c) c.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  function rmCrawl(s) { var i = state.crawl.indexOf(s); if (i > -1) state.crawl.splice(i, 1); renderCrawl(); }
  function renderCrawl() {
    var box = el('ol-crawl-list'); if (!box) return;
    if (!state.crawl.length) { box.innerHTML = '<p class="ol-crawl-empty">Add a couple of stops from any shop above (“+ Add to crawl”) and we’ll route them into one late-night run you can open in Maps or send to a friend.</p>'; var f = el('ol-crawl-foot'); if (f) f.style.display = 'none'; return; }
    var stops = state.crawl.map(bySlug).filter(Boolean);
    box.innerHTML = stops.map(function (sh, idx) { var st = openState(sh.per); return '<div class="ol-crawl-stop"><span class="num">' + (idx + 1) + '</span><span><span class="cs-nm">' + esc(sh.nm) + '</span><br><span class="cs-meta">' + esc(sh.ci) + ' · ' + esc(st.label) + '</span></span><button class="cs-x" data-uncrawl="' + esc(sh.s) + '" aria-label="Remove">×</button></div>'; }).join('');
    var f = el('ol-crawl-foot'); if (f) f.style.display = 'flex';
    var tot = el('ol-crawl-tot');
    if (tot && stops.length > 1) { var d = 0; for (var i = 1; i < stops.length; i++) d += miles(stops[i - 1].la, stops[i - 1].lo, stops[i].la, stops[i].lo); tot.textContent = stops.length + ' stops · ~' + (Math.round(d * 10) / 10) + ' mi end to end'; }
    else if (tot) tot.textContent = stops.length + ' stop, add one more to make a route';
  }
  function crawlUrl() { var stops = state.crawl.map(bySlug).filter(Boolean); if (!stops.length) return '#'; return 'https://www.google.com/maps/dir/' + stops.map(function (s) { return s.la + ',' + s.lo; }).join('/'); }
  function shareCrawl() {
    var stops = state.crawl.map(bySlug).filter(Boolean); if (!stops.length) return;
    var txt = 'Late-night boba crawl: ' + stops.map(function (s) { return s.nm; }).join(' to ') + '. ' + crawlUrl();
    if (navigator.share) { navigator.share({ title: 'Boba Night crawl', text: txt, url: crawlUrl() }).catch(function () {}); }
    else if (navigator.clipboard) { navigator.clipboard.writeText(txt).then(function () { var b = el('ol-crawl-share'); if (b) { var o = b.textContent; b.textContent = 'Copied ✓'; setTimeout(function () { b.textContent = o; }, 1600); } }); }
  }

  /* ---------------------------------------------------------- mood chips */
  var MOODS = [
    { k: 'all',    em: '🌙', lbl: 'Everything late', f: function () { return true; } },
    { k: 'dinner', em: '🍽️', lbl: 'After dinner', f: function (e) { return e.open && e.close >= 1290; } },
    { k: 'movie',  em: '🎬', lbl: 'After a movie', f: function (e) { return e.open && e.close >= 1380; } },
    { k: 'drive',  em: '🚗', lbl: 'Late drive', f: function (e) { return e.open && e.close >= 1440; } },
    { k: 'friends',em: '🎉', lbl: 'Out with friends', f: function (e) { return e.open && e.close >= 1350; } }
  ];
  function renderMoodChips() {
    var box = el('ol-mood-chips'); if (!box) return;
    box.innerHTML = MOODS.map(function (m, i) { return '<button class="ol-chip' + (i === 0 ? ' is-on' : '') + '" data-mood="' + m.k + '"><span class="em">' + m.em + '</span>' + m.lbl + '</button>'; }).join('');
    renderMood('all');
  }
  function renderMood(k) {
    var m = MOODS.filter(function (x) { return x.k === k; })[0] || MOODS[0];
    var ev = evalAll().filter(function (e) { return m.f(e); }).map(function (x) { return x.sh; });
    ev.sort(function (a, c) { return (closeTonight(c.per) || 0) - (closeTonight(a.per) || 0) || (c.r || 0) - (a.r || 0); });
    var out = el('ol-mood-list'); if (out) { out.innerHTML = '<p class="ol-count">' + ev.length + ' spots · ' + esc(m.lbl.toLowerCase()) + '</p>' + grid(ev.slice(0, 12)); paintStars(); }
  }

  /* --------------------------------------------------------------- map */
  var MAP, LAYER;
  function initMap() {
    var box = el('ol-map'); if (!box) return;
    if (!window.L || !L.map) { box.innerHTML = '<div class="ol-map-fallback">The live map needs a moment (or a connection). Every shop below still links straight to directions.</div>'; return; }
    MAP = L.map(box, { zoomControl: true, scrollWheelZoom: false, attributionControl: true }).setView([33.87, -117.95], 9);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { maxZoom: 19, attribution: '© OpenStreetMap © CARTO' }).addTo(MAP);
    window.__olMap = MAP; drawPins(ALL);
  }
  function pinIcon(kind) { return L.divIcon({ className: '', html: '<span class="ol-pin ' + kind + '"></span>', iconSize: [16, 16], iconAnchor: [8, 15] }); }
  function drawPins(list) {
    if (!MAP) return; if (LAYER) MAP.removeLayer(LAYER); LAYER = L.layerGroup().addTo(MAP);
    var seen = {};
    list.forEach(function (sh) {
      if (sh.la == null || sh.lo == null) return; var key = sh.la.toFixed(4) + ',' + sh.lo.toFixed(4); if (seen[key]) return; seen[key] = 1;
      var st = openState(sh.per), kind = st.open ? (st.close >= 1440 ? 'now' : 'now') : 'closed';
      var m = L.marker([sh.la, sh.lo], { icon: pinIcon(st.open ? 'now' : 'late') });
      m.bindPopup('<span class="pnm">' + esc(sh.nm) + '</span>' + esc(sh.ci) + (sh.r ? ' · ★ ' + sh.r.toFixed(1) : '') + '<br>' + esc(st.label) + '<br><a href="' + dir(sh) + '" target="_blank" rel="nofollow noopener">Directions</a> · <a href="' + (sh.url || '/boba/ca/' + sh.cs + '/') + '">Shop</a>');
      LAYER.addLayer(m);
    });
  }
  function mapHighlight(list) { if (MAP) drawPins(list); }

  /* ------------------------------------------------------------- sticky */
  function renderSticky() {
    var s = el('ol-sticky-val'); if (!s) return;
    var openN = evalAll().filter(function (e) { return e.open; }).length;
    s.innerHTML = '<b>' + openN + '</b> open now · <b>' + state.saved.length + '</b> saved';
  }

  /* ---------------------------------------------------------- live fetch */
  function perFromHours(h) { if (!h || !h.periods) return null; var out = []; h.periods.forEach(function (p) { if (!p.open) return; out.push({ d: p.open.day, o: p.open.time, c: p.close ? p.close.time : null }); }); return out.length ? out : null; }
  function lcOf(per) { var mx = 0; per.forEach(function (p) { if (p.c == null) return; var o = toMin(p.o), c = toMin(p.c); if (c == null) return; var h = Math.floor(c / 60); if (c <= o) h += 24; if (h > mx) mx = h; }); return mx; }
  function fetchLive() {
    if (!window.fetch) return;
    fetch(SB + '/rest/v1/niteboba_finder?select=s,n,c,cs,la,lo,rating,reviews,price_level,hours&status=eq.open', { headers: { apikey: KEY, Authorization: 'Bearer ' + KEY } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (rows) {
        if (!rows || !rows.length) return;
        var late = [];
        rows.forEach(function (row) {
          var per = perFromHours(row.hours); if (!per) return; var lc = lcOf(per); if (lc < 21) return;
          late.push({ s: row.s, nm: row.n, ci: row.c, cs: row.cs, la: row.la == null ? null : +row.la, lo: row.lo == null ? null : +row.lo, r: row.rating, rv: row.reviews, pl: row.price_level, per: per, lc: lc, url: '/boba/ca/' + row.cs + '/' });
        });
        if (late.length < 20) return; // sanity: keep baked seed if response looks thin
        ALL = late; live = true;
        renderLive(); renderSlider(); renderMood(currentMood()); renderSticky(); if (MAP) drawPins(ALL);
        var note = el('ol-live-note'); if (note) note.textContent = 'Showing all ' + ALL.length + ' late spots, live from our database.';
      })
      .catch(function () { /* keep baked seed */ });
  }
  function currentMood() { var on = document.querySelector('#ol-mood-chips .is-on'); return on ? on.getAttribute('data-mood') : 'all'; }

  /* --------------------------------------------------------------- wire */
  function wire() {
    document.addEventListener('click', function (e) {
      var t = e.target.closest ? e.target.closest('[data-bucket],[data-crawl],[data-uncrawl],[data-save],[data-mood],#ol-shuffle-btn,#ol-crawl-open,#ol-crawl-share,#ol-crawl-clear') : null;
      if (!t) return;
      if (t.hasAttribute('data-bucket')) { state.bucket = t.getAttribute('data-bucket'); renderLive(); }
      else if (t.hasAttribute('data-crawl')) { addCrawl(t.getAttribute('data-crawl')); }
      else if (t.hasAttribute('data-uncrawl')) { rmCrawl(t.getAttribute('data-uncrawl')); }
      else if (t.hasAttribute('data-save')) { toggleSave(t.getAttribute('data-save')); }
      else if (t.hasAttribute('data-mood')) { Array.prototype.forEach.call(document.querySelectorAll('#ol-mood-chips .ol-chip'), function (c) { c.classList.remove('is-on'); }); t.classList.add('is-on'); renderMood(t.getAttribute('data-mood')); }
      else if (t.id === 'ol-shuffle-btn') { renderShuffle(); }
      else if (t.id === 'ol-crawl-open') { if (state.crawl.length) window.open(crawlUrl(), '_blank'); }
      else if (t.id === 'ol-crawl-share') { shareCrawl(); }
      else if (t.id === 'ol-crawl-clear') { state.crawl = []; renderCrawl(); }
    });
    var r = el('ol-slider'); if (r) r.addEventListener('input', renderSlider);
  }

  function init() {
    wire();
    renderLive(); renderSliderStatic(); renderMoodChips(); renderGems(); renderCrawl(); renderSticky();
    if ('IntersectionObserver' in window) {
      var mo = el('ol-map');
      if (mo) { var io = new IntersectionObserver(function (en, obs) { en.forEach(function (x) { if (x.isIntersecting) { initMap(); obs.disconnect(); } }); }, { rootMargin: '200px' }); io.observe(mo); }
      else initMap();
    } else initMap();
    fetchLive();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();