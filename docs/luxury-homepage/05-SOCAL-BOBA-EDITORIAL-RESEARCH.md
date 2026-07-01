# 05 - Southern California Boba Editorial and Menu Research

## Footprint (verified in the directory)
321 shops, 45 cities, 5 regions: The 626 119, Orange County 84, Greater LA 69, San Diego 28, Inland Empire 21. 138 chains, 183 independents. After-dark clusters: Rowland Heights, San Gabriel, Arcadia (626); Irvine, Westminster/Little Saigon, Fullerton (OC); Convoy Street (San Diego).

## Sourced menus (first-party, checked 2026-07-01)
Recorded in data/research/source-ledger.csv; drinks in data/homepage/society-drinks.json.

| Chain | Source | Notes |
|---|---|---|
| 7 Leaves Cafe | 7leavescafe.com/menu | Loose-leaf milk teas, herbal, sea-cream |
| Sharetea | 1992sharetea.com/drinks-menu-2024 | Pearl/Okinawa/Hokkaido, wintermelon, mojito |
| Kung Fu Tea | kungfutea.com | Milk caps, punch series, Wow milk |
| Tastea | gotastea.com/menu | Tiger milk tea, avocado, seasonal watermelon jasmine |
| Chatime | chatime.com/drinks/ | Official US menu (55 drinks); 12 signatures recorded; sugar 0/30/50/100 |
| CoCo Fresh Tea & Juice | cocobubbletea.com/menu | Non-dairy creamer on several; fresh-milk taro series |

Total available to the recommendation logic: **66 drinks across 6 chains.** Every recommended drink maps to a real shop in the directory (each chain has locations in the 321-shop set).

## Rules honored
Official sources first; no Google/Yelp scraping; no copied reviews or long marketing text; original tasting notes from listed ingredients; caffeine/dairy only when stated; no invented prices, hours, wait times, or best-seller labels; availability caveats kept visible.

## Honest status vs target
Target is 15 chains / 75 drinks / 40 mappable locations. This pass reached 6 chains / 66 drinks (all mappable). The gap is data-gathering, not homepage design. Next-pass chains (all already in the directory, so recommendations will map): Ten Ren's Tea Time, Tea Station, Quickly, Lollicup, BAMBU, Tapioca Express, Class 302, Cha For Tea, Zero Degrees, Snow Monster, It's Boba Time, Meet Fresh, Blackball. Adding ~9 clears both thresholds.

## Assets
data/research/asset-ledger.csv tracks every homepage image slot; all are original, owned, art-directed CSS/SVG placeholders (no licensed photography sourced here). See doc 09 to replace them.
