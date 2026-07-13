/* Tonight's Pour — the hero selection rotates daily at 5 PM, chosen
   deterministically from the sourced SOCIETY menu (66 drinks, official
   sources only). Static HTML remains as the no-JS fallback; this rewrites
   the card in place so every visitor sees today's pour, not a fixed one. */
(function () {
  var CBS = window.CBS; if (!CBS || !CBS.S || !CBS.S.drinks.length) return;

  function wire() {
    var card = document.querySelector(".note--float"); if (!card) return;

    // Day index that ticks over at 5 PM local — "tonight" starts at five.
    var now = new Date();
    var shifted = new Date(now.getTime() - 17 * 3600 * 1000);
    var dayN = Math.floor((shifted.getTime() - shifted.getTimezoneOffset() * 60000) / 86400000);

    var drinks = CBS.S.drinks;
    var d = drinks[((dayN % drinks.length) + drinks.length) % drinks.length];
    var chain = CBS.chain(d);
    var shop = CBS.shopFor(d, null);
    if (!shop) return; // keep static fallback if the chain has no locations

    var profile = CBS.profileUrl(shop);
    var maps = CBS.mapsUrl(shop.name, shop.city);
    var kick = card.querySelector(".note-kick");
    if (kick) kick.textContent = "Tonight’s pour · changes daily at 5";
    var nd = card.querySelector(".note-drink"); if (nd) nd.textContent = d.n;
    var nw = card.querySelector(".note-where");
    if (nw) nw.innerHTML = "at " + CBS.esc(shop.name) + ' <a href="' + profile + '">' + CBS.esc(shop.city) + "</a>";
    var why = card.querySelector(".note-why"); if (why) why.textContent = d.sum;
    var chips = card.querySelector(".chiprow"); if (chips) chips.innerHTML = CBS.tagsHTML(d);
    var acts = card.querySelector(".note-actions");
    if (acts) {
      var savePayload = CBS.esc(JSON.stringify({ id: d.id, name: d.n + " · " + shop.name, where: shop.city, url: profile }));
      acts.innerHTML =
        '<a class="btn-mini btn-mini--solid" href="' + CBS.esc(d.src) + '" target="_blank" rel="noopener">The menu</a>' +
        '<a class="btn-mini" href="' + maps + '" target="_blank" rel="noopener">Directions</a>' +
        '<button class="btn-mini" type="button" data-save=\'' + savePayload + "'>Keep it</button>" +
        '<button class="btn-mini" type="button" data-send="' + CBS.esc(d.n + " at " + shop.name + " (" + shop.city + ")") + '">Send</button>';
    }
    var src = card.querySelector(".note-src");
    if (src) src.textContent = chain.name + "’s menu, checked July 1, 2026. We show only what the official menu states.";

    // The card sits outside the concierge/black-book roots, so wire its own
    // save/send here (scoped to the card to avoid double-handling elsewhere).
    card.addEventListener("click", function (ev) {
      var sv = ev.target.closest("[data-save]");
      if (sv && CBS.bb) { try { CBS.bb.add(JSON.parse(sv.getAttribute("data-save"))); CBS.toast("Kept in your Black Book"); } catch (e) {} return; }
      var sd = ev.target.closest("[data-send]");
      if (sd) { CBS.share("Tonight’s pour · NiteBoba Society", sd.getAttribute("data-send") + "\n\nvia NiteBoba Society"); }
    });
  }
  if (document.readyState !== "loading") wire(); else document.addEventListener("DOMContentLoaded", wire);
})();
