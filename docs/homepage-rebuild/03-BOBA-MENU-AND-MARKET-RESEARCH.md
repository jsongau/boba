# 03 — Boba Menu and Market Research

_Researched 2026-07-01 from official chain sites and first-party ordering pages. Facts only (drink names, categories, and caffeine/dairy where a source states them). Flavor summaries are original, written from listed ingredients. No marketing copy copied, no photography rehosted, no prices invented. Full provenance in `data/research/source-ledger.csv`; machine-readable menus in `data/menus/chains/*.json`._

## Scope of this pass
This is a **starter dataset of four chains** chosen because (a) they have findable official menus and (b) they are already represented in the CapyBoba directory, so every drink maps to a real location we list. It is not the full 25-chain sweep the brief asks for; the remaining chains are the next data pass. What exists now is enough to power a real Craving Cup and Spin the Straw.

| Chain | Directory locations | Primary source | Confidence |
|---|---:|---|---|
| 7 Leaves Cafe | 8 | 7leavescafe.com/menu | high |
| Sharetea | 5 | 1992sharetea.com + DoorDash first-party | high |
| Kung Fu Tea | 3 | kungfutea.com/faq + DoorDash first-party | high |
| Tastea | 4 | gotastea.com/menu | medium |

Total: **42 drinks across 20 real locations.**

## What was collected per drink
Name, category, an original one-line flavor summary, taste coordinates (creamy↔refreshing, mellow↔tea-forward, familiar↔adventurous) for the Craving Cup, `caffeine_status`, `dairy_status`, and `seasonal`. `price_min`/`price_max` are **null** — no official price list was verified, and the brief forbids invented prices. `caffeine`/`dairy` are only set to `yes`/`no` where a source states it; otherwise `unknown`.

## Chain notes (facts)
- **7 Leaves Cafe** — categories: milk teas (Jasmine, Oolong, Assam, Taro, Mung Bean, Thai), Herbal Tea (officially caffeine-free), Strawberry fruit tea (officially caffeine-free), Matcha, House Coffee (Ca Phe Sua Da). Sea cream, boba, grass jelly, custard pudding toppings. Milk teas contain dairy; several drinks list allergens on the official nutrition pages.
- **Sharetea** — categories: Milk Tea, Fruit Tea, Brewed Tea, Fresh Milk (with oat/almond/coconut alternatives), Creama (salted cheese-foam), Ice Blended, Tea Mojito. Wintermelon and Wintermelon Lemonade are officially caffeine-free. Sweetness 0/30/50/80/100.
- **Kung Fu Tea** — categories (from the official FAQ): Classic, Milk Tea, Milk Strike, Milk Cap, Punch (fruit-forward), Wow Milk, Espresso, Yogurt, Slush. The four core teas (Black, Green, Oolong, Thai) contain caffeine; Winter Melon items and Wow Milk (fresh milk, no tea) are caffeine-free per source. Standard creamer contains a milk protein (not dairy-free); plant milk at participating stores. Sweetness 0/30/50/75/100.
- **Tastea** — SoCal-native (started in San Diego). Categories: milk teas, fruit teas, smoothies, slushes, coffee, plus food. Signatures include Tiger Milk Tea, Rose Matcha Milk Tea, Matcha Coffee, Avocado Avalanche. Menu rotates seasonally (e.g., watermelon + white peach in summer), so confidence is medium and items are flagged with availability notes.

## Rules honored
Official-first sourcing; robots/terms respected; no Google/Yelp scraping; no customer reviews copied; no long brand descriptions reproduced; every fact carries a `source_url` and `checked_at`; blocked or uncertain items left `unknown` rather than guessed.

## What this unblocks
A recommendation is now always **a real drink that is on a real chain's official menu, shown at a real location already in the directory** — which is exactly what the Craving Cup and Spin the Straw need to exist honestly.

## Next data passes
Add the remaining priority chains (Sunright, OMOMO, Gong cha, Tiger Sugar, Happy Lemon, CHICHA San Chen, The Alley, Xing Fu Tang, Feng Cha, Ding Tea, and the rest); note that several are **not yet in the directory**, so they need directory rows before their drinks can map to a location. Per-location menu variance stays flagged; caffeine/dairy stay `unknown` unless a source states them.
