/* House Choice — "Leave it to the house." Quiet constraints, then a single
   selection revealed like a turned menu card. No wheel, no slot machine. */
(function () {
  var CBS = window.CBS; if (!CBS) return;
  var S = CBS.S, seed = 1, root;

  var CITIES = ["", "Irvine", "San Gabriel", "Los Angeles", "San Diego", "Arcadia", "Rowland Heights", "Garden Grove", "Fullerton"];

  function controls() {
    var cityOpts = CITIES.map(function (c) { return '<option value="' + c + '">' + (c || "Anywhere in Southern California") + "</option>"; }).join("");
    return '<div class="hc-controls" style="display:grid;gap:1rem;max-width:640px;margin:0 auto 1.6rem">' +
      '<label style="display:grid;gap:.4rem;font-size:.82rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted-dk)">City' +
        '<select data-hc="city" style="background:var(--smoked);border:1px solid var(--line-dk);color:var(--pearl);padding:.8rem 1rem;border-radius:4px;font-family:var(--sans);font-size:1rem">' + cityOpts + "</select></label>" +
      '<div class="hc-segs" style="display:grid;gap:1rem" data-hc-segwrap>' + seg("style", "The pour", [["", "Any"], ["tea", "Tea-forward"], ["dessert", "Dessert-like"]]) + seg("caf", "Caffeine", [["", "Any"], ["yes", "With"], ["no", "Without"]]) + "</div>" +
    "</div>" +
    '<div style="text-align:center"><button class="btn btn-primary" type="button" data-hc-reveal>Reveal tonight\u2019s choice</button></div>';
  }
  function seg(key, label, opts) {
    return '<div><span style="display:block;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted-dk);margin-bottom:.5rem">' + label + "</span>" +
      '<div class="seg" role="group" aria-label="' + label + '" style="display:inline-flex;border:1px solid var(--line-dk);border-radius:4px;overflow:hidden">' +
      opts.map(function (o, i) { return '<button type="button" data-seg="' + key + '" data-val="' + o[0] + '" aria-pressed="' + (i === 0 ? "true" : "false") + '" style="background:' + (i === 0 ? "rgba(197,164,109,.14)" : "transparent") + ';border:0;color:var(--pearl);padding:.6rem 1rem;font-family:var(--sans);font-size:.88rem;cursor:pointer;min-height:44px">' + o[1] + "</button>"; }).join("") +
      "</div></div>";
  }

  function pick(state) {
    var pool = S.drinks.filter(function (d) {
      if (state.city && !(CBS.chain(d).locs || []).some(function (l) { return l.city === state.city; })) return false;
      if (state.caf && d.caf !== state.caf) return false;
      return true;
    });
    if (!pool.length) return null;
    pool.sort(function (a, b) {
      function s(d) { var v = CBS.hash(d.id + "|" + seed) % 20; if (state.style === "tea") v += d.tf; else if (state.style === "dessert") v += (d.cr - d.tf); return v; }
      return s(b) - s(a);
    });
    return pool[0];
  }

  function reveal(state) {
    var d = pick(state);
    var box = root.querySelector("[data-hc-out]");
    if (!d) { box.innerHTML = '<p class="lede" style="text-align:center">No sourced match for that combination yet. Widen the city or caffeine and the house will choose again.</p>'; box.classList.add("show"); return; }
    var shop = CBS.shopFor(d, state.city) || CBS.shopFor(d), ch = CBS.chain(d).name;
    var save = JSON.stringify({ id: d.id, name: d.n + " \u00b7 " + ch, where: shop.city, url: CBS.profileUrl(shop) });
    box.innerHTML = '<div class="note hc-card" style="max-width:460px;margin:0 auto">' +
      '<p class="note-kick">The house has chosen</p>' +
      '<h3 class="note-drink">' + CBS.esc(d.n) + "</h3>" +
      '<p class="note-where">at ' + CBS.esc(ch) + ' <a href="' + CBS.profileUrl(shop) + '">' + CBS.esc(shop.city) + "</a></p>" +
      '<p class="note-why">' + CBS.esc(d.sum) + "</p>" +
      '<div class="chiprow">' + CBS.tagsHTML(d) + "</div>" +
      '<div class="note-actions" style="margin-top:1rem">' +
        '<a class="btn-mini btn-mini--solid" href="' + d.src + '" target="_blank" rel="noopener">The menu</a>' +
        '<a class="btn-mini" href="' + CBS.mapsUrl(ch, shop.city) + '" target="_blank" rel="noopener">Directions</a>' +
        '<button class="btn-mini" type="button" data-hc-save=\'' + CBS.esc(save) + '\'>Keep it</button>' +
        '<button class="btn-mini" type="button" data-hc-send="' + CBS.esc(d.n + " at " + ch + " (" + shop.city + ")") + '">Send</button>' +
        '<button class="btn-mini" type="button" data-hc-again>Choose again</button>' +
      "</div>" +
      '<p class="note-src">' + CBS.esc(ch) + "\u2019s menu, checked July 1, 2026.</p></div>";
    box.classList.add("show");
    box.setAttribute("tabindex", "-1"); box.focus();
  }

  function state() {
    return {
      city: root.querySelector('[data-hc="city"]').value,
      style: (root.querySelector('[data-seg="style"][aria-pressed="true"]') || {}).getAttribute ? root.querySelector('[data-seg="style"][aria-pressed="true"]').getAttribute("data-val") : "",
      caf: (root.querySelector('[data-seg="caf"][aria-pressed="true"]') || {}).getAttribute ? root.querySelector('[data-seg="caf"][aria-pressed="true"]').getAttribute("data-val") : ""
    };
  }

  function wire() {
    root = document.querySelector("[data-house]"); if (!root) return;
    root.innerHTML = controls() + '<div class="cq-result" data-hc-out style="margin-top:1.8rem"></div>';
    root.addEventListener("click", function (ev) {
      var sg = ev.target.closest("[data-seg]");
      if (sg) { var k = sg.getAttribute("data-seg"); root.querySelectorAll('[data-seg="' + k + '"]').forEach(function (b) { b.setAttribute("aria-pressed", "false"); b.style.background = "transparent"; }); sg.setAttribute("aria-pressed", "true"); sg.style.background = "rgba(197,164,109,.14)"; return; }
      if (ev.target.closest("[data-hc-reveal]") || ev.target.closest("[data-hc-again]")) { seed++; reveal(state()); return; }
      var sv = ev.target.closest("[data-hc-save]"); if (sv) { try { CBS.bb.add(JSON.parse(sv.getAttribute("data-hc-save"))); } catch (e) {} return; }
      var sd = ev.target.closest("[data-hc-send]"); if (sd) { CBS.share("Tonight, from NiteBoba Society", sd.getAttribute("data-hc-send") + " \u00b7 the house choice at NiteBoba Society"); return; }
    });
  }
  if (document.readyState !== "loading") wire(); else document.addEventListener("DOMContentLoaded", wire);
})();
