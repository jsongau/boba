/* ============================================================================
   BOBA NIGHT — OPT-IN CHIME SOUND SYSTEM (js/sound.js)
   Self-initializing on DOMContentLoaded. Exposes:

       window.BobaSound = { chime(name), pop(), setEnabled(bool), enabled }

   Every tone is SYNTHESIZED at runtime with the WebAudio API — there are no
   .mp3/.wav assets, so the feature adds zero network weight. Palette:
     · pop    — soft marimba tap for clicks / surprises
     · reveal — a brighter two-note chime for card / panel reveals
     · tick   — a very quiet, heavily rate-limited hover blip
     · toggle — a short confirming chime played when sound is switched ON

   DEFAULT OFF, persisted in localStorage 'bobanight_sound_v1'. Sound NEVER
   autoplays: the AudioContext is only created / resumed inside the user
   gesture that enables sound, which also satisfies browser autoplay policy.
   On load a small toggle button (.bn-sound-toggle, aria-pressed) is injected
   into the nav actions area next to the Tonight CTA (fixed top-right fallback).

   Styling lives in css/sound.css. This file owns behavior only and does not
   touch any page markup or other script. Console logs are emitted so headless
   verification can assert the AudioContext + oscillators actually fire.
   ========================================================================== */
(function () {
  'use strict';

  var LS_KEY = 'bobanight_sound_v1';
  var TAG = '[BobaSound]';

  /* ---- persisted state (default OFF) ------------------------------------ */
  function readPref() {
    try { return localStorage.getItem(LS_KEY) === 'on'; }
    catch (e) { return false; }
  }
  function writePref(on) {
    try { localStorage.setItem(LS_KEY, on ? 'on' : 'off'); } catch (e) {}
  }

  var enabled = readPref();     // whether chimes are allowed to play
  var ctx = null;               // lazily created AudioContext
  var master = null;            // master gain so nothing ever clips loud
  var toggleEl = null;          // the injected button

  var reduceMotion = false;
  try {
    reduceMotion = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (e) {}

  /* ---- rate limiting — never a machine gun ------------------------------ */
  var lastAny = 0;              // last time ANY sound played
  var lastByName = {};          // last time each named sound played
  var GLOBAL_GAP = 40;          // ms floor between any two tones
  var COOLDOWN = { pop: 55, reveal: 180, tick: 90, toggle: 0 };

  function now() {
    return (window.performance && performance.now)
      ? performance.now() : Date.now();
  }

  /* ---- the synth --------------------------------------------------------- */
  function ensureCtx() {
    if (ctx) return ctx;
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) { console.warn(TAG + ' WebAudio unavailable'); return null; }
    ctx = new AC();
    master = ctx.createGain();
    master.gain.value = 0.5;    // headroom so layered notes stay gentle
    master.connect(ctx.destination);
    console.info(TAG + ' audiocontext:created state=' + ctx.state);
    return ctx;
  }

  function resume() {
    if (ctx && ctx.state === 'suspended' && ctx.resume) {
      ctx.resume().then(function () {
        console.info(TAG + ' audiocontext:resumed state=' + ctx.state);
      }, function () {});
    }
  }

  // One marimba-ish voice: a short pitched blip with a soft attack + decay.
  // type/gain/dur shape the timbre; 'delay' schedules chord notes in sequence.
  function voice(freq, opts) {
    opts = opts || {};
    var c = ensureCtx();
    if (!c) return;
    var t0 = c.currentTime + (opts.delay || 0);
    var dur = opts.dur || 0.18;
    var peak = opts.gain != null ? opts.gain : 0.16;

    var osc = c.createOscillator();
    osc.type = opts.type || 'triangle';
    osc.frequency.setValueAtTime(freq, t0);
    if (opts.glide) {
      osc.frequency.exponentialRampToValueAtTime(freq * opts.glide, t0 + dur);
    }

    var g = c.createGain();
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(peak, t0 + 0.012);        // quick attack
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);        // marimba decay

    osc.connect(g);
    g.connect(master);
    osc.start(t0);
    osc.stop(t0 + dur + 0.02);
    return 1;
  }

  // Named chime recipes. Each returns the oscillator count it fired.
  function render(name) {
    switch (name) {
      case 'pop':
        // fundamental + a soft octave shimmer = a rounded marimba tap
        voice(523.25, { type: 'triangle', gain: 0.16, dur: 0.16 });      // C5
        voice(1046.5, { type: 'sine',     gain: 0.05, dur: 0.11 });      // C6
        return 2;
      case 'reveal':
        // rising E5 -> B5 -> E6, brighter, for a card/panel opening
        voice(659.25, { type: 'triangle', gain: 0.13, dur: 0.20 });
        voice(987.77, { type: 'triangle', gain: 0.12, dur: 0.24, delay: 0.06 });
        voice(1318.5, { type: 'sine',     gain: 0.07, dur: 0.26, delay: 0.12 });
        return 3;
      case 'tick':
        // a whisper-quiet high blip for hover
        voice(1244.5, { type: 'sine', gain: 0.028, dur: 0.05 });
        return 1;
      case 'toggle':
        // played when sound is switched on, so the user hears it works
        voice(587.33, { type: 'triangle', gain: 0.14, dur: 0.16 });
        voice(880.0,  { type: 'sine',     gain: 0.10, dur: 0.18, delay: 0.05 });
        return 2;
      default:
        voice(523.25, { type: 'triangle', gain: 0.14, dur: 0.16 });
        return 1;
    }
  }

  // Gatekeeper: honors enabled state, reduced-motion, and rate limits.
  // 'force' lets the toggle-on confirmation play the instant sound is enabled.
  function play(name, force) {
    if (!enabled && !force) return;
    var t = now();
    if (t - lastAny < GLOBAL_GAP) return;
    var cd = COOLDOWN[name] != null ? COOLDOWN[name] : 60;
    if (lastByName[name] && t - lastByName[name] < cd) return;

    ensureCtx();
    resume();
    var oscs = render(name);
    lastAny = t;
    lastByName[name] = t;
    console.info(TAG + ' play name=' + name + ' osc=' + oscs +
      ' ctx=' + (ctx ? ctx.state : 'none'));
  }

  /* ---- public API -------------------------------------------------------- */
  var BobaSound = {
    chime: function (name) { play(name || 'pop'); },
    pop: function () { play('pop'); },
    setEnabled: function (on) {
      on = !!on;
      var changed = on !== enabled;
      enabled = on;
      writePref(on);
      reflect();
      if (on && changed) {
        // First enable is a genuine user gesture — build + resume the ctx now,
        // then play a confirming chime so the choice is audible.
        ensureCtx();
        resume();
        play('toggle', true);
      }
      console.info(TAG + ' setEnabled=' + on);
    }
  };
  // 'enabled' as a live getter so the field always mirrors real state.
  Object.defineProperty(BobaSound, 'enabled', {
    enumerable: true,
    get: function () { return enabled; }
  });
  window.BobaSound = BobaSound;

  /* ---- the toggle button ------------------------------------------------- */
  var SVG =
    '<svg class="bn-sound-svg" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" ' +
      'stroke-linejoin="round" aria-hidden="true">' +
      '<path class="bn-sound-spk" d="M4 9.5v5h3.2L12 18V6L7.2 9.5H4z"/>' +
      '<path class="bn-sound-wave" d="M15.4 9.2a4 4 0 0 1 0 5.6"/>' +
      '<path class="bn-sound-wave" d="M17.8 7a7.2 7.2 0 0 1 0 10"/>' +
      '<path class="bn-sound-slash" d="M4.5 4.5l15 15"/>' +
    '</svg>';

  function reflect() {
    if (!toggleEl) return;
    toggleEl.setAttribute('aria-pressed', enabled ? 'true' : 'false');
    var label = enabled ? 'Sound on' : 'Sound off';
    toggleEl.setAttribute('aria-label', label);
    toggleEl.setAttribute('title', label);
  }

  function buildToggle() {
    if (document.querySelector('.bn-sound-toggle')) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'bn-sound-toggle';
    btn.innerHTML = SVG;
    btn.addEventListener('click', function () {
      BobaSound.setEnabled(!enabled);
    });

    var actions = document.querySelector('.bn-actions');
    if (actions) {
      var cta = actions.querySelector('.bn-cta');
      if (cta) actions.insertBefore(btn, cta);
      else actions.appendChild(btn);
    } else {
      btn.classList.add('bn-sound-toggle--float');
      document.body.appendChild(btn);
    }
    toggleEl = btn;
    reflect();
  }

  /* ---- wiring (only ever audible once enabled) --------------------------- */
  function wire() {
    // Primary CTA clicks -> pop. Delegated + capture so it survives re-renders.
    document.addEventListener('click', function (e) {
      if (!enabled) return;
      var t = e.target;
      if (!t || !t.closest) return;
      if (t.closest('.bn-sound-toggle')) return;            // handled directly
      if (t.closest('.bn-cta, .bn-bb--cta, [data-bn-sound="cta"]')) {
        play('pop');
      }
    }, true);

    // Nav mega-panel opening -> reveal chime. nav-midnight.js flips
    // aria-expanded on .bn-trigger; we chime only on the open transition.
    document.addEventListener('click', function (e) {
      if (!enabled) return;
      var trg = e.target && e.target.closest &&
        e.target.closest('.bn-trigger, [data-bn-open-search]');
      if (!trg) return;
      // read state after nav.js has toggled it
      requestAnimationFrame(function () {
        var open = trg.getAttribute('aria-expanded') === 'true' ||
          trg.hasAttribute('data-bn-open-search');
        if (open) play('reveal');
      });
    }, false);

    // Hover tick on nav triggers — whisper quiet, rate-limited hard by cooldown.
    if (!reduceMotion) {
      document.addEventListener('pointerenter', function (e) {
        if (!enabled) return;
        var t = e.target;
        if (t && t.closest && t.closest('.bn-trigger')) play('tick');
      }, true);
    }
    // Card / surprise reveals are voiced by their owners calling
    // BobaSound.pop() / .chime('reveal') — the API above serves them.
  }

  /* ---- boot -------------------------------------------------------------- */
  function init() {
    buildToggle();
    wire();
    console.info(TAG + ' init enabled=' + enabled);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
