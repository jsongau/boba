/* ============================================================================
   BOBA NIGHT — unified navigation behavior (nav-midnight.js)
   Vanilla, no dependencies. Disclosure panels (click-to-open, Escape-close),
   SHOPS region tablist, cmd-K / slash search overlay, mobile drawer with
   region accordions, fixed bottom bar. Keyboard-accessible throughout.
   ========================================================================== */
(function () {
  "use strict";
  var doc = document;
  function $(sel, root) { return (root || doc).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || doc).querySelectorAll(sel)); }

  var header = $("[data-bn-header]");
  if (!header) return;

  /* ------------------------------------------------------- desktop panels */
  var items = $$(".bn-item", header);
  var openItem = null;

  function closePanel() {
    if (!openItem) return;
    var trig = $(".bn-trigger", openItem);
    var panel = $(".bn-panel", openItem);
    openItem.removeAttribute("data-open");
    trig.setAttribute("aria-expanded", "false");
    // let the fade run, then hide from a11y tree
    panel.setAttribute("hidden", "");
    openItem = null;
    header.removeAttribute("data-panel-open");
  }

  function openPanel(item) {
    if (openItem === item) { closePanel(); return; }
    if (openItem) closePanel();
    var trig = $(".bn-trigger", item);
    var panel = $(".bn-panel", item);
    panel.removeAttribute("hidden");
    // next frame so the transition plays from the hidden state
    requestAnimationFrame(function () { item.setAttribute("data-open", ""); });
    item.setAttribute("data-open", "");
    trig.setAttribute("aria-expanded", "true");
    header.setAttribute("data-panel-open", "");
    openItem = item;
  }

  items.forEach(function (item) {
    var trig = $(".bn-trigger", item);
    trig.addEventListener("click", function (e) {
      e.stopPropagation();
      openPanel(item);
    });
    // hover-intent is intentionally NOT used: click-to-open per spec.
  });

  // close on outside click
  doc.addEventListener("click", function (e) {
    if (openItem && !openItem.contains(e.target)) closePanel();
  });

  /* --------------------------------------------- SHOPS region tablist swap */
  $$(".bn-mega--shops").forEach(function (mega) {
    var tabs = $$(".bn-rail-b[role='tab']", mega);
    var panes = $$(".bn-pane", mega);
    function select(tab, focus) {
      var region = tab.getAttribute("data-region");
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
      });
      panes.forEach(function (p) {
        if (p.getAttribute("data-region") === region) p.removeAttribute("hidden");
        else p.setAttribute("hidden", "");
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { select(tab); });
      tab.addEventListener("mouseenter", function () { select(tab); });
      tab.addEventListener("keydown", function (e) {
        var k = e.key, n = null;
        if (k === "ArrowDown" || k === "ArrowRight") n = tabs[(i + 1) % tabs.length];
        else if (k === "ArrowUp" || k === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
        else if (k === "Home") n = tabs[0];
        else if (k === "End") n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
  });

  /* --------------------------------------------------------- search overlay */
  var overlay = $("#bn-search");
  var overlayInput = overlay ? $("#bn-overlayq", overlay) : null;
  var resultsBox = overlay ? $("#bn-results", overlay) : null;
  var emptyMsg = overlay ? $("[data-bn-empty]", overlay) : null;
  var index = null, indexLoading = false;
  var lastFocus = null;
  var activeRes = -1;

  function loadIndex(cb) {
    if (index) { cb(index); return; }
    if (indexLoading) return;
    indexLoading = true;
    fetch("/js/search-index.json").then(function (r) { return r.json(); })
      .then(function (data) { index = data; indexLoading = false; cb(index); })
      .catch(function () { indexLoading = false; });
  }

  function openOverlay() {
    if (!overlay) return;
    lastFocus = doc.activeElement;
    overlay.removeAttribute("hidden");
    doc.body.classList.add("bn-lock");
    closePanel();
    closeDrawer();
    loadIndex(function () {});
    requestAnimationFrame(function () { overlayInput.focus(); });
  }
  function closeOverlay() {
    if (!overlay || overlay.hasAttribute("hidden")) return;
    overlay.setAttribute("hidden", "");
    doc.body.classList.remove("bn-lock");
    overlayInput.value = "";
    renderResults("");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function esc(s) { return String(s).replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; }); }
  function highlight(name, q) {
    var i = name.toLowerCase().indexOf(q);
    if (i < 0) return esc(name);
    return esc(name.slice(0, i)) + "<mark>" + esc(name.slice(i, i + q.length)) + "</mark>" + esc(name.slice(i + q.length));
  }

  var GROUPS = [
    { key: "shops", label: "Tea Houses", meta: function (r) { return r.c; } },
    { key: "cities", label: "Cities", meta: function () { return ""; } },
    { key: "pages", label: "Pages", meta: function (r) { return r.g || ""; } },
    { key: "ingredients", label: "Ingredients", meta: function () { return "Pantry"; } }
  ];

  function renderResults(q) {
    if (!resultsBox) return;
    activeRes = -1;
    q = (q || "").trim().toLowerCase();
    if (!q) { resultsBox.innerHTML = ""; resultsBox.appendChild(emptyMsg); overlayInput.setAttribute("aria-expanded", "false"); return; }
    if (!index) { return; }
    var html = "", any = false;
    GROUPS.forEach(function (g) {
      var rows = (index[g.key] || []).filter(function (r) {
        return (r.n || "").toLowerCase().indexOf(q) >= 0;
      }).slice(0, 5);
      if (!rows.length) return;
      any = true;
      html += '<div class="bn-group-h">' + esc(g.label) + "</div>";
      rows.forEach(function (r) {
        var m = g.meta(r);
        html += '<a class="bn-res" role="option" href="' + esc(r.u) + '">' +
          '<span class="bn-res-name">' + highlight(r.n, q) + "</span>" +
          (m ? '<span class="bn-res-meta">' + esc(m) + "</span>" : "") + "</a>";
      });
    });
    overlayInput.setAttribute("aria-expanded", any ? "true" : "false");
    resultsBox.innerHTML = any ? html : '<p class="bn-results-empty">No matches for “' + esc(q) + '”.</p>';
  }

  function resItems() { return $$(".bn-res", resultsBox); }
  function setActive(i) {
    var els = resItems();
    if (!els.length) return;
    activeRes = (i + els.length) % els.length;
    els.forEach(function (el, n) {
      if (n === activeRes) { el.setAttribute("aria-selected", "true"); el.scrollIntoView({ block: "nearest" }); }
      else el.removeAttribute("aria-selected");
    });
  }

  if (overlay) {
    overlayInput.addEventListener("input", function () { renderResults(overlayInput.value); });
    overlayInput.addEventListener("keydown", function (e) {
      var els = resItems();
      if (e.key === "ArrowDown") { e.preventDefault(); setActive(activeRes + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); setActive(activeRes - 1); }
      else if (e.key === "Enter") {
        if (activeRes >= 0 && els[activeRes]) { window.location.href = els[activeRes].getAttribute("href"); }
      }
    });
    $$("[data-bn-search-close]", overlay).forEach(function (b) {
      b.addEventListener("click", closeOverlay);
    });
  }

  // openers: persistent field, drawer button, bottom-bar button
  $$("[data-bn-search-open]").forEach(function (el) {
    el.addEventListener("click", function (e) { e.preventDefault(); openOverlay(); });
    el.addEventListener("submit", function (e) { e.preventDefault(); openOverlay(); });
  });
  $$("[data-bn-open-search]").forEach(function (el) {
    el.addEventListener("click", function (e) { e.preventDefault(); openOverlay(); });
  });

  /* --------------------------------------------------------------- drawer */
  var drawer = $("#bn-drawer");
  var burger = $(".bn-burger", header);

  function openDrawer() {
    if (!drawer) return;
    drawer.removeAttribute("hidden");
    requestAnimationFrame(function () { drawer.setAttribute("data-open", ""); });
    burger.setAttribute("aria-expanded", "true");
    doc.body.classList.add("bn-lock");
    var x = $(".bn-drawer-x", drawer);
    if (x) x.focus();
  }
  function closeDrawer() {
    if (!drawer || drawer.hasAttribute("hidden")) return;
    drawer.removeAttribute("data-open");
    burger.setAttribute("aria-expanded", "false");
    doc.body.classList.remove("bn-lock");
    var d = drawer;
    var onEnd = function () { d.setAttribute("hidden", ""); d.removeEventListener("transitionend", onEnd); };
    d.addEventListener("transitionend", onEnd);
    // fallback for reduced-motion (no transition fires)
    setTimeout(function () { if (!d.hasAttribute("data-open")) d.setAttribute("hidden", ""); }, 320);
    if (burger) burger.focus();
  }

  if (burger) burger.addEventListener("click", function () {
    if (drawer && drawer.hasAttribute("hidden")) openDrawer(); else closeDrawer();
  });
  if (drawer) {
    $$("[data-bn-drawer-close]", drawer).forEach(function (b) { b.addEventListener("click", closeDrawer); });
    // region accordions
    $$(".bn-acc-b", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var on = b.getAttribute("aria-expanded") === "true";
        b.setAttribute("aria-expanded", on ? "false" : "true");
      });
    });
  }

  /* ---------------------------------------------------------- global keys */
  doc.addEventListener("keydown", function (e) {
    // cmd-K / ctrl-K -> search
    if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) {
      e.preventDefault(); openOverlay(); return;
    }
    // "/" -> search (unless typing in a field)
    if (e.key === "/" && !/^(INPUT|TEXTAREA|SELECT)$/.test((e.target.tagName || "")) && !e.target.isContentEditable) {
      e.preventDefault(); openOverlay(); return;
    }
    if (e.key === "Escape") {
      if (overlay && !overlay.hasAttribute("hidden")) { closeOverlay(); return; }
      if (drawer && !drawer.hasAttribute("hidden")) { closeDrawer(); return; }
      if (openItem) { var t = $(".bn-trigger", openItem); closePanel(); if (t) t.focus(); }
    }
  });
})();
