/* Stack Bank service worker — offline app shell (v6) */
const CACHE='stack-bank-v6';
const FILES=['./','./stack-bank-premium.html','./manifest.webmanifest',
  './stack-bank-icons/icon-192.png','./stack-bank-icons/icon-512.png',
  './stack-bank-icons/icon-512-maskable.png','./stack-bank-icons/apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  if(new URL(e.request.url).origin!==location.origin)return; // leave fonts/CDN to the network
  e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request).then(res=>{
    const copy=res.clone();
    caches.open(CACHE).then(c=>c.put(e.request,copy));
    return res;
  }).catch(()=>caches.match('./stack-bank-premium.html'))));
});
