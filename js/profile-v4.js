(function () {
  "use strict";
  var D = JSON.parse(document.getElementById("bn-shop-data").textContent);
  var DAYN = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  var WEEK = 10080;

  /* ---------- America/Los_Angeles clock ---------- */
  function laParts() {
    try {
      var parts = new Intl.DateTimeFormat("en-US", {
        timeZone: "America/Los_Angeles", weekday: "short",
        hour: "numeric", minute: "numeric", hour12: false
      }).formatToParts(new Date());
      var map = {};
      parts.forEach(function (p) { map[p.type] = p.value; });
      var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
      var h = parseInt(map.hour, 10); if (h === 24) h = 0;
      return { day: days[map.weekday], min: h * 60 + parseInt(map.minute, 10) };
    } catch (e) {
      var d = new Date();
      return { day: d.getDay(), min: d.getHours() * 60 + d.getMinutes() };
    }
  }
  function toMin(t) { return parseInt(t.slice(0, 2), 10) * 60 + parseInt(t.slice(2), 10); }
  function fmt(t) {
    var h = parseInt(t.slice(0, 2), 10), m = t.slice(2);
    var ap = h >= 12 ? "PM" : "AM"; var hh = h % 12; if (hh === 0) hh = 12;
    return hh + ":" + m + " " + ap;
  }
  /* periods: [[openDay,"HHMM",closeDay,"HHMM"],...] with midnight wrap support */
  function openInfo(periods, now) {
    var t = now.day * 1440 + now.min, i, p, s, e;
    for (i = 0; i < periods.length; i++) {
      p = periods[i];
      s = p[0] * 1440 + toMin(p[1]);
      e = p[2] * 1440 + toMin(p[3]);
      if (e <= s) e += WEEK;
      if ((t >= s && t < e) || (t + WEEK >= s && t + WEEK < e)) return { open: true, closes: p[3] };
    }
    var best = null, bd = WEEK + 1, d;
    for (i = 0; i < periods.length; i++) {
      p = periods[i];
      s = p[0] * 1440 + toMin(p[1]);
      d = (s - t + WEEK) % WEEK;
      if (d < bd) { bd = d; best = p; }
    }
    return { open: false, next: best };
  }
  function findPeriod(periods, day) {
    for (var i = 0; i < periods.length; i++) if (periods[i][0] === day) return periods[i];
    return null;
  }

  /* ---------- live status pills, today row, facts, nearby ---------- */
  function updateStatus() {
    var now = laParts();
    var info = openInfo(D.periods, now);
    var text, cls;
    if (info.open) {
      text = "Open now, closes " + fmt(info.closes); cls = "status open js-status-pill";
    } else if (info.next) {
      text = "Closed, opens " + fmt(info.next[1]) +
        (info.next[0] !== now.day ? " " + DAYN[info.next[0]].slice(0, 3) : "");
      cls = "status closed js-status-pill";
    } else { return; }
    Array.prototype.forEach.call(document.querySelectorAll(".js-status-pill"), function (el) {
      el.className = cls;
      el.innerHTML = '<span class="led"></span>';
      el.appendChild(document.createTextNode(text));
    });
    var today = findPeriod(D.periods, now.day);
    var facts = document.getElementById("factsToday");
    if (facts) facts.textContent = today ? (fmt(today[1]) + " to " + fmt(today[3])) : "Closed today";
    Array.prototype.forEach.call(document.querySelectorAll(".hours-t tr"), function (tr) {
      var isToday = parseInt(tr.getAttribute("data-day"), 10) === now.day;
      tr.classList.toggle("is-today", isToday);
      var old = tr.querySelector(".hours-today-tag");
      if (old) old.parentNode.removeChild(old);
      if (isToday) {
        var th = tr.querySelector("th"), tag = document.createElement("span");
        tag.className = "hours-today-tag"; tag.textContent = "Today";
        th.appendChild(tag);
      }
    });
    Array.prototype.forEach.call(document.querySelectorAll(".ps-live[data-per]"), function (el) {
      var per;
      try { per = JSON.parse(el.getAttribute("data-per")); } catch (e) { return; }
      if (!per || !per.length) return;
      var s = openInfo(per, now);
      el.classList.remove("is-open", "is-closed");
      if (s.open) { el.textContent = "Open till " + fmt(s.closes); el.classList.add("is-open"); }
      else if (s.next) {
        el.textContent = "Opens " + fmt(s.next[1]) + (s.next[0] !== now.day ? " " + DAYN[s.next[0]] : "");
        el.classList.add("is-closed");
      }
    });
  }
  updateStatus();
  setInterval(updateStatus, 60000);

  /* ---------- save to blackbook ---------- */
  var KEY = "bn-blackbook-" + D.slug;
  var saved = false;
  try { saved = localStorage.getItem(KEY) === "1"; } catch (e) {}
  var hearts = document.querySelectorAll(".js-save");
  function renderSave() {
    Array.prototype.forEach.call(hearts, function (b) {
      b.setAttribute("aria-pressed", saved ? "true" : "false");
    });
  }
  Array.prototype.forEach.call(hearts, function (b) {
    b.addEventListener("click", function () {
      saved = !saved;
      try { saved ? localStorage.setItem(KEY, "1") : localStorage.removeItem(KEY); } catch (e) {}
      renderSave();
    });
  });
  renderSave();

  /* ---------- share modal: compose, chips, crawl, trap ---------- */
  var modal = document.getElementById("psModal");
  var preview = document.getElementById("psPreview");
  var smsLink = document.getElementById("psSms");
  var hint = document.getElementById("psHint");
  var state = { when: "tonight", stops: [] };
  var lastFocus = null;

  function hoursLine() {
    var now = laParts();
    if (state.when === "weekend") {
      var sat = findPeriod(D.periods, 6);
      return sat ? ("Open till " + fmt(sat[3]) + " on Saturday.") : "";
    }
    var p = findPeriod(D.periods, now.day);
    if (!p) return "";
    return "Open till " + fmt(p[3]) + (state.when === "tonight" ? " tonight." : ".");
  }
  function compose() {
    var whenTxt = { tonight: "tonight", sevenpm: "at 7pm", weekend: "this weekend" }[state.when];
    var parts = ["Boba run " + whenTxt + ": " + D.name + ", " + D.addr + ", " + D.city + "."];
    if (D.orderLine) parts.push(D.orderLine);
    var hl = hoursLine(); if (hl) parts.push(hl);
    if (state.stops.length === 1) {
      var s = D.stops[state.stops[0]];
      parts.push("Then " + s.n + ", " + s.mi + " mi away.");
    } else if (state.stops.length === 2) {
      var a = D.stops[state.stops[0]], b = D.stops[state.stops[1]];
      parts.push("Then " + a.n + " (" + a.mi + " mi) and " + b.n + " (" + b.mi + " mi).");
    }
    parts.push(D.url);
    var msg = parts.join(" ");
    preview.textContent = msg;
    smsLink.setAttribute("href", "sms:?&body=" + encodeURIComponent(msg));
    return msg;
  }
  Array.prototype.forEach.call(modal.querySelectorAll("[data-when]"), function (btn) {
    btn.addEventListener("click", function () {
      state.when = btn.getAttribute("data-when");
      Array.prototype.forEach.call(modal.querySelectorAll("[data-when]"), function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      compose();
    });
  });
  Array.prototype.forEach.call(modal.querySelectorAll("[data-stop]"), function (btn) {
    btn.addEventListener("click", function () {
      var idx = parseInt(btn.getAttribute("data-stop"), 10);
      var at = state.stops.indexOf(idx);
      if (at > -1) {
        state.stops.splice(at, 1);
        btn.setAttribute("aria-pressed", "false");
        hint.textContent = "Up to two stops, all a short walk from " + D.name + ".";
      } else if (state.stops.length < 2) {
        state.stops.push(idx);
        btn.setAttribute("aria-pressed", "true");
        hint.textContent = state.stops.length === 2 ? "Two stops keeps it a walk." : "Room for one more stop.";
      } else {
        hint.textContent = "Two stops max. Remove one to swap.";
        return;
      }
      compose();
    });
  });

  function focusables() {
    var f = modal.querySelectorAll('a[href],button:not([disabled]):not([hidden]),[tabindex]:not([tabindex="-1"])');
    return Array.prototype.filter.call(f, function (el) { return el.offsetParent !== null; });
  }
  function trap(e) {
    if (e.key === "Escape") { e.preventDefault(); closeModal(); return; }
    if (e.key !== "Tab") return;
    var f = focusables();
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
    else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
  }
  function openModal() {
    lastFocus = document.activeElement;
    compose();
    modal.hidden = false;
    document.body.classList.add("bn-lock");
    document.addEventListener("keydown", trap);
    var x = modal.querySelector(".ps-x");
    if (x) x.focus();
  }
  function closeModal() {
    modal.hidden = true;
    document.body.classList.remove("bn-lock");
    document.removeEventListener("keydown", trap);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  Array.prototype.forEach.call(document.querySelectorAll("[data-share-open]"), function (b) {
    b.addEventListener("click", openModal);
  });
  Array.prototype.forEach.call(modal.querySelectorAll("[data-share-close]"), function (b) {
    b.addEventListener("click", closeModal);
  });

  /* ---------- copy + native share ---------- */
  function flash(btn, txt) {
    var orig = btn.textContent;
    btn.textContent = txt;
    setTimeout(function () { btn.textContent = orig; }, 1600);
  }
  function copyText(txt, btn) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(txt).then(function () { flash(btn, "Copied"); },
        function () { fallbackCopy(txt, btn); });
    } else { fallbackCopy(txt, btn); }
  }
  function fallbackCopy(txt, btn) {
    var ta = document.createElement("textarea");
    ta.value = txt; ta.setAttribute("readonly", "");
    ta.style.position = "fixed"; ta.style.left = "-9999px";
    document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); flash(btn, "Copied"); } catch (e) {}
    document.body.removeChild(ta);
  }
  document.getElementById("psCopyLink").addEventListener("click", function () { copyText(D.url, this); });
  document.getElementById("psCopyMsg").addEventListener("click", function () { copyText(compose(), this); });
  var nativeBtn = document.getElementById("psNative");
  if (navigator.share) {
    nativeBtn.hidden = false;
    nativeBtn.addEventListener("click", function () {
      navigator.share({ title: D.name, text: compose() }).catch(function () {});
    });
  }
  compose();
})();

/* ==== Find-it near-me map: pearl cards + jump-over + arrival focus ==== */
(function () {
  "use strict";
  var stage = document.querySelector(".mp-stage");
  if (!stage) return;
  var card = document.getElementById("mpCard");

  function laNow() {
    try {
      var p = new Intl.DateTimeFormat("en-US", { timeZone: "America/Los_Angeles", weekday: "short", hour: "numeric", minute: "numeric", hour12: false }).formatToParts(new Date());
      var m = {}; p.forEach(function (x) { m[x.type] = x.value; });
      var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
      var h = parseInt(m.hour, 10); if (h === 24) h = 0;
      return { day: days[m.weekday], min: h * 60 + parseInt(m.minute, 10) };
    } catch (e) { var d = new Date(); return { day: d.getDay(), min: d.getHours() * 60 + d.getMinutes() }; }
  }
  function toMin(t) { return parseInt(t.slice(0, 2), 10) * 60 + parseInt(t.slice(2), 10); }
  function fmtT(t) { var h = parseInt(t.slice(0, 2), 10), ap = h >= 12 ? "PM" : "AM", hh = h % 12 || 12; return hh + ":" + t.slice(2) + " " + ap; }
  function openState(per) {
    if (!per || !per.length) return null;
    var now = laNow(), t = now.day * 1440 + now.min, W = 10080;
    for (var i = 0; i < per.length; i++) {
      var s = per[i][0] * 1440 + toMin(per[i][1]), e = per[i][2] * 1440 + toMin(per[i][3]);
      if (e <= s) e += W;
      if ((t >= s && t < e) || (t + W >= s && t + W < e)) return { open: true, till: per[i][3] };
    }
    return { open: false };
  }

  function showCard(el, isCenter) {
    var n = el.getAttribute("data-n"), c = el.getAttribute("data-c"), mi = el.getAttribute("data-mi");
    var per = null;
    try { per = JSON.parse(el.getAttribute("data-per") || "null"); } catch (e) {}
    var st = openState(per);
    var html = '<button class="x" type="button" aria-label="Close">&times;</button>'
      + '<p class="t">' + n + '</p>'
      + '<p class="m">' + (isCenter ? c : c + " &middot; " + mi + "&nbsp;mi away") + '</p>';
    if (st) html += '<p class="st' + (st.open ? "" : " is-closed") + '"><span class="led"></span>' + (st.open ? "Open till " + fmtT(st.till) : "Closed right now") + '</p>';
    var nm = el.getAttribute("data-nm");
    var links = [];
    if (!isCenter) links.push('<a class="go" href="' + el.getAttribute("href") + '">Jump over</a>');
    if (nm) links.push('<a class="go" href="' + nm + '">' + (isCenter ? "Open in the night map" : "Night map") + '</a>');
    if (links.length) html += '<span class="golinks">' + links.join("") + '</span>';
    card.innerHTML = html;
    card.hidden = false;
    /* position near the spot, clamped inside the stage */
    var sr = stage.getBoundingClientRect(), er = el.getBoundingClientRect();
    var x = er.left - sr.left + er.width / 2, y = er.top - sr.top;
    card.style.left = Math.max(6, Math.min(x - 95, sr.width - 200)) + "px";
    card.style.top = (y > sr.height / 2 ? y - card.offsetHeight - 16 : y + 30) + "px";
    card.querySelector(".x").addEventListener("click", function () { card.hidden = true; });
    card.querySelector(".x").focus({ preventScroll: true });
  }

  Array.prototype.forEach.call(stage.querySelectorAll(".mp-spot"), function (a) {
    a.addEventListener("click", function (ev) {
      ev.preventDefault();
      showCard(a, false);
    });
  });
  var center = stage.querySelector(".mp-center");
  if (center) center.addEventListener("click", function () { showCard(center, true); });
  window.__mpShowCard = showCard;
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && card) card.hidden = true; });
  document.addEventListener("click", function (e) {
    if (!card.hidden && !card.contains(e.target) && !e.target.closest(".mp-spot") && !e.target.closest(".mp-center")) card.hidden = true;
  });
  /* the map itself is a door: tapping open ground (no pearl, no card) opens
     the Boba Night Map centered on this shop. If a card is open, the first
     tap just closes it (handled above). */
  var face = document.querySelector(".mp-face");
  if (face && center) {
    face.addEventListener("click", function (e) {
      if (!card.hidden) return;
      if (e.target.closest(".mp-spot") || e.target.closest(".mp-center") || e.target.closest(".mp-card") || e.target.closest("a")) return;
      var nm = center.getAttribute("data-nm");
      if (nm) window.location.href = nm;
    });
  }

  /* arrival via a pearl: #map centers the shop and opens its card */
  if (location.hash === "#map") {
    var sec = document.getElementById("map");
    if (sec) {
      sec.classList.add("mp-focus");
      setTimeout(function () {
        sec.scrollIntoView({ block: "center" });
        if (center) showCard(center, true);
      }, 250);
    }
  }
})();

/* ==== Find-it upgrade: real night-map tiles (same CARTO source as /near-me/),
   lazy-mounted when the section scrolls into view. The percent-positioned
   pearl chart stays in the DOM as the crawlable no-JS fallback and is hidden
   only after tiles actually mount. ==== */
(function () {
  "use strict";
  var face = document.querySelector(".mp-face");
  var leafBox = document.getElementById("mpLeaf");
  var stage = document.querySelector(".mp-stage");
  if (!face || !leafBox || !stage) return;

  var mounted = false;
  function mount() {
    if (mounted || typeof window.L === "undefined") return;
    mounted = true;
    var Lf = window.L;
    var center = stage.querySelector(".mp-center");
    var clat = parseFloat(center.getAttribute("data-lat")), clng = parseFloat(center.getAttribute("data-lng"));
    var map = Lf.map(leafBox, { zoomControl: false, dragging: false, scrollWheelZoom: false,
      doubleClickZoom: false, touchZoom: false, boxZoom: false, keyboard: false, tap: false });
    Lf.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
      { maxZoom: 19, attribution: "&copy; OpenStreetMap &copy; CARTO" }).addTo(map);
    var pts = [[clat, clng]];
    var spots = stage.querySelectorAll(".mp-spot");
    Array.prototype.forEach.call(spots, function (a) {
      pts.push([parseFloat(a.getAttribute("data-lat")), parseFloat(a.getAttribute("data-lng"))]);
    });
    map.fitBounds(pts, { padding: [34, 34], maxZoom: 15.2 });
    /* leaflet inits before layout settles when lazy-mounted: recompute twice */
    setTimeout(function () { map.invalidateSize(); map.fitBounds(pts, { padding: [34, 34], maxZoom: 15.2 }); }, 180);
    /* neighbor pearls as leaflet markers that reuse the card logic */
    Array.prototype.forEach.call(spots, function (a) {
      var chain = a.className.indexOf("mp-chain") > -1;
      var icon = Lf.divIcon({ className: "mp-leafspot" + (chain ? " mp-chain" : ""),
        html: '<span class="mp-dot"></span>', iconSize: [26, 26], iconAnchor: [13, 13] });
      var m = Lf.marker([parseFloat(a.getAttribute("data-lat")), parseFloat(a.getAttribute("data-lng"))],
        { icon: icon, keyboard: false }).addTo(map);
      m.on("click", function () {
        var el = m.getElement();
        ["data-n", "data-c", "data-mi", "data-nm", "data-per"].forEach(function (k) {
          var v = a.getAttribute(k); if (v !== null) el.setAttribute(k, v);
        });
        el.setAttribute("href", a.getAttribute("href"));
        if (window.__mpShowCard) window.__mpShowCard(el, false);
      });
    });
    /* the shop itself: glowing neon pin, click opens its card */
    var cicon = Lf.divIcon({ className: "mp-leafcenter",
      html: '<svg viewBox="0 0 24 24"><path d="M12 21c-4-4.5-7-8-7-11a7 7 0 0 1 14 0c0 3-3 6.5-7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>',
      iconSize: [40, 40], iconAnchor: [20, 34] });
    Lf.marker([clat, clng], { icon: cicon, keyboard: false }).addTo(map)
      .on("click", function () { if (window.__mpShowCard) window.__mpShowCard(center, true); });
    map.on("click", function () {
      var cardEl = document.getElementById("mpCard");
      if (cardEl && !cardEl.hidden) { cardEl.hidden = true; return; }
      var nm = center.getAttribute("data-nm");
      if (nm) window.location.href = nm;
    });
    face.classList.add("mp-has-tiles");
  }

  function loadLeaflet() {
    if (typeof window.L !== "undefined") { mount(); return; }
    var css = document.createElement("link");
    css.rel = "stylesheet"; css.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
    document.head.appendChild(css);
    var js = document.createElement("script");
    js.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
    js.onload = mount;               /* on failure nothing happens: grid chart remains */
    document.head.appendChild(js);
  }

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { loadLeaflet(); io.disconnect(); } });
    }, { rootMargin: "400px" });
    io.observe(face);
  } else { loadLeaflet(); }
})();

/* ==== Order it to go: sheet + sticky capsule reveal ==== */
(function () {
  "use strict";
  var modal = document.getElementById("odModal");
  var cap = document.getElementById("odCap");
  if (!modal) return;
  modal.hidden = true;
  var lastFocus = null;
  function openSheet() {
    lastFocus = document.activeElement;
    modal.hidden = false;
    var x = modal.querySelector(".od-x");
    if (x) x.focus({ preventScroll: true });
  }
  function closeSheet() {
    modal.hidden = true;
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }
  Array.prototype.forEach.call(document.querySelectorAll("[data-order-open]"), function (b) {
    b.addEventListener("click", openSheet);
  });
  Array.prototype.forEach.call(modal.querySelectorAll("[data-order-close]"), function (b) {
    b.addEventListener("click", closeSheet);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modal.hidden) closeSheet();
  });
  /* capsule appears once the hero scrolls away (desktop only via CSS) */
  if (cap) {
    cap.hidden = false;
    var hero = document.querySelector(".hero");
    if (hero && "IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { cap.classList.toggle("is-on", !e.isIntersecting); });
      }, { threshold: 0 }).observe(hero);
    } else {
      cap.classList.add("is-on");
    }
  }
})();
