#!/usr/bin/env python3
# Builds /directory/ — the live, market-aware shop directory.
# Baked for crawlers: all 172 city links with counts, grouped by county.
# Live for humans: 1,117 shops fetched from niteboba_finder at view time.
import json, html, os

CITIES = json.load(open(os.path.join(os.path.dirname(__file__), 'cities.json')))
e = html.escape
CA = sum(x[3] for x in CITIES if x[0] != 'Clark')
LV = sum(x[3] for x in CITIES if x[0] == 'Clark')
TOTAL = CA + LV
COUNTY_LABEL = {"Los Angeles": "Los Angeles County", "Orange": "Orange County", "San Diego": "San Diego County",
                "Riverside": "Riverside County", "San Bernardino": "San Bernardino County",
                "Ventura": "Ventura County", "Imperial": "Imperial County", "Clark": "Las Vegas Valley"}
ORDER = ["Los Angeles", "Orange", "San Diego", "Riverside", "San Bernardino", "Ventura", "Imperial", "Clark"]

def city_href(county, cs):
    return ("/boba/nv/%s/" if county == "Clark" else "/boba/ca/%s/") % cs

groups = ""
for county in ORDER:
    rows = [x for x in CITIES if x[0] == county]
    if not rows: continue
    total = sum(x[3] for x in rows)
    links = "".join('<a href="%s">%s<b>%d</b></a>' % (city_href(county, cs), e(c), n) for _, c, cs, n in rows)
    groups += ('<details class="cty"%s><summary><span>%s</span><i>%d shops · %d cities</i></summary>'
               '<div class="ctyl">%s</div></details>\n'
               % (' open' if county in ("Los Angeles", "Clark") else '', e(COUNTY_LABEL[county]), total, len(rows), links))

page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boba Shop Directory — Southern California &amp; Las Vegas | Boba Night</title>
<meta name="description" content="Every boba shop Boba Night tracks: __CA__ across Southern California and __LV__ in the Las Vegas Valley, with live hours, Google ratings, and pages for each shop.">
<link rel="canonical" href="https://www.bobanight.com/directory/">
<meta property="og:title" content="The Boba Night Directory">
<meta property="og:description" content="__TOTAL__ boba shops, hours checked, nothing paid to be here.">
<meta property="og:image" content="https://www.bobanight.com/og-card.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/components/footer.css">
<style>
:root{--bg:#0B0C0E;--cream:#f6ead8;--champ:#C5A46D;--gilt:#F4DDA2;--pink:#ff2f6d;--jade:#3fbf8f;--muted:#a8998a;--line:rgba(197,164,109,.3)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--cream);font:16px/1.65 "Inter",system-ui,sans-serif;overflow-x:clip}
.dw{max-width:1080px;margin:0 auto;padding:150px 22px 90px}
.kick{font:600 10.5px/1 "Inter";letter-spacing:.24em;text-transform:uppercase;color:var(--champ)}
h1{font:600 clamp(30px,4.6vw,48px)/1.1 "Fraunces",serif;margin:14px 0 12px;text-wrap:balance}
h1 i{color:var(--pink);font-style:italic}
.lede{color:var(--muted);max-width:60ch;font-size:16.5px}
.lede b{color:var(--cream);font-weight:600}
h2{font:600 clamp(21px,3vw,28px)/1.2 "Fraunces",serif;margin:8px 0 14px}
.sx{margin:58px 0 0}
/* live stat strip */
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:30px 0 0}
.stat{border:1px solid var(--line);border-radius:14px;padding:16px 18px;background:linear-gradient(180deg,#15120c,#101012)}
.stat .n{font:300 32px/1 "Fraunces",serif;color:var(--gilt)}
.stat .n .ld{display:inline-block;width:26px;height:8px;border-radius:99px;background:rgba(197,164,109,.25);animation:ldp 1.2s ease-in-out infinite}
@keyframes ldp{50%{opacity:.4}}
.stat .l{font:600 11px "Inter";letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:6px}
.stat.jade .n{color:var(--jade)}
/* market chips */
.mrow{display:flex;gap:8px;margin:26px 0 0;flex-wrap:wrap}
.mchip{border:1px solid var(--line);background:rgba(197,164,109,.06);color:var(--cream);border-radius:99px;
  padding:9px 16px;font:600 13px "Inter";cursor:pointer;transition:.15s}
.mchip b{color:var(--champ);font-weight:600;margin-left:6px}
.mchip[aria-pressed="true"]{background:linear-gradient(180deg,#fbf3e4,#ecd9b8);color:#0B0C0E;border-color:#a9854e}
.mchip[aria-pressed="true"] b{color:#5c4726}
/* browser controls */
.ctl{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:0 0 16px}
.dsr{flex:1 1 240px;min-width:200px;height:46px;border-radius:13px;border:1px solid var(--line);
  background:rgba(255,255,255,.04);color:var(--cream);font:500 14px "Inter";padding:0 16px;outline:none}
.dsr::placeholder{color:#77695c}
.dsr:focus{border-color:var(--gilt)}
.fch{border:1px solid var(--line);background:none;color:var(--muted);border-radius:99px;padding:8px 14px;
  font:600 12.5px "Inter";cursor:pointer;transition:.15s;white-space:nowrap}
.fch[aria-pressed="true"]{background:rgba(63,191,143,.12);border-color:rgba(63,191,143,.6);color:#7fe0b6}
.fch.k[aria-pressed="true"]{background:rgba(197,164,109,.16);border-color:var(--champ);color:var(--gilt)}
select.dso{height:38px;border-radius:10px;border:1px solid var(--line);background:#15120c;color:var(--cream);
  font:600 12.5px "Inter";padding:0 10px;outline:none}
/* cards */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.card{display:block;text-decoration:none;color:var(--cream);border:1px solid var(--line);border-radius:15px;
  padding:16px 18px;background:linear-gradient(180deg,#14110b,#0f0f11);transition:border-color .15s,transform .15s;position:relative}
.card:hover{border-color:var(--gilt);transform:translateY(-2px)}
.card .cn{font:600 17px "Fraunces",serif;margin:0 66px 3px 0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.card .cc{font-size:12.5px;color:var(--muted)}
.card .cr{margin-top:8px;font:600 12.5px "Inter";color:#c9a96a}
.card .cr small{color:var(--muted);font-weight:500}
.card .ob{position:absolute;top:16px;right:16px;font:700 10px "Inter";letter-spacing:.06em;border-radius:99px;padding:4px 9px}
.card .ob.on{color:#7fe0b6;background:rgba(63,191,143,.12);border:1px solid rgba(63,191,143,.45)}
.card .ob.off{color:#b8a58f;background:rgba(197,164,109,.08);border:1px solid rgba(197,164,109,.3)}
.more{display:block;margin:20px auto 0;border:1px solid var(--line);background:none;color:var(--gilt);
  border-radius:99px;padding:13px 26px;font:600 13.5px "Inter";cursor:pointer;transition:.15s}
.more:hover{border-color:var(--gilt);background:rgba(197,164,109,.08)}
.dcount{color:var(--muted);font-size:13px;margin:0 0 14px}
.dempty{color:var(--muted);border:1px dashed var(--line);border-radius:14px;padding:22px;font-size:14.5px}
/* surprise */
.spr{display:flex;gap:14px;align-items:center;flex-wrap:wrap;border:1px solid var(--line);border-radius:16px;
  padding:18px 20px;background:linear-gradient(180deg,#17130c,#101013)}
.spr .st{flex:1 1 260px}
.spr .st b{font:600 17px "Fraunces",serif}
.spr .st p{color:var(--muted);font-size:13.5px;margin-top:2px}
.sprb{border:0;border-radius:99px;padding:14px 26px;cursor:pointer;font:700 14px "Inter";color:#1c1207;
  background:linear-gradient(180deg,#e8c98e,#C5A46D 55%,#a9854e);box-shadow:0 10px 26px -8px rgba(197,164,109,.9),inset 0 1px 0 rgba(255,255,255,.5)}
.sprb:active{transform:translateY(1px)}
.sprr{width:100%;display:none;margin-top:6px;border-top:1px solid rgba(197,164,109,.2);padding-top:14px}
.sprr.on{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.sprr .rn{font:600 19px "Fraunces",serif}
.sprr .rm{color:var(--muted);font-size:13px}
.sprr a{margin-left:auto;text-decoration:none;font:700 13px "Inter";color:#fff;border-radius:99px;padding:10px 18px;
  background:linear-gradient(180deg,#ff5d8b,#ff2f6d)}
/* cities (baked) */
.cty{border:1px solid var(--line);border-radius:14px;margin:0 0 10px;background:rgba(197,164,109,.04);overflow:hidden}
.cty summary{display:flex;align-items:baseline;gap:12px;cursor:pointer;list-style:none;padding:15px 18px;font:600 16px "Fraunces",serif}
.cty summary::-webkit-details-marker{display:none}
.cty summary::after{content:"▾";margin-left:auto;color:var(--champ);transition:transform .2s}
.cty[open] summary::after{transform:rotate(180deg)}
.cty summary i{font:500 12px "Inter";color:var(--muted);font-style:normal}
.ctyl{display:flex;flex-wrap:wrap;gap:8px;padding:2px 18px 16px}
.ctyl a{display:inline-flex;gap:7px;align-items:baseline;text-decoration:none;color:var(--cream);font:500 13px "Inter";
  border:1px solid rgba(197,164,109,.25);border-radius:99px;padding:7px 13px;transition:.15s}
.ctyl a b{color:var(--champ);font-weight:600;font-size:11px}
.ctyl a:hover{border-color:var(--gilt);color:var(--gilt)}
@media(max-width:820px){.dw{padding-top:118px}.grid{grid-template-columns:1fr}.stats{grid-template-columns:1fr 1fr 1fr;gap:8px}.stat{padding:12px}.stat .n{font-size:24px}}
</style>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CollectionPage","name":"Boba Night Directory","url":"https://www.bobanight.com/directory/","description":"__TOTAL__ boba shops across Southern California and the Las Vegas Valley with checked hours and Google ratings.","breadcrumb":{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.bobanight.com/"},{"@type":"ListItem","position":2,"name":"Directory","item":"https://www.bobanight.com/directory/"}]}}
</script>
</head>
<body>
<div id="bn-nav"></div>
<main class="dw">
  <section>
    <p class="kick">The directory</p>
    <h1>Every shop, every city, <i>one room</i>.</h1>
    <p class="lede"><b>__CA__ boba shops</b> across Southern California and <b>__LV__</b> in the Las Vegas Valley — live hours, Google ratings as reported, and a page for every shop. Nothing here paid to be listed.</p>
    <div class="stats" aria-label="Live counts">
      <div class="stat jade"><div class="n" id="stOpen"><span class="ld"></span></div><div class="l">Open right now</div></div>
      <div class="stat"><div class="n" id="stLate"><span class="ld"></span></div><div class="l">Pouring past 11 PM</div></div>
      <div class="stat"><div class="n" id="stTop"><span class="ld"></span></div><div class="l">Rated 4.5★ or higher</div></div>
    </div>
    <div class="mrow" id="mktRow" role="group" aria-label="Market">
      <button class="mchip" data-m="sc" aria-pressed="true">Southern California<b>__CA__</b></button>
      <button class="mchip" data-m="lv" aria-pressed="false">Las Vegas<b>__LV__</b></button>
    </div>
  </section>

  <section class="sx" aria-label="Feeling lucky">
    <div class="spr">
      <div class="st"><b>Can&rsquo;t decide? Let the house pour.</b><p>One open shop from your market, dealt at random.</p></div>
      <button class="sprb" id="sprGo" type="button">Deal me a shop</button>
      <div class="sprr" id="sprR"></div>
    </div>
  </section>

  <section class="sx" aria-label="Browse the shops">
    <h2>Pour through the list.</h2>
    <div class="ctl">
      <input class="dsr" id="dQ" type="text" placeholder="Search by shop name&hellip;" aria-label="Search shops by name">
      <button class="fch" id="fOpen" aria-pressed="false" type="button">● Open now</button>
      <button class="fch k" id="fOrig" aria-pressed="false" type="button">Independents only</button>
      <select class="dso" id="dSort" aria-label="Sort order">
        <option value="rv">Most reviewed</option>
        <option value="rt">Top rated</option>
        <option value="az">A to Z</option>
      </select>
    </div>
    <p class="dcount" id="dCount">Loading the room&hellip;</p>
    <div class="grid" id="dGrid"></div>
    <button class="more" id="dMore" type="button" hidden>Pour 24 more</button>
  </section>

  <section class="sx" aria-label="Cities">
    <p class="kick">By city</p>
    <h2>Boba by city, __NCITIES__ cities strong.</h2>
__GROUPS__
  </section>
</main>
<div id="bn-footer"></div>
<script src="/components/nav.js" defer></script>
<script src="/components/footer.js" defer></script>
<script>
(function(){
'use strict';
var ROWS=[],VIEW=[],page=0,PER=24;
var F={m:'sc',open:false,orig:false,q:'',sort:'rv'};
try{if(localStorage.getItem('bn_market')==='lv')F.m='lv';}catch(e){}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c];});}
function laNow(){try{var f=new Intl.DateTimeFormat("en-US",{timeZone:"America/Los_Angeles",weekday:"short",hour:"2-digit",minute:"2-digit",hour12:false});
  var p={};f.formatToParts(new Date()).forEach(function(x){p[x.type]=x.value;});
  return {day:{Sun:0,Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6}[p.weekday],mins:(+p.hour%24)*60+(+p.minute)};}
  catch(e){var d=new Date();return {day:d.getDay(),mins:d.getHours()*60+d.getMinutes()};}}
var NOW=laNow();
function mins(t){var a=t.split(":");return (+a[0])*60+(+a[1]);}
function openNow(h){if(!h)return null;var cur=NOW.mins,i;
  var per=h[String(NOW.day)],y=h[String((NOW.day+6)%7)];
  if(per)for(i=0;i<per.length;i++){var sp=per[i];if(sp&&sp.length>1){var s=mins(sp[0]),en=mins(sp[1]);if(en<=s)en+=1440;if(cur>=s&&cur<en)return true;}}
  if(y)for(i=0;i<y.length;i++){var sp2=y[i];if(sp2&&sp2.length>1){var s2=mins(sp2[0]),e2=mins(sp2[1]);if(e2<=s2&&cur<e2)return true;}}
  return false;}
function lateNight(h){if(!h)return false;
  for(var d in h){var per=h[d];for(var i=0;i<per.length;i++){var sp=per[i];if(sp&&sp.length>1){var e2=mins(sp[1]),s2=mins(sp[0]);if(e2<=s2||e2>=23*60)return true;}}}
  return false;}
function href(x){return (x.county==='Clark'?'/boba/nv/':'/boba/ca/')+x.cs+'/'+x.s+'/';}
function inMarket(x){return F.m==='lv'?x.county==='Clark':x.county!=='Clark';}
function apply(){
  var q=F.q.toLowerCase();
  VIEW=ROWS.filter(function(x){
    if(!inMarket(x))return false;
    if(F.open&&x.o!==true)return false;
    if(F.orig&&x.store_type==='chain')return false;
    if(q&&String(x.n).toLowerCase().indexOf(q)<0)return false;
    return true;});
  if(F.sort==='rv')VIEW.sort(function(a,b){return (b.reviews||0)-(a.reviews||0);});
  else if(F.sort==='rt')VIEW.sort(function(a,b){return (b.rating||0)-(a.rating||0)||(b.reviews||0)-(a.reviews||0);});
  else VIEW.sort(function(a,b){return String(a.n).localeCompare(String(b.n));});
  page=0;render(true);}
function render(reset){
  var g=document.getElementById('dGrid');
  if(reset)g.innerHTML='';
  var slice=VIEW.slice(page*PER,(page+1)*PER);
  g.insertAdjacentHTML('beforeend',slice.map(function(x){
    return '<a class="card" href="'+href(x)+'">'
      +'<span class="ob '+(x.o===true?'on':'off')+'">'+(x.o===true?'OPEN':'CLOSED')+'</span>'
      +'<span class="cn">'+esc(x.n)+'</span>'
      +'<span class="cc">'+esc(x.c)+' · '+esc(x.county==='Clark'?'Las Vegas Valley':x.county+' County')+'</span>'
      +(x.rating?'<div class="cr">★ '+x.rating+' <small>· '+(x.reviews||0)+' on Google</small></div>':'<div class="cr"><small>No Google rating yet</small></div>')
      +'</a>';}).join(''));
  page++;
  var shown=Math.min(page*PER,VIEW.length);
  document.getElementById('dCount').textContent=VIEW.length?('Showing '+shown+' of '+VIEW.length+' shops'):'0 shops match — loosen a filter below';
  if(!VIEW.length)g.innerHTML='<div class="dempty">Nothing matches those filters. Loosen one and the room refills.</div>';
  document.getElementById('dMore').hidden=shown>=VIEW.length;}
function stats(){
  var mk=ROWS.filter(inMarket);
  var o=mk.filter(function(x){return x.o===true;}).length;
  var l=mk.filter(function(x){return lateNight(x.hours);}).length;
  var t=mk.filter(function(x){return (x.rating||0)>=4.5;}).length;
  document.getElementById('stOpen').textContent=o;
  document.getElementById('stLate').textContent=l;
  document.getElementById('stTop').textContent=t;}
function mktUI(){document.querySelectorAll('#mktRow .mchip').forEach(function(b){
  b.setAttribute('aria-pressed',String(b.getAttribute('data-m')===F.m));});}
document.getElementById('mktRow').addEventListener('click',function(ev){
  var b=ev.target.closest('.mchip');if(!b)return;
  F.m=b.getAttribute('data-m');mktUI();stats();apply();});
document.getElementById('dQ').addEventListener('input',function(){F.q=this.value.trim();apply();});
document.getElementById('fOpen').addEventListener('click',function(){F.open=!F.open;this.setAttribute('aria-pressed',String(F.open));apply();});
document.getElementById('fOrig').addEventListener('click',function(){F.orig=!F.orig;this.setAttribute('aria-pressed',String(F.orig));apply();});
document.getElementById('dSort').addEventListener('change',function(){F.sort=this.value;apply();});
document.getElementById('dMore').addEventListener('click',function(){render(false);});
document.getElementById('sprGo').addEventListener('click',function(){
  var open=ROWS.filter(function(x){return inMarket(x)&&x.o===true;});
  var pool=open.length?open:ROWS.filter(inMarket);
  if(!pool.length)return;
  var x=pool[Math.floor(Math.random()*pool.length)];
  var r=document.getElementById('sprR');
  r.className='sprr on';
  r.innerHTML='<span class="rn">'+esc(x.n)+'</span><span class="rm">'+esc(x.c)
    +(x.rating?(' · ★ '+x.rating):'')+(x.o===true?' · open now':'')+'</span>'
    +'<a href="'+href(x)+'">View shop</a>';});
fetch('https://hfvbeqlefwwjlrbyxpbj.supabase.co/rest/v1/niteboba_finder?select=s,cs,n,c,county,rating,reviews,store_type,hours',
  {headers:{apikey:'sb_publishable_wlfujszvn2logC3KNL3MsA_AW1F42kf'}})
  .then(function(r){return r.ok?r.json():[];})
  .then(function(rows){
    ROWS=rows.map(function(x){x.o=openNow(x.hours);return x;});
    mktUI();stats();apply();})
  .catch(function(){document.getElementById('dCount').textContent='The live list could not load. The cities below always work.';});
})();
</script>
</body>
</html>
'''
page = (page.replace('__CA__', str(CA)).replace('__LV__', str(LV)).replace('__TOTAL__', str(TOTAL))
        .replace('__NCITIES__', str(len(CITIES))).replace('__GROUPS__', groups))
out = os.path.join(os.path.dirname(__file__), '..', 'prod', 'directory')
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'index.html'), 'w').write(page)
print('directory built:', len(page), 'bytes ·', CA, 'CA +', LV, 'LV ·', len(CITIES), 'cities baked')
