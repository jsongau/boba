/* First Meet — for two people who matched and need a first hang.
   Energy picker points at the right intent page; the Pearl Deck deals
   conversation cards. All editorial content, no shop facts asserted. */
(function () {
  var RECS = {
    calm: {
      line: "Quiet rooms with real seats — order at the counter, sit, actually talk.",
      href: "/best/first-date/", cta: "See first-meet rooms"
    },
    playful: {
      line: "Rooms with food and a little noise — popcorn chicken gives your hands something to do.",
      href: "/best/with-food/", cta: "See boba-and-food rooms"
    },
    late: {
      line: "The evening ran long. These rooms are known for staying open past nine.",
      href: "/best/open-late/", cta: "See late rooms"
    }
  };

  var DECK = [
    "What's your default order — and when did it last change?",
    "Sweetness percentage: what do you actually ask for, and is it the truth?",
    "Pearls, grass jelly, pudding, or nothing. Defend your answer.",
    "What's the farthest you've ever gone for one specific drink?",
    "Who introduced you to boba? Do they know what they started?",
    "The drink you ordered once and will never order again?",
    "Do you judge people who order the same thing every time? Be honest.",
    "What would your signature drink be called?",
    "Milk tea or fruit tea — and what does that split say about a person?",
    "First boba memory. Go.",
    "You can only keep one topping for the rest of your life. Which one?",
    "Hot tea in winter: sophisticated, or a betrayal of the ice?",
    "What's the correct move when the shop gets your order wrong?",
    "Straw-first or lid-off? There is a wrong answer.",
    "If your week was a drink order, what would today be?",
    "What drink do you order for someone else to convert them?",
    "Describe your taste in three toppings.",
    "The 626, Little Saigon, or Convoy — where does your loyalty live?",
    "What's a drink you pretend to like more than you do?",
    "Last photo in your camera roll that involves a drink. Explain.",
    "You open a shop tomorrow. What's it called and what's the one drink?",
    "Whose order do you secretly think is better than yours?",
    "What's your walk-out song when you grab the drink off the counter?",
    "Final card: same time next week, different shop. Yes or yes?"
  ];

  function wire() {
    var card = document.getElementById("fmCard"), q = document.getElementById("fmQ"),
        draw = document.getElementById("fmDraw"), count = document.getElementById("fmCount"),
        rec = document.getElementById("fmRec"), hint = document.getElementById("fmHint");
    if (!card || !q) return;

    // deck: shuffle once per load, deal without repeats until exhausted
    var order = DECK.map(function (_, i) { return i; });
    for (var i = order.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = order[i]; order[i] = order[j]; order[j] = t; }
    var pos = -1, dealt = 0;
    function deal() {
      pos = (pos + 1) % order.length; dealt++;
      q.textContent = DECK[order[pos]];
      if (count) count.textContent = "Card " + (((dealt - 1) % DECK.length) + 1) + " of " + DECK.length;
      if (hint && dealt === 1) hint.textContent = "Conversation, not interrogation · tap for another";
      card.classList.remove("is-dealt"); void card.offsetWidth; card.classList.add("is-dealt");
    }
    card.addEventListener("click", deal);
    card.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); deal(); } });
    if (draw) draw.addEventListener("click", deal);
    var send = document.getElementById("fmSend");
    if (send) send.addEventListener("click", function () {
      if (pos < 0) deal();
      var text = DECK[order[pos]] + "\n\n— from The Pearl Deck · niteboba.vercel.app";
      if (window.CBS && CBS.share) CBS.share("The Pearl Deck · NiteBoba", text);
      else if (navigator.clipboard) navigator.clipboard.writeText(text);
    });

    // energy picker
    var picks = [].slice.call(document.querySelectorAll(".fm-pick"));
    function select(key) {
      picks.forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-fm") === key)); });
      var r = RECS[key]; if (!r || !rec) return;
      rec.innerHTML = r.line + ' <a href="' + r.href + '">' + r.cta + " →</a>";
    }
    picks.forEach(function (b) { b.addEventListener("click", function () { select(b.getAttribute("data-fm")); }); });
    select("calm");
  }
  if (document.readyState !== "loading") wire(); else document.addEventListener("DOMContentLoaded", wire);
})();
