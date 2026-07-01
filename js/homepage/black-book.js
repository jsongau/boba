/* The Black Book — a private notebook of saved drinks and shops (localStorage).
   Exposes CBS.bb for other modules; renders the #blackbook section. */
(function () {
  var CBS = (window.CBS = window.CBS || {});
  var KEY = "capyboba_blackbook_v1";
  var listeners = [];

  function read() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } }
  function write(a) { try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {} listeners.forEach(function (f) { f(a); }); }

  CBS.bb = {
    all: read,
    has: function (id) { return read().some(function (e) { return e.id === id; }); },
    add: function (entry) {
      var a = read();
      if (a.some(function (e) { return e.id === entry.id; })) { CBS.toast("Already in your Black Book"); return false; }
      a.unshift({ id: entry.id, name: entry.name, where: entry.where || "", url: entry.url || "", at: Date.now() });
      write(a); CBS.toast("Kept in your Black Book"); return true;
    },
    remove: function (id) { write(read().filter(function (e) { return e.id !== id; })); },
    clear: function () { write([]); },
    onChange: function (f) { listeners.push(f); }
  };

  function render() {
    var root = document.getElementById("blackbook"); if (!root) return;
    var body = root.querySelector("[data-bb-body]"); var foot = root.querySelector("[data-bb-foot]");
    var a = read();
    if (!a.length) {
      body.innerHTML = '<div class="bb-empty"><span class="serif-hi">Nothing kept yet.</span>' +
        "Save a drink from any selection and it will wait for you here, with the shop and the checked menu.</div>";
      if (foot) foot.style.display = "none";
      return;
    }
    if (foot) foot.style.display = "";
    body.innerHTML = '<ul class="bb-list">' + a.map(function (e) {
      var where = e.where ? '<span class="bb-w">' + CBS.esc(e.where) + "</span>" : "";
      var name = e.url ? '<a href="' + e.url + '">' + CBS.esc(e.name) + "</a>" : CBS.esc(e.name);
      return '<li class="bb-entry"><div><div class="bb-d">' + name + "</div>" + where +
        '</div><button class="bb-x" type="button" data-rm="' + CBS.esc(e.id) + '" aria-label="Remove ' + CBS.esc(e.name) + '">Remove</button></li>';
    }).join("") + "</ul>";
  }

  function wire() {
    var root = document.getElementById("blackbook"); if (!root) return;
    root.addEventListener("click", function (ev) {
      var rm = ev.target.closest("[data-rm]"); if (rm) { CBS.bb.remove(rm.getAttribute("data-rm")); return; }
      if (ev.target.closest("[data-bb-send]")) {
        var a = CBS.bb.all(); if (!a.length) return;
        var lines = a.slice(0, 12).map(function (e) { return "\u2022 " + e.name + (e.where ? " \u00b7 " + e.where : ""); });
        CBS.share("My Black Book \u00b7 CapyBoba Society", "My Black Book:\n" + lines.join("\n") + "\n\nvia CapyBoba Society");
      }
      if (ev.target.closest("[data-bb-clear]")) { if (confirm("Clear your Black Book on this device?")) CBS.bb.clear(); }
    });
    CBS.bb.onChange(render);
    render();
  }
  if (document.readyState !== "loading") wire(); else document.addEventListener("DOMContentLoaded", wire);
})();
