/* An Evening In — the routes are server-rendered and useful without JS.
   This only enhances them: reveal the backup stop, and send the plan. */
(function () {
  var CBS = window.CBS; if (!CBS) return;
  function wire() {
    var wrap = document.querySelector("[data-routes]"); if (!wrap) return;
    wrap.addEventListener("click", function (ev) {
      var bk = ev.target.closest("[data-backup]");
      if (bk) { var t = document.getElementById(bk.getAttribute("data-backup")); if (t) { var h = t.hasAttribute("hidden"); if (h) { t.removeAttribute("hidden"); bk.textContent = "Hide the backup"; } else { t.setAttribute("hidden", ""); bk.textContent = "Reveal the backup"; } } return; }
      var sd = ev.target.closest("[data-route-send]");
      if (sd) { CBS.share("An evening out \u00b7 CapyBoba Society", sd.getAttribute("data-route-send") + "\n\nvia CapyBoba Society"); return; }
    });
  }
  if (document.readyState !== "loading") wire(); else document.addEventListener("DOMContentLoaded", wire);
})();
