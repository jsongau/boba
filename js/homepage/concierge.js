/* The Tea Concierge — four unhurried questions, then one real selection from
   sourced menu data. Keyboard + touch; no drag, no score, no game visuals. */
(function () {
  var CBS = window.CBS; if (!CBS) return;
  var S = CBS.S;

  // Each answer nudges a taste target {cr, tf}, a set of preferred categories, and adventure.
  var STEPS = [
    { key: "evening", q: "What kind of evening is this?", opts: [
      { v: "solo", t: "A solo reset", d: "Quiet, for you", sw: "#123F35", cats: ["brewed_tea", "milk_tea"], adv: 0 },
      { v: "date", t: "A date", d: "Something considered", sw: "#7A2433", cats: ["matcha", "milk_tea"], adv: 0.5 },
      { v: "friends", t: "With friends", d: "Easy and generous", sw: "#C5A46D", cats: ["slush", "fruit_tea", "milk_tea"], adv: 0.5 },
      { v: "study", t: "A long session", d: "Something to sit with", sw: "#342235", cats: ["milk_tea", "brewed_tea"], adv: 0 },
      { v: "after", t: "After dinner", d: "A sweet nightcap", sw: "#8E734B", cats: ["cheese_foam", "smoothie", "matcha"], adv: 0.5 },
      { v: "spont", t: "Something spontaneous", d: "Surprise me a little", sw: "#0E332B", cats: [], adv: 1 }
    ] },
    { key: "sip", q: "What should the first sip feel like?", opts: [
      { v: "silky", t: "Silky", d: "Creamy, rounded", sw: "#C5A46D", cr: 86, tf: 45, cats: ["milk_tea", "fresh_milk"] },
      { v: "bright", t: "Bright", d: "Fruit and tea", sw: "#7A2433", cr: 4, tf: 35, cats: ["fruit_tea"] },
      { v: "teaforward", t: "Deeply tea-forward", d: "Clean, brewed", sw: "#123F35", cr: 10, tf: 92, cats: ["brewed_tea"] },
      { v: "toasted", t: "Toasted", d: "Oolong, brown sugar", sw: "#8E734B", cr: 80, tf: 62, cats: ["milk_tea"] },
      { v: "floral", t: "Floral", d: "Jasmine, matcha", sw: "#342235", cr: 58, tf: 62, cats: ["matcha", "milk_tea"] },
      { v: "dessert", t: "Dessert-like", d: "Rich, sweet", sw: "#0B0C0E", cr: 82, tf: 18, cats: ["smoothie", "slush", "cheese_foam", "milk_tea"] }
    ] },
    { key: "adv", q: "How adventurous should the choice be?", opts: [
      { v: "familiar", t: "Familiar", d: "A trusted classic", sw: "#C5A46D", adv: 0 },
      { v: "considered", t: "Considered", d: "A step sideways", sw: "#8E734B", adv: 0.5 },
      { v: "unexpected", t: "Unexpected", d: "Something new", sw: "#7A2433", adv: 1 }
    ] },
    { key: "where", q: "Where should we look?", opts: [
      { v: "", t: "No preference", d: "Anywhere in Southern California", sw: "#123F35", city: "" },
      { v: "Irvine", t: "Irvine", d: "Orange County", sw: "#8E734B", city: "Irvine" },
      { v: "San Gabriel", t: "San Gabriel", d: "The 626", sw: "#7A2433", city: "San Gabriel" },
      { v: "Los Angeles", t: "Los Angeles", d: "Greater LA", sw: "#342235", city: "Los Angeles" },
      { v: "San Diego", t: "San Diego", d: "Convoy and beyond", sw: "#0E332B", city: "San Diego" },
      { v: "drive", t: "Willing to drive", d: "Open to the best", sw: "#C5A46D", city: "" }
    ] }
  ];

  var answers = {}, step = 0, root, lastId = null;

  function scored() {
    var s2 = STEPS[1].opts.filter(function (o) { return o.v === answers.sip; })[0] || {};
    var target = { cr: s2.cr != null ? s2.cr : 60, tf: s2.tf != null ? s2.tf : 50 };
    var cats = {};
    [STEPS[0], STEPS[1]].forEach(function (st) {
      var o = st.opts.filter(function (x) { return x.v === answers[st.key]; })[0];
      if (o && o.cats) o.cats.forEach(function (c) { cats[c] = (cats[c] || 0) + 1; });
    });
    var advOpt = STEPS[2].opts.filter(function (o) { return o.v === answers.adv; })[0];
    var e0 = STEPS[0].opts.filter(function (o) { return o.v === answers.evening; })[0] || {};
    var advPref = advOpt ? advOpt.adv : (e0.adv != null ? e0.adv : 0.5);
    var w4 = STEPS[3].opts.filter(function (o) { return o.v === answers.where; })[0] || {};
    var city = w4.city || "";

    var pool = S.drinks.filter(function (d) { return !city || (CBS.chain(d).locs || []).some(function (l) { return l.city === city; }); });
    if (!pool.length) pool = S.drinks;

    var ranked = pool.map(function (d) {
      var dist = Math.abs(d.cr - target.cr) + Math.abs(d.tf - target.tf);
      var score = 200 - dist;
      if (cats[d.cat]) score += 26 * cats[d.cat];
      score -= Math.abs((d.adv ? 1 : 0) - advPref) * 34;
      score += CBS.hash(d.id) % 9; // gentle tie-break so "another" varies
      return { d: d, score: score };
    }).sort(function (a, b) { return b.score - a.score; });

    var primary = ranked[0].d;
    if (lastId && ranked.length > 3 && primary.id === lastId) primary = ranked[1].d;
    var alt = null;
    for (var i = 0; i < ranked.length; i++) { if (ranked[i].d.ch !== primary.ch) { alt = ranked[i].d; break; } }
    if (!alt) alt = ranked[1] ? ranked[1].d : primary;
    lastId = primary.id;
    return { primary: primary, alt: alt, city: city };
  }

  function whyLine(d) {
    var bits = [];
    if (d.cr >= 70) bits.push("silky"); else if (d.cr <= 15) bits.push("clean and bright");
    if (d.tf >= 75) bits.push("deeply tea-forward"); else if (d.tf >= 45) bits.push("tea-forward");
    if (d.dai === "no") bits.push("dairy-free");
    if (d.caf === "no") bits.push("caffeine-free");
    var lead = bits.slice(0, 2).join(", ");
    return (lead ? lead.charAt(0).toUpperCase() + lead.slice(1) + ". " : "") + d.sum;
  }

  function noteHTML(res) {
    var d = res.primary, shop = CBS.shopFor(d, res.city) || CBS.shopFor(d);
    var alt = res.alt, altShop = CBS.shopFor(alt, res.city) || CBS.shopFor(alt);
    var ch = CBS.chain(d).name, chAlt = CBS.chain(alt).name;
    var save = JSON.stringify({ id: d.id, name: d.n + " \u00b7 " + ch, where: shop.city, url: CBS.profileUrl(shop) });
    return '<div class="note" role="group" aria-label="Your selection">' +
      '<p class="note-kick">The concierge suggests</p>' +
      '<h3 class="note-drink">' + CBS.esc(d.n) + "</h3>" +
      '<p class="note-where">at ' + CBS.esc(ch) + ' <a href="' + CBS.profileUrl(shop) + '">' + CBS.esc(shop.city) + "</a></p>" +
      '<p class="note-why">' + CBS.esc(whyLine(d)) + "</p>" +
      '<div class="chiprow">' + CBS.tagsHTML(d) + "</div>" +
      '<p class="note-meta" style="margin-top:.9rem">Or, quieter: <strong>' + CBS.esc(alt.n) + "</strong> at " + CBS.esc(chAlt) + " \u00b7 " + CBS.esc(altShop.city) + "</p>" +
      '<div class="note-actions">' +
        '<a class="btn-mini btn-mini--solid" href="' + d.src + '" target="_blank" rel="noopener">The menu</a>' +
        '<a class="btn-mini" href="' + CBS.mapsUrl(ch, shop.city) + '" target="_blank" rel="noopener">Directions</a>' +
        '<button class="btn-mini" type="button" data-save=\'' + CBS.esc(save) + '\'>Keep it</button>' +
        '<button class="btn-mini" type="button" data-send="' + CBS.esc(d.n + " at " + ch + " (" + shop.city + ")") + '">Send</button>' +
        '<button class="btn-mini" type="button" data-again>Another</button>' +
      "</div>" +
      '<p class="note-src">' + CBS.esc(ch) + "\u2019s menu, checked July 1, 2026. We show only what the official menu states.</p>" +
    "</div>";
  }

  function renderStep() {
    var st = STEPS[step];
    var prog = STEPS.map(function (_, i) { return '<i class="' + (i <= step ? "on" : "") + '"></i>'; }).join("");
    var opts = st.opts.map(function (o) {
      return '<button class="cq-opt" type="button" role="listitem" data-v="' + CBS.esc(o.v) +
        '" aria-pressed="' + (answers[st.key] === o.v ? "true" : "false") + '">' +
        '<span class="swatch" style="background:' + o.sw + '"></span>' +
        '<span class="ot">' + CBS.esc(o.t) + "</span><span class=\"od\">" + CBS.esc(o.d) + "</span></button>";
    }).join("");
    root.querySelector("[data-cq-shell]").innerHTML =
      '<div class="cq-progress" aria-hidden="true">' + prog + "</div>" +
      '<div class="cq-step active"><p class="cq-q">' + CBS.esc(st.q) + '</p>' +
      '<div class="cq-opts" role="list">' + opts + "</div>" +
      '<div class="cq-nav">' + (step > 0 ? '<button class="cq-back" type="button" data-back>\u2190 Back</button>' : "") + "</div></div>";
    var res = root.querySelector("[data-cq-result]"); if (res) res.classList.remove("show");
    // Only move focus after the user has interacted — focusing on initial page
    // load scroll-hijacks the visitor past the hero (real bug, fixed 12JUL26).
    var focusable = root.querySelector(".cq-opt");
    if (focusable && window.__cqInteracted) focusable.focus({preventScroll:true});
  }

  document.addEventListener("click", function () { window.__cqInteracted = true; }, { once: true, capture: true });

  function showResult() {
    var res = scored();
    var box = root.querySelector("[data-cq-result]");
    box.innerHTML = noteHTML(res);
    box.classList.add("show");
    root.querySelector("[data-cq-shell]").innerHTML =
      '<div class="cq-progress" aria-hidden="true">' + STEPS.map(function () { return '<i class="on"></i>'; }).join("") + "</div>" +
      '<p class="cq-q" style="font-size:1.2rem;color:var(--silver)">Your selection for the evening</p>';
    box.setAttribute("tabindex", "-1"); box.focus();
    var live = root.querySelector("[data-cq-live]"); if (live) live.textContent = "Selected: " + res.primary.n + " at " + CBS.chain(res.primary).name + ", " + (CBS.shopFor(res.primary, res.city) || CBS.shopFor(res.primary)).city;
  }

  function wire() {
    root = document.querySelector("[data-concierge]"); if (!root) return;
    root.innerHTML =
      '<div class="concierge-shell">' +
        '<div data-cq-shell></div>' +
        '<div class="cq-result" data-cq-result></div>' +
        '<p class="sr-only" role="status" aria-live="polite" data-cq-live></p>' +
      "</div>";
    root.addEventListener("click", function (ev) {
      var opt = ev.target.closest(".cq-opt");
      if (opt) { answers[STEPS[step].key] = opt.getAttribute("data-v"); if (step < STEPS.length - 1) { step++; renderStep(); } else { showResult(); } return; }
      if (ev.target.closest("[data-back]")) { if (step > 0) { step--; renderStep(); } return; }
      if (ev.target.closest("[data-again]")) { showResult(); return; }
      var sv = ev.target.closest("[data-save]"); if (sv) { try { CBS.bb.add(JSON.parse(sv.getAttribute("data-save"))); } catch (e) {} return; }
      var sd = ev.target.closest("[data-send]"); if (sd) { CBS.share("A selection from NiteBoba Society", sd.getAttribute("data-send") + " \u00b7 chosen at NiteBoba Society"); return; }
    });
    renderStep();
  }
  if (document.readyState !== "loading") wire(); else document.addEventListener("DOMContentLoaded", wire);
})();
