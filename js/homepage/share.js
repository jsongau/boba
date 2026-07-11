/* NiteBoba Society — shared foundation (namespace CBS): data helpers, sharing,
   toast, and scroll reveal. Loaded before the feature modules. */
(function () {
  var CBS = (window.CBS = window.CBS || {});
  var S = (CBS.S = window.SOCIETY || { drinks: [], chains: {} });

  CBS.esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
  CBS.hash = function (s) { var h = 0, i; s = String(s); for (i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0; return h; };
  CBS.drinkById = function (id) { for (var i = 0; i < S.drinks.length; i++) if (S.drinks[i].id === id) return S.drinks[i]; return null; };
  CBS.chain = function (d) { return S.chains[d.ch] || { name: d.ch, locs: [] }; };
  CBS.shopFor = function (d, city) {
    var locs = CBS.chain(d).locs || [];
    if (!locs.length) return null;
    if (city) { var f = locs.filter(function (l) { return l.city === city; }); if (f.length) return f[CBS.hash(d.id) % f.length]; }
    return locs[CBS.hash(d.id) % locs.length];
  };
  var CAT = { milk_tea: "Milk tea", fruit_tea: "Fruit tea", brewed_tea: "Fresh tea", cheese_foam: "Cheese foam", slush: "Slush", coffee: "Coffee", fresh_milk: "Fresh milk", matcha: "Matcha", smoothie: "Smoothie" };
  CBS.catLabel = function (c) { return CAT[c] || c; };
  CBS.teaLabel = function (d) { var t = d.tea_base; if (!t || t === "none") return null; return t.replace(/\b\w/g, function (m) { return m.toUpperCase(); }); };
  CBS.tags = function (d) {
    var out = [];
    if (d.caf === "yes") out.push("Caffeine"); else if (d.caf === "no") out.push("Caffeine-free");
    if (d.dai === "yes") out.push("Contains dairy"); else if (d.dai === "no") out.push("Dairy-free");
    return out;
  };
  CBS.tagsHTML = function (d) { return CBS.tags(d).map(function (t) { return '<span class="tag">' + t + "</span>"; }).join(""); };
  CBS.mapsUrl = function (name, city) {
    return "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(name + " " + city + " CA");
  };
  CBS.profileUrl = function (shop) { return "/boba/ca/" + shop.cs + "/" + shop.s + "/"; };

  CBS.toast = function (msg) {
    var t = document.getElementById("cbsToast");
    if (!t) { t = document.createElement("div"); t.id = "cbsToast"; t.className = "toast"; t.setAttribute("role", "status"); t.setAttribute("aria-live", "polite"); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add("show");
    clearTimeout(t._t); t._t = setTimeout(function () { t.classList.remove("show"); }, 2200);
  };
  CBS.share = function (title, text) {
    if (navigator.share) { navigator.share({ title: title, text: text }).catch(function () {}); return; }
    var s = text; if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(s).then(function () { CBS.toast("Copied to share"); }).catch(function () { CBS.toast(s); });
    } else { CBS.toast("Copy: " + s); }
  };

  // scroll reveal (content is visible even if this never runs)
  function initReveal() {
    var els = [].slice.call(document.querySelectorAll(".reveal"));
    if (!("IntersectionObserver" in window) || !els.length) { els.forEach(function (e) { e.classList.add("in"); }); return; }
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    els.forEach(function (e) { io.observe(e); });
  }
  if (document.readyState !== "loading") initReveal(); else document.addEventListener("DOMContentLoaded", initReveal);
})();
