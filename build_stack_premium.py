#!/usr/bin/env python3
"""Build Stack Bank Premium from stack-bank__17.html — keeps ALL logic/screens,
replaces the visual layer: animated background, professional SVG icons, premium glass/gold."""
import json, pathlib, re

SRC = pathlib.Path("workspace/user/files/stack-bank__17.html")
DST = pathlib.Path("workspace/user/files/stack-bank-premium.html")
t = SRC.read_text(encoding="utf-8")
assert "<title>Stack Bank</title>" in t
assert "function load()" in t

PREMIUM_CSS = r"""
/* ================= STACK BANK — PREMIUM v4 =================
   Animated living background + professional animated SVG icons
   + gold / violet / mint glass system. Overrides the basic theme. */
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&display=swap');
:root{
  --gold:#f0c35b; --gold2:#e9a93b; --violet:#6d5efc; --violet2:#a855f7;
  --mint:#2ee6a8; --ink:#05070d; --glass:rgba(255,255,255,.06);
  --stroke:rgba(255,255,255,.11); --stroke-gold:rgba(240,195,91,.45);
}
html{scroll-behavior:smooth}
body{
  background:#05070d !important;
  font-family:'Sora','Inter',system-ui,sans-serif !important;
}
/* ---------- LIVING ANIMATED BACKGROUND ---------- */
.sb-bg{position:fixed; inset:0; z-index:0; overflow:hidden; pointer-events:none}
.sb-bg canvas{position:absolute; inset:0; width:100%; height:100%; opacity:.9}
.sb-blob{position:absolute; border-radius:50%; filter:blur(70px); will-change:transform,opacity; mix-blend-mode:screen}
.sb-b1{width:58vmax;height:58vmax;left:-18%;top:-22%;background:radial-gradient(circle at 35% 35%,rgba(109,94,252,.55),rgba(109,94,252,0) 65%);animation:blob1 26s ease-in-out infinite alternate}
.sb-b2{width:46vmax;height:46vmax;right:-14%;top:6%;background:radial-gradient(circle at 60% 40%,rgba(168,85,247,.48),rgba(168,85,247,0) 65%);animation:blob2 32s ease-in-out infinite alternate}
.sb-b3{width:52vmax;height:52vmax;left:22%;bottom:-32%;background:radial-gradient(circle at 50% 50%,rgba(46,230,168,.28),rgba(46,230,168,0) 65%);animation:blob3 28s ease-in-out infinite alternate}
.sb-b4{width:34vmax;height:34vmax;right:18%;bottom:8%;background:radial-gradient(circle at 50% 50%,rgba(240,195,91,.32),rgba(240,195,91,0) 65%);animation:blob4 22s ease-in-out infinite alternate}
.sb-b5{width:22vmax;height:22vmax;left:38%;top:28%;background:radial-gradient(circle at 50% 50%,rgba(91,124,250,.35),rgba(91,124,250,0) 65%);animation:blob1 36s ease-in-out infinite alternate-reverse}
@keyframes blob1{0%{transform:translate3d(0,0,0) scale(1)}50%{transform:translate3d(9vw,6vh,0) scale(1.18) rotate(8deg)}100%{transform:translate3d(-4vw,10vh,0) scale(.94) rotate(-6deg)}}
@keyframes blob2{0%{transform:translate3d(0,0,0) scale(1)}50%{transform:translate3d(-8vw,9vh,0) scale(1.22)}100%{transform:translate3d(5vw,-5vh,0) scale(1.05)}}
@keyframes blob3{0%{transform:translate3d(0,0,0) scale(1)}50%{transform:translate3d(7vw,-7vh,0) scale(1.15)}100%{transform:translate3d(-6vw,4vh,0) scale(.96)}}
@keyframes blob4{0%{transform:translate3d(0,0,0) scale(1);opacity:.9}50%{transform:translate3d(-6vw,-8vh,0) scale(1.25);opacity:1}100%{transform:translate3d(4vw,6vh,0) scale(1);opacity:.75}}
.sb-beam{position:absolute; left:50%; top:-30%; width:140vmax; height:140vmax; transform:translateX(-50%);
  background:conic-gradient(from 0deg,transparent 0deg,rgba(109,94,252,.10) 40deg,transparent 90deg,rgba(240,195,91,.09) 170deg,transparent 230deg,rgba(46,230,168,.08) 300deg,transparent 360deg);
  animation:spinBeam 48s linear infinite; filter:blur(10px)}
@keyframes spinBeam{to{transform:translateX(-50%) rotate(360deg)}}
.sb-grid{position:absolute; inset:0; background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px); background-size:44px 44px;
  -webkit-mask-image:radial-gradient(80% 60% at 50% 0%,#000 0%,transparent 78%); mask-image:radial-gradient(80% 60% at 50% 0%,#000 0%,transparent 78%); animation:gridDrift 18s linear infinite}
@keyframes gridDrift{to{background-position:0 44px,44px 0}}
.sb-noise{position:absolute; inset:0; opacity:.05; background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='0.6'/%3E%3C/svg%3E")}
.sb-vignette{position:absolute; inset:0; background:radial-gradient(120% 90% at 50% 40%,transparent 55%,rgba(0,0,0,.55) 100%)}
.sb-orb{position:absolute; width:10px; height:10px; border-radius:50%; background:var(--gold); box-shadow:0 0 18px 4px rgba(240,195,91,.55); animation:orbFloat 9s ease-in-out infinite}
.sb-orb.o2{left:12%; top:62%; background:#8b5cf6; box-shadow:0 0 18px 4px rgba(139,92,246,.55); animation-delay:-3s}
.sb-orb.o3{left:82%; top:58%; background:#2ee6a8; box-shadow:0 0 18px 4px rgba(46,230,168,.5); animation-delay:-6s}
.sb-orb.o1{left:68%; top:18%}
@keyframes orbFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-26px)}}
body::before,body::after{display:none !important}
#app,.onboard{position:relative; z-index:1}
/* ---------- PREMIUM TYPE & SURFACES ---------- */
.brand b{font-size:17px; letter-spacing:-.3px}
.brand small{color:#aab2c8}
.logo{
  background:linear-gradient(135deg,#f7d774,#e9a93b 45%,#8a5a00) !important; color:#171200 !important;
  box-shadow:0 0 0 1px rgba(240,195,91,.55),0 10px 28px -8px rgba(240,195,91,.55),inset 0 1px 0 rgba(255,255,255,.7) !important;
  position:relative; overflow:hidden}
.logo::after{content:""; position:absolute; inset:0; background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.75) 50%,transparent 70%); transform:translateX(-120%); animation:logoShine 4.5s ease-in-out infinite}
@keyframes logoShine{0%,55%{transform:translateX(-120%)}85%,100%{transform:translateX(120%)}}
.demo-chip{
  background:linear-gradient(120deg,rgba(240,195,91,.22),rgba(240,195,91,.06)) !important;
  border:1px solid rgba(240,195,91,.45) !important; color:#ffe1a1 !important;
  box-shadow:0 0 20px rgba(240,195,91,.18)}
.demo-chip::before{content:""; width:6px; height:6px; border-radius:50%; background:var(--gold); box-shadow:0 0 10px var(--gold); animation:dotPulse 1.6s ease-in-out infinite}
@keyframes dotPulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.6);opacity:.55}}
/* Hero — living gradient, not a flat block */
.hero{
  background:linear-gradient(125deg,#5b7cfa,#7c5cff 38%,#a855f7 62%,#2ee6a8 135%) !important;
  background-size:220% 220% !important; animation:heroFlow 12s ease infinite !important;
  border:1px solid rgba(255,255,255,.28) !important;
  box-shadow:0 30px 60px -20px rgba(109,94,252,.65),inset 0 1px 0 rgba(255,255,255,.35) !important;
  overflow:hidden}
@keyframes heroFlow{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.hero::before{content:""; position:absolute; inset:0; background:linear-gradient(110deg,transparent 35%,rgba(255,255,255,.22) 50%,transparent 65%); background-size:250% 100%; animation:heroSweep 5s ease-in-out infinite; pointer-events:none}
@keyframes heroSweep{0%{background-position:180% 0}100%{background-position:-80% 0}}
.hero .amt{
  background:linear-gradient(100deg,#fff 20%,#ffe9b0 55%,#fff 80%) !important;
  background-size:200% 100% !important; -webkit-background-clip:text !important; background-clip:text !important;
  color:transparent !important; animation:amtShine 4s linear infinite; filter:drop-shadow(0 4px 18px rgba(0,0,0,.25))}
@keyframes amtShine{to{background-position:200% 0}}
.hero .row button{transition:transform .2s,background .2s}
.hero .row button:hover{background:rgba(255,255,255,.28); transform:translateY(-2px)}
/* Glass cards — gradient border, inner light */
.card,.tiles button,.chip-toggle,.stat,.easybtn{
  background:linear-gradient(160deg,rgba(255,255,255,.075),rgba(255,255,255,.028)) !important;
  border:1px solid var(--stroke) !important;
  box-shadow:0 18px 44px -22px rgba(0,0,0,.75),inset 0 1px 0 rgba(255,255,255,.08) !important;
  backdrop-filter:blur(18px) saturate(150%); -webkit-backdrop-filter:blur(18px) saturate(150%)}
.tiles button{transition:transform .28s cubic-bezier(.2,.8,.2,1),border-color .28s,box-shadow .28s}
.tiles button:hover{transform:translateY(-4px); border-color:rgba(240,195,91,.5) !important; box-shadow:0 24px 44px -18px rgba(109,94,252,.55),inset 0 1px 0 rgba(255,255,255,.14)}
.tiles button:active{transform:scale(.96)}
.shead h3{letter-spacing:.1em; text-transform:uppercase; font-size:.72rem; color:rgba(234,234,242,.78)}
.shead h3::before{background:linear-gradient(90deg,var(--gold),var(--violet)); box-shadow:0 0 10px rgba(240,195,91,.7); animation:dotPulse 2s ease-in-out infinite}
/* ---------- PROFESSIONAL ANIMATED ICONS — never static emoji ---------- */
.se{display:inline-flex; align-items:center; justify-content:center; vertical-align:-.18em; line-height:0}
.se .sic,.sic{width:1.12em; height:1.12em; display:block; stroke-width:1.8;
  filter:drop-shadow(0 0 7px rgba(109,94,252,.35)); transition:transform .25s ease,filter .25s ease}
.tiles .ti .sic{width:1.35em; height:1.35em}
.tiles button:hover .sic{transform:translateY(-2px) scale(1.12) rotate(-4deg); filter:drop-shadow(0 0 10px rgba(240,195,91,.6))}
.icobtn .sic{width:1.3em; height:1.3em}
.icobtn:hover .sic{transform:scale(1.12)}
button:hover .se .sic{transform:scale(1.1)}
.avatar .sic{width:1.25em; height:1.25em}
.logo .sic{width:1.3em; height:1.3em}
nav .sic{width:1.35em; height:1.35em}
nav button.on .sic{filter:drop-shadow(0 0 10px rgba(240,195,91,.7))}
.bigbtn .sic{width:1.15em; height:1.15em}
/* icon micro-motion: bell swings, sparkle twinkles, shield breathes */
.se[data-ic="bell"] .sic{transform-origin:top center}
.icobtn:hover .se[data-ic="bell"] .sic{animation:bellSwing .7s ease-in-out}
@keyframes bellSwing{0%,100%{transform:rotate(0)}25%{transform:rotate(14deg)}60%{transform:rotate(-10deg)}}
.se[data-ic="spark"] .sic{animation:sparkTw 2.4s ease-in-out infinite}
@keyframes sparkTw{0%,100%{transform:scale(1) rotate(0); opacity:1}50%{transform:scale(1.18) rotate(18deg); opacity:.85}}
.se[data-ic="shield"] .sic{animation:shieldBreath 3s ease-in-out infinite}
@keyframes shieldBreath{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
/* Icon chips — gradient, not flat colour blocks */
.tiles .ti,.avatar,.jemoji,.bav{
  background:linear-gradient(135deg,rgba(109,94,252,.28),rgba(240,195,91,.18)) !important;
  border:1px solid rgba(255,255,255,.14) !important; box-shadow:inset 0 1px 0 rgba(255,255,255,.18)}
/* Buttons — gold/violet gradient + travelling shine */
.bigbtn{
  background:linear-gradient(135deg,#6d5efc,#a855f7 55%,#e9a93b 130%) !important;
  position:relative; overflow:hidden; transition:transform .2s,box-shadow .25s}
.bigbtn::after{content:""; position:absolute; inset:0; background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.35) 50%,transparent 70%); transform:translateX(-120%); transition:transform .7s ease}
.bigbtn:hover::after{transform:translateX(120%)}
.bigbtn:hover{transform:translateY(-2px); box-shadow:0 20px 40px -12px rgba(139,92,246,.6)}
.bigbtn.gold{background:linear-gradient(135deg,#f7d774,#ff8a3d) !important; color:#241a00 !important}
.bigbtn.ghost{background:rgba(255,255,255,.06) !important; border:1px solid var(--stroke) !important}
/* Bank card — holographic foil + tilt shine */
.bankcard{
  background:linear-gradient(130deg,#171b2e,#232a4a 42%,#0d1017 78%,#2a1e4d) !important;
  transform-style:preserve-3d; transition:transform .25s ease,box-shadow .25s ease; will-change:transform}
.bankcard::after{content:""; position:absolute; inset:0; border-radius:inherit; pointer-events:none;
  background:radial-gradient(420px 180px at var(--mx,80%) var(--my,10%),rgba(255,255,255,.22),transparent 60%),
  linear-gradient(115deg,transparent 38%,rgba(240,195,91,.20) 50%,transparent 62%); background-size:100% 100%,250% 100%;
  animation:cardSweep 6s ease-in-out infinite}
@keyframes cardSweep{0%{background-position:0 0,180% 0}100%{background-position:0 0,-80% 0}}
.bankcard .num4{font-family:'Inter',monospace; letter-spacing:3px; text-shadow:0 2px 14px rgba(0,0,0,.4)}
/* Nav — floating premium pill */
nav{background:rgba(12,16,30,.78) !important; backdrop-filter:blur(24px) saturate(160%); border:1px solid rgba(255,255,255,.14) !important; box-shadow:0 24px 50px -18px rgba(0,0,0,.75),inset 0 1px 0 rgba(255,255,255,.1) !important}
nav button.on{color:#ffe1a1}
nav .sendfab{background:linear-gradient(135deg,#f0c35b,#a855f7) !important; box-shadow:0 16px 34px -10px rgba(240,195,91,.6),0 0 0 1px rgba(255,255,255,.25) inset !important; position:relative; overflow:hidden}
nav .sendfab::after{content:""; position:absolute; inset:0; background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.5) 50%,transparent 70%); transform:translateX(-120%); animation:logoShine 3.8s ease-in-out infinite}
/* Onboarding — same living background */
.onboard{background:radial-gradient(1000px 600px at 50% -20%,rgba(109,94,252,.38),transparent 60%),#05070d !important}
.onboard .orb{filter:blur(70px); opacity:.55}
.onb-card{background:linear-gradient(180deg,rgba(16,20,38,.72),rgba(7,9,15,.94)) !important; backdrop-filter:blur(22px); border:1px solid var(--stroke)}
.onb-card h1 em{background:linear-gradient(90deg,#f0c35b,#a855f7,#2ee6a8); -webkit-background-clip:text; background-clip:text; color:transparent}
/* Pills, bars, modal, toast */
.pill.mint{box-shadow:0 0 14px rgba(46,230,168,.15)}
.bar i,.jar .bar i{background:linear-gradient(90deg,#6d5efc,#a855f7,#f0c35b) !important; background-size:200% 100%; animation:barFlow 3s linear infinite}
@keyframes barFlow{to{background-position:200% 0}}
.modal{box-shadow:0 -20px 60px rgba(0,0,0,.6)}
.toast{background:rgba(16,20,38,.96) !important; border:1px solid rgba(240,195,91,.4) !important; box-shadow:0 18px 44px rgba(0,0,0,.6),0 0 24px rgba(240,195,91,.12)}
.switch.on{background:linear-gradient(90deg,#6d5efc,#a855f7,#e9a93b) !important}
input[type=range]{accent-color:#e9a93b}
@media (prefers-reduced-motion:reduce){
  .sb-blob,.sb-beam,.sb-grid,.hero,.hero::before,.logo::after,.bankcard::after,.bar i,.jar .bar i{animation:none !important}
  #sbCanvas{display:none}
}
"""

BG_HTML = r"""
<div class="sb-bg" aria-hidden="true">
  <div class="sb-beam"></div>
  <div class="sb-blob sb-b1"></div><div class="sb-blob sb-b2"></div><div class="sb-blob sb-b3"></div>
  <div class="sb-blob sb-b4"></div><div class="sb-blob sb-b5"></div>
  <div class="sb-grid"></div>
  <canvas id="sbCanvas"></canvas>
  <div class="sb-orb o1"></div><div class="sb-orb o2"></div><div class="sb-orb o3"></div>
  <div class="sb-noise"></div><div class="sb-vignette"></div>
</div>
"""

PREMIUM_JS = r"""
<script>
/* ===== Stack Premium v4 — animated background + pro icon engine ===== */
(function(){
  /* --- 1. Gold-dust particle canvas (living background) --- */
  function mq(q){ try{ return typeof window.matchMedia==='function' && window.matchMedia(q).matches; }catch(e){ return false; } }
  function raf2(fn){ if(typeof requestAnimationFrame==='function') return requestAnimationFrame(fn); return setTimeout(fn,16); }
  function caf2(id){ if(typeof cancelAnimationFrame==='function') cancelAnimationFrame(id); else clearTimeout(id); }
  var cv=document.getElementById('sbCanvas');
  if(cv && !mq('(prefers-reduced-motion: reduce)')){
    var ctx=null; try{ ctx=cv.getContext('2d'); }catch(e){ ctx=null; }
    if(ctx){ var W, H, ps=[], raf=null;
    var COLORS=['240,195,91','109,94,252','46,230,168','168,85,247','255,255,255'];
    function size(){ var r=cv.getBoundingClientRect(); W=cv.width=r.width*devicePixelRatio; H=cv.height=r.height*devicePixelRatio; }
    function make(n){ ps=[]; for(var i=0;i<n;i++) ps.push({x:Math.random()*W,y:Math.random()*H,r:(Math.random()*1.8+.6)*devicePixelRatio,s:Math.random()*.35+.08,o:Math.random()*.55+.15,ph:Math.random()*6.28,c:COLORS[i%COLORS.length],tw:Math.random()*.02+.005}); }
    function tick(){ ctx.clearRect(0,0,W,H); var t=Date.now()/1000;
      for(var i=0;i<ps.length;i++){ var p=ps[i]; p.y-=p.s; p.x+=Math.sin(t*.6+p.ph)*.25;
        if(p.y<-10){p.y=H+10;p.x=Math.random()*W;}
        var a=p.o*(.55+.45*Math.sin(t*2*p.tw*60+p.ph));
        ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,6.283); ctx.fillStyle='rgba('+p.c+','+Math.max(.05,a)+')'; ctx.fill();
        if(p.r>1.6*devicePixelRatio){ ctx.beginPath(); ctx.arc(p.x,p.y,p.r*3.2,0,6.283); ctx.fillStyle='rgba('+p.c+','+(a*.12)+')'; ctx.fill(); } }
      raf=raf2(tick); }
    size(); make(Math.min(90,Math.floor(innerWidth/14))); tick();
    addEventListener('resize',function(){ size(); });
    document.addEventListener('visibilitychange',function(){ if(document.hidden){caf2(raf);raf=null;} else if(!raf){tick();} });
  } }
  /* --- 2. Mouse parallax on the aurora + card tilt + hero shine --- */
  var bg=document.querySelector('.sb-bg');
  if(bg && mq('(pointer:fine)')){
    addEventListener('pointermove',function(e){
      var x=(e.clientX/innerWidth-.5), y=(e.clientY/innerHeight-.5);
      bg.style.transform='translate3d('+(x*10)+'px,'+(y*8)+'px,0)';
    },{passive:true});
  }
  document.addEventListener('pointermove',function(e){
    var c=e.target.closest && e.target.closest('.bankcard'); if(!c) return;
    var r=c.getBoundingClientRect(), px=(e.clientX-r.left)/r.width, py=(e.clientY-r.top)/r.height;
    c.style.setProperty('--mx',(px*100)+'%'); c.style.setProperty('--my',(py*100)+'%');
    c.style.transform='perspective(900px) rotateY('+((px-.5)*10)+'deg) rotateX('+((.5-py)*8)+'deg)';
  },{passive:true});
  document.addEventListener('pointerout',function(e){
    var c=e.target.closest && e.target.closest('.bankcard'); if(c) c.style.transform='';
  });
  /* --- 3. Professional icon engine v2 — replaces EVERY remaining emoji
         with a Lucide-style stroke SVG. Flags + currency symbols are kept. --- */
  var PATHS={
    bell:'<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
    gear:'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h.08a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51h.08a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v.08a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    up:'<path d="M12 19V5"/><path d="m5 12 7-7 7 7"/>',
    send:'<path d="M7 17 17 7"/><path d="M8 7h9v9"/>',
    jar:'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.66 3.58 3 8 3s8-1.34 8-3V5"/><path d="M4 12c0 1.66 3.58 3 8 3s8-1.34 8-3"/>',
    chat:'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    weather:'<path d="M12 2v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="M20 12h2"/><path d="m19.07 4.93-1.41 1.41"/><path d="M15.9 12.5a4 4 0 0 0-5.8-4"/><path d="M13 22H3a4 4 0 0 1 0-8h1a6.5 6.5 0 0 1 9-6.03"/>',
    sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    cloud:'<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
    rain:'<path d="M4 14.9A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.24"/><path d="M16 14v6"/><path d="M8 14v6"/><path d="M12 16v6"/>',
    storm:'<path d="M6 16.33A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 .5 8.97"/><path d="m13 12-3 5h4l-3 5"/>',
    fog:'<path d="M3 10h18"/><path d="M5 14h14"/><path d="M7 18h10"/>',
    user:'<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    bot:'<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
    shield:'<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    chart:'<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    check:'<path d="M20 6 9 17l-5-5"/>',
    zap:'<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    bank:'<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
    cash:'<rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01"/><path d="M18 12h.01"/>',
    wallet:'<path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/>',
    fly:'<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    receipt:'<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1-2-1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 17.5v-11"/>',
    users:'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    globe:'<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    mic:'<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/>',
    id:'<rect width="20" height="16" x="2" y="4" rx="2"/><circle cx="8" cy="10" r="2"/><path d="M6 18c0-1.5 1-3 2-3s2 1.5 2 3"/><path d="M14 8h4"/><path d="M14 12h4"/>',
    signal:'<path d="M2 20h.01"/><path d="M7 20v-4"/><path d="M12 20v-8"/><path d="M17 20V8"/><path d="M22 4v16"/>',
    home:'<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    card:'<rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/>',
    spark:'<path d="M9.94 15.5 8.5 14.06 2.36 12.48a.5.5 0 0 1 0-.96L8.5 9.94 10.08 3.8a.5.5 0 0 1 .96 0l1.58 6.14 6.14 1.58a.5.5 0 0 1 0 .96l-6.14 1.58-1.58 6.14a.5.5 0 0 1-.96 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/>',
    phone:'<rect width="14" height="20" x="5" y="2" rx="2"/><path d="M12 18h.01"/>',
    phonecall:'<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    lock:'<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    arrow:'<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    arrowright:'<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    snow:'<line x1="2" x2="22" y1="12" y2="12"/><line x1="12" x2="12" y1="2" y2="22"/><path d="m20 16-4-4 4-4"/><path d="m4 8 4 4-4 4"/><path d="m16 4-4 4-4-4"/><path d="m8 20 4-4 4 4"/>',
    eye:'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    list:'<rect width="8" height="8" x="3" y="3" rx="1"/><rect width="8" height="8" x="13" y="3" rx="1"/><rect width="8" height="8" x="3" y="13" rx="1"/><rect width="8" height="8" x="13" y="13" rx="1"/>',
    scooter:'<circle cx="18.5" cy="17.5" r="3.5"/><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="15" cy="5" r="1"/><path d="M12 17.5V14l-3-3 4-3 2 3h2"/>',
    car:'<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H8.2c-.8 0-1.5.4-1.9 1.1L4.6 11l-2.1.3C1.6 11.4 1 12.1 1 13v3c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
    fuel:'<line x1="3" x2="15" y1="22" y2="22"/><line x1="4" x2="14" y1="9" y2="9"/><path d="M14 22V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v18"/><path d="M14 13h2a2 2 0 0 1 2 2v2a2 2 0 0 0 4 0V9.83a2 2 0 0 0-.59-1.42L18 5"/>',
    gift:'<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    wrench:'<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    tv:'<rect width="20" height="15" x="2" y="7" rx="2"/><polyline points="17 2 12 7 7 2"/>',
    armchair:'<path d="M19 9V6a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v3"/><path d="M3 16a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v1.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V11a2 2 0 0 0-4 0z"/><path d="M5 18v2"/><path d="M19 18v2"/>',
    target:'<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    camera:'<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
    pen:'<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>',
    pointer:'<path d="m3 3 7.07 16.97 2.51-7.39 7.39-2.51L3 3z"/>',
    barchart:'<line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/>',
    medal:'<circle cx="12" cy="15" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
    star:'<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    link:'<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    mail:'<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    hand:'<path d="M18 11V6.5a1.5 1.5 0 0 0-3 0V11m0-5.5v-2a1.5 1.5 0 0 0-3 0V11m0-7.5a1.5 1.5 0 0 0-3 0v8"/><path d="M18 8a1.5 1.5 0 0 1 3 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a1.5 1.5 0 0 1 2.12-2.12L5 16"/>',
    thumb:'<path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88Z"/>',
    plug:'<path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    exchange:'<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    package:'<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/><path d="M12 22V12"/><path d="m3.3 7 8.7 5 8.7-5"/>',
    plus:'<path d="M5 12h14"/><path d="M12 5v14"/>',
    flask:'<path d="M10 2v7.5a2 2 0 0 1-.2.9L4.71 20.5a1 1 0 0 0 .9 1.5h12.78a1 1 0 0 0 .9-1.5L14.2 10.4a2 2 0 0 1-.2-.9V2"/><path d="M8.5 2h7"/><path d="M7 16h10"/>',
    file:'<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    refresh:'<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    volume:'<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>',
    play:'<polygon points="6 3 20 12 6 21 6 3"/>',
    coins:'<circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18"/><path d="M7 6h1v4"/><path d="m16.71 13.88.7.71-2.82 2.82"/>',
    eth:'<path d="M12 2 5.5 12.5 12 16.5 18.5 12.5Z"/><path d="M12 22 5.5 14.5 12 17.5 18.5 14.5Z"/>',
    more:'<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>',
    layers:'<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>'
  };
  var MAP={
    '🤖':'bot','🛡':'shield','🛡️':'shield','⚙️':'gear','⚙':'gear','📈':'chart','✅':'check','💬':'chat',
    '🌤':'weather','🌤️':'weather','⛅':'weather','⛅️':'weather','💡':'zap','🏦':'bank','💵':'cash','🔔':'bell',
    '↗️':'send','↗':'send','🍯':'jar','📲':'phone','🧾':'receipt','🤝':'users','🌐':'globe','🌍':'globe',
    '💸':'fly','🎤':'mic','🪪':'id','⬆️':'up','⬆':'up','📶':'signal','🛴':'scooter','🏧':'card','🏠':'home',
    '💳':'card','❄️':'snow','❄':'snow','👁️':'eye','👁':'eye','✨':'spark','📱':'phone','☀️':'sun','☀':'sun',
    '🧑':'user','👵':'user','🧓':'user','👴':'user','🔒':'lock','🔐':'lock','➤':'arrow','📋':'list',
    '☁️':'cloud','☁':'cloud','🌧️':'rain','🌧':'rain','⛈️':'storm','⛈':'storm','🌫️':'fog','🌫':'fog',
    '👋':'hand','📞':'phonecall','✉️':'mail','🔗':'link','🚗':'car','🎁':'gift','🎉':'spark','🔧':'wrench',
    '⛽':'fuel','🍿':'tv','🪑':'armchair','🛵':'scooter','💰':'wallet','🎯':'target','📸':'camera',
    '✍️':'pen','✍':'pen','👆':'pointer','📊':'barchart','🥇':'medal','★':'star','🫵':'pointer','🧕':'user',
    '👍':'thumb','🔌':'plug','💱':'exchange','🛎':'bell','📦':'package','➕':'plus','🧪':'flask','📄':'file',
    '🔁':'refresh','🔊':'volume','▶':'play','₿':'coins','Ξ':'eth','⋯':'more','→':'arrowright','✓':'check'
  };
  var KEYS=Object.keys(MAP).sort(function(a,b){return b.length-a.length});
  var esc=function(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');};
  var RX=new RegExp('('+KEYS.map(esc).join('|')+')(?:\uFE0F|[\u{1F3FB}-\u{1F3FF}])?','gu');
  function svgFor(k){ var name=MAP[k]; if(!name||!PATHS[name]) return null;
    return '<svg class="sic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+PATHS[name]+'</svg>'; }
  var SKIP={SCRIPT:1,STYLE:1,TEXTAREA:1,SVG:1,NOSCRIPT:1,INPUT:1,SELECT:1,OPTION:1};
  function swap(node){ var txt=node.nodeValue; if(!txt) return; RX.lastIndex=0; if(!RX.test(txt)) return; RX.lastIndex=0;
    var frag=document.createDocumentFragment(), last=0, m;
    while((m=RX.exec(txt))){ var s=svgFor(m[1]); if(!s) continue;
      frag.appendChild(document.createTextNode(txt.slice(last,m.index)));
      var sp=document.createElement('span'); sp.className='se'; sp.setAttribute('data-ic',MAP[m[1]]); sp.innerHTML=s; frag.appendChild(sp);
      last=m.index+m[0].length; }
    if(last<txt.length) frag.appendChild(document.createTextNode(txt.slice(last)));
    node.parentNode.replaceChild(frag,node); }
  function walk(root){ if(!root) return;
    var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:function(n){ var p=n.parentNode; return (p&&SKIP[p.nodeName])?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT; }},null);
    var list=[], n; while(w.nextNode()) list.push(w.currentNode);
    for(var i=0;i<list.length;i++){ try{swap(list[i]);}catch(e){} } }
  var mo=null;
  function pass(){ if(mo) mo.disconnect(); try{walk(document.body);}catch(e){} if(mo) mo.observe(document.body,{childList:true,subtree:true,characterData:true}); }
  pass();
  mo=new MutationObserver(function(){ raf2(pass); });
  mo.observe(document.body,{childList:true,subtree:true,characterData:true});
  window.sbIconsV4=pass;
  /* Logo mark becomes a professional layers icon */
  var logo=document.querySelector('.brand .logo');
  if(logo && logo.textContent.trim()==='S'){ logo.innerHTML='<svg class="sic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'+PATHS.layers+'</svg>'; }
})();
</script>
"""

# 1. premium CSS before </head>
if "</head>" not in t:
    raise SystemExit("no </head>")
t = t.replace("</head>", "<style>\n" + PREMIUM_CSS + "\n</style>\n</head>", 1)

# 2. animated background right after <body>
t = t.replace("<body>", "<body>\n" + BG_HTML, 1)

# 2b. country flags are static emoji — clean country names in the select instead
t = re.sub(r"[\U0001F1E6-\U0001F1FF]+\s*", "", t)

# 3. premium JS before the LAST </body> (original file has a stray early </body> before its scripts)
if "</body>" not in t:
    raise SystemExit("no </body>")
idx = t.rfind("</body>")
t = t[:idx] + PREMIUM_JS + "\n" + t[idx:]

# 4. Title bump
t = t.replace("<title>Stack Bank</title>", "<title>Stack Bank — Premium</title>", 1)

# ---------- v5: ladder hero on home + real edge cases ----------
V5_CSS = r"""
/* ===== Stack Premium v5 — ladder hero + edge states ===== */
#ladderHero{background:linear-gradient(155deg,rgba(246,196,83,.10),rgba(124,108,255,.10) 55%,rgba(46,230,168,.07)) !important;border:1px solid rgba(246,196,83,.35) !important}
.lh-head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
.lh-kicker{font-size:10.5px;font-weight:800;letter-spacing:1.4px;color:#ffd98a}
.lh-salary{font-size:34px;font-weight:800;letter-spacing:-1px;margin:4px 0 2px}
.lh-salary small{font-size:13px;font-weight:600;color:var(--tx2);letter-spacing:0}
.splitbar{display:flex;height:12px;border-radius:99px;overflow:hidden;background:rgba(255,255,255,.09);margin:14px 0 10px}
.splitbar i{display:block;height:100%}
.seg-salary{background:linear-gradient(90deg,#f6c453,#e08a2e)}
.seg-buffer{background:linear-gradient(90deg,#7c6cff,#a855f7)}
.seg-jars{background:linear-gradient(90deg,#2ee6a8,#2bb5d6)}
.seg-spend{background:rgba(255,255,255,.25)}
.lh-legend{display:grid;grid-template-columns:1fr 1fr;gap:7px 12px;font-size:12.5px;color:var(--tx2)}
.lh-legend b{color:var(--tx)}
.lh-dot{display:inline-block;width:9px;height:9px;border-radius:99px;margin-right:6px}
.lh-foot{margin-top:14px;padding-top:12px;border-top:1px solid var(--line);font-size:12px;line-height:1.6;color:var(--tx2)}
.lh-btns{display:flex;gap:10px;margin-top:14px}
.lh-btns .bigbtn{padding:13px 10px;font-size:13.5px}
"""
t = t.replace("</head>", "<style>\n" + V5_CSS + "\n</style>\n</head>", 1)

# Ladder hero placeholder, right after the balance hero on home
t = t.replace(
  '  <button class="bigbtn ghost" style="margin-top:14px" onclick="easyOn()">',
  '  <div class="card" id="ladderHero" style="margin-top:14px"></div>\n  <button class="bigbtn ghost" style="margin-top:14px" onclick="easyOn()">', 1)

V5_JS = r"""
/* ===== Stack Premium v5 — ladder hero + edge cases ===== */
function ladderMath(){
  var L=S.ladder, cur=S.weekly[5]||0;
  var avg=S.weekly.slice(0,5).reduce(function(a,b){return a+b;},0)/5;
  var sweep=Math.max(0,Math.round((cur-avg)*0.6));
  var jarsCut=Math.round(cur*(S.autoPct||10)/100);
  var salary=L.on?Math.min(L.weekly,cur):L.weekly;
  var buffer=L.on?sweep:0, jars=L.on?jarsCut:0;
  var spend=Math.max(0,cur-salary-buffer-jars);
  return {cur:cur,avg:avg,salary:salary,buffer:buffer,jars:jars,spend:spend,reserve:L.reserve||0,weeks:L.weekly?Math.floor((L.reserve||0)/L.weekly):0};
}
function nextFriday(){
  var d=new Date(), add=(5-d.getDay()+7)%7||7, f=new Date(d.getTime()+add*864e5);
  return f.toLocaleDateString('en-US',{weekday:'long',month:'short',day:'numeric'});
}
function renderLadderHero(){
  var el=$('ladderHero'); if(!el) return;
  var m=ladderMath(), L=S.ladder;
  var pct=function(v){ return m.cur>0?Math.max(5,Math.round(v/m.cur*100)):0; };
  var pill=L.on?'<span class="pill mint">Live</span>':'<span class="pill gold">Paused</span>';
  var note=L.on
    ? 'This week you earned <b>$'+money(m.cur)+'</b>. Your ladder splits it before you can spend it.'
    : 'Preview of your week on <b>$'+money(m.cur)+'</b> of gig income. Turn the ladder on to lock this split in.';
  el.innerHTML =
    '<div class="lh-head"><div><div class="lh-kicker">PAYCHECK LADDER · YOUR STEADY SALARY</div>'+
    '<div class="lh-salary">$'+money(L.weekly)+' <small>every Friday · next '+nextFriday()+'</small></div></div>'+pill+'</div>'+
    '<div class="mut" style="margin-top:2px">'+note+'</div>'+
    '<div class="splitbar"><i class="seg-salary" style="width:'+pct(m.salary)+'%"></i><i class="seg-buffer" style="width:'+pct(m.buffer)+'%"></i><i class="seg-jars" style="width:'+pct(m.jars)+'%"></i><i class="seg-spend" style="width:'+pct(m.spend)+'%"></i></div>'+
    '<div class="lh-legend">'+
    '<span><i class="lh-dot" style="background:#f6c453"></i>Salary <b>$'+money(m.salary)+'</b></span>'+
    '<span><i class="lh-dot" style="background:#a855f7"></i>Buffer <b>$'+money(m.buffer)+'</b></span>'+
    '<span><i class="lh-dot" style="background:#2ee6a8"></i>Jars <b>$'+money(m.jars)+'</b></span>'+
    '<span><i class="lh-dot" style="background:rgba(255,255,255,.4)"></i>To spend <b>$'+money(m.spend)+'</b></span></div>'+
    '<div class="lh-foot">Buffer reserve: <b>$'+money(m.reserve)+'</b> · covers <b>'+m.weeks+' Friday'+(m.weeks===1?'':'s')+'</b> with no new income.<br>🛡 Protected: biometric lock · AI fraud check on every move · nothing leaves without your approval.</div>'+
    '<div class="lh-btns"><button class="bigbtn" onclick="go(\'ladder\')">See my ladder</button>'+
    '<button class="bigbtn ghost" onclick="toggleLadder()">'+(L.on?'Pause ladder':'Turn ladder on')+'</button></div>';
}
/* --- Edge case 1: failed transfer is a real record, not a vanishing toast --- */
function failSend(to,a,why){
  S.txs.unshift({d:'Today',t:'Send to '+to+' — failed',a:-a,i:'↗️',k:'out',st:'failed',why:why});
  S.lastFailed={n:to,a:a}; save(); render();
}
function retryFailed(){
  var f=S.lastFailed; if(!f){go('send');return;}
  go('send'); $('sendTo').value=f.n; $('sendAmt').value=f.a;
  toast('Filled in again. Check it and send when ready.');
}
/* --- Edge case 2: bad network queues the send, settles when data returns --- */
function settlePending(){
  var pend=S.txs.filter(function(tx){return tx.k==='pend'&&tx.st==='pending';});
  var done=0, failed=0;
  pend.forEach(function(tx){
    var amt=Math.abs(tx.a), fee=tx.fee||0;
    if(amt+fee<=S.balance){
      S.balance-=(amt+fee); tx.k='out'; tx.st='settled'; tx.t=tx.t.replace(' · queued','');
      if(fee>0)S.txs.unshift({d:'Today',t:'Send fee',a:-fee,i:'💸',k:'out'});
      done++;
    } else { tx.st='failed'; tx.t=tx.t.replace(' · queued',' — failed'); tx.why='Not enough balance when data returned'; failed++; }
  });
  if(done>0||failed>0){ save(); render(); toast(done>0?('Data back: '+done+' queued send'+(done>1?'s':'')+' delivered.'):'Queued send failed: not enough balance now. No money moved.'); }
}
/* --- Edge case 3: duplicate-charge guard on sends --- */
function confirmDupSend(){
  var l=S.lastSend; closeModal(); if(!l)return;
  S.lastSend={n:l.n,a:l.a,ts:0}; S._dupOk=true;
  $('sendTo').value=l.n; $('sendAmt').value=l.a; doSend();
}
/* --- Edge case 4: an Ajo member defaults, escrow covers, trust drops --- */
function missedPayment(i){
  var c=S.circle, m=c.members[i];
  if(!m||i<c.paid||i===0)return;
  if(c.escrow<c.amt){toast('Escrow is too low to cover this share.');return;}
  c.escrow-=c.amt; c.pot+=c.amt; c.paid++;
  m.trust=Math.max(0,m.trust-8); m.missed=true;
  S.txs.unshift({d:'Today',t:'Ajo escrow covered '+m.n+' · Round '+c.round,a:-c.amt,i:'🤝',k:'out'});
  S.notifs.unshift({t:'Ajo: '+m.n+' missed this round',d:'Escrow covered their $'+money(c.amt)+' share. Their trust score dropped to '+m.trust+'.'});
  save(); render(); renderCircles();
  toast('Escrow covered '+m.n+'. Their trust dropped to '+m.trust+'.');
}
"""
# Inject v5 functions into the main script, before load() runs
assert "load();\n</script>" in t
t = t.replace("load();\n</script>", V5_JS + "\nload();\n</script>", 1)

# renderHome now refreshes the ladder hero on every visit
t = t.replace("  const t=S.txs.slice(0,4).map(txRow).join('');",
              "  if(window.renderLadderHero)renderLadderHero();\n  const t=S.txs.slice(0,4).map(txRow).join('');", 1)

# txRow: show a real status pill for failed / pending / duplicate / settled moves
OLD_TXROW = """function txRow(t){
  const sign=t.a>0?'+':'−', cls=t.a>0?'pos':'neg';
  return '<div class="rowline"><div class="avatar">'+t.i+'</div><div class="grow"><b>'+t.t+'</b><div class="dim">'+t.d+'</div></div><div class="amt"><b class="'+cls+'">'+sign+'$'+money(Math.abs(t.a))+'</b></div></div>';
}"""
NEW_TXROW = """function txRow(t){
  const sign=t.a>0?'+':'−', cls=t.a>0?'pos':'neg';
  let pill='';
  if(t.st==='failed')pill='<span class="pill red">Failed</span>';
  else if(t.st==='pending'||t.k==='pend')pill='<span class="pill gold">Pending</span>';
  else if(t.st==='duplicate')pill='<span class="pill blue">Duplicate</span>';
  else if(t.st==='settled')pill='<span class="pill mint">Sent</span>';
  const retry=t.st==='failed'?'<button class="pill gold" style="margin-top:4px" onclick="retryFailed()">Retry</button>':'';
  return '<div class="rowline"><div class="avatar">'+t.i+'</div><div class="grow"><b>'+t.t+'</b><div class="dim">'+t.d+(t.why?' · '+t.why:'')+'</div></div><div class="amt" style="text-align:right"><b class="'+cls+'">'+sign+'$'+money(Math.abs(t.a))+'</b><div style="margin-top:4px">'+pill+retry+'</div></div></div>';
}"""
assert OLD_TXROW in t
t = t.replace(OLD_TXROW, NEW_TXROW, 1)

# doSend: duplicate guard, offline queue, failed record (replaces the happy-path-only version)
OLD_SEND = """function doSend(){
  const to=$('sendTo').value.trim(), a=parseFloat($('sendAmt').value);
  if(!to||!a){toast('Add a recipient and amount');return}
  if(a+2.99>S.balance){toast('Not enough balance');return}
  S.balance-=(a+2.99);S.txs.unshift({d:'Today',t:'To '+to,a:-a,i:'↗️',k:'out'});
  S.txs.unshift({d:'Today',t:'Send fee',a:-2.99,i:'💸',k:'out'});
  S.lastSend={n:to,a:a};earnBack(a);
  $('sendTo').value='';$('sendAmt').value='';
  save();render();toast('Sent $'+money(a)+' to '+to+'. Instant.');
}"""
NEW_SEND = """function doSend(){
  const to=$('sendTo').value.trim(), a=parseFloat($('sendAmt').value);
  if(!to||!a){toast('Add a recipient and amount');return}
  if(S.lastSend&&S.lastSend.n===to&&S.lastSend.a===a&&Date.now()-(S.lastSend.ts||0)<60000){
    openModal('<h3>Wait — possible duplicate</h3><div class="mut">You sent $'+money(a)+' to '+to+' less than a minute ago. Send it again?</div><button class="bigbtn" onclick="confirmDupSend()">Yes, send again</button><button class="bigbtn ghost" style="margin-top:10px" onclick="closeModal()">No, cancel</button>');
    return;
  }
  if(!S.net){
    S.txs.unshift({d:'Today',t:'To '+to+' · queued',a:-a,i:'↗️',k:'pend',st:'pending',fee:2.99});
    S.lastSend={n:to,a:a,ts:Date.now()};
    $('sendTo').value='';$('sendAmt').value='';
    save();render();toast('No data. Send queued — it goes out the second data returns. No money moved yet.');
    return;
  }
  if(a+2.99>S.balance){ failSend(to,a,'Not enough balance'); toast('Send failed: not enough balance. No money moved.'); return; }
  S.balance-=(a+2.99);S.txs.unshift({d:'Today',t:'To '+to,a:-a,i:'↗️',k:'out'});
  S.txs.unshift({d:'Today',t:'Send fee',a:-2.99,i:'💸',k:'out'});
  if(S._dupOk){S.txs[1].st='duplicate';S._dupOk=false;}
  S.lastSend={n:to,a:a,ts:Date.now()};earnBack(a);
  $('sendTo').value='';$('sendAmt').value='';
  save();render();toast('Sent $'+money(a)+' to '+to+'. Instant.');
}"""
assert OLD_SEND in t
t = t.replace(OLD_SEND, NEW_SEND, 1)

# netToggle: settle queued sends the moment data returns
OLD_NET = """function netToggle(){
  S.net=!S.net;
  if(S.net){toast('Data is back.')}
  else{toast('Data off. Everything still completes instantly: USSD, SMS, QR and sends. Settlement runs quietly in the background.')}
  save();renderOffline();
}"""
NEW_NET = """function netToggle(){
  S.net=!S.net;
  if(S.net){settlePending();toast('Data is back.')}
  else{toast('Data off. Sends queue safely and settle when data returns.')}
  save();renderOffline();
}"""
assert OLD_NET in t
t = t.replace(OLD_NET, NEW_NET, 1)

# Easy sends also stamp the duplicate guard
t = t.replace("  S.lastSend={n:n,a:a};earnBack(a);\n  closeModal();save();render();renderEasy();",
              "  S.lastSend={n:n,a:a,ts:Date.now()};earnBack(a);\n  closeModal();save();render();renderEasy();", 1)

# Ajo member rows: missed state + Missed button; drawPot clears missed flags
OLD_MEMBER = """  $('circleMembers').innerHTML=c.members.map((m,i)=>{
    const paid=i<c.paid;
    return '<div class="rowline"><div class="avatar">'+(i===0?'🫵':i%2?'🧑🏾':'🧕🏾')+'</div><div class="grow"><b>'+m.n+(i===0?' (you)':'')+'</b><div class="dim">Draws #'+(i+1)+' in the order</div></div><div style="text-align:right">'+trustPill(m.trust)+'<div class="'+(paid?'check':'dim')+'" style="font-size:11px;margin-top:2px">'+(paid?'Paid ✓':'Waiting')+'</div></div></div>';
  }).join('');"""
NEW_MEMBER = """  $('circleMembers').innerHTML=c.members.map((m,i)=>{
    const paid=i<c.paid;
    const missedBtn=(!paid&&i!==0)?'<button class="pill red" style="margin-top:4px" onclick="missedPayment('+i+')">Missed</button>':'';
    const state=paid?'Paid ✓':(m.missed?'Missed · escrow covered':'Waiting');
    const col=paid?'#2ee6a8':(m.missed?'#ff5d73':'');
    return '<div class="rowline"><div class="avatar">'+(i===0?'🫵':i%2?'🧑🏾':'🧕🏾')+'</div><div class="grow"><b>'+m.n+(i===0?' (you)':'')+'</b><div class="dim">Draws #'+(i+1)+' in the order</div></div><div style="text-align:right">'+trustPill(m.trust)+'<div style="font-size:11px;margin-top:2px;color:'+col+'">'+state+'</div>'+missedBtn+'</div></div>';
  }).join('');"""
assert OLD_MEMBER in t
t = t.replace(OLD_MEMBER, NEW_MEMBER, 1)
t = t.replace("c.members.forEach(m=>{m.trust=Math.min(100,m.trust+1)});",
              "c.members.forEach(m=>{m.trust=Math.min(100,m.trust+1);m.missed=false;});", 1)

# Ajo escrow must always cover at least one share, or the "escrow covers" promise is broken by construction
t = t.replace("amt:25,escrow:20", "amt:25,escrow:50", 1)
t = t.replace("function renderCircles(){\n  const c=S.circle;",
              "function renderCircles(){\n  const c=S.circle;\n  if(c.escrow<c.amt)c.escrow=c.amt; // escrow must always cover at least one share", 1)

# Engine A (the original file's icon pass) only eats VS16 after an emoji, so a skin-tone
# modifier survives as a stray square (🧑🏾 -> icon + 🏾). Make it eat tones too.
OLD_RX_TAIL = r"+'\uFE0F?'"
# Engine A builds its regex WITHOUT the 'u' flag, so tones must be written as UTF-16
# surrogate pairs: high surrogate \uD83C + low surrogate in \uDFFB-\uDFFF.
NEW_RX_TAIL = r"+'(?:\uFE0F|\uD83C[\uDFFB-\uDFFF])?'"
assert OLD_RX_TAIL in t, "engine A RX tail not found"
t = t.replace(OLD_RX_TAIL, NEW_RX_TAIL, 1)

# ---------- v6: installable PWA — manifest + service worker + install button ----------
PWA_LINKS = (
  '<link rel="manifest" href="./manifest.webmanifest">\n'
  '<meta name="theme-color" content="#070b18">\n'
  '<meta name="mobile-web-app-capable" content="yes">\n'
  '<meta name="apple-mobile-web-app-capable" content="yes">\n'
  '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
  '<meta name="apple-mobile-web-app-title" content="Stack Bank">\n'
  '<link rel="apple-touch-icon" href="./stack-bank-icons/apple-touch-icon.png">'
)
t = t.replace('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
              '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + PWA_LINKS, 1)

t = t.replace("    <button onclick=\"go('offline')\">📶 Works offline</button>",
              "    <button onclick=\"go('offline')\">📶 Works offline</button>\n    <button onclick=\"installApp()\">📲 Install app</button>", 1)

MANIFEST = {
  "name": "Stack Bank",
  "short_name": "Stack Bank",
  "description": "A steady weekly salary from uneven gig income.",
  "start_url": "./stack-bank-premium.html",
  "scope": "./",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#070b18",
  "theme_color": "#070b18",
  "icons": [
    {"src": "./stack-bank-icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
    {"src": "./stack-bank-icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
    {"src": "./stack-bank-icons/icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
  ],
}
(DST.parent / "manifest.webmanifest").write_text(json.dumps(MANIFEST, indent=2) + "\n", encoding="utf-8")

SW_JS = r"""/* Stack Bank service worker — offline app shell (v6) */
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
"""
(DST.parent / "sw.js").write_text(SW_JS, encoding="utf-8")

V6_JS = r"""
/* ===== Stack Premium v6 — installable PWA ===== */
var _installEvt=null;
window.addEventListener('beforeinstallprompt',function(e){e.preventDefault();_installEvt=e;});
function installApp(){
  if(_installEvt){
    _installEvt.prompt();
    _installEvt.userChoice.then(function(c){if(c.outcome==='accepted')toast('Stack Bank is installing. Look for it on your home screen.');_installEvt=null;});
    return;
  }
  openModal('<h3>Install Stack Bank</h3><div class="mut">Put the app on your home screen so it opens like a real app, even with no data.</div><div class="okbox" style="font-size:15px;line-height:1.7"><b>Android (Chrome):</b> tap the three dots at the top right, then <b>Add to Home screen</b>.<br><b>iPhone (Safari):</b> tap Share, then <b>Add to Home Screen</b>.<br><br>It only works from a web link (https), not from a downloaded file — open the hosted link to install it.</div><button class="bigbtn" onclick="closeModal()">Got it</button>');
}
if('serviceWorker' in navigator){window.addEventListener('load',function(){navigator.serviceWorker.register('./sw.js').catch(function(){});});}
"""
assert "load();\n</script>" in t
t = t.replace("load();\n</script>", V6_JS + "\nload();\n</script>", 1)

DST.write_text(t, encoding="utf-8")
print(f"wrote {DST}  {DST.stat().st_size} bytes  lines={t.count(chr(10))+1}")
# quick checks
import collections
chars = collections.Counter(c for c in t if ord(c) > 0x1F000)
print("remaining high emoji in file (expected only in JS MAP strings + flags):", chars.most_common(12))
print("has sbCanvas:", "sbCanvas" in t, "| has blob1:", "blob1" in t, "| has sbIconsV4:", "sbIconsV4" in t)
print("premium css present:", "STACK BANK — PREMIUM v4" in t)
