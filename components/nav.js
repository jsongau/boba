/* Boba Night universal mega nav — components/nav.js
   One nav for every page. A template includes ONE line before </body>:
     <script src="/components/nav.js" defer></script>
   Optionally place <div id="bn-nav"></div> where the header should mount
   (defaults to the top of <body>). The loader injects components/nav.html,
   attaches the required stylesheets, then loads the nav behavior scripts in
   order. Pages that already contain a baked header (the homepage) are
   detected and skipped, so including this everywhere is always safe.
   Editing components/nav.html updates the nav on every included page on the
   next load. Never regenerate page templates for a nav change. */
(function(){
'use strict';
function mount(){
  if(document.querySelector('[data-bn-header]')||document.getElementById('fuse'))return;
  ['/css/nav-midnight.css','/css/finder.css','/css/sound.css'].forEach(function(href){
    if(!document.querySelector('link[href="'+href+'"]')){
      var l=document.createElement('link');l.rel='stylesheet';l.href=href;document.head.appendChild(l);}
  });
  fetch('/components/nav.html').then(function(r){return r.text();}).then(function(html){
    var host=document.getElementById('bn-nav');
    if(host){host.outerHTML=html;}
    else{document.body.insertAdjacentHTML('afterbegin',html);}
    function load(src){return new Promise(function(res){
      if(document.querySelector('script[src="'+src+'"]'))return res();
      var s=document.createElement('script');s.src=src;s.onload=res;s.onerror=res;document.body.appendChild(s);});}
    load('/js/nav-midnight.js')
      .then(function(){return load('/js/homepage/near-me.js');})
      .then(function(){return load('/js/sound.js');});
  }).catch(function(){});
}
if(document.readyState!=='loading')mount();
else document.addEventListener('DOMContentLoaded',mount);
})();
