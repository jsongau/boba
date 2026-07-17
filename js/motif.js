/* ============================================================================
   BOBA NIGHT — THE MOTIF SYSTEM (js/motif.js)
   Self-initializing on DOMContentLoaded. Injects an original inline SVG for
   every .boba-motif[data-motif], draws .boba-divider, and wires the click
   "surprise" on both motifs and any .boba-surprise element. All visual motion
   is defined in css/motif.css (transform/opacity, reduced-motion gated); this
   file only toggles state classes and spawns the burst nodes.

   Zero dependencies, zero asset requests (SVG is inline), defer-friendly.
   If window.BobaSound exists and is enabled, a surprise plays BobaSound.pop()
   — guarded so the family is silent and harmless when sound is absent.
   ========================================================================== */
(function () {
  'use strict';

  /* ------- the original mark family. One 44x44 grid, one hairline weight. --
     Parts are painted by class (css/motif.css) so the lacquer palette stays
     centralized. The group carrying character motion is tagged .bm-anim (plus
     a motif-specific class the surprise keyframes hook). aria-hidden: these are
     decorative; the .boba-motif button carries the accessible label. */
  var MOTIFS = {
    /* tapioca pearl — a single glossy sphere */
    'pearl':
      '<g class="bm-anim bm-pearl-g">' +
        '<circle cx="22" cy="24" r="11" class="bm-fill-pearl bm-stroke"/>' +
        '<ellipse cx="18" cy="19.6" rx="3.1" ry="4.1" class="bm-hi"/>' +
      '</g>',

    /* jelly cube — an isometric lacquered cube with a top facet */
    'jelly':
      '<g class="bm-anim bm-jelly-g">' +
        '<path d="M12 18 L22 13 L32 18 L22 23 Z" class="bm-fill-amber bm-stroke"/>' +
        '<path d="M12 18 L12 30 L22 35 L22 23 Z" class="bm-fill-amber-2 bm-stroke"/>' +
        '<path d="M32 18 L32 30 L22 35 L22 23 Z" class="bm-fill-amber-3 bm-stroke"/>' +
        '<path d="M15 20.2 L18.4 22" class="bm-hi-line"/>' +
      '</g>',

    /* grass jelly — dark cubes stacked above a chawan bowl */
    'grass-jelly':
      '<g class="bm-anim">' +
        '<path d="M9 24 Q22 37 35 24" class="bm-fill-dark bm-stroke"/>' +
        '<path d="M9 24 H35" class="bm-stroke"/>' +
        '<rect x="14.5" y="14" width="7" height="7" rx="1.6" class="bm-fill-jelly bm-stroke-thin"/>' +
        '<rect x="22" y="15.5" width="6.4" height="6.4" rx="1.6" class="bm-fill-jelly bm-stroke-thin"/>' +
        '<rect x="19" y="8.5" width="6" height="6" rx="1.5" class="bm-fill-jelly bm-stroke-thin"/>' +
      '</g>',

    /* red bean — a cluster of azuki beans with seams */
    'red-bean':
      '<g class="bm-anim bm-bean-g">' +
        '<ellipse cx="17.5" cy="25" rx="6" ry="4" transform="rotate(-18 17.5 25)" class="bm-fill-bean bm-stroke-thin"/>' +
        '<ellipse cx="27" cy="21.5" rx="6" ry="4" transform="rotate(12 27 21.5)" class="bm-fill-bean bm-stroke-thin"/>' +
        '<ellipse cx="23.5" cy="30" rx="6" ry="4" transform="rotate(-6 23.5 30)" class="bm-fill-bean bm-stroke-thin"/>' +
        '<path d="M15 24.5 Q17.5 23.4 20 24.6" class="bm-hairline"/>' +
        '<path d="M24.5 21 Q27 20 29.5 21.4" class="bm-hairline"/>' +
      '</g>',

    /* taro — the milk-tea swirl, aubergine + cream (no neon purple) */
    'taro':
      '<g class="bm-anim bm-taro-g">' +
        '<circle cx="22" cy="22" r="11" class="bm-fill-taro bm-stroke"/>' +
        '<path d="M22 11 A11 11 0 0 1 22 33 A5.5 5.5 0 0 1 22 22 A5.5 5.5 0 0 0 22 11 Z" class="bm-fill-cream"/>' +
        '<circle cx="22" cy="16.5" r="1.7" class="bm-fill-taro"/>' +
        '<circle cx="22" cy="27.5" r="1.7" class="bm-fill-cream"/>' +
      '</g>',

    /* egg tart — fluted shell, custard, one cinnabar caramel spot */
    'egg-tart':
      '<g class="bm-anim bm-tart-g">' +
        '<path d="M12 18 L32 18 L28.5 30 Q22 33.5 15.5 30 Z" class="bm-fill-gold bm-stroke"/>' +
        '<path d="M16 18.6 L17.4 29.5" class="bm-flute"/>' +
        '<path d="M22 18.6 L22 31" class="bm-flute"/>' +
        '<path d="M28 18.6 L26.6 29.5" class="bm-flute"/>' +
        '<ellipse cx="22" cy="18" rx="10" ry="3.2" class="bm-fill-custard bm-stroke-thin"/>' +
        '<ellipse cx="19" cy="17.4" rx="2" ry="1.1" class="bm-fill-cinnabar"/>' +
      '</g>',

    /* milk foam — a dome of bubbles with two rising ones */
    'foam':
      '<g class="bm-anim bm-foam-g">' +
        '<circle cx="15.5" cy="25" r="5" class="bm-fill-pearl bm-stroke-thin"/>' +
        '<circle cx="28.5" cy="25" r="5" class="bm-fill-pearl bm-stroke-thin"/>' +
        '<circle cx="22" cy="22.5" r="6.4" class="bm-fill-pearl bm-stroke"/>' +
        '<path d="M10.5 28.5 H33.5" class="bm-stroke-thin"/>' +
        '<circle cx="18" cy="14.5" r="1.7" class="bm-bubble"/>' +
        '<circle cx="26.5" cy="12.5" r="1.3" class="bm-bubble"/>' +
      '</g>',

    /* drizzle — three streams pouring into gold drops */
    'drizzle':
      '<g class="bm-anim bm-drizzle-g">' +
        '<path d="M12 13 H32" class="bm-stroke"/>' +
        '<path d="M17 14 q-1.4 4 0 8 q1.2 3 0 6" class="bm-stream"/>' +
        '<path d="M22 14 q1.2 4 0 8 q-1.2 3 0 6" class="bm-stream"/>' +
        '<path d="M27 14 q1.4 4 0 8 q-1.2 3 0 6" class="bm-stream"/>' +
        '<path d="M17 30 q-2.2 2.6 0 4.4 q2.2-1.8 0-4.4 Z" class="bm-drop"/>' +
        '<path d="M22 30 q-2.2 2.6 0 4.4 q2.2-1.8 0-4.4 Z" class="bm-drop"/>' +
        '<path d="M27 30 q-2.2 2.6 0 4.4 q2.2-1.8 0-4.4 Z" class="bm-drop"/>' +
      '</g>',

    /* matcha — a chawan of whisked jade froth with a swirl */
    'matcha':
      '<g class="bm-anim bm-matcha-g">' +
        '<path d="M11 22 Q22 36 33 22" class="bm-fill-dark bm-stroke"/>' +
        '<ellipse cx="22" cy="22" rx="11" ry="3.5" class="bm-fill-jade bm-stroke"/>' +
        '<path d="M22 22 m-6 0 a6 6 0 1 1 3 5.1" class="bm-swirl-jade"/>' +
        '<circle cx="18" cy="21" r="1.1" class="bm-froth"/>' +
        '<circle cx="26" cy="22.6" r="1" class="bm-froth"/>' +
      '</g>'
  };

  var SVG_OPEN = '<svg class="bm-svg" viewBox="0 0 44 44" aria-hidden="true" focusable="false">';
  var SVG_CLOSE = '</svg>';

  /* champagne-thread beads: the divider is drawn with the pearl motif */
  var DIVIDER_SVG =
    '<svg class="bm-div-svg" viewBox="0 0 74 22" aria-hidden="true" focusable="false">' +
      '<path d="M6 11 H68" class="bm-hairline"/>' +
      '<circle cx="25" cy="11" r="5" class="bm-fill-pearl bm-stroke-thin bm-bead bm-bead-1"/>' +
      '<circle cx="37" cy="11" r="6" class="bm-fill-pearl bm-stroke bm-bead bm-bead-2"/>' +
      '<circle cx="49" cy="11" r="5" class="bm-fill-pearl bm-stroke-thin bm-bead bm-bead-3"/>' +
      '<ellipse cx="35" cy="9" rx="1.5" ry="2" class="bm-hi"/>' +
    SVG_CLOSE;

  function pop() {
    try {
      if (window.BobaSound && window.BobaSound.enabled && typeof window.BobaSound.pop === 'function') {
        window.BobaSound.pop();
      }
    } catch (e) { /* sound is a nicety, never a dependency */ }
  }

  var REDUCE = false;
  try {
    REDUCE = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (e) { REDUCE = false; }

  /* toggle .is-open long enough for the one-shot keyframe to run, then clear
     so the next click re-fires. No timers pile up: each mark tracks its own. */
  function surprise(el) {
    pop();
    if (REDUCE) return;              // honor the user; class churn adds nothing
    if (el._bmT) { clearTimeout(el._bmT); el.classList.remove('is-open'); }
    // force reflow so re-adding the class restarts the animation
    void el.offsetWidth;
    el.classList.add('is-open');
    el._bmT = setTimeout(function () {
      el.classList.remove('is-open');
      el._bmT = null;
    }, 760);
  }

  function buildMotif(el) {
    var name = el.getAttribute('data-motif');
    var art = MOTIFS[name];
    if (!art) return;                // unknown motif: leave the node untouched
    if (el.querySelector('.bm-svg')) return;   // idempotent
    el.insertAdjacentHTML('beforeend', SVG_OPEN + art + SVG_CLOSE);

    // make it operable + labelled if the author used a plain element
    var tag = el.tagName.toLowerCase();
    if (tag !== 'button' && tag !== 'a') {
      if (!el.hasAttribute('role')) el.setAttribute('role', 'button');
      if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '0');
    }
    if (!el.hasAttribute('aria-label') && !el.textContent.trim()) {
      el.setAttribute('aria-label', name.replace('-', ' ') + ' boba motif');
    }

    el.addEventListener('click', function () { surprise(el); });
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        surprise(el);
      }
    });
  }

  function buildDivider(el) {
    if (el.querySelector('.bm-div-beads')) return;
    el.insertAdjacentHTML('beforeend',
      '<span class="bm-div-line"></span>' +
      '<span class="bm-div-beads">' + DIVIDER_SVG + '</span>' +
      '<span class="bm-div-line"></span>');
    if (!el.hasAttribute('role')) el.setAttribute('role', 'separator');
    if (!el.hasAttribute('aria-hidden')) el.setAttribute('aria-hidden', 'true');
  }

  /* .boba-surprise: on click, spray a few pearls that float up and fade.
     Nodes are removed after the animation so nothing accumulates. */
  function wireSurprise(el) {
    if (el._bmSurprise) return;
    el._bmSurprise = true;
    el.addEventListener('click', function (ev) {
      pop();
      if (REDUCE) return;
      var burst = document.createElement('span');
      burst.className = 'bm-burst';
      var n = 6;
      for (var i = 0; i < n; i++) {
        var p = document.createElement('i');
        var ang = (Math.PI * (0.15 + 0.7 * (i / (n - 1))));  // fan upward
        var dist = 20 + Math.random() * 16;
        var bx = Math.round(-Math.cos(ang) * dist);
        var by = Math.round(-(16 + Math.sin(ang) * dist));
        p.style.setProperty('--bx', bx + 'px');
        p.style.setProperty('--by', by + 'px');
        // origin near the click point, relative to the element box
        var rect = el.getBoundingClientRect();
        var ox = (typeof ev.clientX === 'number' && ev.clientX) ? (ev.clientX - rect.left) : rect.width / 2;
        var oy = (typeof ev.clientY === 'number' && ev.clientY) ? (ev.clientY - rect.top) : rect.height / 2;
        p.style.left = ox + 'px';
        p.style.top = oy + 'px';
        p.style.animationDelay = (i * 24) + 'ms';
        burst.appendChild(p);
      }
      el.appendChild(burst);
      setTimeout(function () { if (burst.parentNode) burst.parentNode.removeChild(burst); }, 900);
    });
  }

  function init() {
    var motifs = document.querySelectorAll('.boba-motif');
    for (var i = 0; i < motifs.length; i++) buildMotif(motifs[i]);
    var dividers = document.querySelectorAll('.boba-divider');
    for (var j = 0; j < dividers.length; j++) buildDivider(dividers[j]);
    var surprises = document.querySelectorAll('.boba-surprise');
    for (var k = 0; k < surprises.length; k++) wireSurprise(surprises[k]);
  }

  // public hook so dynamically added markup can be wired after injection
  window.BobaMotif = { refresh: init };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
