/* The Tasting Flight — two or three real drinks presented side by side.
   Compare tea base, texture, caffeine, dairy; save, add to plan, or send. */
(function () {
  var CBS = window.CBS; if (!CBS) return;
  var S = CBS.S, root, seed = 1;

  // Build a flight: one silky classic, one bright/fruit, one unexpected — all sourced.
  function buildFlight() {
    var byRole = {
      classic: S.drinks.filter(function (d) { return d.cat === "milk_tea" && d.cr >= 74 && !d.adv; }),
      bright: S.drinks.filter(function (d) { return d.cat === "fruit_tea" || (d.cat === "brewed_tea" && d.tf >= 60); }),
      unexpected: S.drinks.filter(function (d) { return d.adv === 1 && (d.cat === "cheese_foam" || d.cat === "matcha" || d.cat === "smoothie" || d.tea_base === "none"); })
    };
    function pick(arr, salt) { if (!arr.length) return S.drinks[CBS.hash(salt + seed) % S.drinks.length]; return arr[CBS.hash(salt + seed) % arr.length]; }
    var out = [], used = {};
    [["A classic", "classic"], ["Something bright", "bright"], ["The wildcard", "unexpected"]].forEach(function (r) {
      var d = pick(byRole[r[1]], r[1]); var guard = 0;
      while (used[d.id] && guard++ < 8) { seed++; d = pick(byRole[r[1]], r[1]); }
      used[d.id] = 1; out.push({ role: r[0], d: d });
    });
    return out;
  }

  function pourHTML(item) {
    var d = item.d, shop = CBS.shopFor(d), ch = CBS.chain(d).name;
    var tea = CBS.teaLabel(d) || "\u00b7";
    var caf = d.caf === "yes" ? "Yes" : d.caf === "no" ? "No" : "Not stated";
    var dai = d.dai === "yes" ? "Yes" : d.dai === "no" ? "No" : "Not stated";
    var save = JSON.stringify({ id: d.id, name: d.n + " \u00b7 " + ch, where: shop.city, url: CBS.profileUrl(shop) });
    return '<div class="pour-col">' +
      '<span class="pc-kind">' + CBS.esc(item.role) + "</span>" +
      '<h3 class="pc-name">' + CBS.esc(d.n) + "</h3>" +
      '<p class="pc-where">' + CBS.esc(ch) + ' \u00b7 <a href="' + CBS.profileUrl(shop) + '">' + CBS.esc(shop.city) + "</a></p>" +
      '<p class="pc-note">' + CBS.esc(d.sum) + "</p>" +
      '<dl class="pc-spec"><dt>Style</dt><dd>' + CBS.esc(CBS.catLabel(d.cat)) + "</dd>" +
        "<dt>Tea base</dt><dd>" + CBS.esc(tea) + "</dd>" +
        "<dt>Caffeine</dt><dd>" + caf + "</dd><dt>Dairy</dt><dd>" + dai + "</dd></dl>" +
      '<div class="pc-actions">' +
        '<button class="btn-mini" type="button" data-tf-save=\'' + CBS.esc(save) + '\'>Keep it</button>' +
        '<a class="btn-mini" href="' + d.src + '" target="_blank" rel="noopener">Menu</a>' +
      "</div></div>";
  }

  function current() { return root._flight || (root._flight = buildFlight()); }

  function render() {
    var grid = root.querySelector("[data-flight-grid]");
    grid.innerHTML = current().map(pourHTML).join("");
  }

  function wire() {
    root = document.querySelector("[data-flight]"); if (!root) return;
    render();
    root.addEventListener("click", function (ev) {
      var sv = ev.target.closest("[data-tf-save]"); if (sv) { try { CBS.bb.add(JSON.parse(sv.getAttribute("data-tf-save"))); } catch (e) {} return; }
      if (ev.target.closest("[data-tf-shuffle]")) { seed++; root._flight = buildFlight(); render(); return; }
      if (ev.target.closest("[data-tf-send]")) {
        var lines = current().map(function (i) { var sh = CBS.shopFor(i.d); return "\u2022 " + i.d.n + " \u00b7 " + CBS.chain(i.d).name + " (" + sh.city + ")"; });
        CBS.share("A tasting flight \u00b7 CapyBoba Society", "A tasting flight:\n" + lines.join("\n") + "\n\nvia CapyBoba Society");
      }
    });
  }
  if (document.readyState !== "loading") wire(); else document.addEventListener("DOMContentLoaded", wire);
})();
