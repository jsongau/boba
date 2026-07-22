var DATA=(window.FINDER_DATA||{shops:[],locations:[]});
(function(){
"use strict";
var SHOPS=DATA.shops, LOCS=DATA.locations;
var state={origin:null,label:"",radius:8,sort:"closest",list:[],idx:0,sound:true,cityLock:null,scope:"all",scopeCounts:null};
var $=function(id){return document.getElementById(id);};
var fuse=$("fuse"),q=$("q"),sug=$("sug"),dock=$("dock"),head=$("dockHead"),body=$("dockBody"),foot=$("dockFoot");

function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c];});}
function miles(a,b,c,d){var R=3958.7613,t=Math.PI/180,x=(c-a)*t,y=(d-b)*t,
  h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*t)*Math.cos(c*t)*Math.sin(y/2)*Math.sin(y/2);
  return R*2*Math.atan2(Math.sqrt(h),Math.sqrt(1-h));}
function laNow(){try{var f=new Intl.DateTimeFormat("en-US",{timeZone:"America/Los_Angeles",weekday:"short",hour:"2-digit",minute:"2-digit",hour12:false});
  var p={};f.formatToParts(new Date()).forEach(function(x){p[x.type]=x.value;});
  return {day:{Sun:0,Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6}[p.weekday],mins:(+p.hour%24)*60+(+p.minute)};}
  catch(e){var d=new Date();return {day:d.getDay(),mins:d.getHours()*60+d.getMinutes()};}}
function openNow(s,t){var per=s.per;if(!per||!per.length)return null;var wk=10080,cur=t.day*1440+t.mins;
  for(var i=0;i<per.length;i++){var od=per[i][0],ot=per[i][1],cd=per[i][2],ct=per[i][3];if(ot==null||ct==null)continue;
    var st=od*1440+(+ot.slice(0,2))*60+(+ot.slice(2)),en=(cd==null?od:cd)*1440+(+ct.slice(0,2))*60+(+ct.slice(2));
    if(en<=st)en+=wk;var sh=[0,wk,-wk];for(var j=0;j<3;j++){if(cur>=st+sh[j]&&cur<en+sh[j])return true;}}
  return false;}
function fmt12(hm){var h=+hm.slice(0,2),m=hm.slice(2);var ap=h>=12&&h<24?"PM":"AM";h=h%12;if(h===0)h=12;
  return h+(m==="00"?"":":"+m)+" "+ap;}
function todayLine(s,t){var wt=s.wt||[];
  if(wt.length)return (wt[(t.day+6)%7]||"").replace(/^[A-Za-z]+:\s*/,"");
  var per=s.per;if(!per||!per.length)return null;
  var out=[];
  for(var i=0;i<per.length;i++){var p=per[i];
    if(p[0]===t.day&&p[1]!=null&&p[3]!=null)out.push(fmt12(p[1])+" to "+fmt12(p[3]));}
  return out.length?out.join(", "):"Closed today";}
/* live Google ratings + review counts from Supabase (source of truth), cached this visit */
(function(){
  var K="bn_rat_v1";
  function apply(m){for(var i=0;i<SHOPS.length;i++){var r=m[SHOPS[i].sl];if(r){SHOPS[i].r=r[0];SHOPS[i].rv=r[1];}}
    if(state.origin&&state.list.length)reveal(false);}
  try{var c=JSON.parse(sessionStorage.getItem(K)||"null");
    if(c&&c.m&&(Date.now()-c.t)<36e5){setTimeout(function(){apply(c.m);},0);return;}}catch(e){}
  fetch("https://hfvbeqlefwwjlrbyxpbj.supabase.co/rest/v1/niteboba_finder?select=s,rating,reviews",
    {headers:{apikey:"sb_publishable_wlfujszvn2logC3KNL3MsA_AW1F42kf"}})
    .then(function(r){return r.ok?r.json():[];})
    .then(function(rows){var m={};rows.forEach(function(x){if(x.rating!=null)m[x.s]=[x.rating,x.reviews||0];});
      try{sessionStorage.setItem(K,JSON.stringify({t:Date.now(),m:m}));}catch(e){}
      apply(m);})
    .catch(function(){});
})();

/* sound — warm brass base, yin-yang alternation on the pour */
var AC=null;
function ctx(){if(!state.sound)return null;
  try{if(!AC)AC=new (window.AudioContext||window.webkitAudioContext)();
    if(AC.state==="suspended")AC.resume();return AC;}catch(e){return null;}}
function tone(freq,dur,type,vol,when,bend){var c=ctx();if(!c)return;
  var t=(when||0)+c.currentTime,o=c.createOscillator(),g=c.createGain();
  o.type=type||"sine";o.frequency.setValueAtTime(freq,t);
  if(bend)o.frequency.exponentialRampToValueAtTime(bend,t+dur);
  g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(vol||0.12,t+0.012);
  g.gain.exponentialRampToValueAtTime(0.0001,t+dur);
  o.connect(g);g.connect(c.destination);o.start(t);o.stop(t+dur+0.05);}
function noise(dur,f1,f2,vol){var c=ctx();if(!c)return;
  var t=c.currentTime,len=Math.floor(c.sampleRate*dur),buf=c.createBuffer(1,len,c.sampleRate),d=buf.getChannelData(0);
  for(var i=0;i<len;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/len,1.6);
  var src=c.createBufferSource();src.buffer=buf;
  var bp=c.createBiquadFilter();bp.type="bandpass";bp.Q.value=1.1;
  bp.frequency.setValueAtTime(f1,t);bp.frequency.exponentialRampToValueAtTime(f2,t+dur*0.8);
  var g=c.createGain();g.gain.setValueAtTime(0.0001,t);
  g.gain.exponentialRampToValueAtTime(vol||0.1,t+dur*0.15);g.gain.exponentialRampToValueAtTime(0.0001,t+dur);
  src.connect(bp);bp.connect(g);g.connect(c.destination);src.start(t);src.stop(t+dur);}
var SCALE=[329.63,392,440,523.25,587.33,659.25];
var SND={
  tick:function(v){tone(1500+v*40,0.03,"square",0.05);},
  go:function(){tone(300,0.16,"sine",0.12,0,80);noise(0.3,240,1200,0.08);},
  reveal:function(i){tone(392,0.5,"triangle",0.1);tone(587.33,0.6,"triangle",0.08,0.06);},
  next:function(i){noise(0.13,400,1600,0.055);
    var n=SCALE[Math.floor(i/2)%SCALE.length];
    if(i%2===0){tone(n,0.44,"triangle",0.11,0.05);}          /* yin: low, warm */
    else{tone(n*2,0.4,"sine",0.07,0.05);tone(n*3,0.22,"sine",0.03,0.1);} /* yang: bright twin */
  },
  empty:function(){tone(220,0.3,"sine",0.08,0,170);}
};

/* typeahead */
var matches=[],act=-1;
var PIN='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#a9854e" stroke-width="1.9"><path d="M12 21c-4-4.5-7-8-7-11a7 7 0 0 1 14 0c0 3-3 6.5-7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>';
function matchZip(z){var out=[];
  for(var i=0;i<LOCS.length;i++){var L=LOCS[i];if(!L.zips)continue;
    for(var j=0;j<L.zips.length;j++){if(L.zips[j].indexOf(z)===0){out.push({L:L,zip:L.zips[j],ex:L.zips[j]===z});break;}}}
  out.sort(function(a,b){if(a.ex!==b.ex)return a.ex?-1:1;return b.L.n-a.L.n;});
  return out.slice(0,6).map(function(o){return {loc:o.L,zip:o.zip};});}
function matchCity(s){return LOCS.filter(function(L){return L.city.toLowerCase().indexOf(s)>=0;})
  .sort(function(a,b){var x=a.city.toLowerCase().indexOf(s)===0,y=b.city.toLowerCase().indexOf(s)===0;
    if(x!==y)return x?-1:1;if((b.n>0)!==(a.n>0))return b.n>0?1:-1;return a.city.localeCompare(b.city);})
  .slice(0,6).map(function(L){return {loc:L,zip:null};});}
function paint(){
  if(!matches.length){sug.classList.remove("on");sug.innerHTML="";q.setAttribute("aria-expanded","false");return;}
  var isZip=/^\d/.test(q.value.trim());
  sug.innerHTML='<div class="cap">'+(isZip?"Matching ZIP codes":"Matching locations")+'</div>'+matches.map(function(m,i){
    var L=m.loc,name=m.zip||L.city,sub=m.zip?(L.city+" · "+L.area):(L.area);
    var cnt=L.n?('<span class="rc">'+L.n+' shop'+(L.n>1?'s':'')+'</span>'):'<span class="rc z">find nearest</span>';
    return '<button data-i="'+i+'" class="'+(i===act?'act':'')+'" role="option">'+PIN+'<span><span class="rn">'+esc(name)+'</span><span class="rs">'+esc(sub)+'</span></span>'+cnt+'</button>';}).join("");
  sug.classList.add("on");q.setAttribute("aria-expanded","true");}
function pick(m){if(!m)return;var L=m.loc;
  q.value=m.zip?(L.city+" "+m.zip):L.city;matches=[];paint();
  state.origin={lat:L.lat,lng:L.lng};state.label=m.zip?(L.city+" "+m.zip):L.city;
  state.cityLock=L.city;state.scope="city";
  if(window.__f3Lock)window.__f3Lock(L.city,m.zip||"");
  SND.go();search(true);}
function nearestCity(lat,lng){var best=null,bd=1e9;
  for(var i=0;i<LOCS.length;i++){var L=LOCS[i];if(L.lat==null||L.lng==null)continue;
    var d=miles(lat,lng,L.lat,L.lng);if(d<bd){bd=d;best=L;}}
  return (best&&bd<=25)?{city:best.city,area:best.area,dist:bd}:null;}
q.addEventListener("input",function(){var v=q.value.trim();act=-1;
  if(!v){matches=[];paint();return;}
  matches=/^\d/.test(v)?matchZip(v.replace(/\D/g,"")):matchCity(v.toLowerCase());
  if(!matches.length){sug.innerHTML='<div class="mb-none">No SoCal city or ZIP matches "'+esc(v)+'".</div>';sug.classList.add("on");}
  else paint();});
q.addEventListener("keydown",function(e){if(!matches.length)return;
  if(e.key==="ArrowDown"){act=Math.min(act+1,matches.length-1);paint();e.preventDefault();}
  else if(e.key==="ArrowUp"){act=Math.max(act-1,0);paint();e.preventDefault();}
  else if(e.key==="Enter"){pick(matches[Math.max(act,0)]);e.preventDefault();}
  else if(e.key==="Escape"){matches=[];paint();}});
sug.addEventListener("click",function(e){var b=e.target.closest("button");if(b)pick(matches[+b.dataset.i]);});
document.addEventListener("click",function(e){if(!e.target.closest(".mb-field")){matches=[];paint();}});
$("gps").addEventListener("click",function(e){e.stopPropagation();
  if(!navigator.geolocation)return;
  navigator.geolocation.getCurrentPosition(function(p){
    state.origin={lat:p.coords.latitude,lng:p.coords.longitude};
    var nc=nearestCity(p.coords.latitude,p.coords.longitude);
    state.label=nc?nc.city:"your location";q.value=nc?nc.city:"";
    state.cityLock=nc?nc.city:null;state.scope=nc?"city":"all";
    matches=[];paint();
    if(nc&&window.__f3Lock)window.__f3Lock(nc.city,"");
    SND.go();search(true);},function(){},{enableHighAccuracy:true,timeout:9000,maximumAge:60000});});

/* search + pour loop */
function build(){if(!state.origin)return [];
  var t=laNow();
  var l=SHOPS.filter(function(s){return s.st==="open"||s.st==="seed";})
    .map(function(s){return {s:s,d:miles(state.origin.lat,state.origin.lng,s.lat,s.lng),o:openNow(s,t),tl:todayLine(s,t)};})
    .filter(function(x){return x.d<=state.radius;});
  var lock=state.cityLock;
  state.scopeCounts={city:lock?l.filter(function(x){return x.s.c===lock;}).length:0,all:l.length};
  if(state.scope==="city"&&lock)l=l.filter(function(x){return x.s.c===lock;});
  if(state.sort==="open")l.sort(function(a,b){var ao=a.o===true?0:1,bo=b.o===true?0:1;if(ao!==bo)return ao-bo;return a.d-b.d;});
  else l.sort(function(a,b){return a.d-b.d;});
  return l;}
function search(fresh){
  state.list=build();state.idx=0;
  dock.classList.add("on");
  head.innerHTML='<span class="dh-t">Pouring near <b>'+esc(state.label)+'</b> · within '+state.radius+' mi</span>'
    +'<button class="dock-x" id="dockX" aria-label="Close">&times;</button>';
  $("dockX").onclick=function(){dock.classList.remove("on");};
  if(!state.list.length){
    body.innerHTML='<div class="dock-empty">Nothing inside that range. Give the dial a turn — the room refills as it widens.</div>';
    foot.innerHTML='<span class="counter">0 within '+state.radius+' mi</span>'
      +(state.radius<20?'<button class="widen" id="widen">Widen to '+Math.min(20,state.radius+5)+' mi</button>':'');
    var w=$("widen");if(w)w.onclick=function(){setRadius(Math.min(20,state.radius+5),true);};
    SND.empty();renderNear();return;}
  reveal(fresh);renderNear();}
function reveal(fresh){
  var x=state.list[state.idx],s=x.s;
  var badge=x.o===null?'<span class="tag">hours verifying</span>':(x.o?'<span class="tag open">● Open now</span>':'<span class="tag shut">Closed now</span>');
  var maps="https://www.google.com/maps/dir/?api=1&destination="+encodeURIComponent(s.n+" "+(s.ad||"")+" "+s.c+" CA");
  var up=state.list.slice(state.idx+1,state.idx+3).map(function(y){return '<span class="nm">'+esc(y.s.n)+'</span>';}).join('<span>·</span>');
  var typ=s.f?'★ Featured':(s.ty==="specialty"?"Original":"Chain");
  var other=state.cityLock&&s.c!==state.cityLock;
  var rate=s.r?'<div class="sd-rate">★ '+s.r+'</div><div class="sd-rv">'+(s.rv||0)+' on Google</div>':'';
  body.innerHTML='<div class="spot re-a">'
    +'<div class="spot-dist"><div class="mi">'+(x.d<0.1?"0.1":x.d.toFixed(1))+'</div><div class="u">MILES</div>'+rate+'</div>'
    +'<h3 class="spot-name">'+esc(s.n)+'</h3>'
    +'<div class="spot-meta"><span class="tag city'+(other?' oth':'')+'"><span class="tc">'+esc(s.c)+'</span><b class="ty'+(s.f?' fe':'')+'">'+typ+'</b></span>'+badge+'</div>'
    +'<p class="spot-hours">'+(x.tl?'<span>Today:</span> '+esc(x.tl):'<span class="sh-vg">Hours being verified</span>')+'</p>'
    +'<div class="spot-actions"><a class="sbtn go" target="_blank" rel="noopener" href="'+maps+'">Directions</a>'
    +'<a class="sbtn" target="_blank" rel="noopener" href="https://www.bobanight.com'+s.p+'">View shop</a></div>'
    +(up?'<div class="updeck">Up next: '+up+'</div>':'')+'</div>';
  foot.innerHTML='<span class="counter"><b>'+(state.idx+1)+'</b> of <b>'+state.list.length+'</b> '
    +(state.scope==="city"&&state.cityLock?('in '+esc(state.cityLock)):('within '+state.radius+' mi'))+' · '
    +(state.sort==="closest"?"closest first":"open now first")+'</span>'
    +'<button class="nextb" id="nextb">Pour another</button>';
  $("nextb").onclick=next;
  if(fresh)SND.reveal(state.idx);}
function next(){if(!state.list.length)return;
  state.idx=(state.idx+1)%state.list.length;
  SND.next(state.idx);reveal(false);
  var sp=body.querySelector(".spot");if(sp){sp.classList.remove("re-a");void sp.offsetWidth;sp.classList.add("re-a");}}
function setRadius(v,doSearch){v=Math.max(1,Math.min(20,Math.round(v)));
  var changed=v!==state.radius;if(!changed&&!doSearch)return;
  state.radius=v;updateRadiusUI();
  if(changed)SND.tick(v);
  clearTimeout(setRadius._t);
  if(state.origin&&!window.__radHold)setRadius._t=setTimeout(function(){search(false);},220);}
$("sortClosest").onclick=function(){state.sort="closest";sortUI();if(state.origin)search(false);};
$("sortOpen").onclick=function(){state.sort="open";sortUI();if(state.origin)search(false);};
function sortUI(){$("sortClosest").setAttribute("aria-pressed",state.sort==="closest");
  $("sortOpen").setAttribute("aria-pressed",state.sort==="open");}
$("snd").onclick=function(){state.sound=!state.sound;this.setAttribute("aria-pressed",state.sound);};
addEventListener("scroll",function(){fuse.classList.toggle("scrolled",scrollY>40);},{passive:true});

/* cherry meter: drag RIGHT = farther, 1..20 mi */
var meter=$("meter"),mh=$("mHandle"),mv=$("mVal"),CW=26;
function usable(){return Math.max(1,(meter?meter.clientWidth:150)-CW);}
function xFor(v){return ((v-1)/19)*usable();}
function updateRadiusUI(){var x=xFor(state.radius);
  if(mh){mh.style.left=x+"px";mh.setAttribute("aria-valuenow",state.radius);mh.setAttribute("aria-valuetext",state.radius+" miles");}
  if(mv){mv.style.left=(x+CW/2)+"px";mv.textContent=state.radius+" mi";}
  var cv=document.getElementById("chipVal");if(cv)cv.textContent=state.radius+" mi";}
function vFromX(clientX){var r=meter.getBoundingClientRect();var t=(clientX-r.left-CW/2)/usable();
  t=Math.max(0,Math.min(1,t));return Math.round(1+t*19);}
var dragMe=$("dragMe"),dmSeen=false,dmT=null;
function hideDragMe(){dmSeen=true;if(dragMe)dragMe.classList.remove("show");if(dmT){clearInterval(dmT);dmT=null;}}
function pulseDragMe(){if(dmSeen||!dragMe)return;dragMe.classList.add("show");setTimeout(function(){dragMe.classList.remove("show");},2600);}
if(meter){
  var dragging=false;
  meter.addEventListener("pointerdown",function(e){dragging=true;hideDragMe();meter.setPointerCapture(e.pointerId);setRadius(vFromX(e.clientX));e.preventDefault();});
  meter.addEventListener("pointermove",function(e){if(dragging)setRadius(vFromX(e.clientX));});
  meter.addEventListener("pointerup",function(){dragging=false;});
  meter.addEventListener("wheel",function(e){hideDragMe();setRadius(state.radius+(e.deltaY<0?1:-1));e.preventDefault();},{passive:false});
  mh.addEventListener("keydown",function(e){
    if(e.key==="ArrowRight"||e.key==="ArrowUp"){hideDragMe();setRadius(state.radius+1);e.preventDefault();}
    if(e.key==="ArrowLeft"||e.key==="ArrowDown"){hideDragMe();setRadius(state.radius-1);e.preventDefault();}});
  var ticksBuilt=false;
  function buildTicks(){var g=$("mTicks");if(!g||ticksBuilt)return;ticksBuilt=true;var W=usable();
    for(var v=1;v<=20;v++){var big=(v===1||v%5===0);var cx=CW/2+((v-1)/19)*W;
      var t=document.createElement("span");t.className="tick"+(big?" big":"");t.style.left=cx+"px";g.appendChild(t);
      if(big){var lb=document.createElement("span");lb.className="tnum";lb.style.left=cx+"px";lb.textContent=v;g.appendChild(lb);}}}
  var chip=$("meterChip"),fin=document.querySelector(".finder-inline");
  if(chip)chip.addEventListener("click",function(e){if(e.target.closest(".dragme"))return;hideDragMe();
    var open=fin.classList.toggle("meter-open");chip.setAttribute("aria-expanded",open);
    if(open)setTimeout(function(){buildTicks();updateRadiusUI();},280);});
  /* Drag-Me nudge: first pop ~2.5s, then every ~7s until the user grabs it */
  setTimeout(function(){if(!dmSeen){dragMe.classList.add("show");setTimeout(function(){dragMe.classList.remove("show");},2600);}},2500);
  dmT=setInterval(pulseDragMe,7200);
}

/* integrated "near you" module inside the Shops mega panel */
var megaShops=document.querySelector("#bnpanel-shops .bn-mega--shops"),nearBox=null;
if(megaShops){nearBox=document.createElement("div");nearBox.className="bn-near";megaShops.appendChild(nearBox);}
function renderNear(){if(!nearBox)return;
  if(!state.origin){
    nearBox.innerHTML='<h4>Near you</h4><p class="bn-near-p">Say where you are and this menu pours the closest rooms.</p>'
      +'<div class="bn-near-chips">'+["Cerritos","Rowland Heights","Irvine","Chino Hills"].map(function(c){
        return '<button type="button" data-c="'+c+'">'+c+'</button>';}).join("")+'</div>';
    nearBox.querySelectorAll("button[data-c]").forEach(function(b){
      b.addEventListener("click",function(){window.__demo.pick(b.getAttribute("data-c"));});});
    return;}
  var t=laNow();
  var top=SHOPS.filter(function(x){return x.st==="open"||x.st==="seed";})
    .map(function(x){return {s:x,d:miles(state.origin.lat,state.origin.lng,x.lat,x.lng),o:openNow(x,t)};})
    .sort(function(a,b){return a.d-b.d;}).slice(0,3);
  nearBox.innerHTML='<h4>Near '+esc(state.label)+'</h4>'
    +top.map(function(x){return '<a class="bn-near-row" href="https://www.bobanight.com'+x.s.p+'">'
      +'<span class="od'+(x.o===true?'':' off')+'"></span>'+esc(x.s.n)
      +'<span class="mi">'+(x.d<0.1?"0.1":x.d.toFixed(1))+' mi</span></a>';}).join("")
    +'<p class="bn-near-range">within '+state.radius+' mi · drag the cream to widen</p>';}
renderNear();
updateRadiusUI();

window.__demo={pick:function(name){q.value=name;q.dispatchEvent(new Event("input"));if(matches.length)pick(matches[0]);},
  next:next,setRadius:function(v){setRadius(v,true);},setRadiusSilent:function(v){setRadius(v,false);},updateUI:updateRadiusUI,state:state,nearestCity:nearestCity,
  setScope:function(v){if(v!=="city"&&v!=="all")return;if(state.scope===v)return;state.scope=v;if(state.origin)search(false);}};
})();
(function(){var f=document.getElementById('fuse'),d=document.getElementById('dock');
function fit(){d.style.top=f.getBoundingClientRect().bottom+'px';}
addEventListener('scroll',fit,{passive:true});addEventListener('resize',fit);fit();
var mo=new MutationObserver(fit);mo.observe(f,{attributes:true});})();
(function(){
var box=document.getElementById("tyFloat"),q=document.getElementById("tyQ"),res=document.getElementById("tyRes");
if(!box||!q)return;
document.getElementById("tyX").onclick=function(){box.style.display="none";};
var BASE="https://www.bobanight.com";
var PAGES=[["Brown sugar vs tiger sugar","Guides","/guide/brown-sugar-vs-tiger-sugar/"],["Crystal boba vs tapioca","Guides","/guide/crystal-boba-vs-tapioca/"],["Loose-leaf vs powder","Guides","/guide/loose-leaf-vs-powder/"],["How to order non-dairy","Guides","/guide/order-non-dairy-boba/"],["What 50% sweet means","Guides","/guide/what-50-percent-sweet-means/"],["What cheese foam is","Guides","/guide/what-is-cheese-foam/"],["The Pantry: ingredients","Guides","/pantry/"],["Best for date night","Best for","/best/date-night/"],["Best for first dates","Best for","/best/first-date/"],["Open late","Best for","/best/open-late/"],["Best for brown sugar","Best for","/best/brown-sugar/"],["Best for matcha","Best for","/best/matcha/"],["Non-dairy picks","Best for","/best/non-dairy/"],["New openings","New","/new/"],["Roulette","Tools","/tools/roulette/"],["Drink Matcher","Tools","/tools/drink-matcher/"],["Date Night Planner","Tools","/tools/date-planner/"],["The Pearl Ratings","Critic","/critic/"],["How we rank","Critic","/how-we-rank/"],["Meetups & clubs","Meetups","/meetups/"]];
var ING=[["Tapioca pearls / boba"],["Crystal boba"],["Cheese foam"],["Taro"],["Matcha"],["Brown sugar"],["Wintermelon"],["Oolong"],["Grass jelly"],["Egg pudding"],["Thai tea"],["Lychee jelly"]];
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c];});}
function hi(t,n){var i=t.toLowerCase().indexOf(n.toLowerCase());if(i<0)return esc(t);
  return esc(t.slice(0,i))+'<mark>'+esc(t.slice(i,i+n.length))+'</mark>'+esc(t.slice(i+n.length));}
q.addEventListener("input",function(){var n=q.value.trim();
  if(n.length<2){res.hidden=true;res.innerHTML="";return;}
  var shops=DATA.shops.filter(function(x){return x.n.toLowerCase().indexOf(n.toLowerCase())>=0;}).slice(0,5);
  var pages=PAGES.filter(function(p){return p[0].toLowerCase().indexOf(n.toLowerCase())>=0;}).slice(0,4);
  var ing=ING.filter(function(p){return p[0].toLowerCase().indexOf(n.toLowerCase())>=0;}).slice(0,4);
  var h="";
  if(shops.length){h+='<p class="tg">Tea houses</p>'+shops.map(function(x){
    return '<a href="'+BASE+x.p+'"><span>'+hi(x.n,n)+'</span><em>'+esc(x.c)+'</em></a>';}).join("");}
  if(pages.length){h+='<p class="tg">Pages</p>'+pages.map(function(p){
    return '<a href="'+BASE+p[2]+'"><span>'+hi(p[0],n)+'</span><em>'+esc(p[1])+'</em></a>';}).join("");}
  if(ing.length){h+='<p class="tg">Ingredients</p>'+ing.map(function(p){
    return '<a href="'+BASE+'/pantry/"><span>'+hi(p[0],n)+'</span><em>Pantry</em></a>';}).join("");}
  res.innerHTML=h||'<p class="tg" style="border:0">Nothing matches &ldquo;'+esc(n)+'&rdquo;</p>';
  res.hidden=false;});
q.addEventListener("keydown",function(e){if(e.key==="Escape"){q.value="";res.hidden=true;}});
})();

/* --- per-region featured house (Supabase-driven, lazy, cached) --- */
(function(){
  var SB="https://uqefyfqwwkkvydkgepgf.supabase.co";
  var KEY="sb_publishable_0Y-o-QD73luyTYUcjWRWzQ_7b9ogFLs";
  var panel=document.getElementById("bnpanel-shops"); if(!panel) return;
  var feat=panel.querySelector(".bn-feat"); if(!feat) return;
  var tEl=feat.querySelector(".bn-feat-t"), sEl=feat.querySelector(".bn-feat-s");
  var MAP=null, pending=false;
  function apply(region){
    var r=MAP&&MAP[region]; if(!r) return;
    if(r.shop_path) feat.setAttribute("href", r.shop_path);
    if(tEl&&r.shop_name) tEl.textContent=r.shop_name;
    if(sEl) sEl.textContent=(r.shop_city?r.shop_city+" · ":"")+(r.blurb||"");
  }
  function current(){
    var sel=panel.querySelector('.bn-rail-b[aria-selected="true"]');
    return sel?sel.getAttribute("data-region"):"the-626";
  }
  function load(){
    if(MAP||pending) return; pending=true;
    fetch(SB+"/rest/v1/boba_region_featured?select=region_key,shop_name,shop_city,shop_path,blurb",
      {headers:{apikey:KEY,Authorization:"Bearer "+KEY}})
      .then(function(r){return r.ok?r.json():[];})
      .then(function(rows){MAP={};(rows||[]).forEach(function(x){MAP[x.region_key]=x;});apply(current());})
      .catch(function(){});
  }
  panel.addEventListener("click",function(e){
    var b=e.target.closest(".bn-rail-b[data-region]"); if(b){load();apply(b.getAttribute("data-region"));}
  });
  var trig=document.querySelector('.bn-trigger[aria-controls="bnpanel-shops"]');
  if(trig){["mouseenter","focus","click"].forEach(function(ev){trig.addEventListener(ev,load);});}
})();


/* ===== NAV V1 base behavior (panel clamp, radius popover w/ hold + Set) ===== */

(function(){
  function clampPanels(){
    document.querySelectorAll(".fuse .bn-item").forEach(function(it){
      var p=it.querySelector(".bn-panel"); if(!p) return;
      p.style.left="50%"; p.style.transform="translateX(-50%)";
      var r=p.getBoundingClientRect();
      var pad=12, shift=0;
      if(r.left<pad) shift=pad-r.left;
      if(r.right>innerWidth-pad) shift=(innerWidth-pad)-r.right;
      if(shift) p.style.transform="translateX(calc(-50% + "+shift+"px))";
    });
  }
  addEventListener("resize",clampPanels);
  document.querySelectorAll(".fuse .bn-trigger").forEach(function(t){
    t.addEventListener("mouseenter",function(){requestAnimationFrame(clampPanels);});
    t.addEventListener("click",function(){requestAnimationFrame(clampPanels);});
  });
  setTimeout(clampPanels,300);
  var chip=document.getElementById("meterChip"), pop=document.getElementById("radPop");
  function radius(){ return (window.__demo&&__demo.state&&__demo.state.radius)||5; }
  function paint(){ var v=document.getElementById("radVal"); if(v) v.textContent=radius();
    var cv=document.getElementById("chipVal"); if(cv) cv.textContent=radius()+" mi"; }
  if(chip&&pop){
    chip.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();
      pop.hidden=!pop.hidden; var fi=document.querySelector(".finder-inline"); if(fi)fi.classList.remove("meter-open");
      if(!pop.hidden){window.__radHold=true; pop.dataset.start=radius(); paint(); requestAnimationFrame(function(){ if(window.__demo&&__demo.updateUI)__demo.updateUI(); });}
      else{closePop();}},true);
    function closePop(){ if(pop.hidden){window.__radHold=false;return;}
      pop.hidden=true; window.__radHold=false;
      var st=parseInt(pop.dataset.start||"0",10);
      if(window.__demo&&__demo.state.origin&&radius()!==st){__demo.setRadius(radius());} }
    window.__closeRadPop=closePop;
    document.addEventListener("click",function(e){ if(!pop.hidden && !e.target.closest("#radAnchor")) closePop(); });
    document.addEventListener("keydown",function(e){ if(e.key==="Escape") closePop(); });
    var setBtn=document.createElement("button");
    setBtn.type="button"; setBtn.className="rad-set"; setBtn.textContent="Set range";
    pop.appendChild(setBtn);
    setBtn.addEventListener("click",function(e){e.stopPropagation();closePop();});
  }
  var mi=document.getElementById("radMinus"), pl=document.getElementById("radPlus");
  if(mi) mi.addEventListener("click",function(){ if(window.__demo)__demo.setRadiusSilent(Math.max(1,radius()-1)); paint(); });
  if(pl) pl.addEventListener("click",function(){ if(window.__demo)__demo.setRadiusSilent(Math.min(20,radius()+1)); paint(); });
  var mv=document.getElementById("mVal");
  if(mv){ new MutationObserver(paint).observe(mv,{childList:true,characterData:true,subtree:true}); }
})();

/* ===== NAV V1 skin (pearl caret, jewel-box) ===== */

(function(){
  /* Pulse #radVal whenever its text changes */
  var rv = document.getElementById("radVal");
  if(!rv) return;
  var last = rv.textContent;
  new MutationObserver(function(){
    var now = rv.textContent;
    if(now === last) return;
    last = now;
    rv.classList.remove("pulse");
    /* force restart of the animation */
    void rv.offsetWidth;
    rv.classList.add("pulse");
  }).observe(rv, {childList:true, characterData:true, subtree:true});
  rv.addEventListener("animationend", function(){ rv.classList.remove("pulse"); });
})();


/* ===== dock filters: Open now + Originals/Chains ===== */
(function(){
  var dock=document.getElementById("dock"), body=document.getElementById("dockBody"), foot=document.getElementById("dockFoot");
  if(!dock||!body||!window.__demo) return;
  var F={open:false,kind:"all"}, all=null;
  var bar=document.createElement("div"); bar.className="dock-filters"; bar.id="dockFilters";
  var LAMP='<svg class="lampsvg" viewBox="0 0 64 32" aria-hidden="true">'
    +'<defs><linearGradient id="lmTrack" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101214"/><stop offset="1" stop-color="#1c1f24"/></linearGradient>'
    +'<radialGradient id="lmKnob" cx=".33" cy=".3" r=".95"><stop offset="0" stop-color="#f4e3c2"/><stop offset=".45" stop-color="#C5A46D"/><stop offset="1" stop-color="#7a5f35"/></radialGradient></defs>'
    +'<rect x="1" y="1" width="62" height="30" rx="15" fill="url(#lmTrack)" stroke="rgba(197,164,109,.4)"/>'
    +'<rect x="2.5" y="2.5" width="59" height="27" rx="13.5" fill="none" stroke="rgba(0,0,0,.55)"/>'
    +'<g class="lm-knob"><circle cx="16" cy="16" r="11" fill="url(#lmKnob)"/>'
    +'<circle cx="16" cy="16" r="11" fill="none" stroke="rgba(122,95,53,.85)"/>'
    +'<path d="M10.5 12.4h11M10.5 16h11M10.5 19.6h11" stroke="rgba(58,42,16,.3)" stroke-width="1"/>'
    +'<circle class="lm-led" cx="16" cy="16" r="3.1" fill="#3a3f3d"/>'
    +'<circle class="lm-core" cx="16" cy="16" r="1.5" fill="#a8e6c8" opacity="0"/></g></svg>';
  bar.innerHTML='<span class="dfl">Show</span>'
    +'<span class="df-seg" id="dfSeg"><span class="df-ind" aria-hidden="true"></span>'
    +'<button type="button" class="dfc" data-k="all" aria-pressed="true">All</button>'
    +'<button type="button" class="dfc" data-k="orig" aria-pressed="false">Originals<span class="ct"></span></button>'
    +'<button type="button" class="dfc" data-k="chain" aria-pressed="false">Chains<span class="ct"></span></button></span>'
    +'<span class="df-seg df-seg--scope" id="dfScopeSeg" style="display:none"><span class="df-ind" aria-hidden="true"></span>'
    +'<button type="button" class="dfc" data-s="city" aria-pressed="true"><span class="sc-city">This city</span><span class="ct"></span></button>'
    +'<button type="button" class="dfc" data-s="all" aria-pressed="false">Within <b class="sc-mi">8</b> mi<span class="ct"></span></button></span>'
    +'<button type="button" class="dfc df-lamp" data-open aria-pressed="false">'+LAMP+'<span class="lab">Open now</span></button>';
  body.parentNode.insertBefore(bar, body);
  function segUI(){ bar.querySelectorAll(".df-seg").forEach(function(seg){
    var b=seg.querySelector('.dfc[aria-pressed="true"]'), ind=seg.querySelector(".df-ind");
    if(!b||!ind||!b.offsetWidth) return;
    ind.style.width=b.offsetWidth+"px";
    ind.style.transform="translateX("+b.offsetLeft+"px)"; }); }
  function scopeUI(){ var seg=document.getElementById("dfScopeSeg"); if(!seg) return;
    var st=window.__demo.state, lock=st.cityLock;
    seg.style.display=lock?"":"none";
    if(!lock) return;
    seg.querySelector(".sc-city").textContent=lock;
    seg.querySelector(".sc-mi").textContent=st.radius;
    var cs=seg.querySelectorAll(".ct");
    if(st.scopeCounts){cs[0].textContent=" "+st.scopeCounts.city;cs[1].textContent=" "+st.scopeCounts.all;}
    seg.querySelectorAll(".dfc[data-s]").forEach(function(x){x.setAttribute("aria-pressed",String(x.getAttribute("data-s")===st.scope));}); }
  addEventListener("resize",segUI);
  function counts(){ if(!all) return;
    var o=0,c=0; all.forEach(function(x){ if(x.s.ty==="specialty")o++; else if(x.s.ty==="chain")c++; });
    var els=bar.querySelectorAll(".ct"); els[0].textContent=" "+o; els[1].textContent=" "+c;
    requestAnimationFrame(segUI); }
  function apply(){
    if(!all) return;
    var f=all.filter(function(x){
      if(F.open&&x.o!==true) return false;
      if(F.kind==="orig") return x.s.ty==="specialty";
      if(F.kind==="chain") return x.s.ty==="chain";
      return true; });
    f.__f=true; var st=window.__demo.state; st.list=f; st.idx=-1;
    if(f.length){ window.__demo.next(); }
    else{
      body.innerHTML='<div class="dock-empty">Nothing matches those filters inside this range. Clear a filter or widen the range.</div>';
      if(foot) foot.innerHTML='<span class="counter">0 of '+all.length+' match</span>';
    }
  }
  bar.addEventListener("click",function(e){
    var b=e.target.closest(".dfc"); if(!b) return;
    if(b.hasAttribute("data-s")){ window.__demo.setScope(b.getAttribute("data-s")); scopeUI(); segUI(); return; }
    if(b.hasAttribute("data-open")){ F.open=!F.open; b.setAttribute("aria-pressed",String(F.open)); }
    else{ F.kind=b.getAttribute("data-k");
      bar.querySelectorAll(".dfc[data-k]").forEach(function(x){x.setAttribute("aria-pressed",String(x===b));});
      segUI(); }
    apply();
  });
  new MutationObserver(function(){
    var st=window.__demo.state;
    if(st.list&&st.list.length&&!st.list.__f){ all=st.list.slice(); counts(); if(F.open||F.kind!=="all"){apply();} }
    else if(st.list&&!st.list.length&&!st.list.__f){ all=null; }
    scopeUI();
    requestAnimationFrame(segUI);
  }).observe(body,{childList:true});
})();

/* ===== NAV F3 base fixes (card auto-close) ===== */

(function(){
  var dock=document.getElementById("dock"), q=document.getElementById("q"), chip=document.getElementById("meterChip");
  function closeCard(){ if(dock) dock.classList.remove("on"); }
  if(q){ q.addEventListener("focus",closeCard); q.addEventListener("input",closeCard); }
  if(chip){ chip.addEventListener("click",closeCard,true); }
})();

/* ===== NAV F3 BEACON skin ===== */

(function(){
"use strict";
var q=document.getElementById("q");
var field=q&&q.closest(".mb-field");
if(!q||!field) return;

/* ============ 1. empty-state CTA ============ */
q.setAttribute("placeholder","Type your city or ZIP");

var sweep=document.createElement("span");
sweep.className="f3-sweep"; sweep.setAttribute("aria-hidden","true");
field.appendChild(sweep);

var helper=document.createElement("div");
helper.className="f3-helper";
helper.textContent="Boba near you in one tap, or type a city";
field.appendChild(helper);

function hasChip(){return !!field.querySelector(".f3-chip");}
function syncEmpty(){
  var empty=!q.value.trim(), foc=document.activeElement===q;
  field.classList.toggle("f3-empty", empty&&!foc&&!hasChip());
  field.classList.toggle("f3-hint", empty&&foc);
}
q.addEventListener("focus",syncEmpty);
q.addEventListener("blur",function(){setTimeout(syncEmpty,0);});
q.addEventListener("input",syncEmpty);
syncEmpty();

/* pin beacon: one tap to your location */
var beacon=document.createElement("button");
beacon.type="button"; beacon.id="f3Beacon"; beacon.className="f3-beacon";
beacon.title="Find boba near my location";
beacon.setAttribute("aria-label","Find boba near my location");
beacon.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21c-4-4.5-7-8-7-11a7 7 0 0 1 14 0c0 3-3 6.5-7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>';
field.insertAdjacentElement("afterend",beacon);

function flashErr(){
  beacon.classList.remove("f3-err"); void beacon.offsetWidth;
  beacon.classList.add("f3-err");
  setTimeout(function(){beacon.classList.remove("f3-err");},1200);
}
beacon.addEventListener("click",function(e){
  e.stopPropagation();
  if(!navigator.geolocation||!window.__demo){flashErr();return;}
  navigator.geolocation.getCurrentPosition(function(p){
    removeChip();
    var st=window.__demo.state;
    st.origin={lat:p.coords.latitude,lng:p.coords.longitude};
    var nc=window.__demo.nearestCity&&window.__demo.nearestCity(p.coords.latitude,p.coords.longitude);
    st.label=nc?nc.city:"Your location";
    st.cityLock=nc?nc.city:null;st.scope=nc?"city":"all";
    q.value=nc?nc.city:"";
    var sg=document.getElementById("sug");
    if(sg){sg.classList.remove("on");sg.innerHTML="";q.setAttribute("aria-expanded","false");}
    window.__demo.setRadius(st.radius);
    if(nc&&window.__f3Lock)window.__f3Lock(nc.city,"");
    syncEmpty();
  },function(){flashErr();},{enableHighAccuracy:true,timeout:9000,maximumAge:60000});
});

/* ============ 3. locked-location chip: city picks, ZIP picks, GPS pins ============ */
var CHIP_RE=/^(.+) (\d{5})$/, lastLock=null;
function removeChip(){
  var c=field.querySelector(".f3-chip");
  if(c) c.remove();
  field.classList.remove("f3-haschip");
}
function makeChip(city,zip){
  removeChip();
  var c=document.createElement("div");
  c.className="f3-chip";
  c.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 21c-4-4.5-7-8-7-11a7 7 0 0 1 14 0c0 3-3 6.5-7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>'
    +'<span class="fc-city"></span><span class="fc-zip"></span>'
    +'<svg class="fc-lock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>'
    +'<button type="button" class="f3-chipx" aria-label="Clear location">&times;</button>';
  c.querySelector(".fc-city").textContent=city;
  c.querySelector(".fc-zip").textContent=zip||"";
  c.addEventListener("click",function(e){
    if(e.target.closest(".f3-chipx")){
      e.stopPropagation();
      q.value="";
      lastLock=null;
      removeChip();
      q.dispatchEvent(new Event("input",{bubbles:true}));
      q.focus();
      return;
    }
    q.focus(); /* the focus handler lifts the chip for editing */
  });
  field.appendChild(c);
  field.classList.add("f3-haschip");
  /* tidy any stale "no match" suggestion panel now hidden behind the chip */
  var sg=document.getElementById("sug");
  if(sg){sg.classList.remove("on");sg.innerHTML="";q.setAttribute("aria-expanded","false");}
  syncEmpty();
}
window.__f3Lock=function(city,zip){
  lastLock={city:city,zip:zip||""};
  if(document.activeElement!==q) makeChip(city,zip||"");
};
function checkChip(){
  if(document.activeElement===q) return;
  var v=q.value.trim();
  var m=CHIP_RE.exec(v);
  if(m){ makeChip(m[1],m[2]); return; }
  if(lastLock && v===lastLock.city){ makeChip(lastLock.city,lastLock.zip); return; }
  removeChip();
}
q.addEventListener("blur",function(){setTimeout(checkChip,0);});
q.addEventListener("focus",function(){removeChip();syncEmpty();});
checkChip();

/* ============ 2. Open-now LED pill in the card header zone ============ */
/* Reparent the [data-open] button into an absolutely-positioned nest that
   STAYS a descendant of #dockFilters, so the original delegated click
   listener keeps firing untouched. */
(function(){
  var bar=document.getElementById("dockFilters");
  var ob=bar&&bar.querySelector(".dfc[data-open]");
  if(!bar||!ob) return;
  var nest=document.createElement("span");
  nest.className="f3-lednest";
  nest.appendChild(ob);
  bar.appendChild(nest);
})();

/* ============ 4. dropdown polish: tag ZIP rows for champagne styling ============ */
(function(){
  var sg=document.getElementById("sug");
  if(!sg) return;
  function tag(){
    sg.querySelectorAll(".rn").forEach(function(n){
      if(/^\d{5}$/.test(n.textContent.trim())) n.classList.add("f3-zip");
    });
  }
  new MutationObserver(tag).observe(sg,{childList:true,subtree:true});
  tag();
})();
})();

/* ===== nav hover closes the radius popover (silent) ===== */
(function radNavClose(){
  var pop=document.getElementById("radPop"); if(!pop) return;
  document.querySelectorAll(".fuse .bn-item").forEach(function(it){
    it.addEventListener("mouseenter",function(){ if(!pop.hidden){ pop.hidden=true; window.__radHold=false; } });
  });
})();
