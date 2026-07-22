/* Boba Night universal mega nav — components/nav.js
   One nav for every page. A template includes ONE line before </body>:
     <script src="/components/nav.js" defer></script>
   Optionally place <div id="bn-nav"></div> where the header should mount
   (defaults to the top of <body>). The loader injects components/nav.html,
   attaches the required stylesheets, then loads the nav behavior scripts in
   order. Pages that already contain a baked header (the homepage) are
   detected and skipped, so including this everywhere is always safe.
   PREVIEWS AND OFF-SITE PAGES: load this script with an absolute URL —
     <script src="https://www.bobanight.com/components/nav.js" defer></script>
   The loader reads its own script URL and pulls every asset (markup, css,
   behavior js) from that origin, so a file in Downloads opened over file://
   shows the same live nav as the site. Never bake nav markup into a page.
   Editing components/nav.html updates the nav on every included page on the
   next load. Never regenerate page templates for a nav change. */
(function(){
'use strict';
var BASE='';
try{
  var me=document.currentScript||document.querySelector('script[src*="components/nav.js"]');
  if(me&&me.src){var u=new URL(me.src,location.href);if(u.origin&&u.origin!=='null'&&u.origin!==location.origin)BASE=u.origin;}
  if(!BASE&&location.protocol==='file:')BASE='https://www.bobanight.com';
}catch(e){if(location.protocol==='file:')BASE='https://www.bobanight.com';}
function mount(){
  if(document.querySelector('[data-bn-header]')||document.getElementById('fuse'))return;
  ['/css/nav-midnight.css','/css/finder.css','/css/sound.css'].forEach(function(href){
    if(!document.querySelector('link[href*="'+href+'"]')){
      var l=document.createElement('link');l.rel='stylesheet';l.href=BASE+href;document.head.appendChild(l);}
  });
  fetch(BASE+'/components/nav.html').then(function(r){return r.text();}).then(function(html){
    var host=document.getElementById('bn-nav');
    if(host){host.outerHTML=html;}
    else{document.body.insertAdjacentHTML('afterbegin',html);}
    if(BASE){[].slice.call(document.querySelectorAll('.bn-header a[href^="/"], .bn-bottombar a[href^="/"], .fuse a[href^="/"]')).forEach(function(a){
      var h=a.getAttribute('href');if(h&&h.charAt(0)==='/'&&h.charAt(1)!=='/')a.href=BASE+h;});
      [].slice.call(document.querySelectorAll('.bn-header img[src^="/"], .fuse img[src^="/"]')).forEach(function(im){
      var s=im.getAttribute('src');if(s&&s.charAt(0)==='/'&&s.charAt(1)!=='/')im.src=BASE+s;});}
    function load(src){return new Promise(function(res){
      if(document.querySelector('script[src*="'+src+'"]'))return res();
      var s=document.createElement('script');s.src=BASE+src;s.onload=res;s.onerror=res;document.body.appendChild(s);});}
    load('/js/nav-midnight.js')
      .then(function(){return load('/js/homepage/near-me.js');})
      .then(function(){return load('/js/sound.js');});
  }).catch(function(){});
}
if(document.readyState!=='loading')mount();
else document.addEventListener('DOMContentLoaded',mount);
})();
