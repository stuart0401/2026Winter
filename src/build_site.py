import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from illus import ALL, DEFS
from gen import LIGHT, DARK, FILLS, ICON

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
art_json = json.dumps({k: f() for k, f in ALL.items()}, ensure_ascii=False)
icon_json = json.dumps(dict(ICON, car='<path d="M4 15.5V12l2-5h12l2 5v3.5"></path><rect x="3" y="12" width="18" height="5" rx="1.5"></rect><circle cx="7.5" cy="18" r="1.8"></circle><circle cx="16.5" cy="18" r="1.8"></circle>', bike='<circle cx="6" cy="16" r="3.6"></circle><circle cx="18" cy="16" r="3.6"></circle><path d="M6 16l4-7h6l2 7M10 9l3 7h-7M13 6h3"></path>', tag='<path d="M5.5 8h13l-1.2 12.5H6.7z"></path><path d="M9 10.5V7a3 3 0 0 1 6 0v3.5"></path>', plane='<path d="M2.5 13.5 21 7.5c1.2-.4 1.9.9.8 1.6L6 17.5 3.5 17z"></path><path d="M11 11 8.5 5l2-.6 5 4.8M10 15.4 9 20l2 .2 3.6-6.7"></path>',
                                camera='<path d="M4 8h3l1.6-2.5h6.8L17 8h3v11H4z"></path><circle cx="12" cy="13.2" r="3.6"></circle>', share='<path d="M12 15V3.5M7.5 8 12 3.5 16.5 8"></path><path d="M5 12v8h14v-8"></path>', dl='<path d="M12 4v11M7.5 10.5 12 15l4.5-4.5"></path><path d="M5 19.5h14"></path>', shuffle='<path d="M4 7h3.5c4 0 5 10 9 10H20M17 14l3 3-3 3M4 17h3.5c1.4 0 2.4-1.2 3.3-2.8M14 9.2C14.9 7.9 15.6 7 17 7h3M17 4l3 3-3 3"></path>', trash='<path d="M5 7h14M10 7V4.5h4V7M7 7l1 12.5h8L17 7"></path>', x='<path d="M6 6l12 12M18 6 6 18"></path>', map='<path d="M9 4 3.5 6v14L9 18l6 2 5.5-2V4L15 6z"></path><path d="M9 4v14M15 6v14"></path>', ext='<path d="M14 5h5v5M19 5l-8 8"></path><path d="M17 14v5H5V7h5"></path>', walk='<circle cx="13" cy="4.5" r="1.8"></circle><path d="M10 21l2-6 3 3v3M9 12l2-4 3 1 2 3M11 8l-3 2-1 3"></path>'), ensure_ascii=False)
fills = ''.join(f'.f-{c}{{fill:var(--{c})}}' for c in FILLS)

TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>2026 東京冬令營</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Roboto:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
/* Picture-book diary: paper ground, ink-outlined plates, washi tape, hanko date seals, timeline of illustrated stops. */
:root{__LIGHT__
  --font:"Roboto","Noto Sans TC","PingFang TC","Heiti TC","Microsoft JhengHei",sans-serif;
  color-scheme:light}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){__DARK__}}
:root[data-theme="dark"]{__DARK__}
__FILLS__.f-afill{fill:var(--afill)}.f-bfill{fill:var(--bfill)}.f-pine{fill:var(--pinef)}.f-ink{fill:var(--olc)}
.ol{fill:none;stroke:var(--olc);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}.ol.thin{stroke-width:1.7}.ol.xthin{stroke-width:1.1}.ol.dash{stroke-dasharray:6 7}
.hl{fill:none;stroke:var(--hlc);stroke-width:2.6;stroke-linecap:round;opacity:.75}.sh{fill:var(--olc);opacity:.13}.hatch{stroke:var(--olc);stroke-width:1.2;opacity:.35}.groove{fill:none;stroke:var(--stone);stroke-width:1;opacity:.55}

*{box-sizing:border-box}
html{scroll-padding-block:76px 124px}
html,body{margin:0;min-height:100%}
body{background-color:var(--paper);color:var(--ink);font-family:var(--font);font-size:1rem;line-height:1.65;-webkit-font-smoothing:antialiased;
  background-image:radial-gradient(circle at 1px 1px,var(--line) 1px,transparent 0);background-size:18px 18px}
h1,h2,h3{margin:0;line-height:1.25;text-wrap:balance}
p{margin:0}
button{font:inherit;color:inherit}
.num{font-variant-numeric:tabular-nums}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:12px}
.wrap{max-width:1200px;margin:0 auto;padding:calc(20px + env(safe-area-inset-top)) 28px calc(130px + env(safe-area-inset-bottom));display:flex;flex-direction:column;gap:36px}
.view{display:none}.view.active{display:flex;flex-direction:column;gap:40px}

/* shared pieces */
.top{display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--ink)}
.brand-seal{width:38px;height:38px;border-radius:50%;background:var(--accentbg);border:2.5px solid var(--ink);color:var(--onaccent);display:grid;place-items:center;font-weight:900;font-size:17px;transform:rotate(-8deg)}
.brand b{display:block;font-weight:900;font-size:17px;letter-spacing:.04em;line-height:1.2}
.brand small{display:block;font-size:12px;color:var(--soft);letter-spacing:.14em;font-weight:500;line-height:1.2}
.btn{white-space:nowrap;display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px;min-width:44px;padding:8px 16px;border:2px solid var(--ink);background:var(--card);border-radius:999px;font-size:14px;font-weight:700;cursor:pointer;box-shadow:0 3px 0 var(--line)}
.btn svg,.ico{width:20px;height:20px;flex:none;fill:none;stroke:currentColor;stroke-width:2.1;stroke-linecap:round;stroke-linejoin:round}
.card{background:var(--card);border:2.5px solid var(--ink);border-radius:22px;box-shadow:0 5px 0 var(--line)}
.plate{background:var(--card);border:2.5px solid var(--ink);border-radius:28px;padding:12px;box-shadow:0 6px 0 var(--line)}
.pic{border:2px solid var(--ink);border-radius:16px;overflow:hidden;background:var(--sky);aspect-ratio:16/10}
.pic svg{display:block;width:100%;height:100%}
.tape{position:absolute;height:26px;opacity:.85;background-color:var(--tape);background-image:repeating-linear-gradient(90deg,rgba(255,255,255,.28) 0 6px,transparent 6px 12px);border-left:2px dashed rgba(0,0,0,.12);border-right:2px dashed rgba(0,0,0,.12);pointer-events:none;z-index:2}
.tape.pink{background-color:var(--pink)}
.seal{flex:none;border-radius:50%;background:var(--accentbg);color:var(--onaccent);border:2.5px solid var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1;box-shadow:inset 0 0 0 4px rgba(255,255,255,.22)}
.seal b{font-weight:900;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.seal i{font-style:normal;font-weight:700;letter-spacing:.08em;margin-top:3px}
.seal.pine{background:var(--pinebg)}.seal.b{background:var(--bfill)}
.tag{display:inline-flex;align-items:center;font-size:13px;font-weight:500;padding:3px 12px;border-radius:999px;background:var(--chip);color:var(--ink)}
.tag.spot{background:color-mix(in srgb,var(--pinebg) 22%,var(--card))}
.tag.opt{background:color-mix(in srgb,var(--yellow) 40%,var(--card))}
.tag.a{background:color-mix(in srgb,var(--a) 22%,var(--card))}.tag.b{background:color-mix(in srgb,var(--b) 24%,var(--card))}
.tags{display:flex;gap:6px;flex-wrap:wrap}
.sec{display:flex;flex-direction:column;gap:18px}
.sec-title{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.sec-title h2{font-size:24px;font-weight:900;letter-spacing:.04em;display:flex;align-items:center;gap:12px}
.sec-title h2::before{content:"";width:22px;height:6px;border-radius:3px;background:var(--accentbg)}
.sec-title span{font-size:14px;color:var(--soft)}
.bar{flex:1;height:12px;border:2px solid var(--ink);border-radius:999px;overflow:hidden;background:var(--paper)}
.bar i{display:block;height:100%;background:var(--pinebg)}
.progress{display:flex;align-items:center;gap:10px}
.progress b{font-size:14px;font-variant-numeric:tabular-nums}
.foot{font-size:13px;color:var(--soft)}

/* home */
.hero{display:flex;flex-wrap:wrap;gap:40px;align-items:center}
.hero-art{position:relative;flex:1 1 540px;min-width:0}
.hero-body{flex:1 1 360px;min-width:0;display:flex;flex-direction:column;gap:22px}
.hero h1 span{display:block}
.hero h1 .en{font-size:24px;font-weight:700;letter-spacing:.18em;color:var(--accent)}
.hero h1 .zh{font-size:clamp(40px,7vw,60px);font-weight:900;letter-spacing:.04em;line-height:1.15}
.hero p{font-size:17px;color:var(--soft);max-width:34em}
.count{display:flex;align-items:center;gap:18px}
.count .seal{width:104px;height:104px;transform:rotate(-8deg)}.count .seal b{font-size:40px}.count .seal i{font-size:14px}
.count div span{display:block;font-size:14px;color:var(--soft)}.count div strong{display:block;font-size:22px;font-weight:900}
.route{display:flex;align-items:center;gap:10px;padding:12px 18px;border:2px dashed var(--ink);border-radius:16px;font-weight:700;font-size:14px}
.route i{flex:1;min-width:14px;border-top:2.5px dotted var(--soft)}
.passes{display:flex;flex-wrap:wrap;gap:20px}
.pass{flex:1 1 360px;display:flex;overflow:hidden}
.pass .main{flex:1;padding:20px 22px;display:flex;flex-direction:column;gap:14px;min-width:0}
.pass .hd{display:flex;justify-content:space-between;align-items:center;gap:8px}
.pass .no{font-weight:900;font-size:20px;letter-spacing:.06em}
.pass .rt{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:14px}
.pass .t{font-size:clamp(26px,4vw,34px);font-weight:700;line-height:1;font-variant-numeric:tabular-nums}
.pass .ap{font-size:13px;color:var(--soft);margin-top:6px}
.pass .ln{position:relative;border-top:2.5px dashed var(--soft)}
.pass .ln svg{position:absolute;left:50%;top:-14px;transform:translateX(-50%);width:28px;height:28px;padding:2px;background:var(--card);fill:var(--accentbg);stroke:var(--ink);stroke-width:1.4;stroke-linejoin:round}
.pass .cut{border-left:2.5px dashed var(--line);margin:14px 0}
.pass .stub{width:104px;flex:none;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:16px 8px;background:var(--chip)}
.pass .stub span{font-size:12px;font-weight:700;letter-spacing:.12em;color:var(--soft)}
.pass .stub b{font-size:28px;font-weight:900;line-height:1;font-variant-numeric:tabular-nums}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:16px}
.tile{position:relative;display:flex;flex-direction:column;gap:10px;padding:16px;text-align:left;cursor:pointer;color:var(--ink)}
@media (hover:hover) and (pointer:fine) and (prefers-reduced-motion:no-preference){.tile{transition:transform 150ms cubic-bezier(0.23,1,0.32,1)}.tile:hover{transform:translateY(-3px)}}
.tile .row{display:flex;align-items:center;justify-content:space-between}
.tile .seal{width:56px;height:56px}.tile .seal b{font-size:21px}.tile .seal i{font-size:10px}
.tile .wd{font-size:13px;font-weight:700;color:var(--soft)}
.tile strong{display:block;font-weight:900;font-size:17px;line-height:1.35}
.tile small{display:block;font-size:13px;color:var(--soft);line-height:1.45}
.quick{display:flex;flex-wrap:wrap;gap:16px}
.q{flex:1 1 250px;display:flex;flex-direction:column;gap:12px;padding:18px 20px;text-decoration:none;color:var(--ink)}
.q .hd{display:flex;align-items:center;gap:10px}
.q .ib{width:40px;height:40px;border-radius:12px;background:var(--chip);display:grid;place-items:center}
.q strong{display:block;font-weight:900;font-size:16px;line-height:1.3}.q small{display:block;font-size:13px;color:var(--soft)}
.stays{display:flex;flex-wrap:wrap;gap:20px}
.stay{flex:1 1 360px;display:flex;gap:16px;align-items:center;padding:12px}
.stay .pic{width:150px;flex:none;border-radius:14px}
.stay strong{display:block;font-weight:900;font-size:17px;line-height:1.4}.stay span{display:block;font-size:14px}.stay small{display:block;font-size:13px;color:var(--soft)}

/* trip */
.chips{position:sticky;top:0;z-index:6;display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin:-8px -28px 0;padding:10px 28px;background:color-mix(in srgb,var(--paper) 90%,transparent);backdrop-filter:blur(6px)}
.chips::-webkit-scrollbar{display:none}
.chip{flex:none;min-height:44px;padding:8px 18px;border:2px solid var(--ink);border-radius:999px;font-weight:900;font-size:14px;background:var(--card);cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.chip small{font-weight:500;opacity:.8}
.chip[aria-pressed="true"]{background:var(--accentbg);color:var(--onaccent)}
.chip.today{background:var(--pinebg);color:var(--onaccent)}
.dayhead{display:flex;flex-wrap:wrap;gap:36px;align-items:center}
.dayhead .art{position:relative;flex:1 1 500px;min-width:0}
.dayhead .art .pic{aspect-ratio:16/9}
.dayhead .info{flex:1 1 340px;min-width:0;display:flex;flex-direction:column;gap:16px}
.dayhead .ttl{display:flex;align-items:center;gap:16px}
.dayhead .seal{width:84px;height:84px;transform:rotate(-6deg)}.dayhead .seal b{font-size:32px}.dayhead .seal i{font-size:13px}
.dayhead .eyebrow{display:block;font-size:15px;font-weight:700;color:var(--accent);letter-spacing:.1em}
.dayhead h1{font-size:clamp(32px,5vw,46px);font-weight:900;letter-spacing:.04em}
.stats{display:flex;gap:12px}
.stats div{flex:1;padding:12px 14px;border:2px solid var(--ink);border-radius:16px;background:var(--card)}
.stats b{display:block;font-size:26px;font-weight:900;line-height:1.1;font-variant-numeric:tabular-nums}
.stats span{font-size:13px;color:var(--soft)}
.memo{position:relative;max-width:760px;padding:18px 22px 16px;background:color-mix(in srgb,var(--yellow) 30%,var(--card));border:2px solid var(--ink);border-radius:6px 22px 22px 22px;transform:rotate(-.5deg);font-size:15.5px;line-height:1.7}
.memo b{color:var(--accent)}
.daymain{display:flex;flex-wrap:wrap;gap:32px;align-items:flex-start}
.timeline{flex:999 1 560px;min-width:0;display:flex;flex-direction:column;gap:22px}
.flow .groups{flex:none}
.split{display:flex;flex-direction:column;gap:18px;padding:18px 0 4px;border-top:2px dashed var(--line)}
.flow-hd{display:flex;align-items:center;gap:8px;font-size:17px;font-weight:900}
.flow-hd .ico,.flow-hd svg{width:20px;height:20px;flex:none}
.side{flex:1 1 290px;min-width:0;display:flex;flex-direction:column;gap:18px}
.side .card{padding:18px 20px;display:flex;flex-direction:column;gap:10px}
.side h2{font-size:18px;font-weight:900;display:flex;align-items:center;gap:8px}
.side .pic{border-radius:14px}
.sh-row{display:flex;flex-direction:column;gap:6px}
.sh-lb{font-size:13px;font-weight:700;color:var(--soft)}
.sh-times{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.sh-times span{text-align:center;font-weight:700;font-size:15px;padding:4px 0;border:2px solid var(--ink);border-radius:10px;background:var(--paper)}
.sh-times span.past{opacity:.38;text-decoration:line-through}
.sh-times span.next{background:var(--accentbg);color:var(--onaccent)}
.mv.shx{flex-direction:column;align-items:stretch;padding:0;gap:0}
.shx-head{display:flex;align-items:center;gap:14px;width:100%;padding:11px 16px;min-height:60px;border:0;background:transparent;text-align:left;cursor:pointer;border-radius:16px}
.shx-head>div{flex:1;min-width:0}
.shx-head .nx{display:inline-block;margin-top:4px;padding:1px 10px;border-radius:999px;background:var(--accentbg);color:var(--onaccent);font-size:13px;font-weight:700}
.shx-head .chev{width:22px;height:22px;flex:none;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;transition:transform 200ms cubic-bezier(.23,1,.32,1)}
.shx[data-open="true"] .chev{transform:rotate(180deg)}
.shx-body{display:grid;grid-template-rows:0fr;transition:grid-template-rows 220ms cubic-bezier(.23,1,.32,1)}
.shx[data-open="true"] .shx-body{grid-template-rows:1fr}
.shx-body>div{overflow:hidden}
.shx-body .in{padding:0 16px 14px;display:flex;flex-direction:column;gap:10px}
/* photos */
.album{display:flex;flex-wrap:wrap;align-items:center;gap:16px;padding:18px 20px}
.album .tx{flex:1 1 240px;display:flex;flex-direction:column;gap:4px}
.album h2{font-size:20px;font-weight:900;display:flex;align-items:center;gap:8px}
.album p{font-size:14px;color:var(--soft)}
.btn.primary{background:var(--accentbg);color:var(--onaccent)}
.btn[disabled]{opacity:.45;cursor:not-allowed}
.go-map{display:inline-flex;align-items:center;gap:6px;min-width:0;line-height:1.3;word-break:keep-all;padding-block:6px;min-height:44px;margin-top:10px;padding:0 14px 0 12px;border:2px solid currentColor;border-radius:999px;font-size:13.5px;font-weight:700;color:var(--accent);text-decoration:none;-webkit-tap-highlight-color:transparent}
.go-map .ico{width:17px;height:17px;flex:none}
.lk-row{display:flex;flex-wrap:wrap;gap:0 10px}
.extra{margin-top:14px;padding-top:12px;border-top:2px dashed var(--soft)}
.extra-hd{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.extra-hd strong{font-size:16px;font-weight:800}
.extra p{margin-top:6px}
.go-map{max-width:100%}
@media (max-width:520px){div.alt-op>span.ib{display:none}}
div.mv.alt{gap:10px}
.alt-hd{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.alt-hd strong{font-size:16px;font-weight:800}
.alt-pill{padding:1px 10px;border-radius:999px;background:var(--accentbg);color:var(--onaccent);font-size:12.5px;font-weight:700}
.alt-lead{display:block;font-size:14px;color:var(--soft);line-height:1.5}
.alt-op{display:flex;align-items:flex-start;gap:10px;padding:10px 0 2px;border-top:1.5px dotted var(--soft)}
.alt-op>div{flex:1;min-width:0}
.alt-op strong{display:block;font-weight:700;font-size:15.5px;line-height:1.4}
.alt-op small{display:block;font-size:14px;color:var(--soft);line-height:1.5}
.alt-tag{flex:none;display:grid;place-items:center;width:26px;height:26px;margin-top:7px;border-radius:50%;background:var(--ink);color:var(--card);font-weight:900;font-size:13px}
.go-map.solo{margin-top:0;align-self:flex-start}
@media (hover:hover){.go-map:hover{background:var(--accent);color:var(--card)}}
.go-map:active{background:var(--accent);color:var(--card)}
div.mv:not(.shx){flex-direction:column;align-items:stretch}
.mv-row{display:flex;align-items:flex-start;gap:14px}
.mv-row>div{flex:1;min-width:0}
.near{margin-top:12px;border-top:2px dashed var(--soft);grid-column:1/-1;width:100%}
.card.stop>.near{flex-basis:100%}
.near-hd{display:flex;align-items:center;gap:10px;width:100%;min-height:52px;padding:8px 2px 4px;border:0;background:transparent;color:inherit;font:inherit;text-align:left;cursor:pointer;-webkit-tap-highlight-color:transparent}
.near-hd>.ico{width:22px;height:22px;flex:none;color:var(--accent)}
.near-hd>span{flex:1;min-width:0;font-weight:800;font-size:15px}
.near-hd small{display:block;font-weight:500;font-size:12.5px;color:var(--soft)}
.near-hd .chev{width:22px;height:22px;flex:none;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;transition:transform 200ms cubic-bezier(.23,1,.32,1)}
.near[data-open="true"] .chev{transform:rotate(180deg)}
.near-body{display:grid;grid-template-rows:0fr;transition:grid-template-rows 220ms cubic-bezier(.23,1,.32,1)}
.near[data-open="true"] .near-body{grid-template-rows:1fr}
.near-body>div{overflow:hidden}
.near ul{list-style:none;margin:4px 0 0;padding:0;display:flex;flex-direction:column}
.near li{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1.5px dotted var(--soft)}
.near li:last-child{border-bottom:0}
.nr-tx{flex:1;min-width:0}
.nr-tx strong{display:block;font-size:14.5px;line-height:1.4;overflow-wrap:anywhere}
.nr-tx span{display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:13px;color:var(--soft);font-variant-numeric:tabular-nums}
.nr-k{padding:0 8px;border-radius:999px;font-size:12px;font-weight:700;background:var(--pinebg);color:var(--onaccent)}
.nr-k[data-k="超市"],.nr-k[data-k="唐吉訶德"]{background:var(--accentbg)}.nr-k[data-k="MUJI"],.nr-k[data-k="3COINS"]{background:var(--bfill)}
.nr-map{display:inline-flex;align-items:center;justify-content:center;gap:4px;flex:none;min-width:64px;min-height:44px;padding:0 10px;border:2px solid currentColor;border-radius:999px;font-size:13px;font-weight:700;color:var(--accent);text-decoration:none}
.nr-map .ico{width:16px;height:16px}
@media (hover:hover){.nr-map:hover{background:var(--accent);color:var(--card)}}
.near .foot{margin:6px 0 2px;font-size:12.5px}
.sp-top{display:flex;align-items:center;gap:8px}.sp-top .ck{flex:1;min-width:0}
.map-btn{flex:none;display:inline-flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;min-width:52px;min-height:48px;border:2px solid var(--ink);border-radius:12px;color:var(--ink);text-decoration:none;font-size:11.5px;font-weight:700;background:var(--paper)}
.map-btn .ico{width:20px;height:20px}
.sp{display:flex;flex-direction:column;gap:8px;background:var(--card);border:2px solid var(--ink);border-radius:18px;padding:8px 14px 12px;box-shadow:0 3px 0 var(--line)}
.checks .sp .ck{padding:0;background:transparent;border:0;box-shadow:none}
.ph-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding-left:38px}
.ph{position:relative;width:56px;height:56px;border:2px solid var(--ink);border-radius:10px;overflow:hidden;padding:0;cursor:pointer;background:var(--chip)}
.ph img{display:block;width:100%;height:100%;object-fit:cover}
.ph.more{display:grid;place-items:center;font-weight:900;font-size:14px}
.ph-add{display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:6px 12px;border:2px dashed var(--ink);border-radius:12px;font-size:13px;font-weight:700;cursor:pointer;color:var(--ink)}
.ph-add .ico{width:18px;height:18px}
.ph-input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
.ph-input:focus-visible+.ph-add{outline:3px solid var(--accent);outline-offset:2px}
.modal{position:fixed;inset:0;z-index:40;display:flex;align-items:flex-end;justify-content:center;visibility:hidden;transition:visibility 0s linear 300ms}
.modal[data-open="true"]{visibility:visible;transition:none}
.modal-bg{position:absolute;inset:0;border:0;width:100%;background:rgba(10,10,20,.5);opacity:0;transition:opacity 200ms ease-out;cursor:pointer}
.modal[data-open="true"] .modal-bg{opacity:1}
.modal-box{position:relative;width:100%;max-width:560px;max-height:92%;overflow:auto;background:var(--paper);border:2.5px solid var(--ink);border-bottom:0;border-radius:26px 26px 0 0;padding:16px 18px calc(22px + env(safe-area-inset-bottom));display:flex;flex-direction:column;gap:14px;transform:translateY(100%);transition:transform 300ms cubic-bezier(.32,.72,0,1)}
.modal[data-open="true"] .modal-box{transform:translateY(0)}
@media (min-width:860px){.modal{align-items:center}.modal-box{border-bottom:2.5px solid var(--ink);border-radius:26px;transform:translateY(24px);opacity:0;transition:transform 260ms cubic-bezier(.23,1,.32,1),opacity 200ms ease-out}.modal[data-open="true"] .modal-box{transform:none;opacity:1}}
.modal-hd{display:flex;align-items:center;justify-content:space-between;gap:12px}
.modal-hd h2{font-size:20px;font-weight:900}
.share-prev{border:2px solid var(--ink);border-radius:16px;overflow:hidden;background:var(--chip);display:grid;place-items:center;min-height:200px}
.share-prev img{display:block;width:100%;height:auto}
.share-prev .wait{padding:40px;color:var(--soft);font-size:14px}
.fmt{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));padding:4px;border:2px solid var(--ink);border-radius:999px;background:var(--card)}
.fmt button{min-height:40px;border:0;border-radius:999px;background:transparent;color:var(--soft);font-weight:700;cursor:pointer}
.fmt button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.acts{display:flex;flex-wrap:wrap;gap:10px}
.acts .btn{flex:1 1 140px}
.lb-img{border:2px solid var(--ink);border-radius:16px;overflow:hidden;background:var(--chip)}
.lb-img img{display:block;width:100%;max-height:60vh;object-fit:contain}
@media (prefers-reduced-motion: reduce){.shx-body,.near-body,.chev,.modal-box,.modal-bg{transition:none!important}}
.tl{display:grid;grid-template-columns:84px 24px minmax(0,1fr);column-gap:14px;align-items:start}
.tl .tm{text-align:right;padding-top:10px;font-weight:700;font-size:15px;line-height:1.3;font-variant-numeric:tabular-nums}
.tl .rail{position:relative;align-self:stretch}
.tl .rail::before{content:"";position:absolute;left:3px;top:12px;width:18px;height:18px;border-radius:50%;background:var(--dot,var(--accentbg));border:2.5px solid var(--ink);box-sizing:border-box;z-index:1}
.tl .rail::after{content:"";position:absolute;left:11px;top:30px;bottom:-22px;border-left:2.5px dotted var(--soft)}
.tl:last-child .rail::after{display:none}
.tl.move{--dot:var(--chip)}.tl.opt{--dot:var(--yellow)}.tl.ga{--dot:var(--a)}.tl.gb{--dot:var(--b)}
.stop{display:flex;flex-wrap:wrap;gap:18px;align-items:center;padding:12px}
.stop.dashed{border-style:dashed}
.stop .pic{flex:1 1 210px;max-width:250px;border-radius:14px}
.stop .tx{flex:999 1 220px;min-width:0;display:flex;flex-direction:column;gap:6px;padding:4px 8px 4px 0}
.stop h3{font-size:19px;font-weight:900;line-height:1.35}
.stop p{font-size:15px;color:var(--soft);max-width:36em}
.mv{display:flex;align-items:center;gap:14px;padding:11px 16px;border:2px dashed var(--soft);border-radius:18px;background:color-mix(in srgb,var(--card) 55%,transparent)}
.mv .ib{width:40px;height:40px;flex:none;border-radius:50%;background:var(--chip);display:grid;place-items:center}
.mv strong{display:block;font-weight:700;font-size:16px;line-height:1.4}.mv small{display:block;font-size:14px;color:var(--soft);line-height:1.5}
.seg{display:none;grid-template-columns:repeat(2,minmax(0,1fr));padding:4px;border:2px solid var(--ink);border-radius:999px;background:var(--card)}
.seg button{min-height:42px;border:0;border-radius:999px;background:transparent;color:var(--soft);font-weight:700;font-size:15px;cursor:pointer}
.seg button[aria-pressed="true"]{color:var(--onaccent);font-weight:900}
.seg button[data-g="A"][aria-pressed="true"]{background:var(--afill)}.seg button[data-g="B"][aria-pressed="true"]{background:var(--bfill)}
.groups{flex:999 1 560px;min-width:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
.gcol{display:flex;flex-direction:column;gap:18px;min-width:0}
.gcol h2{display:flex;align-items:center;gap:10px;font-size:19px;font-weight:900}
.gcol h2 .seal{width:38px;height:38px}.gcol h2 .seal b{font-size:16px}
.gbadge{flex:none;width:46px;height:46px;border-radius:50%;border:2.5px solid var(--ink);display:grid;place-items:center;background:var(--afill)}
.gbadge[data-g="B"]{background:var(--bfill)}
.gbadge .gico{width:32px;height:32px}
.gbadge[data-g="A"]{background:var(--sky)}
.gcol h2 .gname{display:block;font-size:13px;font-weight:800;letter-spacing:.06em;color:var(--soft)}
.seg button{display:inline-flex;align-items:center;justify-content:center;gap:8px}
.seg .gico{width:26px;height:26px;flex:none}
.seg .sg-t{display:flex;flex-direction:column;align-items:flex-start;line-height:1.25;text-align:left}
.seg .sg-t small{font-size:12px;font-weight:600;opacity:.85}
.seg button{padding:6px 10px}
.gcol .stop{border-top-width:7px}
.gcol[data-g="A"] .stop{border-top-color:var(--a)}.gcol[data-g="B"] .stop{border-top-color:var(--b)}
.gcol .stop .pic{max-width:none;flex-basis:100%}
.gcol .tl{grid-template-columns:62px 24px minmax(0,1fr);column-gap:10px}
.gnote{font-size:14px;color:var(--soft)}
.ck{display:flex;align-items:center;gap:12px;min-height:44px;cursor:pointer;position:relative}
.ck input{position:absolute;opacity:0;width:1px;height:1px}
.ck .box{width:26px;height:26px;flex:none;border:2.5px solid var(--ink);border-radius:8px;display:grid;place-items:center;background:var(--paper)}
.ck .box svg{width:16px;height:16px;fill:none;stroke:var(--onaccent);stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;opacity:0}
.ck input:checked+.box{background:var(--pinebg)}.ck input:checked+.box svg{opacity:1}
.ck input:focus-visible+.box{outline:3px solid var(--accent);outline-offset:2px}
.ck .lb{font-size:15px;font-weight:500;line-height:1.4;min-width:0;overflow-wrap:anywhere}
.ck input:checked~.lb{text-decoration:line-through;text-decoration-thickness:2px;color:var(--soft)}
.ck .lb small{display:block;font-size:13px;color:var(--soft);text-decoration:none}

/* list pages */
.lhero{position:relative;display:flex;flex-wrap:wrap;gap:24px;align-items:center;padding:12px}
.lhero .pic{flex:0 1 300px;border-radius:16px}
.lhero .tx{flex:1 1 300px;display:flex;flex-direction:column;gap:10px;padding:8px 12px}
.lhero h1{font-size:clamp(28px,4.5vw,38px);font-weight:900;letter-spacing:.04em}
.lhero p{color:var(--soft)}
.lhero .progress{max-width:420px}
.checks{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.checks.one{grid-template-columns:1fr}
.cat-hint{font-size:13.5px;color:var(--soft);padding-top:10px}
.ck .lb .tag{margin-right:4px;vertical-align:1px}
.ck-row{display:flex;align-items:center;gap:6px}
.ck-row .ck{flex:1;min-width:0}
.ck-del{flex:none;width:44px;height:44px;display:grid;place-items:center;border:0;border-radius:12px;background:transparent;color:var(--soft);cursor:pointer}
.ck-del .ico{width:18px;height:18px}
.ck-del.confirm{width:auto;padding:0 12px;gap:4px;display:inline-flex;align-items:center;border:2px solid var(--accent);border-radius:999px;color:var(--accent);font-size:13px;font-weight:700;white-space:nowrap}
@media (hover:hover){.ck-del:hover{background:var(--chip);color:var(--accent)}}
.restore-row{margin-top:12px}
.add-item{display:flex;gap:8px;margin-top:14px}
.add-item input{flex:1;min-width:0;min-height:44px;padding:0 14px;border:2px solid var(--ink);border-radius:12px;background:var(--paper);color:var(--ink);font:inherit;font-size:16px}
.add-item input::placeholder{color:var(--soft)}
.add-item .btn{flex:none}
.add-msg{min-height:1.4em;margin-top:6px;font-size:13.5px;font-weight:700;color:var(--accent)}
.add-item input[aria-invalid="true"]{border-color:var(--accent)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.tips-card{margin-top:22px;padding:18px 20px;border-color:var(--accent)}
.tips-card h2{display:flex;align-items:center;gap:8px;font-size:18px;font-weight:900}
.lug{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:12px 0 6px}
.lug>div{padding:12px 14px;border:2px dashed var(--line);border-radius:14px;background:var(--paper)}
.lug b{display:block;font-size:15px;font-weight:900}
.lug span{display:block;font-size:14.5px;margin-top:4px}
.checks .ck{background:var(--card);border:2px solid var(--ink);border-radius:16px;padding:8px 14px;box-shadow:0 3px 0 var(--line)}
.checks .ck .th{width:64px;flex:none;border-width:2px;border-radius:10px}
.cats-tools{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.cats-tools span{font-size:14px;color:var(--soft)}
.cats{display:flex;flex-direction:column;gap:12px}
.cat{background:var(--card);border:2.5px solid var(--ink);border-radius:20px;box-shadow:0 4px 0 var(--line);overflow:hidden}
.cat-hd{display:grid;grid-template-columns:auto minmax(0,1fr) auto auto;align-items:center;gap:12px;width:100%;min-height:64px;padding:12px 16px;border:0;background:transparent;text-align:left;cursor:pointer;color:var(--ink)}
.cat-hd .n{width:32px;height:32px;border-radius:50%;background:var(--accentbg);color:var(--onaccent);border:2px solid var(--ink);display:grid;place-items:center;font-size:14px;font-weight:900}
.cat.done .cat-hd .n{background:var(--pinebg)}
.cat-hd .nm{display:flex;flex-direction:column;gap:6px;min-width:0}
.cat-hd .nm strong{font-size:17px;font-weight:900;line-height:1.3;overflow-wrap:anywhere}
.cat-hd .mini{height:8px;border:1.5px solid var(--ink);border-radius:999px;background:var(--paper);overflow:hidden;max-width:260px}
.cat-hd .mini i{display:block;height:100%;background:var(--pinebg)}
.cat-hd .c{min-width:64px;text-align:center;font-size:13px;font-weight:700;color:var(--soft);background:var(--chip);padding:3px 10px;border-radius:999px;font-variant-numeric:tabular-nums;white-space:nowrap}
.cat.done .cat-hd .c{background:var(--pinebg);color:var(--onaccent)}
.cat-hd .chev{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;transition:transform 200ms cubic-bezier(.23,1,.32,1)}
.cat[data-open="true"] .cat-hd .chev{transform:rotate(180deg)}
.cat-body{display:grid;grid-template-rows:0fr;transition:grid-template-rows 220ms cubic-bezier(.23,1,.32,1)}
.cat[data-open="true"] .cat-body{grid-template-rows:1fr}
.cat-body>div{overflow:hidden}
.cat-body .in{padding:4px 14px 16px;border-top:2px dashed var(--line)}
.cat-body .in .checks{padding-top:12px}
.cat .checks{grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}
@media (prefers-reduced-motion: reduce){.cat-body,.cat-hd .chev{transition:none!important}}
.reset.danger{border-color:var(--accent);color:var(--accent);font-weight:700}
.reset{align-self:flex-start;border:2px solid var(--soft);background:transparent;border-radius:999px;padding:8px 16px;min-height:44px;cursor:pointer;font-size:13px;color:var(--soft)}

/* nav */
.nav{position:fixed;left:0;right:0;bottom:0;z-index:20;padding:0 12px calc(12px + env(safe-area-inset-bottom));pointer-events:none}
.nav-in{pointer-events:auto;max-width:640px;margin:0 auto;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px;padding:6px;background:var(--card);border:2.5px solid var(--ink);border-radius:28px;box-shadow:0 5px 0 var(--line),0 14px 34px rgba(20,16,12,.18)}
.nav a{display:flex;flex-direction:column;align-items:center;gap:2px;padding:7px 2px;min-height:44px;border-radius:20px;text-decoration:none;font-size:12px;font-weight:700;white-space:nowrap;color:var(--soft)}
.nav a .ico{width:22px;height:22px}
.nav a[aria-current="page"]{background:var(--accentbg);color:var(--onaccent);box-shadow:inset 0 0 0 2px var(--ink)}

@media (max-width:859px){
  .side .shuttle{display:none}
  .wrap{padding-left:16px;padding-right:16px;gap:28px}
  .chips{margin:-8px -16px 0;padding:10px 16px}
  .seg{display:grid}
  .groups{grid-template-columns:1fr}
  .groups[data-show="A"] .gcol[data-g="B"],.groups[data-show="B"] .gcol[data-g="A"]{display:none}
  .gcol>h2{display:none}
  .tl{grid-template-columns:52px 22px minmax(0,1fr);column-gap:10px}
  .gcol .tl{grid-template-columns:52px 22px minmax(0,1fr)}
  .stop .pic{max-width:none;flex-basis:100%}
  .dayhead{gap:20px}.hero{gap:24px}
  .brand small{display:none}
}
@media (max-width:420px){
  .cat-hd{grid-template-columns:auto minmax(0,1fr) auto;row-gap:6px}
  .cat-hd .n{grid-row:1 / span 2}
  .cat-hd .nm{grid-column:2;grid-row:1}
  .cat-hd .c{grid-column:2;grid-row:2;justify-self:start}
  .cat-hd .chev{grid-column:3;grid-row:1 / span 2}
}
@media (max-width:600px){
  .lhero{flex-wrap:nowrap;gap:14px;align-items:center;padding:10px}
  .lhero .pic{flex:0 0 104px;aspect-ratio:1/1;border-radius:14px}
  .lhero .tx{flex:1 1 auto;min-width:0;padding:2px 4px;gap:6px}
  .lhero h1{font-size:24px}
  .lhero p{font-size:13.5px;line-height:1.5}
}
@media (max-width:380px){
  .brand b{font-size:15px}.brand-seal{width:34px;height:34px;font-size:15px}
  #themeBtn{padding:8px}
  #themeLabel{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
}
@media (max-width:420px){
  .nav a{font-size:11px}.nav-in{padding:5px;gap:2px}
  .stats div{padding:10px}.stats b{font-size:22px}
  .pass .stub{width:84px}
  .stay .pic{width:110px}
}
@media (prefers-reduced-motion: reduce){*{transition:none!important}}
</style>
</head>
<body>
__DEFS__
<div class="wrap">
  <header class="top">
    <a class="brand" href="#home"><span class="brand-seal" aria-hidden="true">冬</span><span><b>2026 東京冬令營</b><small>TOKYO · KARUIZAWA</small></span></a>
    <button class="btn" id="themeBtn" type="button"><svg viewBox="0 0 24 24" aria-hidden="true" id="themeIco"></svg><span id="themeLabel">深色模式</span></button>
  </header>
  <main>
    <section class="view" id="view-home" aria-label="首頁"></section>
    <section class="view" id="view-trip" aria-label="行程"></section>
    <section class="view" id="view-spots" aria-label="行程確認清單"></section>
    <section class="view" id="view-prep" aria-label="待議及待辦"></section>
    <section class="view" id="view-pack" aria-label="打包清單"></section>
  </main>
</div>
<div class="modal" id="modal" data-open="false"><button type="button" class="modal-bg" data-close="1" aria-label="關閉" tabindex="-1"></button><div class="modal-box" id="modal-box" role="dialog" aria-modal="true" aria-labelledby="modal-title"></div></div>
<nav class="nav" aria-label="主選單"><div class="nav-in" id="nav"></div></nav>

<script>
(function(){
"use strict";
const ART = __ART__;
const ICON = __ICON__;
const store = {
  get(k,d){ try{ const v=localStorage.getItem("twc26:"+k); return v===null?d:JSON.parse(v);}catch(e){ return d; } },
  set(k,v){ try{ localStorage.setItem("twc26:"+k, JSON.stringify(v)); }catch(e){} }
};
const esc = s => String(s).replace(/[&<>"]/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const ico = (n, cls) => `<svg class="ico${cls?" "+cls:""}" viewBox="0 0 24 24" aria-hidden="true">${ICON[n]||""}</svg>`;
const pic = (k, extra) => `<div class="pic${extra?" "+extra:""}">${ART[k]||""}</div>`;
const seal = (top, bottom, cls) => `<div class="seal ${cls||""}"><b>${top}</b><i>${bottom}</i></div>`;
const tape = (style, cls) => `<span class="tape ${cls||""}" style="${style}" aria-hidden="true"></span>`;
const GNAME = {A:"大邱組", B:"三口組"};
const GICON = {
  A:`<svg viewBox="0 0 24 24" aria-hidden="true" class="gico"><path d="M3.2 13.6c-.9-3.6.6-8.4 4.4-9.4 2.6-.7 4.4.6 5.2 2.3l1.2 2.7c.5 1.1 1.7 1.4 2.6.8l1.4-.9c1.2-.8 2.9.4 2.3 1.8l-2.6 6.2c-1 2.4-3.4 4-6.2 3.8-4-.3-7.4-3.3-8.3-7.3z" fill="#C98A4B" stroke="#2B2420" stroke-width="1.4" stroke-linejoin="round"/><path d="M6 8.4c.8-1 1.6-1.4 2.6-1.5M5.4 11.2c1-.9 2.3-1.3 3.6-1.1" fill="none" stroke="#2B2420" stroke-width="1.1" stroke-linecap="round"/><circle cx="13.2" cy="14.6" r="4.4" fill="#FFFDF7" stroke="#2B2420" stroke-width="1.4"/><path d="M10.4 12.2c1 1.4 1 3.4 0 4.8M16 12.2c-1 1.4-1 3.4 0 4.8" fill="none" stroke="#D45F3A" stroke-width="1.1" stroke-linecap="round"/></svg>`,
  B:`<svg viewBox="0 0 24 24" aria-hidden="true" class="gico"><g fill="#FFFDF7" stroke="#2B2420" stroke-width="1.4"><circle cx="5.2" cy="10.4" r="2.8"/><path d="M1 21.2c0-3.4 1.9-5.4 4.2-5.4s4.2 2 4.2 5.4z"/><circle cx="18.8" cy="10.4" r="2.8"/><path d="M14.6 21.2c0-3.4 1.9-5.4 4.2-5.4s4.2 2 4.2 5.4z"/><circle cx="12" cy="7.4" r="3.2"/><path d="M7 21.2c0-4.2 2.2-7.2 5-7.2s5 3 5 7.2z"/></g></svg>`
};
const gBadge = g => `<span class="gbadge" data-g="${g}">${GICON[g]}</span>`;
const tagH = (t, k) => `<span class="tag ${k||""}">${esc(t)}</span>`;
const CHECK = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>`;

/* ---------- data ---------- */
/* card item: {t,title,note,art,spot,opt,group}; move item: {t,title,note,m:<icon>} */
const DAYS = [
  {id:"d1", date:"13", wd:"日", title:"抵達日", sub:"抵達成田 → 銀座；大邱組先辦 JTTP 二次審查", art:"d_arrive", seal:"", stay:"TOSEI酒店 可可尼築地銀座", stayArt:"ginza", stayNote:"12/13、12/15–12/18 住宿",
   pre:[
    {t:"09:15", title:"JX314 台中起飛", note:"星宇冬季班表，請以電子機票為準", m:"plane"},
    {t:"13:25", title:"抵達成田第 2 航廈", note:"入境、領行李約 1 小時", m:"plane"}
   ],
   groups:{
    A:{name:"JTTP 二次審查 → 京成 Access", items:[
      {t:"14:30", title:"JTTP 二次審查", note:"入境、領行李後在成田機場辦理，暫估需時約 1 小時。", art:"immigration"},
      {t:"15:52", title:"京成 Access 特急 → 東銀座", note:"直通淺草線免轉車。Google 地圖查 12/13（日）班次：15:52 發車、17:16 到東銀座，東銀座站步行到飯店約 10 分鐘。出發前再查一次。", m:"train"},
      {t:"17:30", title:"TOSEI酒店 check-in", note:"可可尼築地銀座，之後 12/15–12/18 也住這裡。", art:"ginza"}
    ]},
    B:{name:"直接到飯店", items:[
      {t:"14:40", alt:true, title:"機場 → 飯店", opts:[
        {tag:"A", m:"train", title:"京成 Access 特急 → 東銀座，步行到飯店", note:"直通淺草線免轉車，約 1.5 小時；東銀座站步行到飯店約 10 分鐘。出發前查班次。", q:"東銀座駅", ql:"東銀座站"},
        {tag:"B", m:"car", title:"機場接送（專車）直達飯店", note:"Google 地圖模擬 12/13（日）14:40 出發：車程約 50 分–1 小時 15 分，約 16:00 前後抵達。行李多、人多時最省力；請提前預約。", dir:"https://www.google.com/maps/dir/%E6%88%90%E7%94%B0%E5%9B%BD%E9%9A%9B%E7%A9%BA%E6%B8%AF+%E7%AC%AC2%E3%82%BF%E3%83%BC%E3%83%9F%E3%83%8A%E3%83%AB/35.6639906,139.7716542/data=!4m6!4m5!2m3!6e0!7e2!8j1797172800!3e0", ql:"機場到飯店的車程"}]},
      {t:"16:30", title:"TOSEI酒店 check-in", note:"可可尼築地銀座，之後 12/15–12/18 也住這裡。搭接送的話會早一點到。", art:"ginza"}
    ]}
   },
   post:[
    {t:"18:00", title:"散步、晚餐", note:"兩組在飯店會合，一起在銀座一帶散步、吃晚餐。", art:"dinnerwalk"},
    {t:"晚上", title:"銀座 伊東屋 本店", note:"週日 10:00–20:00（營業時間暫供參考）", art:"stationery", opt:"選配"}
   ]},
  {id:"d2", date:"14", wd:"一", title:"輕井澤", sub:"英迪格 check-in、星野區的夜晚", art:"d_hoshino", seal:"pine", stay:"輕井澤英迪格酒店", stayArt:"firepit", stayNote:"check-in 15:00・check-out 11:00・接駁車免預約",
   memo:"<b>行李：</b>12/15 會回同一家飯店，大件行李請寄放 TOSEI，只帶一晚的隨身行李去輕井澤（請先向飯店確認寄放服務）。",
   tips:["星野區晚上計程車少，回程請先請店家或飯店幫忙叫車。","燭光夜在戶外，晚上可能到零度以下，請穿暖。","星野區巴士班次少，來回都建議搭計程車。"], shuttle:true,
   items:[
    {t:"上午", title:"東京自由活動、整理行李", note:"大件行李寄放 TOSEI，只帶一晚的隨身行李。", m:"bag"},
    {t:"12:30", title:"東京車站", note:"在丸之內紅磚站舍拍照，買鐵路便當當午餐。", art:"tokyostation", spot:true},
    {t:"13:20", title:"北陸新幹線 → 輕井澤", note:"約 1 小時 10 分，14:30 前後抵達。建議先劃位，出發前查班次。", m:"train"},
    {t:"14:50", sh:"to", title:"英迪格酒店接駁車 → 酒店", note:"輕井澤站南口上車（暢貨中心旁、樓梯下計程車站附近），約 5 分鐘，免預約。14:50 是第一班。", m:"bus"},
    {t:"15:00", title:"輕井澤英迪格酒店", note:"check-in、放行李。可以泡大浴場、到焚火庭園烤火。", art:"firepit", spot:true},
    {t:"15:30", title:"計程車 → 榆樹街小鎮", note:"約 10 分鐘（6.6 公里），可請飯店櫃台叫車。", m:"taxi"},
    {t:"15:45", title:"榆樹街小鎮（Harunire Terrace）", note:"12 月有聖誕燈飾。逛街、喝咖啡。", art:"harunire"},
    {t:"17:30", title:"榆樹街小鎮晚餐", note:"在榆樹街小鎮一帶吃晚餐。", m:"bowl"},
    {t:"19:30", title:"輕井澤高原教會", note:"榆樹街小鎮步行約 7 分鐘。白天參觀時間 10:00–17:00，晚上教會一帶是燭光夜會場。不參加燭光夜的話，改在晚餐前（17:00 前）先來看教會。", art:"woodchurch", extra:{tag:"晚上選配", title:"聖誕燭光夜", note:"「星降る森のクリスマス」，2026 年 11/29–12/25、19:30–21:30，免費入場。12/14（一）不用抽選，但要事前登錄（11/27 13:00 開放）。", link:{href:"https://candle.karuizawachurch.org/christmas/", label:"燭光夜官網"}}},
    {t:"21:30", title:"計程車回英迪格酒店", note:"約 12 分鐘（6.9 公里）。晚上車少，請先請店家或飯店叫車。", m:"taxi"}
   ]},
  {id:"d3", date:"15", wd:"二", title:"輕井澤 → 東京", sub:"單車遊舊輕井澤、回東京", art:"d_return", seal:"pine", stay:"TOSEI酒店 可可尼築地銀座", stayArt:"ginza", stayNote:"取回寄放行李、重新 check-in", shuttle:true,
   memo:"teamLab Borderless 每月第 1、3 個週二休館，12/15 正好休館，所以排在 12/17。",
   items:[
    {t:"早上", title:"英迪格早餐", note:"吃完早餐、泡個湯再 check-out。", art:"morning"},
    {t:"10:00", sh:"from", title:"check-out，搭英迪格接駁車 → 輕井澤站", note:"約 5 分鐘到南口。另有 9:00、11:00、12:00 班", m:"bus"},
    {t:"10:10", title:"寄放行李、租自行車", note:"行李放車站置物櫃。北口步行約 3 分鐘的白貓自行車（白ネコサイクル）租車，營業 9:00–17:00。路面結冰或下雪就改搭巴士（約 4 分鐘）。", m:"bike"},
    {t:"10:25", title:"APPLE PIE lab 軽井沢", note:"沿輕井澤本通騎約 1.7 公里、10 分鐘內。就在舊輕井澤銀座通入口、圓環旁，推薦現填的蘋果卡士達派。", art:"applepie"},
    {t:"11:00", title:"舊輕井澤銀座通散步", note:"冬季部分店家休息或縮短營業。", art:"street"},
    {t:"11:40", title:"BOULANGERIE ASANOYA", note:"淺野屋舊道本店。麵包當點心或伴手禮。", art:"bread"},
    {t:"12:20", title:"午餐", note:"舊輕銀座一帶", m:"bowl"},
    {t:"13:20", title:"森之教堂（森のチャペル 軽井沢礼拝堂）", note:"回車站的路上，騎車約 3 分鐘。12/15 是週二，教堂公休（週二、三休），只能在外面拍照。旁邊就是新藝術博物館的「白樺與苔之森」教堂，也可以在路邊拍照。", art:"forestchapel"},
    {t:"13:35", title:"輕井澤新藝術博物館", note:"週二 10:00–17:00（週一休館）。1 樓藝廊和書店咖啡免費；2 樓企畫展成人 2,000 日圓，含隈研吾設計的「白樺與苔之森」教堂導覽（每天 2 場、限 10 人）。", art:"artmuseum"},
    {t:"14:45", title:"還自行車、取行李", note:"博物館騎回車站約 3 分鐘，17:00 前要還車。", m:"bike"},
    {t:"15:00", title:"車站一帶逛街", note:"南口旁就是暢貨中心（王子購物廣場），裡面有 MUJI。", m:"walk"},
    {t:"16:00", title:"北陸新幹線回東京", note:"約 1 小時 10 分。出發前查班次、劃位。", m:"train"},
    {t:"17:15", title:"東京車站", note:"站內商店街、買伴手禮。", art:"tokyostation", spot:true, shop:"tokyo"},
    {t:"晚上", title:"回 TOSEI", note:"取回寄放行李、重新 check-in", m:"bed"}
   ]},
  {id:"d4", date:"16", wd:"三", title:"分組日", sub:"大邱組 入管局・東京車站・澀谷／三口組 明治神宮・中目黑", art:"d_split", seal:"b", stay:"TOSEI酒店 可可尼築地銀座", stayArt:"ginza", stayNote:"18:00 兩組在澀谷會合吃晚餐",
   groups:{
    A:{name:"入管局 → 澀谷", items:[
      {t:"07:30", title:"出發 → JR 品川站港南口", note:"淺草線往品川一帶，約 30 分鐘", m:"train"},
      {t:"08:15", title:"都巴士「品99」", note:"在「東京出入国在留管理局前」下車，下車就在門口", m:"bus"},
      {t:"08:30", title:"東京出入國在留管理局", note:"開門前排隊、辦理手續。受理時間平日 9:00–16:00，越早到越好。", art:"immigration", spot:true},
      {t:"辦完後", title:"回品川站 → JR 到東京車站", note:"品川站搭 JR 山手線或京濱東北線，約 10 分鐘", m:"train"},
      {t:"12:00", title:"與日文老師午餐有約", note:"在東京車站一帶。", m:"bowl"},
      {t:"13:30", title:"JR 山手線到澀谷", note:"東京車站到澀谷約 25 分鐘", m:"train"},
      {t:"14:00", title:"Coffee & Cake SHU Premium Shibuya-Ekimae", note:"下午茶休息一下。", art:"cake", spot:true},
      {t:"接著", title:"Tower Records 澀谷店", note:"澀谷站八公口步行約 5 分鐘。營業約 11:00–22:00，晚到也逛得到。", art:"records", spot:true},
      {t:"18:00", title:"在澀谷與三口組會合吃晚餐", note:"", m:"bowl"}
    ]},
    B:{name:"明治神宮 → 中目黑", note:"三口組不用去入管局、SHU 和 Tower Records。", items:[
      {t:"08:30", title:"出發 → 原宿", note:"", m:"train"},
      {t:"09:15", title:"明治神宮", note:"12 月開門 6:40、16:00 關門；御朱印、御守 9:00 起。", art:"torii", spot:true},
      {t:"11:00", title:"表參道／原宿逛街、午餐", note:"", m:"walk", shop:"harajuku"},
      {t:"14:00", title:"星巴克臻選® 東京烘焙工坊", note:"中目黑。營業 7:00–22:00；中目黑站步行約 14 分鐘。", art:"roastery", spot:true},
      {t:"16:30", title:"中目黑／代官山自由逛", note:"", m:"walk", shop:"nakameguro"},
      {t:"18:00", title:"到澀谷與大邱組會合", note:"中目黑到澀谷搭東急東橫線一站", m:"bowl", shop:"shibuya"}
    ]}
   }},
  {id:"d5", date:"17", wd:"四", title:"東京大學＋teamLab", sub:"本鄉校區、麻布台Hills", art:"d_ginkgo", seal:"", stay:"TOSEI酒店 可可尼築地銀座", stayArt:"ginza", stayNote:"日比谷線從神谷町可直達築地",
   items:[
    {t:"09:30", title:"東京大學本鄉校區", note:"搭地鐵到本鄉三丁目或東大前。看赤門、安田講堂、三四郎池。", art:"todai", spot:true},
    {t:"12:00", title:"本鄉一帶午餐", note:"", m:"bowl"},
    {t:"14:00", title:"teamLab Borderless", note:"麻布台Hills，神谷町站 5 號出口直通（日比谷線從築地可直達）。10:00–21:00，最後入場 20:00；成人 3,800 日圓起。請先上網買指定時段票。", art:"teamlab", spot:true},
    {t:"傍晚", title:"晚餐", note:"在麻布台Hills 吃，或回銀座", m:"bowl"}
   ]},
  {id:"d6", date:"18", wd:"五", title:"彈性及購物日", sub:"行程待定", art:"d_shopping", seal:"", stay:"TOSEI酒店 可可尼築地銀座", stayArt:"ginza", stayNote:"最後一晚，可先整理行李",
   items:[
    {t:"全天", title:"自由活動、購物", note:"行程待定", m:"walk"},
    {t:"下午", title:"ASICS Walking 銀座インズ店", note:"ASICS 的健走鞋專門店，在有樂町站旁的銀座インズ 2 一樓，11:00–20:00。從伊東屋步行約 6 分鐘。", art:"walkshoes", spot:true},
    {t:"下午", title:"noix de beurre 銀座三越店", note:"銀座三越 B2F 的費南雪專賣店，10:00–20:00。從伊東屋步行約 5 分鐘。", art:"financier", spot:true},
    {t:"晚上", title:"銀座伊東屋本店", note:"全體一起。平日 10:00–20:00。", art:"stationery", spot:true, shop:"ginza"},
    {t:"之後", title:"銀座晚餐", note:"", m:"bowl"}
   ]},
  {id:"d7", date:"19", wd:"六", title:"返程", sub:"成田第 2 航廈 → 台中", art:"d_home", seal:"", stay:"", stayArt:"", stayNote:"",
   items:[
    {t:"09:30", title:"飯店 check-out", note:"", m:"bag"},
    {t:"09:30", alt:true, title:"飯店 → 機場", opts:[
      {tag:"A", m:"train", title:"京成 Access 特急 → 成田第 2 航廈", note:"10:15 左右從東銀座搭車（飯店步行約 10 分鐘），到成田第 2 航廈約 1.5 小時。", q:"東銀座駅", ql:"東銀座站"},
      {tag:"B", m:"car", title:"機場接送（專車）飯店直達成田第 2 航廈", note:"Google 地圖模擬 12/19（六）09:30 出發：車程約 50 分–1 小時 15 分，約 10:45 前後抵達。請提前預約。", dir:"https://www.google.com/maps/dir/35.6639906,139.7716542/%E6%88%90%E7%94%B0%E5%9B%BD%E9%9A%9B%E7%A9%BA%E6%B8%AF+%E7%AC%AC2%E3%82%BF%E3%83%BC%E3%83%9F%E3%83%8A%E3%83%AB/data=!4m6!4m5!2m3!6e0!7e2!8j1797672600!3e0", ql:"飯店到機場的車程"}]},
    {t:"12:00", title:"抵達成田第 2 航廈、報到", note:"建議起飛前 2 小時到", m:"plane"},
    {t:"14:25", title:"JX315 成田第 2 航廈起飛", note:"", m:"plane"},
    {t:"17:55", title:"抵達台中", note:"辛苦了！", m:"home"}
   ]}
];
const SPOTS = [
  {n:"東京車站", d:"12/14 中午、12/15 傍晚", art:"tokyostation", days:["d2","d3"]},
  {n:"APPLE PIE lab 軽井沢", d:"12/15", art:"applepie", days:["d3"], ord:1},
  {n:"BOULANGERIE ASANOYA", d:"12/15", art:"bread", days:["d3"], ord:2},
  {n:"舊輕井澤銀座通", d:"12/15", art:"street", days:["d3"], ord:1.5},
  {n:"石之教會 內村鑑三記念堂", d:"12/14", art:"stonechurch", days:["d2"], gone:true},
  {n:"輕井澤高原教會", d:"12/14 晚上", art:"woodchurch", days:["d2"], ord:0.7},
  {n:"榆樹街小鎮", d:"12/14", art:"harunire", days:["d2"], ord:0.6},
  {n:"輕井澤英迪格酒店", d:"12/14 住宿", art:"firepit", days:["d2","d3"], ord:0.5},
  {n:"明治神宮", d:"12/16（三口組）", art:"torii", days:["d4"]},
  {n:"星巴克臻選® 東京烘焙工坊", d:"12/16（三口組）", art:"roastery", days:["d4"]},
  {n:"東京出入國在留管理局", d:"12/16（大邱組）", art:"immigration", days:["d4"]},
  {n:"Coffee & Cake SHU Premium Shibuya-Ekimae", d:"12/16（大邱組）", art:"cake", days:["d4"]},
  {n:"Tower Records 澀谷店", d:"12/16（大邱組）", art:"records", days:["d4"]},
  {n:"東京大學", d:"12/17", art:"todai", days:["d5"]},
  {n:"teamLab Borderless", d:"12/17", art:"teamlab", days:["d5"]},
  {n:"銀座 伊東屋 本店", d:"12/18（12/13 選配）", art:"stationery", days:["d6","d1"]},
  {n:"TOSEI酒店 可可尼築地銀座", d:"12/13、12/15–12/18 住宿", art:"ginza", days:["d1"]},
  {n:"森之教堂", d:"12/15（週二公休，外觀拍照）", art:"forestchapel", days:["d3"], ord:3.5},
  {n:"輕井澤新藝術博物館", d:"12/15", art:"artmuseum", days:["d3"], ord:3.6},
  {n:"noix de beurre 銀座三越店", d:"12/18", art:"financier", days:["d6"], ord:14.5},
  {n:"ASICS Walking 銀座インズ店", d:"12/18", art:"walkshoes", days:["d6"], ord:14.4}
];
const LIVE = SPOTS.map((s,i)=>({s,i})).filter(o=>!o.s.gone).sort((a,b)=>(a.s.ord??a.i)-(b.s.ord??b.i));
const spotsDone = () => { const st = store.get("spots",{}); return LIVE.filter(o=>st[o.i]).length; };
const TODO = [
  {name:"待議", hint:"還沒決定、需要大家討論。決定了就打勾。", items:[
    {id:"pickup", n:"12/13、12/19 是否預約成田機場接送", d:"10 人座、中文司機，約 22,000 日圓／趟。"},
    {id:"meet", n:"12/16 晚上在澀谷會合，還是改在原宿或中目黑／代官山", d:"考量澀谷站周邊太大，車站和人潮對二老不友善。"},
    {id:"split13", n:"12/13 是否分組行動", d:"大邱組可在先入境時完成 JTTP 二次審查，兩組分開前往飯店"}]},
  {name:"待辦", hint:"出發前要處理的事。辦好就打勾。", items:[
    {id:"ticket", n:"確認電子機票時間", d:"冬季班表：JX314 09:15→13:25、JX315 14:25→17:55"},
    {id:"pickup-tw", n:"預約大邱及錦祥街機場接送", d:"兩地分開搭車前往"},
    {id:"teamlab", n:"買 teamLab Borderless 門票", d:"12/17 下午入場，指定時段票"},
    {id:"imm", n:"確認入管局能否線上預約", d:"大邱組 12/16"},
    {id:"candle", n:"登錄高原教會燭光夜", d:"12/14 不用抽選，但要事前登錄；11/27（五）13:00 開放", opt:"選配"}]}
];
const TODO_TOTAL = TODO.reduce((n,c)=>n+c.items.length,0);
const todoDone = () => { const st=store.get("todo",{}); return TODO.reduce((n,c)=>n+c.items.filter(it=>st[it.id]).length,0); };
const PACK = [
  {name:"出國", items:["護照","入境簽證 / 健康許可證明","外幣現金","eSIM","當地運輸票券","旅平險","機場接送費用","當地機場快捷票券","購物優惠券","電壓檢查","伴手禮","頸枕","真空袋","真空幫浦"]},
  {name:"必需品", items:["家裡鑰匙","鼻噴劑","個人藥品","通血透骨膏"]},
  {name:"隨身用品", items:["錢包","行動電源","充電線","充電頭","雨傘","隨身水瓶","口罩","眼鏡盒","隱形眼鏡","眼藥水","環保購物袋","護唇膏","護手霜","牙線","衛生紙","爽身濕紙巾"]},
  {name:"衣著及穿搭", items:["內衣褲","外衣褲","外套","睡衣褲","襪子","皮帶","休閒鞋","飯店拖鞋","烘衣神器","髒衣袋"]},
  {name:"化妝品", items:["粉底棒","假睫毛","化妝棉","卸妝棉","卸妝蜜","眉毛夾","定妝噴霧","香水","髮蠟","定型噴霧","小剪刀","鯊魚夾"]},
  {name:"保養品", items:["化妝水","精華液","乳液","面霜","面膜"]},
  {name:"衛生用品", items:["牙刷","牙膏","棉花棒","洗髮精","Femfresh","刮鬍刀","梳子","消臭元"]},
  {name:"JTTP", items:["護照",
    {n:"個人證件照", d:"預設兩吋，可以多帶幾張，以防規定更改"},
    {n:"一次審查通過確認信", d:"信中有申請 ID"},
    {n:"4,000 日圓收入印紙", d:"在郵局或入管局附近的超商買，只能付現金"},
    {n:"申請用信用卡", d:"忘了是哪張的話，可以多帶幾張讓人員確認"}]}
];
const packCustom = () => store.get("packCustom", {});
const packHidden = () => store.get("packHidden", {});
const packHiddenIn = ci => { const h=packHidden(); return PACK[ci].items.filter((_,i)=>h[ci+"-"+i]).length; };
const packItems = ci => { const h=packHidden(); return PACK[ci].items.map((x,i)=>typeof x==="string" ? {k:ci+"-"+i, n:x} : {k:ci+"-"+i, n:x.n, d:x.d}).filter(it=>!h[it.k]).concat((packCustom()[ci]||[]).map(c=>({k:ci+"-c"+c.id, n:c.n, custom:c.id}))); };
const packTotal = () => PACK.reduce((s,_,ci)=>s+packItems(ci).length,0);
const packDone = () => { const st=store.get("pack",{}); return PACK.reduce((s,_,ci)=>s+packItems(ci).filter(it=>st[it.k]).length,0); };

/* ---------- state ---------- */
let curDay = store.get("day","d1"); if(!DAYS.some(d=>d.id===curDay)) curDay="d1";
let curGroup = store.get("group","A");
const countDone = (key) => Object.values(store.get(key,{})).filter(Boolean).length;
function todayDayId(){
  const n=new Date(), t=new Date(n.getFullYear(),n.getMonth(),n.getDate());
  const first=new Date(2026,11,13), last=new Date(2026,11,19);
  if(t<=first) return DAYS[0].id;
  if(t>=last) return DAYS[DAYS.length-1].id;
  return DAYS[Math.round((t-first)/86400000)].id;
}

/* ---------- pieces ---------- */
const PLANE = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 13.5 21 7.5c1.2-.4 1.9.9.8 1.6L6 17.5 3.5 17z M11 11l-2.5-6 2-.6 5 4.8 M10 15.4l-1 4.6 2 .2 3.6-6.7"/></svg>`;
const toMin = t => { const m=/(\d{1,2}):(\d{2})/.exec(t||""); return m ? (+m[1])*60 + (+m[2]) : null; };
function refMin(d, it){
  const n=new Date(), t=new Date(n.getFullYear(),n.getMonth(),n.getDate());
  if(d && t>=new Date(2026,11,13) && t<=new Date(2026,11,19) && todayDayId()===d.id) return n.getHours()*60+n.getMinutes();
  return it ? toMin(it.t) : null;
}
function chipsFor(dir, ref){
  let nextDone=false;
  return `<div class="sh-times">${SHUTTLE[dir].map(t=>{ const m=toMin(t); let c="";
    if(ref!=null && m<ref) c="past"; else if(!nextDone){ c="next"; nextDone=true; }
    return `<span class="num ${c}">${t}</span>`; }).join("")}</div>`;
}
let CUR_DAY_OBJ = null;
/* ---- Google Maps: every place in the trip opens a Maps search ---- */
const MAPQ = {
  "抵達成田第 2 航廈":"成田国際空港 第2ターミナル", "京成 Access 特急 → 東銀座":"東銀座駅", "TOSEI酒店 check-in":"TOSEIホテル ココネ築地銀座", "散步、晚餐":"銀座", "銀座 伊東屋 本店":"銀座 伊東屋 本店",
  "東京車站":"東京駅 丸の内駅舎", "北陸新幹線 → 輕井澤":"軽井沢駅", "巴士到「舊輕井澤」":"旧軽井沢 バス停", "APPLE PIE lab 軽井沢":"APPLE PIE lab 軽井沢",
  "舊輕井澤銀座通散步":"旧軽井沢銀座通り", "BOULANGERIE ASANOYA":"ブランジェ浅野屋 軽井沢旧道本店", "前往星野區":"軽井沢星野エリア", "石之教會 內村鑑三記念堂":"石の教会 内村鑑三記念堂",
  "輕井澤高原教會":"軽井沢高原教会", "榆樹街小鎮（Harunire Terrace）":"ハルニレテラス", "留下來看高原教會聖誕燭光夜":"軽井沢高原教会", "回輕井澤站":"軽井沢駅", "計程車 → 榆樹街小鎮":"ハルニレテラス", "榆樹街小鎮晚餐":"ハルニレテラス", "計程車回英迪格酒店":"ホテルインディゴ軽井沢", "英迪格早餐":"ホテルインディゴ軽井沢", "寄放行李、租自行車":"白ネコサイクル 軽井沢", "還自行車、取行李":"白ネコサイクル 軽井沢", "車站一帶逛街":"軽井沢・プリンスショッピングプラザ", "回品川站 → JR 到東京車站":"東京駅", "與日文老師午餐有約":"東京駅", "noix de beurre 銀座三越店":"ノワ・ドゥ・ブール 銀座三越店", "ASICS Walking 銀座インズ店":"アシックスウォーキング 銀座インズ", "森之教堂（森のチャペル 軽井沢礼拝堂）":"森のチャペル 軽井沢礼拝堂", "回輕井澤站 → 星野區":"軽井沢星野エリア", "行李寄放車站，走到美術館":"軽井沢駅", "輕井澤新藝術博物館":"Karuizawa New Art Museum", "車站一帶午餐、逛街":"軽井沢・プリンスショッピングプラザ",
  "英迪格酒店接駁車 → 酒店":"軽井沢駅南口 バスターミナル", "輕井澤英迪格酒店":"ホテルインディゴ軽井沢", "英迪格悠閒早晨":"ホテルインディゴ軽井沢",
  "check-out，搭英迪格接駁車 → 輕井澤站":"ホテルインディゴ軽井沢", "車站一帶逛街、午餐":"軽井沢・プリンスショッピングプラザ", "北陸新幹線回東京":"軽井沢駅", "回 TOSEI":"TOSEIホテル ココネ築地銀座",
  "出發 → JR 品川站港南口":"品川駅 港南口", "都巴士「品99」":"東京出入国在留管理局前 バス停", "東京出入國在留管理局":"東京出入国在留管理局",
  "JR 山手線到澀谷":"渋谷駅", "Coffee & Cake SHU Premium Shibuya-Ekimae":"Coffee & Cake SHU Premium Shibuya-Ekimae", "Tower Records 澀谷店":"タワーレコード渋谷店",
  "在澀谷與三口組會合吃晚餐":"渋谷駅", "出發 → 原宿":"原宿駅", "明治神宮":"明治神宮", "表參道／原宿逛街、午餐":"表参道",
  "星巴克臻選® 東京烘焙工坊":"スターバックス リザーブ ロースタリー 東京", "中目黑／代官山自由逛":"中目黒駅", "到澀谷與大邱組會合":"渋谷駅",
  "東京大學本鄉校區":"東京大学 本郷キャンパス 赤門", "本鄉一帶午餐":"本郷三丁目駅", "teamLab Borderless":"チームラボボーダレス 麻布台ヒルズ", "晚餐":"麻布台ヒルズ",
  "補 12/16 沒去的地方":"明治神宮", "銀座伊東屋本店":"銀座 伊東屋 本店", "銀座晚餐":"銀座", "京成 Access 特急 → 成田":"東銀座駅", "抵達成田第 2 航廈、報到":"成田国際空港 第2ターミナル", "午餐":"旧軽井沢銀座通り", "飯店 check-out":"TOSEIホテル ココネ築地銀座", "JX315 成田第 2 航廈起飛":"成田国際空港 第2ターミナル", "抵達台中":"台中國際機場", "JX314 台中起飛":"台中國際機場"
};
const SPOTQ = ["東京駅 丸の内駅舎","APPLE PIE lab 軽井沢","ブランジェ浅野屋 軽井沢旧道本店","旧軽井沢銀座通り","石の教会 内村鑑三記念堂","軽井沢高原教会","ハルニレテラス","ホテルインディゴ軽井沢",
  "明治神宮","スターバックス リザーブ ロースタリー 東京","東京出入国在留管理局","Coffee & Cake SHU Premium Shibuya-Ekimae","タワーレコード渋谷店","東京大学 本郷キャンパス","チームラボボーダレス 麻布台ヒルズ","銀座 伊東屋 本店","TOSEIホテル ココネ築地銀座","森のチャペル 軽井沢礼拝堂","Karuizawa New Art Museum","ノワ・ドゥ・ブール 銀座三越店","アシックスウォーキング 銀座インズ"];
const mapUrl = q => "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(q);
const mapLink = (q, name) => `<a class="go-map" href="${mapUrl(q)}" target="_blank" rel="noopener" aria-label="在 Google 地圖開啟：${esc(name)}（另開新視窗）">${ico("map")}在 Google 地圖開啟${ico("ext")}</a>`;
const NEAR = {
  tosei: {stores:[
    {k:"超商", n:"全家 築地市場前店", w:1, h:"24 小時", q:"ファミリーマート 築地市場前店"},
    {k:"超商", n:"全家 築地六丁目店", w:3, h:"24 小時", q:"ファミリーマート 築地六丁目店"},
    {k:"超市", n:"ニューみ乃り屋", w:4, h:"8:00–21:00", q:"ニューみ乃り屋 築地"},
    {k:"超商", n:"7-Eleven 築地 7 丁目店", w:5, h:"24 小時", q:"セブンイレブン 築地7丁目店"},
    {k:"超商", n:"LAWSON 築地六丁目店", w:5, h:"24 小時", q:"ローソン 築地六丁目店"},
    {k:"超市", n:"My Basket 築地二丁目店", w:10, h:"8:00–23:00", q:"マイバスケット 築地二丁目店"}],
    note:"步行時間取自 Google 地圖，營業時間以店家公告為準。"},
  indigo: {stores:[
    {k:"超商", n:"LAWSON 南輕井澤店", w:3, h:"6:00–23:00", q:"ローソン 南軽井沢店"},
    {k:"超商", n:"7-Eleven 輕井澤王子通店", w:8, h:"6:00–23:00", q:"セブンイレブン 軽井沢プリンス通り店"}],
    note:"步行 10 分鐘內沒有超市；兩家超商都是 23:00 打烊。步行時間取自 Google 地圖。"}
};
const SHOP = {
  harajuku: {sub:"表參道・原宿", stores:[
    {k:"UNIQLO", n:"UNIQLO 原宿店", w:"原宿站步行 1 分", h:"11:00–21:00", q:"ユニクロ 原宿店"},
    {k:"MUJI", n:"Found MUJI 青山", w:"表參道站步行 3 分", h:"12:00–20:00", q:"無印良品 青山"},
    {k:"3COINS", n:"3COINS 原宿旗艦店", w:"原宿站步行 7 分", h:"11:00–20:00", q:"3COINS 原宿本店"}],
    note:"這一帶沒有唐吉訶德和 Standard Products；唐吉訶德可以留到下午中目黑或晚上澀谷。"},
  nakameguro: {sub:"中目黑・代官山", stores:[
    {k:"唐吉訶德", n:"唐吉訶德 中目黑本店", w:"星巴克烘焙工坊步行 1 分", h:"24 小時", q:"ドン・キホーテ 中目黒本店"},
    {k:"MUJI", n:"無印良品 代官山", w:"中目黑站步行 11 分", h:"11:00–19:00", q:"無印良品 代官山"}],
    note:"唐吉訶德就在烘焙工坊旁邊，喝完咖啡就能逛。無印良品代官山 19:00 打烊，要去的話先去。"},
  shibuya: {sub:"澀谷站周邊", stores:[
    {k:"UNIQLO", n:"UNIQLO 澀谷道玄坂店", w:"澀谷站前（澀谷 PRIME）", h:"11:00–21:00", q:"ユニクロ 渋谷道玄坂店"},
    {k:"唐吉訶德", n:"MEGA 唐吉訶德 澀谷本店", w:"澀谷站步行 2 分", h:"24 小時", q:"MEGAドン・キホーテ 渋谷本店"},
    {k:"Standard Products", n:"Standard Products 澀谷 Mark City", w:"澀谷站步行 2 分", h:"9:30–21:00", q:"Standard Products 渋谷マークシティ"},
    {k:"MUJI", n:"無印良品 澀谷", w:"澀谷站步行 4 分", h:"11:00–21:00", q:"無印良品 渋谷西武"}],
    note:"會合前或晚餐後都能逛；唐吉訶德 24 小時營業，適合放最後。"},
  tokyo: {sub:"東京車站・八重洲地下街", stores:[
    {k:"甜點", n:"BRULEE MERIZE（東京ギフトパレット）", w:"東京車站步行 1 分（八重洲北口）", h:"9:30–20:30", q:"ブリュレメリゼ 東京ギフトパレット店"},
    {k:"唐吉訶德", n:"お菓子ドンキ・お酒ドンキ（零食、酒類專門）", w:"東京車站步行 2 分", h:"9:00–21:30", q:"お菓子ドンキ お酒ドンキ 八重洲地下街"},
    {k:"3COINS", n:"3COINS 八重洲地下街店", w:"東京車站步行 1 分", h:"10:00–21:00", q:"3COINS 八重洲地下街"},
    {k:"UNIQLO", n:"UNIQLO 東京站八重洲地下街店", w:"東京車站步行 3 分", h:"10:00–20:30", q:"ユニクロ 東京駅八重洲地下街店"},
    {k:"Standard Products", n:"Standard Products 八重洲地下街店", w:"東京車站步行 3 分", h:"10:00–20:00", q:"Standard Products 八重洲地下街"},
    {k:"MUJI", n:"MUJI to GO KITTE 丸之內店", w:"丸之內南口步行 4 分", h:"11:00–20:00", q:"MUJI to GO KITTE丸の内"}],
    note:"BRULEE MERIZE 在八重洲北口的東京ギフトパレット；唐吉訶德、3COINS、UNIQLO、Standard Products 都在八重洲地下街，下雨也不用出站；MUJI to GO 在丸之內側的 KITTE 3F，是小型店，以旅行用品為主。完整的唐吉訶德最近是銀座本店，可以留到 12/18。"},
  ginza: {sub:"從伊東屋步行", stores:[
    {k:"UNIQLO", n:"UNIQLO TOKYO（Marronnier Gate 銀座 2）", w:"步行 4 分", h:"11:00–21:00", q:"UNIQLO TOKYO マロニエゲート銀座2"},
    {k:"Standard Products", n:"Standard Products 銀座（同棟 6F）", w:"步行 4 分", h:"11:00–21:00", q:"Standard Products マロニエゲート銀座"},
    {k:"MUJI", n:"無印良品 銀座旗艦店", w:"步行 4 分", h:"11:00–21:00", q:"無印良品 銀座"},
    {k:"3COINS", n:"3COINS+plus 西銀座", w:"步行 6 分", h:"11:00–20:00", q:"3COINS+plus 西銀座"},
    {k:"UNIQLO", n:"UNIQLO 銀座旗艦店", w:"步行 8 分", h:"11:00–21:00", q:"ユニクロ 銀座店"},
    {k:"唐吉訶德", n:"唐吉訶德 銀座本店", w:"步行 13 分", h:"24 小時", q:"ドン・キホーテ 銀座本館"}],
    note:"伊東屋平日 20:00 打烊，建議先逛伊東屋，再到隔壁幾條街的 UNIQLO TOKYO／MUJI；唐吉訶德在銀座 8 丁目，可以留到晚餐後。"}
};
let NEAR_UID = 0;
function listHTML(title, sub, rows, note, iconName){
  const id = "near-" + (++NEAR_UID);
  const li = rows.map(s=>`<li><div class="nr-tx"><strong>${esc(s.n)}</strong><span><b class="nr-k" data-k="${esc(s.k)}">${esc(s.k)}</b>${esc(s.w)}・${esc(s.h)}</span></div>
    <a class="nr-map" href="${mapUrl(s.q)}" target="_blank" rel="noopener" aria-label="在 Google 地圖開啟：${esc(s.n)}（另開新視窗）">${ico("map")}<span>地圖</span></a></li>`).join("");
  return `<div class="near" data-open="false"><button type="button" class="near-hd" aria-expanded="false" aria-controls="${id}">${ico(iconName)}<span>${title}<small>${esc(sub)}</small></span><svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
    <div class="near-body" id="${id}"><div><ul>${li}</ul><p class="foot">${esc(note)}</p></div></div></div>`;
}
function nearHTML(key){
  const N = NEAR[key];
  return listHTML("附近超商・超市", "步行 10 分鐘內・" + N.stores.length + " 家", N.stores.map(s=>({k:s.k, n:s.n, w:"步行約 "+s.w+" 分", h:s.h, q:s.q})), N.note, "bag");
}
function shopHTML(key){
  const S = SHOP[key];
  return listHTML(S.title || "順路購物", S.sub + "・" + S.stores.length + " 家", S.stores, S.note + "營業時間以 Google 地圖為準。", "tag");
}

function itemHTML(it, grp){
  if(it.sh){
    const ref = refMin(CUR_DAY_OBJ, it), up = SHUTTLE[it.sh].filter(t=>ref==null||toMin(t)>=ref);
    const sum = up.length ? `下一班 ${up[0]}${up[1]?"・之後 "+up.slice(1,3).join("、"):""}` : "今天已無班次";
    const id = "shx-"+it.sh, lab = it.sh==="to" ? "輕井澤站南口 → 酒店" : "酒店 → 輕井澤站南口";
    return `<div class="tl move"><div class="tm">${esc(it.t)}</div><div class="rail"></div><div><div class="mv shx" data-open="false">
      <button type="button" class="shx-head" aria-expanded="false" aria-controls="${id}"><span class="ib">${ico("bus")}</span><div><strong>${esc(it.title)}</strong><span class="nx num">${sum}</span></div>
      <svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
      <div class="shx-body" id="${id}"><div><div class="in"><div class="sh-row"><span class="sh-lb">${lab}</span>${chipsFor(it.sh, ref)}</div>
      <p class="foot">${esc(it.note)}</p>
      <a class="go-map solo" href="${mapUrl(it.sh==="to"?"軽井沢駅南口 バスターミナル":"ホテルインディゴ軽井沢")}" target="_blank" rel="noopener" aria-label="${it.sh==="to"?"上車處：輕井澤站南口":"上車處：英迪格酒店"}，在 Google 地圖開啟（另開新視窗）">${ico("map")}${it.sh==="to"?"上車處：輕井澤站南口":"上車處：英迪格酒店"}，在 Google 地圖開啟${ico("ext")}</a></div></div></div></div></div></div>`;
  }
  if(it.alt){
    const opts = it.opts.map(o=>{
      const href = o.dir || mapUrl(o.q), lab = o.dir ? "Google 地圖車程" : "Google 地圖";
      return `<div class="alt-op"><span class="alt-tag">${o.tag}</span><span class="ib">${ico(o.m)}</span><div><strong>${esc(o.title)}</strong><small>${esc(o.note)}</small>
        <a class="go-map" href="${href}" target="_blank" rel="noopener" aria-label="${lab}：${esc(o.ql||o.title)}（另開新視窗）">${ico("map")}${lab}${ico("ext")}</a></div></div>`;}).join("");
    return `<div class="tl move"><div class="tm">${esc(it.t)}</div><div class="rail"></div><div><div class="mv alt"><div class="alt-hd"><strong>${esc(it.title)}</strong><span class="alt-pill">交通二選一</span></div>${it.lead?`<small class="alt-lead">${esc(it.lead)}</small>`:""}${opts}</div></div></div>`;
  }
  const q = MAPQ[it.title];
  const cls = it.m ? "move" : (it.opt ? "opt" : (grp ? "g"+grp.toLowerCase() : ""));
  let inner;
  if(it.m){
    inner = `<div class="mv"><div class="mv-row"><span class="ib">${ico(it.m)}</span><div><strong>${esc(it.title)}</strong>${it.note?`<small>${esc(it.note)}</small>`:""}${q?mapLink(q,it.title):""}</div></div>${it.shop?shopHTML(it.shop):""}</div>`;
  } else {
    const tags = (it.opt?tagH(it.opt,"opt"):"") + (it.group?tagH(GNAME[it.group], it.group.toLowerCase()):"");
    inner = `<article class="card stop${it.opt?" dashed":""}">${pic(it.art)}<div class="tx"><h3>${esc(it.title)}</h3>${it.note?`<p>${esc(it.note)}</p>`:""}${tags?`<div class="tags">${tags}</div>`:""}<div class="lk-row">${q?mapLink(q,it.title):""}${it.link?`<a class="go-map" href="${it.link.href}" target="_blank" rel="noopener" aria-label="${esc(it.link.label)}（另開新視窗）">${ico("ext")}${esc(it.link.label)}</a>`:""}</div>${it.extra?extraHTML(it.extra):""}</div>${it.shop?shopHTML(it.shop):""}</article>`;
  }
  return `<div class="tl ${cls}"><div class="tm">${esc(it.t)}</div><div class="rail"></div><div>${inner}</div></div>`;
}
function extraHTML(x){
  return `<div class="extra"><div class="extra-hd">${tagH(x.tag,"opt")}<strong>${esc(x.title)}</strong></div><p>${esc(x.note)}</p>${x.link?`<a class="go-map" href="${x.link.href}" target="_blank" rel="noopener" aria-label="${esc(x.link.label)}（另開新視窗）">${ico("ext")}${esc(x.link.label)}</a>`:""}</div>`;
}
function toFirstItem(){
  const v=document.getElementById("view-trip"), first=v.querySelector(".dayhead");
  if(!first) return;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  first.scrollIntoView({block:"start", behavior: reduce ? "auto" : "smooth"});
  const ch = v.querySelector(`.chip[aria-pressed="true"]`); if(ch) ch.focus({preventScroll:true});
}
function stayCard(d){
  const key = d.stay.startsWith("TOSEI") ? "tosei" : "indigo";
  return `<div class="card stay-card"><h2>${ico("bed")}今晚住宿</h2>${pic(d.stayArt)}<div><strong style="display:block">${esc(d.stay)}</strong><span class="foot">${esc(d.stayNote)}</span></div>${nearHTML(key)}</div>`;
}
function checkHTML(key, i, title, sub, artKey, on){
  return `<label class="ck" for="${key}-${i}"><input type="checkbox" id="${key}-${i}" data-key="${key}" data-i="${i}" ${on?"checked":""}><span class="box">${CHECK}</span>${artKey?pic(artKey,"th"):""}<span class="lb">${esc(title)}${sub?`<small>${esc(sub)}</small>`:""}</span></label>`;
}

/* ---------- views ---------- */
function renderHome(){
  const start=new Date(2026,11,13), n=new Date(), today=new Date(n.getFullYear(),n.getMonth(),n.getDate());
  const diff=Math.round((start-today)/86400000);
  const count = diff>0 ? `<div class="count">${seal(diff,"DAYS")}<div><span>距離出發還有</span><strong>${diff} 天</strong></div></div>`
             : diff>-7 ? `<div class="count">${seal(1-diff,"DAY","pine")}<div><span>旅途中</span><strong>第 ${1-diff} 天</strong></div></div>`
             : `<div class="count">${seal("✓","DONE","pine")}<div><span>旅程結束</span><strong>辛苦了！</strong></div></div>`;
  const route = ["台中","東京","輕井澤","東京","台中"].map(s=>`<span>${s}</span>`).join("<i aria-hidden=\"true\"></i>");
  const pass = (no,date,dir,t1,a1,t2,a2)=>`<div class="card pass"><div class="main"><div class="hd"><span class="no">${no}</span>${tagH("星宇航空")}</div>
      <div class="rt"><div><div class="t">${t1}</div><div class="ap">${a1}</div></div><div class="ln" aria-hidden="true">${PLANE}</div><div style="text-align:right"><div class="t">${t2}</div><div class="ap">${a2}</div></div></div></div>
      <div class="cut" aria-hidden="true"></div><div class="stub"><span>${dir}</span><b>${date}</b></div></div>`;
  const tiles = DAYS.map((d,i)=>`<button type="button" class="card tile" data-goday="${d.id}">${d.id==="d4"?tape("top:-12px;left:46%;width:54px;transform:rotate(5deg)"):""}
      <span class="row">${seal(d.date,"12月",d.seal).replace('class="seal','style="transform:rotate('+(i%2?-5:4)+'deg)" class="seal')}<span class="wd">（${d.wd}）</span></span>
      <span><strong>${esc(d.title)}</strong><small>${esc(d.sub)}</small></span></button>`).join("");
  const q = (href,ic,t,s,n,tot)=>`<a class="card q" href="#${href}"><span class="hd"><span class="ib">${ico(ic)}</span><span><strong>${t}</strong><small>${s}</small></span></span>
      <span class="progress"><span class="bar"><i style="width:${n/tot*100}%"></i></span><b>${n} / ${tot}</b></span></a>`;
  const stay = (k,name,when,detail)=>`<div class="card stay">${pic(k)}<div><strong>${name}</strong><span>${when}</span><small>${detail}</small></div></div>`;
  document.getElementById("view-home").innerHTML = `
    <section class="hero">
      <div class="hero-art">${tape("top:-12px;left:36px;width:104px;transform:rotate(-6deg)")}${tape("top:-10px;right:44px;width:92px;transform:rotate(5deg)","pink")}<div class="plate">${pic("hero")}</div></div>
      <div class="hero-body">
        <div class="tags">${tagH("12.13 SUN — 12.19 SAT")}${tagH("七天六夜","opt")}</div>
        <h1><span class="en">2026 WINTER</span><span class="zh">東京冬令營</span></h1>
        <p>東京車站出發，到輕井澤住一晚看雪中教會，再回東京逛神宮、美術館和銀座。</p>
        ${count}
        <div class="route">${route}</div>
      </div>
    </section>
    <section class="sec"><div class="sec-title"><h2>班機</h2><span>星宇冬季班表，請以電子機票為準</span></div>
      <div class="passes">${pass("JX314","12/13","去程","09:15","台中 RMQ","13:25","成田 NRT T2")}${pass("JX315","12/19","回程","14:25","成田 NRT T2","17:55","台中 RMQ")}</div></section>
    <section class="sec"><div class="sec-title"><h2>每日行程</h2><span>點一天直接打開那天的行程</span></div><div class="tiles">${tiles}</div></section>
    <section class="sec"><div class="sec-title"><h2>清單</h2></div><div class="quick">
      ${q("spots","pin","行程確認清單","地圖清單 "+LIVE.length+" 個地點",spotsDone(),LIVE.length)}
      ${q("prep","clip","待議及待辦",TODO[0].items.length+" 項待議、"+TODO[1].items.length+" 項待辦",todoDone(),TODO_TOTAL)}
      ${q("pack","bag","打包清單",PACK.length+" 大類",packDone(),packTotal())}</div></section>
    <section class="sec"><div class="sec-title"><h2>住宿</h2></div><div class="stays">
      ${stay("ginza","TOSEI酒店 可可尼築地銀座","12/13、12/15–12/18・共 5 晚","近東銀座站，Access 特急直達成田")}
      ${stay("firepit","輕井澤英迪格酒店","12/14・1 晚","check-in 15:00・check-out 11:00")}</div></section>
    <p class="foot">營業時間與交通皆為行前查詢資料，出發前請再確認一次。</p>`;
}

function renderTrip(){
  const d = DAYS.find(x=>x.id===curDay), idx = DAYS.indexOf(d); CUR_DAY_OBJ = d;
  const chips = `<button type="button" class="chip today" data-today="1">${ico("cal")}今天</button>` +
    DAYS.map(x=>`<button type="button" class="chip" data-day="${x.id}" aria-pressed="${x.id===curDay}">12/${x.date}<small>${x.wd}</small></button>`).join("");
  let main;
  const st = store.get("spots",{});
  const daySpots = LIVE.filter(o=>o.s.days.includes(d.id));
  const fullSide = `<aside class="side">
      ${daySpots.length?`<div class="card"><h2>今天的清單地點</h2><p class="foot">去過就打勾，和「行程確認」同步</p>${daySpots.map(o=>checkHTML("spots",o.i,o.s.n,"",null,st[o.i])).join("")}</div>`:""}
      ${d.shuttle?shuttleCard():""}
      ${d.tips?`<div class="card"><h2>${ico("note")}小提醒</h2>${d.tips.map(t=>`<p style="font-size:14.5px">・${esc(t)}</p>`).join("")}</div>`:""}
      ${d.stay?stayCard(d):""}
    </aside>`;
  if(d.groups){
    const col = g => `<div class="gcol" data-g="${g}"><h2>${gBadge(g)}<span><span class="gname">${GNAME[g]}</span>${esc(d.groups[g].name)}</span></h2>
      ${d.groups[g].note?`<p class="gnote">${esc(d.groups[g].note)}</p>`:""}${d.groups[g].items.map(it=>itemHTML(it,g)).join("")}</div>`;
    const seg = `<div class="seg" role="group" aria-label="切換組別">${["A","B"].map(g=>`<button type="button" data-g="${g}" aria-pressed="${curGroup===g}">${GICON[g]}<span class="sg-t">${GNAME[g]}<small>${esc(d.groups[g].name)}</small></span></button>`).join("")}</div>`;
    const groups = `<div class="groups" data-show="${curGroup}">${col("A")}${col("B")}</div>`;
    if(d.pre || d.post){
      main = `<div class="daymain"><div class="timeline flow">${(d.pre||[]).map(it=>itemHTML(it)).join("")}
        <section class="split" aria-labelledby="split-h"><h2 class="flow-hd" id="split-h">${ico("shuffle")}兩組分開行動</h2>${seg}${groups}</section>
        ${d.post?`<h2 class="flow-hd">${ico("shuffle")}兩組會合</h2>${d.post.map(it=>itemHTML(it)).join("")}`:""}</div>${fullSide}</div>`;
    } else {
      main = `${seg}
      <div class="daymain">${groups}${d.stay?`<aside class="side">${stayCard(d)}</aside>`:""}</div>`;
    }
  } else {
    main = `<div class="daymain"><div class="timeline">${d.items.map(it=>itemHTML(it)).join("")}</div>${fullSide}</div>`;
  }
  document.getElementById("view-trip").innerHTML = `
    <div class="chips" role="group" aria-label="選擇日期">${chips}</div>
    <section class="dayhead">
      <div class="art">${tape("top:-12px;left:40px;width:96px;transform:rotate(-5deg)")}<div class="plate">${pic(d.art)}</div></div>
      <div class="info">
        <div class="ttl">${seal(d.date,"12月",d.seal)}<div><span class="eyebrow">DAY ${idx+1} ・ 12/${d.date}（${d.wd}）</span><h1>${esc(d.title)}</h1></div></div>
        <div class="tags">${tagH(d.sub)}${d.stay?tagH("住宿："+d.stay):""}</div>
      </div>
    </section>
    ${d.memo?`<div class="memo">${tape("top:-13px;left:24px;width:70px;transform:rotate(-3deg)","pink")}${d.memo}</div>`:""}
    ${main}`;
  const c = document.querySelector(`.chip[data-day="${curDay}"]`);
  if(c && c.scrollIntoView) c.scrollIntoView({block:"nearest",inline:"center"});
}

const SHUTTLE = {to:["14:50","15:40","16:40","17:30","18:20","19:00"], from:["9:00","10:00","11:00","12:00","17:10","18:00"]};
function shuttleCard(){
  const row = (label, arr) => `<div class="sh-row"><span class="sh-lb">${label}</span><div class="sh-times">${arr.map(t=>`<span class="num">${t}</span>`).join("")}</div></div>`;
  return `<div class="card shuttle"><h2>${ico("bus")}英迪格接駁車</h2>${row("輕井澤站南口 → 酒店",SHUTTLE.to)}${row("酒店 → 輕井澤站南口",SHUTTLE.from)}
    <p class="foot">免預約，車程約 5 分鐘。南口上車處在暢貨中心旁、樓梯下計程車站附近。冬季時刻，酒店表示時間可能不另行通知更改。</p></div>`;
}
function listHero(artKey, title, desc, done, total){
  return `<div class="card lhero">${tape("top:-12px;right:48px;width:84px;transform:rotate(5deg)")}${pic(artKey)}<div class="tx"><h1>${title}</h1><p>${desc}</p>
    <div class="progress"><span class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="${total}" aria-valuenow="${done}" aria-label="完成進度"><i style="width:${done/total*100}%"></i></span><b>${done} / ${total}</b></div></div></div>`;
}
/* ---------- photos (IndexedDB, this device only) ---------- */
const PH = { list: [], ok: true, ready: false };
function idb(){ return new Promise((res,rej)=>{ try{ const r=indexedDB.open("twc26",1); r.onupgradeneeded=()=>{ r.result.createObjectStore("photos",{keyPath:"id"}); }; r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error); }catch(e){ rej(e); } }); }
async function phTx(mode, fn){ const db=await idb(); return new Promise((res,rej)=>{ const tx=db.transaction("photos",mode), st=tx.objectStore("photos"); const out=fn(st); tx.oncomplete=()=>res(out&&out.result!==undefined?out.result:out); tx.onerror=()=>rej(tx.error); }); }
async function loadPhotos(){
  try{ const rows = await phTx("readonly", st=>st.getAll());
    PH.list.forEach(p=>URL.revokeObjectURL(p.url));
    PH.list = (rows||[]).sort((a,b)=>a.ts-b.ts).map(r=>({...r, url:URL.createObjectURL(r.blob)}));
  }catch(e){ PH.ok=false; }
  PH.ready = true;
}
function shrink(file){
  return new Promise((res,rej)=>{ const url=URL.createObjectURL(file), img=new Image();
    img.onload=()=>{ const max=1600, k=Math.min(1, max/Math.max(img.naturalWidth,img.naturalHeight));
      const c=document.createElement("canvas"); c.width=Math.round(img.naturalWidth*k); c.height=Math.round(img.naturalHeight*k);
      c.getContext("2d").drawImage(img,0,0,c.width,c.height); URL.revokeObjectURL(url);
      c.toBlob(b=>b?res({blob:b,w:c.width,h:c.height}):rej(new Error("encode")),"image/jpeg",0.86); };
    img.onerror=()=>{ URL.revokeObjectURL(url); rej(new Error("decode")); };
    img.src=url; });
}
async function addPhotos(spot, files){
  for(const f of files){
    try{ const s=await shrink(f); const id=Date.now().toString(36)+Math.random().toString(36).slice(2,7);
      await phTx("readwrite", st=>st.put({id, spot, blob:s.blob, w:s.w, h:s.h, ts:Date.now()})); }
    catch(e){ const quota = e && (e.name==="QuotaExceededError" || /quota/i.test(e.message||""));
      PH.err = quota ? "手機儲存空間不足，有照片沒有存進去。刪掉幾張舊照片後再上傳一次。" : "有照片無法開啟，可能是 HEIC 等格式。請改用 JPG 或 PNG 再上傳一次。"; }
  }
  const st=store.get("spots",{}); st[spot]=true; store.set("spots",st);
  await loadPhotos(); renderSpots();
}
async function delPhoto(id){ try{ await phTx("readwrite", st=>st.delete(id)); }catch(e){} await loadPhotos(); renderSpots(); }

function renderSpots(){
  const st = store.get("spots",{}); const done = spotsDone();
  const n = PH.list.length;
  const album = `<div class="card album"><div class="tx"><h2>${ico("camera")}旅行相簿</h2>
      <p>${!PH.ok ? "這個瀏覽器無法儲存照片，請改用 Safari 或 Chrome 開啟網站。" : n ? `已上傳 ${n} 張照片。一鍵生成可以分享到 IG、FB、LINE 的拼貼圖。` : "在下方地點按「＋ 照片」上傳，上傳後會自動打勾。照片只存在這台裝置，不會上傳到網路。"}</p>
      <p role="status" style="color:var(--accent);font-weight:700">${PH.err||""}</p></div>
      <button type="button" class="btn primary" data-share="open" ${n?"":"disabled"}>${ico("share")}生成分享圖</button></div>`;
  const items = LIVE.map(({s,i})=>{
    const mine = PH.list.filter(p=>p.spot===i), show = mine.slice(-3), more = mine.length - show.length;
    return `<div class="sp"><div class="sp-top">${checkHTML("spots",i,s.n,s.d,s.art,st[i])}<a class="map-btn" href="${mapUrl(SPOTQ[i])}" target="_blank" rel="noopener" aria-label="在 Google 地圖開啟 ${esc(s.n)}（另開新視窗）">${ico("map")}<span>地圖</span></a></div>
      <div class="ph-row">${more>0?`<span class="ph more num" aria-label="還有 ${more} 張">+${more}</span>`:""}${show.map(p=>`<button type="button" class="ph" data-photo="${p.id}" aria-label="查看 ${esc(s.n)} 的照片"><img src="${p.url}" alt=""></button>`).join("")}
      ${PH.ok?`<input type="file" accept="image/*" multiple class="ph-input" id="up-${i}" data-up="${i}"><label class="ph-add" for="up-${i}">${ico("camera")}＋ 照片</label>`:""}</div></div>`;
  }).join("");
  PH.err = "";
  document.getElementById("view-spots").innerHTML = listHero("hero","行程確認清單","Google 地圖清單「2026 東京冬令營」的 "+LIVE.length+" 個地點，全部排進行程。去過就打勾，也可以上傳在那裡拍的照片。",done,LIVE.length)
    + album + `<div class="checks">${items}</div>
    <button class="reset" type="button" data-reset="spots">清除勾選</button><p class="foot">勾選和照片只存在這台裝置的瀏覽器裡，不會同步給其他人。</p>`;
}

/* ---------- share image (canvas) ---------- */
const SH = { fmt: "4x5", seed: 0, blob: null, url: null };
const SPOT_DATE = i => ((SPOTS[i].d.match(/\d{1,2}\/\d{1,2}/)||[""])[0]);
function pickPhotos(seed){
  const bySpot = {}; PH.list.filter(p=>SPOTS[p.spot]&&!SPOTS[p.spot].gone).forEach(p=>{ (bySpot[p.spot]=bySpot[p.spot]||[]).push(p); });
  const rnd = (a)=> a[(Math.abs(Math.sin(seed*999 + a.length*7 + a[0].ts%997))*1e4|0) % a.length];
  const order = Object.keys(bySpot).map(Number).sort((a,b)=>a-b);
  let picks = order.map(k=>rnd(bySpot[k]));
  if(seed>0 && picks.length>6){ const off = seed % picks.length; picks = picks.slice(off).concat(picks.slice(0,off)); }
  return picks.slice(0,6);
}
function loadImg(url){ return new Promise((res,rej)=>{ const i=new Image(); i.onload=()=>res(i); i.onerror=rej; i.src=url; }); }
function rrect(g,x,y,w,h,r){ g.beginPath(); g.moveTo(x+r,y); g.arcTo(x+w,y,x+w,y+h,r); g.arcTo(x+w,y+h,x,y+h,r); g.arcTo(x,y+h,x,y,r); g.arcTo(x,y,x+w,y,r); g.closePath(); }
async function buildShare(){
  const W=1080, H = SH.fmt==="4x5" ? 1350 : 1080;
  const c=document.createElement("canvas"); c.width=W; c.height=H; const g=c.getContext("2d");
  try{ await Promise.all([document.fonts.load('900 64px "Noto Sans TC"'), document.fonts.load('700 30px "Roboto"')]); }catch(e){}
  const F = '"Roboto","Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif';
  const INK="#3B312B", SOFT="#6F5F55", PAPER="#F3ECDF", RED="#D9643F", TAPE="rgba(233,185,73,.85)", PINK="rgba(240,182,164,.9)";
  g.fillStyle=PAPER; g.fillRect(0,0,W,H);
  g.fillStyle="rgba(59,49,43,.13)"; for(let y=12;y<H;y+=24) for(let x=12;x<W;x+=24){ g.beginPath(); g.arc(x,y,1.6,0,7); g.fill(); }
  // header
  g.fillStyle=RED; g.font=`700 26px ${F}`; g.textBaseline="alphabetic";
  g.fillText("2026 WINTER · TOKYO · KARUIZAWA", 72, 104);
  g.fillStyle=INK; g.font=`900 76px ${F}`; g.fillText("東京冬令營", 68, 188);
  g.fillStyle=SOFT; g.font=`500 28px ${F}`; g.fillText("12.13 – 12.19", 72, 236);
  // seal
  g.save(); g.translate(W-138,150); g.rotate(-0.14); g.fillStyle=RED; g.beginPath(); g.arc(0,0,66,0,7); g.fill();
  g.lineWidth=6; g.strokeStyle=INK; g.stroke(); g.lineWidth=3; g.strokeStyle="rgba(255,255,255,.35)"; g.beginPath(); g.arc(0,0,54,0,7); g.stroke();
  g.fillStyle="#FFF8EE"; g.font=`900 60px ${F}`; g.textAlign="center"; g.textBaseline="middle"; g.fillText("冬",0,4); g.restore(); g.textAlign="left"; g.textBaseline="alphabetic";
  // layout
  const picks = pickPhotos(SH.seed), n = picks.length;
  const ROWS = SH.fmt==="4x5" ? {1:[1],2:[1,1],3:[1,2],4:[2,2],5:[2,1,2],6:[2,2,2]} : {1:[1],2:[2],3:[1,2],4:[2,2],5:[3,2],6:[3,3]};
  const rows = ROWS[n] || [1];
  const top=280, bottom=H-130, padX=60, gapY=34, gapX=34;
  const rowH = (bottom-top-gapY*(rows.length-1))/rows.length;
  let k=0;
  for(let r=0;r<rows.length;r++){
    const cols=rows[r], cw=(W-padX*2-gapX*(cols-1))/cols, y=top+r*(rowH+gapY);
    for(let ci=0;ci<cols;ci++,k++){
      const p=picks[k]; const x=padX+ci*(cw+gapX);
      const img = await loadImg(p.url);
      const rot = ((k%2?1:-1)*(1.2+((k*37)%15)/10))*Math.PI/180;
      const cap = Math.min(64, rowH*0.16), bw = 16;
      g.save(); g.translate(x+cw/2, y+rowH/2); g.rotate(rot);
      g.fillStyle="rgba(59,49,43,.18)"; rrect(g,-cw/2+6,-rowH/2+10,cw,rowH,10); g.fill();
      g.fillStyle="#FFFCF5"; rrect(g,-cw/2,-rowH/2,cw,rowH,10); g.fill(); g.lineWidth=4; g.strokeStyle=INK; g.stroke();
      const iw=cw-bw*2, ih=rowH-bw-cap-bw*0.5, ix=-cw/2+bw, iy=-rowH/2+bw;
      const s=Math.max(iw/img.naturalWidth, ih/img.naturalHeight), sw=iw/s, shh=ih/s;
      g.save(); rrect(g,ix,iy,iw,ih,6); g.clip();
      g.drawImage(img,(img.naturalWidth-sw)/2,(img.naturalHeight-shh)/2,sw,shh,ix,iy,iw,ih); g.restore();
      g.lineWidth=3; g.strokeStyle=INK; rrect(g,ix,iy,iw,ih,6); g.stroke();
      const name = SPOTS[p.spot].n, date = SPOT_DATE(p.spot);
      const fs = Math.max(20, Math.min(30, cap*0.48));
      g.fillStyle=INK; g.font=`900 ${fs}px ${F}`; g.textBaseline="middle";
      let label = name; const maxW = iw - g.measureText(date).width - 30;
      while(g.measureText(label).width > maxW && label.length>2) label = label.slice(0,-2)+"…";
      g.fillText(label, ix+4, iy+ih+cap/2+2);
      g.fillStyle=RED; g.font=`700 ${fs*0.9}px ${F}`; g.textAlign="right"; g.fillText(date, ix+iw-4, iy+ih+cap/2+2); g.textAlign="left";
      // tape
      g.save(); g.translate(0,-rowH/2); g.rotate((k%2?-1:1)*0.08); g.fillStyle = k%3===1 ? PINK : TAPE; g.fillRect(-Math.min(70,cw*0.18),-16,Math.min(140,cw*0.36),32);
      g.fillStyle="rgba(255,255,255,.25)"; for(let tx=-Math.min(70,cw*0.18);tx<Math.min(70,cw*0.18);tx+=14) g.fillRect(tx,-16,7,32); g.restore();
      g.restore();
    }
  }
  // footer
  const visited = spotsDone();
  g.fillStyle=INK; g.font=`900 30px ${F}`; g.textBaseline="alphabetic"; g.fillText(`走過 ${visited} / ${LIVE.length} 個地點`, 72, H-58);
  g.fillStyle=SOFT; g.font=`500 26px ${F}`; g.textAlign="right"; g.fillText("#2026東京冬令營", W-72, H-58); g.textAlign="left";
  g.strokeStyle=INK; g.lineWidth=3; g.setLineDash([2,10]); g.lineCap="round"; g.beginPath(); g.moveTo(72,H-104); g.lineTo(W-72,H-104); g.stroke(); g.setLineDash([]);
  return new Promise(res=>c.toBlob(res,"image/jpeg",0.9));
}
let MODAL_TRIGGER = null;
function openModal(html){
  const m=document.getElementById("modal"); if(m.dataset.open!=="true") MODAL_TRIGGER=document.activeElement;
  document.getElementById("modal-box").innerHTML=html; m.dataset.open="true";
  document.querySelector(".wrap").inert=true; document.querySelector(".nav").inert=true;
  setTimeout(()=>{ const b=m.querySelector("[data-close]"); b&&b.focus(); },60);
}
function closeModal(){ const m=document.getElementById("modal"); m.dataset.open="false";
  document.querySelector(".wrap").inert=false; document.querySelector(".nav").inert=false;
  const t=MODAL_TRIGGER; MODAL_TRIGGER=null;
  if(t && document.contains(t)) t.focus(); else { const s=document.querySelector('[data-share="open"]'); s&&s.focus(); } }
const IS_IOS = /iP(hone|ad|od)/.test(navigator.userAgent) || (navigator.platform==="MacIntel" && navigator.maxTouchPoints>1);
function canShareFiles(){
  try{ return !!(navigator.share && navigator.canShare && navigator.canShare({files:[new File([new Blob(["x"],{type:"image/jpeg"})],"t.jpg",{type:"image/jpeg"})]})); }catch(e){ return false; }
}
function shareHTML(){
  const canShare = canShareFiles();
  return `<div class="modal-hd"><h2 id="modal-title">${ico("share")}分享圖</h2><button type="button" class="btn" data-close="1" aria-label="關閉">${ico("x")}</button></div>
    <div class="fmt" role="group" aria-label="圖片比例"><button type="button" data-fmt="4x5" aria-pressed="${SH.fmt==="4x5"}">直式 4:5（IG 貼文）</button><button type="button" data-fmt="1x1" aria-pressed="${SH.fmt==="1x1"}">方形 1:1</button></div>
    <div class="share-prev" id="share-prev"><span class="wait">正在排版…</span></div>
    <div class="acts">${canShare
        ? `<button type="button" class="btn primary" data-share="send">${ico("dl")}${IS_IOS?"存到照片 App":"存到相簿或分享"}</button>`
        : `<button type="button" class="btn primary" data-share="save">${ico("dl")}下載圖片</button>`}
      <button type="button" class="btn" data-share="again">${ico("shuffle")}換一組照片</button></div>
    ${canShare?`<p class="foot"><strong>${IS_IOS?"點上面的按鈕後，在選單裡點「儲存影像」，就會直接存進「照片」App。":"點上面的按鈕後，選「儲存」或要分享的 App。"}</strong>同一個選單也可以直接分享到 IG、LINE。</p>`:""}
    <p class="foot">每個有照片的地點挑一張，最多 6 張。也可以長按上面的預覽圖，選「加入照片」。</p>
    <p class="foot" role="status" id="share-msg"></p>`;
}
async function refreshShare(){
  const box=document.getElementById("share-prev"); if(!box) return;
  box.innerHTML='<span class="wait">正在排版…</span>';
  try{ const b=await buildShare(); if(SH.url) URL.revokeObjectURL(SH.url); SH.blob=b; SH.url=URL.createObjectURL(b);
    box.innerHTML=`<img src="${SH.url}" alt="分享圖預覽：2026 東京冬令營照片拼貼">`; }
  catch(e){ box.innerHTML='<span class="wait">產生圖片時發生問題，請再試一次。</span>'; }
}
async function doShare(kind){
  if(!SH.blob) return;
  const file = new File([SH.blob], "2026-tokyo-winter.jpg", {type:"image/jpeg"});
  const msg = t => { const m=document.getElementById("share-msg"); if(m) m.textContent=t; };
  if(kind==="send"){
    /* files only: adding title/text makes iOS hide "Save Image" */
    try{ await navigator.share({files:[file]}); msg(""); return; }
    catch(e){ if(e && e.name==="AbortError") return; msg("沒辦法開啟分享選單。請長按上面的預覽圖，選「加入照片」。"); return; }
  }
  try{ const a=document.createElement("a"); a.href=SH.url; a.download="2026-tokyo-winter.jpg"; document.body.appendChild(a); a.click(); a.remove(); msg("圖片已下載。"); }catch(e){ msg("沒辦法下載。請在預覽圖上按右鍵另存圖片。"); }
}
let todoOpen = store.get("todoOpen", {0:true,1:true});
function catHTML(kind, ci, name, cd, tot, open, body){
  return `<section class="cat${cd===tot?" done":""}" data-open="${open}">
    <h2 style="margin:0"><button type="button" class="cat-hd" data-${kind}cat="${ci}" aria-expanded="${open}" aria-controls="${kind}-${ci}">
      <span class="n">${cd===tot?`<svg viewBox="0 0 24 24" aria-hidden="true" style="width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>`:ci+1}</span>
      <span class="nm"><strong>${esc(name)}</strong><span class="mini" aria-hidden="true"><i style="width:${tot?cd/tot*100:0}%"></i></span></span>
      <span class="c">${cd} / ${tot}</span>
      <svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button></h2>
    <div class="cat-body" id="${kind}-${ci}"><div><div class="in">${body}</div></div></div></section>`;
}
function renderPrep(){
  const st = store.get("todo",{});
  document.getElementById("view-prep").innerHTML = listHero("plane","待議及待辦","待議是還要討論決定的事，待辦是出發前要處理的事。",todoDone(),TODO_TOTAL)
    + `<div class="cats">${TODO.map((c,ci)=>{ const cd=c.items.filter(it=>st[it.id]).length;
        const body = `<p class="cat-hint">${esc(c.hint)}</p><div class="checks one">${c.items.map(it=>{
          const h = checkHTML("todo",it.id,it.n,it.d,null,st[it.id]);
          return it.opt ? h.replace('<span class="lb">','<span class="lb">'+tagH(it.opt,"opt")+' ') : h; }).join("")}</div>`;
        return catHTML("todo", ci, c.name, cd, c.items.length, !!todoOpen[ci], body); }).join("")}</div>
    <button class="reset" type="button" data-reset="todo">清除勾選</button><p class="foot">勾選只存在這台裝置的瀏覽器裡，不會同步給其他人。</p>`;
}
let packOpen = store.get("packOpen", {});
function renderPack(){
  const st = store.get("pack",{});
  document.getElementById("view-pack").innerHTML = listHero("suitcase","打包清單",`${PACK.length} 大類、共 ${packTotal()} 項。裝進行李就打勾；用不到的項目可以按 ✕ 刪除，也可以在每一類最下面新增自己的項目。`,packDone(),packTotal())
    + `<div class="cats-tools"><span>點大類展開或收起</span><button type="button" class="btn" data-packall="1">${PACK.some((_,ci)=>packOpen[ci])?"全部收起":"全部展開"}</button></div>
    <div class="cats">${PACK.map((c,ci)=>{ const its=packItems(ci), cd=its.filter(it=>st[it.k]).length;
        const hid=packHiddenIn(ci);
        const body = `<div class="checks">${its.map(it=>`<div class="ck-row">${checkHTML("pack",it.k,it.n,it.d||"",null,st[it.k])}<button type="button" class="ck-del" ${it.custom?`data-delcustom="${ci}|${it.custom}"`:`data-delpack="${it.k}"`} aria-label="刪除「${esc(it.n)}」">${ico("x")}</button></div>`).join("")}</div>
          ${hid?`<p class="restore-row"><button type="button" class="btn" data-restorepack="${ci}">還原這一類刪掉的 ${hid} 個預設項目</button></p>`:""}
          <form class="add-item" data-addcat="${ci}"><label class="sr" for="add-${ci}">新增到「${esc(c.name)}」</label>
            <input type="text" id="add-${ci}" maxlength="40" placeholder="例如：暖暖包" autocomplete="off" enterkeyhint="done" aria-describedby="addmsg-${ci}"><button type="submit" class="btn">＋ 新增</button></form>
          <p class="add-msg" id="addmsg-${ci}" role="status"></p>`;
        return catHTML("pack", ci, c.name, cd, its.length, !!packOpen[ci], body); }).join("")}</div>
    <div class="card tips-card"><h2>${ico("note")}溫馨提醒：行李限重</h2>
      <div class="lug"><div><b>去程 12/13 JX314</b><span>託運 1 件（23 公斤）・手提 1 件（7 公斤）</span></div>
      <div><b>回程 12/19 JX315</b><span>託運 2 件（每件 23 公斤）・手提 1 件（7 公斤）</span></div></div>
      <p class="foot">回程可以多託運一件，伴手禮可以留到最後幾天再買。</p></div>
    <button class="reset" type="button" data-reset="pack">清除勾選</button><p class="foot">勾選、刪除和自己新增的項目只存在這台裝置的瀏覽器裡，不會同步給其他人，也不會影響別人的清單。</p>`;
}

/* ---------- nav & routing ---------- */
const NAV = [["home","home","首頁"],["trip","cal","行程"],["spots","pin","行程確認"],["prep","clip","待議待辦"],["pack","bag","打包"]];
document.getElementById("nav").innerHTML = NAV.map(n=>`<a href="#${n[0]}" data-v="${n[0]}">${ico(n[1])}<span>${n[2]}</span></a>`).join("");
const RENDER = {home:renderHome, trip:renderTrip, spots:renderSpots, prep:renderPrep, pack:renderPack};
let ROUTED = false;
function route(){
  let v = (location.hash||"").replace("#",""); if(!RENDER[v]) v="home";
  Object.keys(RENDER).forEach(n=>{ const el=document.getElementById("view-"+n); el.classList.toggle("active", n===v); if(n!==v) el.innerHTML=""; });
  document.querySelectorAll(".nav a").forEach(a=>{ if(a.dataset.v===v) a.setAttribute("aria-current","page"); else a.removeAttribute("aria-current"); });
  RENDER[v](); window.scrollTo(0,0);
  const NAMES={home:"首頁",trip:"行程",spots:"行程確認清單",prep:"待議及待辦",pack:"打包清單"};
  document.title = v==="home" ? "2026 東京冬令營" : NAMES[v]+" · 2026 東京冬令營";
  if(ROUTED){ const h=document.querySelector("#view-"+v+" h1"); if(h){ h.setAttribute("tabindex","-1"); h.focus({preventScroll:true}); } }
  ROUTED = true;
}
window.addEventListener("hashchange", route);

document.addEventListener("click", e=>{
  const go=e.target.closest("[data-goday]");
  if(go){ curDay=go.dataset.goday; store.set("day",curDay); if(location.hash==="#trip") route(); else location.hash="trip"; return; }
  const td=e.target.closest("[data-today]");
  if(td){ curDay=todayDayId(); store.set("day",curDay); renderTrip(); toFirstItem(); return; }
  const ch=e.target.closest("[data-day]");
  if(ch){ curDay=ch.dataset.day; store.set("day",curDay); renderTrip(); toFirstItem(); return; }
  const nh=e.target.closest(".near-hd");
  if(nh){ const w=nh.parentElement, open=w.dataset.open!=="true"; w.dataset.open=open; nh.setAttribute("aria-expanded",open); return; }
  const sx=e.target.closest(".shx-head");
  if(sx){ const w=sx.parentElement, open=w.dataset.open!=="true"; w.dataset.open=open; sx.setAttribute("aria-expanded",open); return; }
  const tc=e.target.closest("[data-todocat]");
  if(tc){ const ci=+tc.dataset.todocat, sec=tc.closest(".cat"), open=sec.dataset.open!=="true";
    sec.dataset.open=open; tc.setAttribute("aria-expanded",open); todoOpen[ci]=open; store.set("todoOpen",todoOpen); return; }
  const dc=e.target.closest("[data-delcustom],[data-delpack]");
  if(dc && dc.dataset.confirm!=="1"){ const nm=dc.getAttribute("aria-label").replace(/^刪除/,"");
    dc.dataset.confirm="1"; dc.classList.add("confirm"); dc.setAttribute("aria-label","再按一次確認刪除"+nm); dc.innerHTML=ico("x")+"<span>再按一次刪除</span>";
    clearTimeout(dc._t); dc._t=setTimeout(()=>{ dc.dataset.confirm=""; dc.classList.remove("confirm"); dc.setAttribute("aria-label","刪除"+nm); dc.innerHTML=ico("x"); },4000); return; }
  if(dc && dc.dataset.delpack){ const k=dc.dataset.delpack, ci=k.split("-")[0]; const h=packHidden(); h[k]=true; store.set("packHidden",h);
    const st=store.get("pack",{}); delete st[k]; store.set("pack",st); renderPack();
    const f=document.getElementById("add-"+ci); if(f) f.focus(); return; }
  const rp=e.target.closest("[data-restorepack]");
  if(rp){ const ci=rp.dataset.restorepack, h=packHidden(); Object.keys(h).forEach(k=>{ if(k.split("-")[0]===ci) delete h[k]; }); store.set("packHidden",h); renderPack();
    const f=document.getElementById("add-"+ci); if(f) f.focus(); return; }
  if(dc){ const [ci,id]=dc.dataset.delcustom.split("|"); const pc=packCustom(); pc[ci]=(pc[ci]||[]).filter(c=>String(c.id)!==id); store.set("packCustom",pc);
    const st=store.get("pack",{}); delete st[ci+"-c"+id]; store.set("pack",st); renderPack();
    const f=document.getElementById("add-"+ci); if(f) f.focus(); return; }
  const ct=e.target.closest("[data-packcat]");
  if(ct){ const ci=+ct.dataset.packcat, sec=ct.closest(".cat"), open=sec.dataset.open!=="true";
    sec.dataset.open=open; ct.setAttribute("aria-expanded",open); packOpen[ci]=open; store.set("packOpen",packOpen);
    const all=document.querySelector("[data-packall]"); if(all) all.textContent = PACK.some((_,i)=>packOpen[i])?"全部收起":"全部展開"; return; }
  const pa=e.target.closest("[data-packall]");
  if(pa){ const open = !PACK.some((_,i)=>packOpen[i]); PACK.forEach((_,i)=>packOpen[i]=open); store.set("packOpen",packOpen);
    document.querySelectorAll("#view-pack .cat").forEach(sec=>{ sec.dataset.open=open; sec.querySelector(".cat-hd").setAttribute("aria-expanded",open); });
    pa.textContent = open?"全部收起":"全部展開"; return; }
  const cl=e.target.closest("[data-close]");
  if(cl){ closeModal(); return; }
  const sb=e.target.closest("[data-share]");
  if(sb){ const k=sb.dataset.share;
    if(k==="open"){ SH.seed=0; openModal(shareHTML()); refreshShare(); }
    else if(k==="again"){ SH.seed++; refreshShare(); }
    else doShare(k); return; }
  const fm=e.target.closest("[data-fmt]");
  if(fm){ SH.fmt=fm.dataset.fmt; document.querySelectorAll("[data-fmt]").forEach(b=>b.setAttribute("aria-pressed", b===fm)); refreshShare(); return; }
  const ph=e.target.closest("[data-photo]");
  if(ph){ const p=PH.list.find(x=>x.id===ph.dataset.photo); if(!p) return;
    openModal(`<div class="modal-hd"><h2 id="modal-title">${esc(SPOTS[p.spot].n)}</h2><button type="button" class="btn" data-close="1" aria-label="關閉">${ico("x")}</button></div>
      <div class="lb-img"><img src="${p.url}" alt="${esc(SPOTS[p.spot].n)} 的照片"></div>
      <div class="acts"><button type="button" class="btn" data-del="${p.id}">${ico("trash")}刪除這張</button></div>`); return; }
  const dl=e.target.closest("[data-del]");
  if(dl){ if(dl.dataset.confirm!=="1"){ dl.dataset.confirm="1"; dl.lastChild.textContent="再按一次確認刪除"; return; } closeModal(); delPhoto(dl.dataset.del); return; }
  const sg=e.target.closest(".seg [data-g]");
  if(sg){ curGroup=sg.dataset.g; store.set("group",curGroup); const g=document.querySelector(".groups"); if(g) g.dataset.show=curGroup;
    document.querySelectorAll(".seg [data-g]").forEach(b=>b.setAttribute("aria-pressed", b.dataset.g===curGroup)); return; }
  const rs=e.target.closest("[data-reset]");
  if(rs){ const k=rs.dataset.reset;
    if(rs.dataset.confirm!=="1"){ const n=Object.values(store.get(k,{})).filter(Boolean).length; if(!n) return;
      rs.dataset.confirm="1"; rs.classList.add("danger"); rs.textContent=`再按一次，清除全部 ${n} 個勾選${k==="spots"?"（照片會保留）":""}`;
      clearTimeout(rs._t); rs._t=setTimeout(()=>{ rs.dataset.confirm=""; rs.classList.remove("danger"); rs.textContent="清除勾選"; },5000); return; }
    store.set(k,{}); ({todo:renderPrep}[k]||RENDER[k])(); }
});
document.addEventListener("submit", e=>{
  const f=e.target.closest("form[data-addcat]"); if(!f) return; e.preventDefault();
  const inp=f.querySelector("input"), n=inp.value.trim(), ci=f.dataset.addcat, msg=document.getElementById("addmsg-"+ci);
  const warn = t => { msg.textContent=t; inp.setAttribute("aria-invalid","true"); inp.focus(); };
  if(!n){ warn("請先輸入項目名稱，再按新增。"); return; }
  if(packItems(+ci).some(it=>it.n.trim().toLowerCase()===n.toLowerCase())){ warn(`「${n}」已經在這一類裡了，換個名稱或直接勾選它。`); inp.select(); return; }
  const pc=packCustom(); (pc[ci]=pc[ci]||[]).push({id:Date.now().toString(36), n}); store.set("packCustom",pc);
  packOpen[ci]=true; store.set("packOpen",packOpen); renderPack();
  const again=document.getElementById("add-"+ci); if(again) again.focus();
});
document.addEventListener("input", e=>{
  const inp=e.target.closest("form[data-addcat] input"); if(!inp || !inp.hasAttribute("aria-invalid")) return;
  inp.removeAttribute("aria-invalid"); const m=document.getElementById(inp.getAttribute("aria-describedby")); if(m) m.textContent="";
});
document.addEventListener("keydown", e=>{ if(e.key==="Escape" && document.getElementById("modal").dataset.open==="true") closeModal(); });
document.addEventListener("change", e=>{
  const up=e.target.closest("input[data-up]");
  if(up){ const files=[...up.files]; if(files.length) addPhotos(+up.dataset.up, files); return; }
  const cb=e.target.closest("input[data-key]"); if(!cb) return;
  const key=cb.dataset.key, st=store.get(key,{}); st[cb.dataset.i]=cb.checked; store.set(key,st);
  const v=(location.hash||"#home").replace("#",""); (RENDER[v]||RENDER.home)();
  const again=document.getElementById(cb.id); if(again) again.focus();
});

/* ---------- theme ---------- */
const root=document.documentElement;
const isDark=()=>{ const t=root.getAttribute("data-theme"); if(t) return t==="dark"; return !!(window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches); };
function paintTheme(){ const d=isDark(); document.getElementById("themeIco").innerHTML=ICON[d?"sun":"moon"]; document.getElementById("themeLabel").textContent=d?"淺色模式":"深色模式"; }
const saved=store.get("theme",null); if(saved==="dark"||saved==="light") root.setAttribute("data-theme",saved);
document.getElementById("themeBtn").addEventListener("click",()=>{ const nx=isDark()?"light":"dark"; root.setAttribute("data-theme",nx); store.set("theme",nx); paintTheme(); });
if(window.matchMedia){ const mq=window.matchMedia("(prefers-color-scheme: dark)"); if(mq.addEventListener) mq.addEventListener("change",paintTheme); }
paintTheme();
route();
loadPhotos().then(()=>{ if((location.hash||"")==="#spots") renderSpots(); });
})();
</script>
</body>
</html>
'''

html = (TEMPLATE.replace("__LIGHT__", LIGHT).replace("__DARK__", DARK).replace("__FILLS__", fills)
        .replace("__DEFS__", DEFS).replace("__ART__", art_json).replace("__ICON__", icon_json))
open(OUT, "w").write(html)
print(OUT, len(html))
