/* Navigation — desktop mega panels on hover and keyboard focus; a refined
   mobile drawer with search and recent selections from the Black Book. */
(function () {
  var CBS = window.CBS || {};
  function wire() {
    var items = [].slice.call(document.querySelectorAll(".nav-item"));
    function closeAll(except) { items.forEach(function (it) { if (it !== except) it.removeAttribute("data-open"); }); }
    items.forEach(function (it) {
      var link = it.querySelector(".nav-link"); if (!link) return;
      it.addEventListener("mouseenter", function () { closeAll(it); it.setAttribute("data-open", ""); });
      it.addEventListener("mouseleave", function () { it.removeAttribute("data-open"); });
      link.addEventListener("click", function (e) { if (it.querySelector(".mega")) { e.preventDefault(); var open = it.hasAttribute("data-open"); closeAll(); if (!open) it.setAttribute("data-open", ""); } });
      link.addEventListener("focus", function () { closeAll(it); });
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeAll(); closeDrawer(); } });
    document.addEventListener("click", function (e) { if (!e.target.closest(".nav-item")) closeAll(); });

    var drawer = document.getElementById("drawer");
    var burger = document.querySelector(".burger");
    function openDrawer() { if (!drawer) return; drawer.setAttribute("data-open", ""); document.body.classList.add("noscroll"); if (burger) burger.setAttribute("aria-expanded", "true"); var f = drawer.querySelector("input,button,a"); if (f) f.focus(); renderRecent(); }
    function closeDrawer() { if (!drawer) return; drawer.removeAttribute("data-open"); document.body.classList.remove("noscroll"); if (burger) burger.setAttribute("aria-expanded", "false"); }
    if (burger) burger.addEventListener("click", openDrawer);
    var xbtn = drawer && drawer.querySelector(".drawer-close"); if (xbtn) xbtn.addEventListener("click", closeDrawer);
    if (drawer) drawer.addEventListener("click", function (e) { if (e.target.closest("a")) closeDrawer(); });

    var navForm = document.querySelector("[data-navsearch]");
    if (navForm) navForm.addEventListener("submit", function (e) { e.preventDefault(); var i = navForm.querySelector("input"); var q = (i && i.value || "").trim(); if (q) location.href = "/directory/?q=" + encodeURIComponent(q); else if (i) i.focus(); });

    var search = drawer && drawer.querySelector(".drawer-search input");
    if (search) search.addEventListener("keydown", function (e) { if (e.key === "Enter") { var q = search.value.trim(); if (q) location.href = "/directory/?q=" + encodeURIComponent(q); } });

    function renderRecent() {
      var box = drawer && drawer.querySelector("[data-recent]"); if (!box || !CBS.bb) return;
      var a = CBS.bb.all().slice(0, 4);
      if (!a.length) { box.parentNode.style.display = "none"; return; }
      box.parentNode.style.display = "";
      box.innerHTML = a.map(function (e) { return '<a href="' + (e.url || "/directory/") + '">' + CBS.esc(e.name) + "</a>"; }).join("");
    }
  }
  if (document.readyState !== "loading") wire(); else document.addEventListener("DOMContentLoaded", wire);
})();
