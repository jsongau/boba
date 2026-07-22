#!/usr/bin/env python3
# Builds /las-vegas/ market homepage + 3 NV city hubs from vegas-data.json.
# Output: prod/las-vegas/index.html, prod/boba/nv/<city>/index.html
import json, os, html

D = json.load(open('vegas-data.json'))
CITY_SLUG = {"Las Vegas": "las-vegas", "Henderson": "henderson", "North Las Vegas": "north-las-vegas"}
COUNTS = {c: len(v) for c, v in D.items()}
TOTAL = sum(COUNTS.values())
e = html.escape

def shop_path(city, slug):
    return "/boba/nv/%s/%s/" % (CITY_SLUG[city], slug)

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://www.bobanight.com{path}">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://www.bobanight.com/og-card.png">
<meta property="og:type" content="website">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/components/footer.css">
<style>
:root{{--bg:#0B0C0E;--cream:#f6ead8;--champ:#C5A46D;--gilt:#F4DDA2;--pink:#ff2f6d;--jade:#2e7d5b;--muted:#a8998a;--line:rgba(197,164,109,.3)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--cream);font:16px/1.65 "Inter",system-ui,sans-serif;overflow-x:clip}}
.lvw{{max-width:1080px;margin:0 auto;padding:150px 22px 90px}}
.kick{{font:600 10.5px/1 "Inter";letter-spacing:.24em;text-transform:uppercase;color:var(--champ)}}
h1{{font:600 clamp(30px,4.6vw,50px)/1.1 "Fraunces",serif;margin:14px 0 12px;text-wrap:balance}}
h1 i{{color:var(--pink);font-style:italic}}
.lede{{color:var(--muted);max-width:58ch;font-size:17px}}
.lede b{{color:var(--cream);font-weight:600}}
h2{{font:600 clamp(22px,3vw,30px)/1.2 "Fraunces",serif;margin:8px 0 6px}}
.sx{{margin:64px 0 0}}
.sx .sl{{color:var(--muted);max-width:62ch;margin-bottom:22px}}
.ctarow{{display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 0}}
.btn{{display:inline-flex;align-items:center;gap:9px;text-decoration:none;border-radius:14px;padding:14px 22px;font:600 14px "Inter";transition:.15s}}
.btn-p{{background:linear-gradient(180deg,#ff5d8b,var(--pink) 55%,#d61c53);color:#fff;box-shadow:0 12px 30px -10px rgba(255,47,109,.75),inset 0 1px 0 rgba(255,255,255,.35)}}
.btn-p:hover{{filter:brightness(1.07)}}
.btn-l{{border:1px solid var(--line);color:var(--gilt)}}
.btn-l:hover{{border-color:var(--gilt);background:rgba(197,164,109,.1)}}
.citygrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.citycard{{display:block;text-decoration:none;color:var(--cream);border:1px solid var(--line);border-radius:16px;padding:22px;background:linear-gradient(180deg,#15120c,#101012);transition:border-color .15s,transform .15s}}
.citycard:hover{{border-color:var(--gilt);transform:translateY(-2px)}}
.citycard .n{{font:300 34px "Fraunces",serif;color:var(--gilt)}}
.citycard .c{{font:600 16px "Fraunces",serif;margin:4px 0 2px}}
.citycard .s{{font-size:12.5px;color:var(--muted)}}
.openrail{{display:grid;gap:10px}}
.openrail .oc{{display:flex;align-items:center;gap:12px;border:1px solid var(--line);border-radius:14px;padding:13px 16px;text-decoration:none;color:var(--cream);background:rgba(197,164,109,.05);transition:border-color .15s}}
.openrail .oc:hover{{border-color:var(--gilt)}}
.openrail .od{{width:9px;height:9px;border-radius:50%;background:#3fbf8f;box-shadow:0 0 8px #3fbf8f;flex:0 0 auto}}
.openrail .on{{font-weight:600;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.openrail .oi{{margin-left:auto;flex:0 0 auto;color:var(--muted);font-size:12.5px;white-space:nowrap}}
.openrail .empty{{color:var(--muted);font-size:14.5px;border:1px dashed var(--line);border-radius:14px;padding:18px}}
.toplist{{display:grid;grid-template-columns:1fr 1fr;gap:8px 22px;counter-reset:tl}}
.toplist a{{display:flex;align-items:baseline;gap:10px;text-decoration:none;color:var(--cream);padding:9px 4px;border-bottom:1px solid rgba(197,164,109,.16);transition:color .15s}}
.toplist a:hover{{color:var(--gilt)}}
.toplist a::before{{counter-increment:tl;content:counter(tl,decimal-leading-zero);font:600 11px "Inter";color:var(--champ);letter-spacing:.08em}}
.toplist .tn{{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:500}}
.toplist .tr{{margin-left:auto;flex:0 0 auto;font-size:12.5px;color:#c9a96a;white-space:nowrap}}
.toplist .tr small{{color:var(--muted)}}
.biglist{{columns:2;column-gap:34px}}
.biglist a{{display:flex;align-items:baseline;gap:10px;text-decoration:none;color:var(--cream);padding:8px 2px;border-bottom:1px solid rgba(197,164,109,.14);break-inside:avoid}}
.biglist a:hover{{color:var(--gilt)}}
.biglist .tn{{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:500;font-size:14.5px}}
.biglist .tr{{margin-left:auto;flex:0 0 auto;font-size:12px;color:#c9a96a;white-space:nowrap}}
.biglist .tr small{{color:var(--muted)}}
.crumb{{font-size:12.5px;color:var(--muted);margin-bottom:8px}}
.crumb a{{color:var(--champ);text-decoration:none}}
.crumb a:hover{{color:var(--gilt)}}
.mkline{{margin-top:56px;border-top:1px solid var(--line);padding-top:22px;color:var(--muted);font-size:13.5px}}
.mkline a{{color:var(--gilt);text-decoration:none}}
@media(max-width:860px){{.lvw{{padding-top:118px}}.citygrid{{grid-template-columns:1fr}}.toplist{{grid-template-columns:1fr}}.biglist{{columns:1}}}}
</style>
{schema}
</head>
<body data-market="lv">
<div id="bn-nav"></div>
<main class="lvw">
'''

FOOT = '''</main>
<div id="bn-footer"></div>
<script src="/components/nav.js" defer></script>
<script src="/components/footer.js" defer></script>
{pagejs}
</body>
</html>
'''

# live open-now enhancement shared by all four pages
OPENJS = '''<script>
(function(){
'use strict';
var HOST=document.getElementById('lvOpen');if(!HOST)return;
var CITY=HOST.getAttribute('data-city')||'';
function laNow(){try{var f=new Intl.DateTimeFormat("en-US",{timeZone:"America/Los_Angeles",weekday:"short",hour:"2-digit",minute:"2-digit",hour12:false});
  var p={};f.formatToParts(new Date()).forEach(function(x){p[x.type]=x.value;});
  return {day:{Sun:0,Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6}[p.weekday],mins:(+p.hour%24)*60+(+p.minute)};}
  catch(e){var d=new Date();return {day:d.getDay(),mins:d.getHours()*60+d.getMinutes()};}}
function openNow(h,t){if(!h)return null;var per=h[String(t.day)];var y=h[String((t.day+6)%7)];var cur=t.mins;
  function inSpan(sp,off){if(!sp||sp.length<2)return false;var a=sp[0].split(":"),b=sp[1].split(":");
    var s=(+a[0])*60+(+a[1])+off,en=(+b[0])*60+(+b[1])+off;if(en<=s)en+=1440;var c=cur+ (off===-1440?0:0);
    return cur>=s&&cur<en;}
  var i;if(per)for(i=0;i<per.length;i++){if(inSpan(per[i],0))return true;}
  if(y)for(i=0;i<y.length;i++){var sp=y[i];if(sp&&sp.length>1){var a=sp[0].split(":"),b=sp[1].split(":");
    var s=(+a[0])*60+(+a[1]),en=(+b[0])*60+(+b[1]);if(en<=s&&cur<en)return true;}}
  return false;}
fetch("https://hfvbeqlefwwjlrbyxpbj.supabase.co/rest/v1/niteboba_finder?select=s,cs,n,c,county,rating,reviews,hours&county=eq.Clark",
  {headers:{apikey:"sb_publishable_wlfujszvn2logC3KNL3MsA_AW1F42kf"}})
  .then(function(r){return r.ok?r.json():[];})
  .then(function(rows){
    var t=laNow();
    var open=rows.filter(function(x){return (!CITY||x.c===CITY)&&openNow(x.hours,t)===true;})
      .sort(function(a,b){return (b.reviews||0)-(a.reviews||0);}).slice(0,8);
    if(!open.length){HOST.innerHTML='<div class="empty">Nothing is pouring at this exact minute. The list below is sorted by what the city loves; doors reopen in the morning.</div>';return;}
    HOST.innerHTML=open.map(function(x){
      return '<a class="oc" href="/boba/nv/'+x.cs+'/'+x.s+'/"><span class="od"></span><span class="on">'+
        String(x.n).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c];})+
        '</span><span class="oi">'+(x.rating?('★ '+x.rating+' · '):'')+x.c+'</span></a>';}).join("");
    var ct=document.getElementById('lvOpenCt');
    if(ct)ct.textContent=String(rows.filter(function(x){return (!CITY||x.c===CITY)&&openNow(x.hours,t)===true;}).length);
  }).catch(function(){});
})();
</script>'''

def stars(r, rv):
    if not r: return '<span class="tr"><small>No Google rating yet</small></span>'
    return '<span class="tr">★ %s <small>· %s on Google</small></span>' % (r, rv)

def toplinks(rows, city, limit):
    out = []
    for slug, name, r, rv in rows[:limit]:
        out.append('<a href="%s"><span class="tn">%s</span>%s</a>' % (shop_path(city, slug), e(name), stars(r, rv)))
    return "\n".join(out)

def alllinks(rows, city):
    out = []
    for slug, name, r, rv in rows:
        out.append('<a href="%s"><span class="tn">%s</span>%s</a>' % (shop_path(city, slug), e(name), stars(r, rv)))
    return "\n".join(out)

# ---------- /las-vegas/ market homepage ----------
strip = [(c, s, n, r, rv) for c, v in D.items() for s, n, r, rv in v
         if any(k in n.lower() for k in ("strip", "mandalay", "miracle mile", "grand bazaar", "unlv"))]
strip_html = "\n".join('<a href="%s"><span class="tn">%s</span>%s</a>' % (shop_path(c, s), e(n), stars(r, rv))
                       for c, s, n, r, rv in strip)
top_all = sorted([(c, s, n, r, rv) for c, v in D.items() for s, n, r, rv in v], key=lambda x: -x[4])[:14]
top_html = "\n".join('<a href="%s"><span class="tn">%s</span>%s</a>' % (shop_path(c, s), e(n), stars(r, rv))
                     for c, s, n, r, rv in top_all)

schema_home = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CollectionPage","name":"Boba in Las Vegas","url":"https://www.bobanight.com/las-vegas/","description":"%d boba shops across Las Vegas, Henderson, and North Las Vegas, hours checked and current.","isPartOf":{"@type":"WebSite","name":"Boba Night","url":"https://www.bobanight.com/"},"breadcrumb":{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.bobanight.com/"},{"@type":"ListItem","position":2,"name":"Las Vegas","item":"https://www.bobanight.com/las-vegas/"}]}}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"How many boba shops are in Las Vegas?","acceptedAnswer":{"@type":"Answer","text":"Boba Night tracks %d boba shops in the Las Vegas Valley: %d in Las Vegas, %d in Henderson, and %d in North Las Vegas, with hours checked against each shop's public listing."}},
{"@type":"Question","name":"Is there boba on the Las Vegas Strip?","acceptedAnswer":{"@type":"Answer","text":"Yes. Tracked shops on or beside the Strip include Happy Lemon at the Grand Bazaar Shops, Happy Lemon at the Showcase Food Court, Kung Fu Tea at Mandalay Bay, and TE'AMO Boba and Dessert in the Miracle Mile Shops."}},
{"@type":"Question","name":"What is the best-reviewed boba in Las Vegas?","acceptedAnswer":{"@type":"Answer","text":"By Google review count, the most-reviewed tracked shop is TK's Boba and Creamery with a 4.9 rating across more than 1,400 reviews, followed by BREW TEA BAR and CHICHA San Chen."}}]}
</script>''' % (TOTAL, TOTAL, COUNTS["Las Vegas"], COUNTS["Henderson"], COUNTS["North Las Vegas"])

home = HEAD.format(
    title="Boba in Las Vegas — %d Shops, Hours Checked | Boba Night" % TOTAL,
    desc="%d boba shops across Las Vegas, Henderson, and North Las Vegas. Real hours, Google ratings, on and off the Strip. Nothing paid to be here." % TOTAL,
    ogtitle="Boba Night · Las Vegas",
    path="/las-vegas/",
    schema=schema_home,
)
home += '''
  <section>
    <p class="kick">Las Vegas boba, checked and current</p>
    <h1>Find boba in Las Vegas <i>tonight</i>.</h1>
    <p class="lede"><b>%d boba shops</b> across Las Vegas, Henderson, and North Las Vegas — Google ratings shown, hours checked against each shop&rsquo;s public listing, nothing paid to be here.</p>
    <div class="ctarow">
      <a class="btn btn-p" href="/boba/nv/las-vegas/">Browse Las Vegas shops</a>
      <a class="btn btn-l" href="#openlv">See who&rsquo;s open right now</a>
    </div>
  </section>

  <section class="sx" id="openlv" aria-label="Open right now in Las Vegas">
    <p class="kick">Live from the valley</p>
    <h2>Boba open right now in Las Vegas.</h2>
    <p class="sl">Checked at this minute, busiest houses first. <span id="lvOpenWrap"><b id="lvOpenCt"></b></span></p>
    <div class="openrail" id="lvOpen" data-city=""></div>
  </section>

  <section class="sx" aria-label="Las Vegas boba by city">
    <p class="kick">The valley, by city</p>
    <h2>Las Vegas boba by city.</h2>
    <p class="sl">Every shop links to its own page: address, tonight&rsquo;s hours, and directions.</p>
    <div class="citygrid">
      <a class="citycard" href="/boba/nv/las-vegas/"><span class="n">%d</span><span class="c">Las Vegas</span><br><span class="s">Chinatown, Summerlin, the Strip, and everywhere between</span></a>
      <a class="citycard" href="/boba/nv/henderson/"><span class="n">%d</span><span class="c">Henderson</span><br><span class="s">Green Valley, Water Street, and the district</span></a>
      <a class="citycard" href="/boba/nv/north-las-vegas/"><span class="n">%d</span><span class="c">North Las Vegas</span><br><span class="s">Aliante, Craig Road, and the north valley</span></a>
    </div>
  </section>

  <section class="sx" aria-label="Boba on the Las Vegas Strip">
    <p class="kick">On the boulevard</p>
    <h2>Boba on the Las Vegas Strip.</h2>
    <p class="sl">Inside the casinos and food halls — cups you can get without leaving the boulevard.</p>
    <div class="toplist">
%s
    </div>
  </section>

  <section class="sx" aria-label="Best reviewed boba in Las Vegas">
    <p class="kick">The valley&rsquo;s favorites</p>
    <h2>The best-reviewed boba in Las Vegas.</h2>
    <p class="sl">Ranked by Google review count across the whole valley — ratings shown as reported, nothing reordered for money.</p>
    <div class="toplist">
%s
    </div>
  </section>

  <p class="mkline">Boba Night also covers Southern California — <a href="/">998 shops across 169 cities</a>. Tap the SC&thinsp;/&thinsp;LV switch in the top corner any time to change market.</p>
''' % (TOTAL, COUNTS["Las Vegas"], COUNTS["Henderson"], COUNTS["North Las Vegas"], strip_html, top_html)
home += FOOT.format(pagejs=OPENJS)

os.makedirs("prod/las-vegas", exist_ok=True)
open("prod/las-vegas/index.html", "w").write(home)

# ---------- city hubs ----------
BLURB = {
    "Las Vegas": "from Chinatown's tea rooms to the Strip's food halls",
    "Henderson": "Green Valley plazas to Water Street",
    "North Las Vegas": "Aliante to Craig Road",
}
for city, rows in D.items():
    cs = CITY_SLUG[city]
    others = [c for c in D if c != city]
    schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CollectionPage","name":"Boba shops in %s, Nevada","url":"https://www.bobanight.com/boba/nv/%s/","breadcrumb":{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.bobanight.com/"},{"@type":"ListItem","position":2,"name":"Las Vegas","item":"https://www.bobanight.com/las-vegas/"},{"@type":"ListItem","position":3,"name":"%s","item":"https://www.bobanight.com/boba/nv/%s/"}]}}
</script>''' % (city, cs, city, cs)
    pg = HEAD.format(
        title="Boba in %s, NV — %d Shops With Hours & Ratings | Boba Night" % (city, len(rows)),
        desc="All %d tracked boba shops in %s, Nevada with Google ratings and checked hours. Every shop links to its full page with directions." % (len(rows), city),
        ogtitle="Boba Night · %s" % city,
        path="/boba/nv/%s/" % cs,
        schema=schema,
    )
    pg += '''
  <section>
    <p class="crumb"><a href="/">Home</a> / <a href="/las-vegas/">Las Vegas</a> / %s</p>
    <p class="kick">%s, Nevada</p>
    <h1>Boba shops in %s.</h1>
    <p class="lede"><b>%d shops</b> tracked in %s — %s. Google ratings shown as reported; tap any shop for its address, tonight&rsquo;s hours, and directions.</p>
  </section>

  <section class="sx" aria-label="Open right now">
    <p class="kick">Live</p>
    <h2>Open right now in %s.</h2>
    <div class="openrail" id="lvOpen" data-city="%s"></div>
  </section>

  <section class="sx" aria-label="All shops">
    <p class="kick">The full list</p>
    <h2>Every boba shop in %s, most reviewed first.</h2>
    <div class="biglist">
%s
    </div>
  </section>

  <p class="mkline">More of the valley: %s · or <a href="/las-vegas/">all of Las Vegas</a> · Boba Night also covers <a href="/">Southern California</a>.</p>
''' % (
        e(city), e(city), e(city), len(rows), e(city), BLURB[city],
        e(city), e(city),
        e(city), alllinks(rows, city),
        " · ".join('<a href="/boba/nv/%s/">%s</a>' % (CITY_SLUG[o], e(o)) for o in others),
    )
    pg += FOOT.format(pagejs=OPENJS)
    os.makedirs("prod/boba/nv/%s" % cs, exist_ok=True)
    open("prod/boba/nv/%s/index.html" % cs, "w").write(pg)

print("built: las-vegas home + %d city hubs · total shops %d" % (len(D), TOTAL))
