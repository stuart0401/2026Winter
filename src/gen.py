import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from illus import ALL, DEFS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_artboards")  # 舊設計稿輸出，網站建置用不到

LIGHT = ("--paper:#F3ECDF;--paper2:#EADFCB;--card:#FFFBF3;--ink:#3B312B;--soft:#6F5F55;--line:#D6C6AE;--chip:#EEE3D0;"
         "--accent:#A8452A;--accentbg:#B44A28;--onaccent:#FFF8EE;--pine:#3D705C;--pinebg:#3F6E5A;--afill:#B04A2A;--bfill:#2F6797;--tape:#E9B949;--a:#C9542F;--b:#33709F;"
         "--olc:#3B312B;--hlc:#FFFFFF;--sky:#C9DFE7;--sky2:#E2EEEA;--night:#2E3A64;--night2:#3A4878;--cloud:#FFFDF7;--snow:#FFFFFF;"
         "--sun:#F2C15E;--glow:#FFD88A;--brown:#A8764D;--pinef:#4C7C66;--green:#8DB487;--leaf:#6B9A74;--stone:#C3B9A9;--stone2:#A39886;"
         "--brick:#BC6447;--blue:#7EA6C4;--yellow:#EDBE5C;--ground:#E6D9BF;--pink:#F0B6A4;--wood:#D9A774;--red:#D45F3A;--water:#8FBCCE;--copper:#C47F46;")
DARK = ("--paper:#161C30;--paper2:#1D2440;--card:#212A45;--ink:#F1E8D8;--soft:#BAB0A1;--line:#36406A;--chip:#2C3557;"
        "--accent:#F29A75;--accentbg:#B44A28;--onaccent:#FFF8EE;--pine:#8CC2A6;--pinebg:#3F7461;--afill:#B04A2A;--bfill:#2F6797;--tape:#C99A3A;--a:#F0916B;--b:#8DB9E0;"
        "--olc:#0E1326;--hlc:#FFF4DC;--sky:#34426E;--sky2:#3E4D7C;--night:#10162B;--night2:#1A2240;--cloud:#55618F;--snow:#DCE3F0;"
        "--sun:#F4E1A4;--glow:#FFD88A;--brown:#8E6B4E;--pinef:#3C6B58;--green:#6D9C7C;--leaf:#4F7F62;--stone:#8C8894;--stone2:#6D6A78;"
        "--brick:#B0664F;--blue:#6E92BA;--yellow:#E3BB62;--ground:#3A4262;--pink:#C58C82;--wood:#B08A62;--red:#D16D50;--water:#4A6E8F;--copper:#C0834F;color-scheme:dark;")

FILLS = ["sky","sky2","night","night2","cloud","snow","sun","glow","brown","green","leaf","stone","stone2","brick","blue","yellow","ground","pink","wood","red","water","copper"]
HELMET = ('<helmet>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&amp;family=Roboto:wght@400;500;700;900&amp;display=swap" rel="stylesheet">\n<style>\n'
    'body{margin:0}\n'
    f'.t-light{{{LIGHT}}}\n.t-dark{{{DARK}}}\n'
    + ''.join(f'.f-{c}{{fill:var(--{c})}}' for c in FILLS) +
    '.f-pine{fill:var(--pinef)}.f-ink{fill:var(--olc)}\n'
    '.ol{fill:none;stroke:var(--olc);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}.ol.thin{stroke-width:1.7}.ol.xthin{stroke-width:1.1}.ol.dash{stroke-dasharray:6 7}\n'
    '.hl{fill:none;stroke:var(--hlc);stroke-width:2.6;stroke-linecap:round;opacity:.75}.sh{fill:var(--olc);opacity:.13}.hatch{stroke:var(--olc);stroke-width:1.2;opacity:.35}.groove{fill:none;stroke:var(--stone);stroke-width:1;opacity:.55}\n'
    'a{color:var(--accent)}a:hover{color:var(--ink)}\n'
    'button:focus-visible,a:focus-visible,input:focus-visible+span{outline:3px solid var(--accent);outline-offset:3px}\n'
    '</style>\n</helmet>')

FONT = "font-family: 'Roboto', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif"

def page(title, body, preview, dark_default=False, fluid=True):
    props = json.dumps({"dark": {"editor": "boolean", "default": dark_default, "section": "主題"},
                        "$preview": {"width": preview[0], "height": preview[1]}}, ensure_ascii=False)
    dd = "true" if dark_default else "false"
    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
{HELMET}
{DEFS}
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{props}'>
class Component extends DCLogic {{
  renderVals() {{
    const dark = this.props.dark ?? {dd};
    return {{ themeClass: dark ? 't-dark' : 't-light', isDark: dark, isLight: !dark }};
  }}
}}
</script>
</body>
</html>
'''

# ---------- icons (stroke) ----------
ICON = {
 "home": '<path d="M3 11 12 4l9 7"></path><path d="M5.5 9.5V20h13V9.5"></path><path d="M10 20v-5h4v5"></path>',
 "cal": '<rect x="3.5" y="5" width="17" height="15" rx="3"></rect><path d="M3.5 10h17M8 3v4M16 3v4"></path>',
 "pin": '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"></path><path d="m9.5 10 2 2 3.5-3.5"></path>',
 "clip": '<rect x="6" y="7" width="12" height="14" rx="2.5"></rect><path d="M9.5 7V4.5h5V7M9.5 12h5M9.5 16h3"></path>',
 "bag": '<rect x="4" y="8" width="16" height="12" rx="3"></rect><path d="M9 8V5.5h6V8M4 13h16M10 13v2h4v-2"></path>',
 "train": '<rect x="6" y="3.5" width="12" height="14" rx="3"></rect><path d="M6 11h12M9 21l1.5-3.5M15 21l-1.5-3.5"></path><circle cx="9" cy="14.3" r=".6"></circle><circle cx="15" cy="14.3" r=".6"></circle>',
 "bus": '<rect x="4.5" y="4" width="15" height="13" rx="2.5"></rect><path d="M4.5 10h15M7.5 20v-3M16.5 20v-3"></path><circle cx="8" cy="13.6" r=".6"></circle><circle cx="16" cy="13.6" r=".6"></circle>',
 "bowl": '<path d="M4 11h16a8 8 0 0 1-16 0z"></path><path d="M9 4l2 5M15 3l-2 6"></path>',
 "taxi": '<path d="M5 16v-4l2-5h10l2 5v4z"></path><path d="M5 16v2M19 16v2M10 4.5h4"></path><circle cx="8" cy="13" r=".7"></circle><circle cx="16" cy="13" r=".7"></circle>',
 "moon": '<path d="M19.5 14.5A8 8 0 0 1 9.5 4.5a8 8 0 1 0 10 10z"></path>',
 "sun": '<circle cx="12" cy="12" r="4.2"></circle><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.2 5.2l1.6 1.6M17.2 17.2l1.6 1.6M5.2 18.8l1.6-1.6M17.2 6.8l1.6-1.6"></path>',
 "bed": '<path d="M3 18V7M3 14h18v4M21 14v-2.5A3.5 3.5 0 0 0 17.5 8H11v6"></path><circle cx="7" cy="11" r="1.8"></circle>',
 "note": '<path d="M12 8v5M12 16.5v.1"></path><circle cx="12" cy="12" r="9"></circle>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"></path>',
}
def icon(name, size=22, color="currentColor", sw=2.1):
    return (f'<svg viewBox="0 0 24 24" aria-hidden="true" style="width: {size}px; height: {size}px; flex: none; fill: none; stroke: {color}; '
            f'stroke-width: {sw}; stroke-linecap: round; stroke-linejoin: round">{ICON[name]}</svg>')

def art(key, ratio="16 / 10", extra=""):
    return f'<div style="aspect-ratio: {ratio}; overflow: hidden; background: var(--sky); {extra}">{ALL[key]()}</div>'

def plate(key, ratio="16 / 10", pad=10, radius=22, shadow=True):
    sh = "box-shadow: 0 6px 0 var(--line);" if shadow else ""
    return (f'<div style="background: var(--card); border: 2.5px solid var(--ink); border-radius: {radius}px; padding: {pad}px; {sh}">'
            f'<div style="border: 2px solid var(--ink); border-radius: {max(radius-8,8)}px; overflow: hidden">{art(key, ratio)}</div></div>')

def tape(top, left, rot, w=88, color="var(--tape)"):
    return (f'<div aria-hidden="true" style="position: absolute; top: {top}; left: {left}; width: {w}px; height: 26px; transform: rotate({rot}deg); '
            f'background-color: {color}; opacity: 0.82; background-image: repeating-linear-gradient(90deg, rgba(255,255,255,0.28) 0 6px, transparent 6px 12px); '
            f'border-left: 2px dashed rgba(0,0,0,0.12); border-right: 2px dashed rgba(0,0,0,0.12)"></div>')

def seal(top, bottom, size=64, bg="var(--accentbg)", rot=-6):
    return (f'<div style="width: {size}px; height: {size}px; flex: none; border-radius: 50%; background: {bg}; color: var(--onaccent); border: 2.5px solid var(--ink); '
            f'display: flex; flex-direction: column; align-items: center; justify-content: center; transform: rotate({rot}deg); box-shadow: inset 0 0 0 4px rgba(255,255,255,0.22); line-height: 1">'
            f'<span style="font-size: {round(size*0.38)}px; font-weight: 900; letter-spacing: -0.02em; font-variant-numeric: tabular-nums">{top}</span>'
            f'<span style="font-size: {max(10, round(size*0.16))}px; font-weight: 700; margin-top: 3px; letter-spacing: 0.08em">{bottom}</span></div>')

def theme_btn(icon_only=False):
    lab_l = "" if icon_only else '<span>深色</span>'
    lab_d = "" if icon_only else '<span>淺色</span>'
    pad = "8px" if icon_only else "8px 16px"
    return (f'<button type="button" aria-label="切換深色或淺色模式" style="display: flex; align-items: center; gap: 8px; min-height: 44px; min-width: 44px; justify-content: center; padding: {pad}; '
            f'border: 2px solid var(--ink); background: var(--card); color: var(--ink); border-radius: 999px; font: inherit; font-size: 14px; font-weight: 700; cursor: pointer; box-shadow: 0 3px 0 var(--line)">'
            f'<sc-if value="{{{{isLight}}}}" hint-placeholder-val="{{{{true}}}}">{icon("moon", 18)}{lab_l}</sc-if>'
            f'<sc-if value="{{{{isDark}}}}" hint-placeholder-val="{{{{false}}}}">{icon("sun", 18)}{lab_d}</sc-if></button>')

def brand(small=False):
    s = 38 if not small else 34
    return (f'<div style="display: flex; align-items: center; gap: 12px">'
            f'<div aria-hidden="true" style="width: {s}px; height: {s}px; border-radius: 50%; background: var(--accentbg); border: 2.5px solid var(--ink); color: var(--onaccent); display: grid; place-items: center; font-weight: 900; font-size: {s*0.45:.0f}px; transform: rotate(-8deg)">冬</div>'
            f'<div style="display: flex; flex-direction: column; line-height: 1.2"><span style="font-weight: 900; font-size: {15 if small else 17}px; letter-spacing: 0.04em">2026 東京冬令營</span>'
            + ('' if small else '<span style="font-size: 12px; color: var(--soft); letter-spacing: 0.14em; font-weight: 500">TOKYO · KARUIZAWA</span>') + '</div></div>')

NAV = [("home","首頁"),("cal","行程"),("pin","行程確認"),("clip","出發前"),("bag","打包")]
def nav(active, fixed_bottom=None):
    items = ''
    for i, (ic, lab) in enumerate(NAV):
        on = i == active
        st = ("background: var(--accentbg); color: var(--onaccent); box-shadow: inset 0 0 0 2px var(--ink);" if on else "color: var(--soft);")
        cur = ' aria-current="page"' if on else ''
        items += (f'<a href="#"{cur} style="display: flex; flex-direction: column; align-items: center; gap: 2px; padding: 7px 2px; min-height: 44px; border-radius: 20px; '
                  f'text-decoration: none; font-size: 12px; font-weight: 700; white-space: nowrap; {st}">{icon(ic, 22)}<span>{lab}</span></a>')
    pos = (f"position: absolute; left: 12px; right: 12px; bottom: {fixed_bottom}px;" if fixed_bottom is not None
           else "position: sticky; bottom: 18px; margin: 0 auto; width: calc(100% - 32px);")
    return (f'<nav aria-label="主選單" style="{pos} max-width: 640px; z-index: 5; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 4px; padding: 6px; '
            f'background: var(--card); border: 2.5px solid var(--ink); border-radius: 28px; box-shadow: 0 5px 0 var(--line), 0 14px 34px rgba(20,16,12,0.18)">{items}</nav>')

def root_open(extra=""):
    return (f'<div class="{{{{themeClass}}}}" style="{FONT}; background-color: var(--paper); color: var(--ink); '
            f'background-image: radial-gradient(circle at 1px 1px, var(--line) 1px, transparent 0); background-size: 18px 18px; line-height: 1.65; {extra}">')

def tag(text, kind="chip"):
    bg = {"chip": "var(--chip)", "spot": "color-mix(in srgb, var(--pinebg) 22%, var(--card))", "opt": "color-mix(in srgb, var(--yellow) 40%, var(--card))",
          "a": "color-mix(in srgb, var(--a) 22%, var(--card))", "b": "color-mix(in srgb, var(--b) 24%, var(--card))"}[kind]
    return f'<span style="display: inline-flex; align-items: center; font-size: 13px; font-weight: 500; padding: 3px 12px; border-radius: 999px; background: {bg}; color: var(--ink)">{text}</span>'

def section_title(t, sub=""):
    s = f'<span style="font-size: 14px; color: var(--soft); font-weight: 500">{sub}</span>' if sub else ''
    return (f'<div style="display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap">'
            f'<h2 style="margin: 0; font-size: 24px; font-weight: 900; letter-spacing: 0.04em; display: flex; align-items: center; gap: 12px; text-wrap: balance">'
            f'<span aria-hidden="true" style="width: 22px; height: 6px; border-radius: 3px; background: var(--accentbg); display: inline-block"></span>{t}</h2>{s}</div>')

# ======================= artboards =======================
def main_home():
    days = [("13","日","抵達日","成田 → 銀座","var(--accentbg)"),("14","一","輕井澤","舊輕銀座・星野區","var(--pinebg)"),
            ("15","二","回東京","英迪格早晨・東京車站","var(--pinebg)"),("16","三","分組日","A 入管局・B 明治神宮","var(--b)"),
            ("17","四","東大＋teamLab","本鄉・麻布台Hills","var(--accentbg)"),("18","五","彈性日","補行程・伊東屋","var(--accentbg)"),
            ("19","六","返程","成田 → 台中","var(--accentbg)")]
    tiles = ''
    for i, (d, w, t, s, c) in enumerate(days):
        tp = tape("-10px", "50%", -4 if i % 2 else 5, 54) if d == "16" else ''
        tiles += (f'<a href="#" style="position: relative; display: flex; flex-direction: column; gap: 10px; padding: 16px; text-decoration: none; color: var(--ink); '
                  f'background: var(--card); border: 2.5px solid var(--ink); border-radius: 20px; box-shadow: 0 5px 0 var(--line)">{tp}'
                  f'<div style="display: flex; align-items: center; justify-content: space-between">{seal(d, "12月", 56, c, -5 if i % 2 else 4)}'
                  f'<span style="font-size: 13px; font-weight: 700; color: var(--soft)">（{w}）</span></div>'
                  f'<div style="display: flex; flex-direction: column; line-height: 1.4"><span style="font-weight: 900; font-size: 17px">{t}</span>'
                  f'<span style="font-size: 13px; color: var(--soft)">{s}</span></div></a>')
    route = ''
    stops = ["台中", "東京", "輕井澤", "東京", "台中"]
    for i, s in enumerate(stops):
        route += f'<span style="font-weight: 700; font-size: 14px">{s}</span>'
        if i < len(stops) - 1:
            route += '<span aria-hidden="true" style="flex: 1; min-width: 18px; border-top: 2.5px dotted var(--soft)"></span>'

    def boarding(no, date, dir_, t1, a1, t2, a2):
        return (f'<div style="flex: 1 1 380px; display: flex; background: var(--card); border: 2.5px solid var(--ink); border-radius: 22px; box-shadow: 0 5px 0 var(--line); overflow: hidden">'
                f'<div style="flex: 1; padding: 20px 24px; display: flex; flex-direction: column; gap: 14px">'
                f'<div style="display: flex; justify-content: space-between; align-items: center"><span style="font-weight: 900; font-size: 20px; letter-spacing: 0.06em">{no}</span>{tag("星宇航空")}</div>'
                f'<div style="display: grid; grid-template-columns: auto minmax(0, 1fr) auto; align-items: center; gap: 14px">'
                f'<div><div style="font-size: 34px; font-weight: 700; line-height: 1; font-variant-numeric: tabular-nums">{t1}</div><div style="font-size: 13px; color: var(--soft); margin-top: 6px">{a1}</div></div>'
                f'<div aria-hidden="true" style="position: relative; border-top: 2.5px dashed var(--soft); height: 0"><div style="position: absolute; left: 50%; top: -15px; transform: translateX(-50%); background: var(--card); padding: 0 6px; color: var(--accent)"><svg viewBox="0 0 24 24" style="width: 24px; height: 24px; fill: var(--accentbg); stroke: var(--ink); stroke-width: 1.4; stroke-linejoin: round"><path d="M2.5 13.5 21 7.5c1.2-.4 1.9.9.8 1.6L6 17.5 3.5 17z M11 11l-2.5-6 2-.6 5 4.8 M10 15.4l-1 4.6 2 .2 3.6-6.7"></path></svg></div></div>'
                f'<div style="text-align: right"><div style="font-size: 34px; font-weight: 700; line-height: 1; font-variant-numeric: tabular-nums">{t2}</div><div style="font-size: 13px; color: var(--soft); margin-top: 6px">{a2}</div></div></div></div>'
                f'<div aria-hidden="true" style="width: 0; border-left: 2.5px dashed var(--line); margin: 14px 0"></div>'
                f'<div style="width: 112px; flex: none; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; padding: 16px 8px; background: var(--chip)">'
                f'<span style="font-size: 12px; font-weight: 700; letter-spacing: 0.12em; color: var(--soft)">{dir_}</span>'
                f'<span style="font-size: 30px; font-weight: 900; line-height: 1; font-variant-numeric: tabular-nums">{date}</span></div></div>')

    def quick(ic, t, d, n, total):
        pct = round(n / total * 100)
        return (f'<a href="#" style="flex: 1 1 260px; display: flex; flex-direction: column; gap: 12px; padding: 18px 20px; text-decoration: none; color: var(--ink); background: var(--card); border: 2.5px solid var(--ink); border-radius: 20px; box-shadow: 0 5px 0 var(--line)">'
                f'<div style="display: flex; align-items: center; gap: 10px"><span style="width: 40px; height: 40px; border-radius: 12px; background: var(--chip); display: grid; place-items: center">{icon(ic, 22)}</span>'
                f'<div style="display: flex; flex-direction: column; line-height: 1.3"><span style="font-weight: 900; font-size: 16px">{t}</span><span style="font-size: 13px; color: var(--soft)">{d}</span></div></div>'
                f'<div style="display: flex; align-items: center; gap: 10px"><div style="flex: 1; height: 12px; border: 2px solid var(--ink); border-radius: 999px; overflow: hidden; background: var(--paper)"><div style="width: {pct}%; height: 100%; background: var(--pinebg)"></div></div>'
                f'<span style="font-size: 14px; font-weight: 700; font-variant-numeric: tabular-nums">{n} / {total}</span></div></a>')

    def stay(key, name, when, detail):
        return (f'<div style="flex: 1 1 380px; display: flex; gap: 16px; align-items: center; padding: 12px; background: var(--card); border: 2.5px solid var(--ink); border-radius: 22px; box-shadow: 0 5px 0 var(--line)">'
                f'<div style="width: 150px; flex: none; border: 2px solid var(--ink); border-radius: 14px; overflow: hidden">{art(key)}</div>'
                f'<div style="display: flex; flex-direction: column; gap: 4px; line-height: 1.45"><span style="font-weight: 900; font-size: 17px">{name}</span>'
                f'<span style="font-size: 14px; color: var(--ink)">{when}</span><span style="font-size: 13px; color: var(--soft)">{detail}</span></div></div>')

    body = (root_open("min-height: 100%;")
        + '<div style="max-width: 1200px; margin: 0 auto; padding: 28px 32px 48px; display: flex; flex-direction: column; gap: 52px">'
        + f'<header style="display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap">{brand()}{theme_btn()}</header>'
        # hero
        + '<section style="position: relative; display: flex; flex-wrap: wrap; gap: 40px; align-items: center">'
        + '<div style="position: relative; flex: 1 1 560px; min-width: 0">' + tape("-12px", "36px", -6, 104) + tape("-10px", "calc(100% - 140px)", 5, 96, "var(--pink)")
        + plate("hero", "16 / 10", 14, 30) + '</div>'
        + '<div style="flex: 1 1 380px; min-width: 0; display: flex; flex-direction: column; gap: 22px">'
        + '<div style="display: flex; gap: 8px; flex-wrap: wrap">' + tag("12.13 SUN — 12.19 SAT") + tag("6 晚 7 天", "opt") + '</div>'
        + '<h1 style="margin: 0; line-height: 1.12; text-wrap: balance"><span style="display: block; font-size: 26px; font-weight: 700; letter-spacing: 0.18em; color: var(--accent)">2026 WINTER</span>'
        + '<span style="display: block; font-size: 60px; font-weight: 900; letter-spacing: 0.04em">東京冬令營</span></h1>'
        + '<p style="margin: 0; font-size: 17px; color: var(--soft); max-width: 34em">東京車站出發，到輕井澤住一晚看雪中教會，再回東京逛神宮、美術館和銀座。</p>'
        + '<div style="display: flex; align-items: center; gap: 18px">' + seal("27", "DAYS", 104, "var(--accentbg)", -8)
        + '<div style="display: flex; flex-direction: column; line-height: 1.4"><span style="font-size: 14px; color: var(--soft)">距離出發還有</span><span style="font-size: 22px; font-weight: 900">27 天</span></div></div>'
        + f'<div style="display: flex; align-items: center; gap: 10px; padding: 12px 18px; border: 2px dashed var(--ink); border-radius: 16px">{route}</div>'
        + '</div></section>'
        # flights
        + '<section style="display: flex; flex-direction: column; gap: 18px">' + section_title("班機", "星宇冬季班表，請以電子機票為準")
        + '<div style="display: flex; flex-wrap: wrap; gap: 20px">'
        + boarding("JX314", "12/13", "去程", "09:15", "台中 RMQ", "13:25", "成田 NRT T2")
        + boarding("JX315", "12/19", "回程", "14:25", "成田 NRT T2", "17:55", "台中 RMQ") + '</div></section>'
        # days
        + '<section style="display: flex; flex-direction: column; gap: 18px">' + section_title("每日行程", "點一天直接打開那天的行程")
        + f'<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 16px">{tiles}</div></section>'
        # quick lists
        + '<section style="display: flex; flex-direction: column; gap: 18px">' + section_title("清單")
        + '<div style="display: flex; flex-wrap: wrap; gap: 16px">' + quick("pin", "行程確認清單", "地圖清單 17 個地點", 0, 17)
        + quick("clip", "出發前確認清單", "出發前要先處理的事", 2, 6) + quick("bag", "打包清單", "7 大類", 18, 69) + '</div></section>'
        # stays
        + '<section style="display: flex; flex-direction: column; gap: 18px">' + section_title("住宿")
        + '<div style="display: flex; flex-wrap: wrap; gap: 20px">'
        + stay("ginza", "TOSEI酒店 可可尼築地銀座", "12/13、12/15–12/18・共 5 晚", "近東銀座站，Access 特急直達成田")
        + stay("firepit", "輕井澤英迪格酒店", "12/14・1 晚", "check-in 15:00・check-out 11:00") + '</div></section>'
        + '<p style="margin: 0; font-size: 13px; color: var(--soft)">營業時間與交通皆為行前查詢資料，出發前請再確認一次。</p>'
        + '</div>' + nav(0) + '<div style="height: 24px"></div></div>')
    return page("首頁 · 2026 東京冬令營", body, (1280, 2250))

def spot_card(t, title, note, key, tags=(), dashed=False):
    bd = "dashed" if dashed else "solid"
    tg = ''.join(tag(*x) if isinstance(x, tuple) else tag(x, "spot") for x in tags)
    return (f'<article style="display: flex; flex-wrap: wrap; gap: 18px; align-items: center; padding: 12px; background: var(--card); border: 2.5px {bd} var(--ink); border-radius: 22px; box-shadow: 0 5px 0 var(--line)">'
            f'<div style="flex: 1 1 220px; max-width: 260px; border: 2px solid var(--ink); border-radius: 14px; overflow: hidden">{art(key)}</div>'
            f'<div style="flex: 999 1 240px; min-width: 0; display: flex; flex-direction: column; gap: 6px; padding: 4px 8px 4px 0">'
            f'<h3 style="margin: 0; font-size: 19px; font-weight: 900; line-height: 1.35; text-wrap: balance">{title}</h3>'
            f'<p style="margin: 0; font-size: 15px; color: var(--soft); max-width: 36em">{note}</p>'
            f'<div style="display: flex; gap: 6px; flex-wrap: wrap; margin-top: 4px">{tg}</div></div></article>')

def move_row(ic, title, note):
    return (f'<div style="display: flex; align-items: center; gap: 14px; padding: 12px 16px; border: 2px dashed var(--soft); border-radius: 18px; background: color-mix(in srgb, var(--card) 55%, transparent)">'
            f'<span style="width: 40px; height: 40px; flex: none; border-radius: 50%; background: var(--chip); display: grid; place-items: center">{icon(ic, 20)}</span>'
            f'<div style="display: flex; flex-direction: column; line-height: 1.4; min-width: 0"><span style="font-weight: 700; font-size: 16px">{title}</span>'
            f'<span style="font-size: 14px; color: var(--soft)">{note}</span></div></div>')

def tl_row(time, content, dot="var(--accentbg)", last=False, timew=88):
    line = '' if last else '<div aria-hidden="true" style="position: absolute; left: 11px; top: 30px; bottom: -22px; border-left: 2.5px dotted var(--soft)"></div>'
    return (f'<div style="display: grid; grid-template-columns: {timew}px 24px minmax(0, 1fr); column-gap: 14px; align-items: start">'
            f'<div style="text-align: right; padding-top: 10px; font-weight: 700; font-size: 16px; font-variant-numeric: tabular-nums; line-height: 1.3">{time}</div>'
            f'<div style="position: relative; align-self: stretch"><div style="position: absolute; left: 3px; top: 12px; width: 18px; height: 18px; border-radius: 50%; background: {dot}; border: 2.5px solid var(--ink); box-sizing: border-box"></div>{line}</div>'
            f'<div style="min-width: 0">{content}</div></div>')

def day_chips(active, compact=False):
    days = [("13","日"),("14","一"),("15","二"),("16","三"),("17","四"),("18","五"),("19","六")]
    pad = "8px 14px" if compact else "8px 18px"
    out = (f'<button type="button" style="flex: none; min-height: 44px; padding: {pad}; border: 2px solid var(--ink); border-radius: 999px; font: inherit; font-weight: 900; font-size: 14px; '
           f'background: var(--pinebg); color: var(--onaccent); cursor: pointer; display: flex; align-items: center; gap: 6px">{icon("cal", 16, "currentColor", 2.4)}今天</button>')
    for d, w in days:
        on = d == active
        st = "background: var(--accentbg); color: var(--onaccent);" if on else "background: var(--card); color: var(--ink);"
        out += (f'<button type="button" aria-pressed="{"true" if on else "false"}" style="flex: none; min-height: 44px; padding: {pad}; border: 2px solid var(--ink); border-radius: 999px; font: inherit; font-weight: 900; font-size: 14px; cursor: pointer; {st}">'
                f'12/{d}<span style="font-weight: 500; margin-left: 4px; opacity: 0.8">{w}</span></button>')
    return out

def trip_desktop():
    rows = [
        ("08:00", spot_card("08:00", "東京車站", "出發前在丸之內紅磚站舍拍照。", "tokyostation", ("地圖清單地點",)), "var(--accentbg)"),
        ("08:50", move_row("train", "北陸新幹線 → 輕井澤", "約 1 小時，建議先劃位"), "var(--chip)"),
        ("10:00", move_row("bus", "巴士到「舊輕井澤」", "輕井澤站搭巴士約 4 分鐘；大件行李可寄放車站置物櫃"), "var(--chip)"),
        ("10:15", spot_card("", "APPLE PIE lab 軽井沢", "就在舊輕井澤銀座通入口、圓環旁。推薦現填的蘋果卡士達派。", "applepie", ("地圖清單地點",)), "var(--accentbg)"),
        ("10:45", spot_card("", "舊輕井澤銀座通散步", "冬季部分店家休息或縮短營業。", "street", ("地圖清單地點",)), "var(--accentbg)"),
        ("11:30", spot_card("", "BOULANGERIE ASANOYA", "淺野屋舊道本店。麵包當早午餐或伴手禮。", "bread", ("地圖清單地點",)), "var(--accentbg)"),
        ("12:30", move_row("bowl", "午餐", "舊輕銀座一帶"), "var(--chip)"),
        ("14:00", move_row("taxi", "前往星野區", "計程車或巴士約 20 分鐘，出發前查巴士班次"), "var(--chip)"),
        ("14:30", spot_card("", "石之教會 內村鑑三記念堂", "內部禁止拍照；有婚禮時可能無法入內。", "stonechurch", ("地圖清單地點",)), "var(--accentbg)"),
        ("15:15", spot_card("", "輕井澤高原教會", "參觀時間 10:00–17:00。", "woodchurch", ("地圖清單地點",)), "var(--accentbg)"),
        ("16:00", spot_card("", "榆樹街小鎮（Harunire Terrace）", "12 月有聖誕燈飾。逛街、喝咖啡、吃晚餐。", "harunire", ("地圖清單地點",)), "var(--accentbg)"),
        ("18:30", spot_card("", "高原教會聖誕燭光夜", "往年 12/1–12/25 晚間舉辦，部分年度採預約制，請確認 2026 年辦法。", "woodchurch", (("選配", "opt"),), True), "var(--yellow)"),
        ("19:30", spot_card("", "輕井澤英迪格酒店", "搭計程車前往。check-in 15:00 起；距輕井澤站車程約 5 分鐘。", "firepit", ("地圖清單地點", ("住宿", "chip"))), "var(--accentbg)"),
    ]
    tl = ''.join(tl_row(t, c, d, i == len(rows) - 1) for i, (t, c, d) in enumerate(rows))
    spots = ["東京車站", "APPLE PIE lab 軽井沢", "舊輕井澤銀座通", "BOULANGERIE ASANOYA", "石之教會 內村鑑三記念堂", "輕井澤高原教會", "榆樹街小鎮", "輕井澤英迪格酒店"]
    checks = ''
    for i, s in enumerate(spots):
        on = i < 2
        checks += (f'<label for="sp{i}" style="display: flex; align-items: center; gap: 12px; min-height: 44px; cursor: pointer">'
                   f'<input type="checkbox" id="sp{i}" {"checked" if on else ""} style="position: absolute; opacity: 0; width: 1px; height: 1px">'
                   f'<span style="width: 26px; height: 26px; flex: none; border: 2.5px solid var(--ink); border-radius: 8px; display: grid; place-items: center; background: {"var(--pinebg)" if on else "var(--paper)"}">{icon("check", 16, "var(--onaccent)", 3.2) if on else ""}</span>'
                   f'<span style="font-size: 15px; font-weight: 500; {"text-decoration: line-through; color: var(--soft);" if on else ""}">{s}</span></label>')
    side_card = lambda inner: f'<div style="background: var(--card); border: 2.5px solid var(--ink); border-radius: 22px; padding: 18px 20px; box-shadow: 0 5px 0 var(--line); display: flex; flex-direction: column; gap: 10px">{inner}</div>'
    tips = ''.join(f'<li style="display: flex; gap: 10px; font-size: 14.5px; line-height: 1.55"><span aria-hidden="true" style="width: 8px; height: 8px; border-radius: 50%; background: var(--accentbg); flex: none; margin-top: 8px"></span>{t}</li>'
                   for t in ["大件行李寄放 TOSEI，只帶一晚的隨身行李。", "冬季舊輕銀座部分店家休息，營業時間以現場為準。", "石之教會內部禁止拍照。", "星野區巴士班次少，可直接搭計程車。"])
    body = (root_open("min-height: 100%;")
        + '<div style="max-width: 1200px; margin: 0 auto; padding: 28px 32px 48px; display: flex; flex-direction: column; gap: 28px">'
        + f'<header style="display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap">{brand()}{theme_btn()}</header>'
        + f'<div role="group" aria-label="選擇日期" style="display: flex; gap: 8px; flex-wrap: wrap">{day_chips("14")}</div>'
        # day head
        + '<section style="display: flex; flex-wrap: wrap; gap: 36px; align-items: center">'
        + '<div style="position: relative; flex: 1 1 520px; min-width: 0">' + tape("-12px", "40px", -5, 96) + plate("stonechurch", "16 / 9", 12, 28) + '</div>'
        + '<div style="flex: 1 1 360px; min-width: 0; display: flex; flex-direction: column; gap: 16px">'
        + '<div style="display: flex; align-items: center; gap: 16px">' + seal("14", "12月", 84, "var(--pinebg)", -6)
        + '<div style="display: flex; flex-direction: column; line-height: 1.3"><span style="font-size: 15px; font-weight: 700; color: var(--accent); letter-spacing: 0.1em">DAY 2 ・ 12/14（一）</span>'
        + '<h1 style="margin: 0; font-size: 46px; font-weight: 900; letter-spacing: 0.04em">輕井澤</h1></div></div>'
        + '<div style="display: flex; gap: 8px; flex-wrap: wrap">' + tag("舊輕井澤銀座、星野區") + tag("住宿：輕井澤英迪格酒店") + '</div>'
        + '<div style="display: flex; gap: 12px">'
        + ''.join(f'<div style="flex: 1; padding: 12px 14px; border: 2px solid var(--ink); border-radius: 16px; background: var(--card)"><div style="font-size: 26px; font-weight: 900; line-height: 1.1; font-variant-numeric: tabular-nums">{n}</div><div style="font-size: 13px; color: var(--soft)">{l}</div></div>'
                  for n, l in [("8", "清單地點"), ("4", "段移動"), ("1", "選配活動")])
        + '</div></div></section>'
        # memo
        + '<div style="position: relative; max-width: 760px; padding: 18px 22px 16px; background: color-mix(in srgb, var(--yellow) 30%, var(--card)); border: 2px solid var(--ink); border-radius: 6px 22px 22px 22px; transform: rotate(-0.6deg)">'
        + tape("-13px", "24px", -3, 70, "var(--pink)")
        + '<p style="margin: 0; font-size: 15.5px; line-height: 1.7"><strong style="color: var(--accent)">行李：</strong>12/15 會回同一家飯店，大件行李請寄放 TOSEI，只帶一晚的隨身行李去輕井澤（請先向飯店確認寄放服務）。</p></div>'
        # main
        + '<div style="display: flex; flex-wrap: wrap; gap: 32px; align-items: flex-start">'
        + f'<div style="flex: 999 1 600px; min-width: 0; display: flex; flex-direction: column; gap: 22px">{tl}</div>'
        + '<aside style="flex: 1 1 300px; min-width: 0; display: flex; flex-direction: column; gap: 18px">'
        + side_card('<h2 style="margin: 0; font-size: 18px; font-weight: 900">今天的清單地點</h2><p style="margin: 0; font-size: 13px; color: var(--soft)">去過就打勾，2 / 8</p>' + checks)
        + side_card('<h2 style="margin: 0; font-size: 18px; font-weight: 900">今晚住宿</h2>'
                    + f'<div style="border: 2px solid var(--ink); border-radius: 14px; overflow: hidden">{art("firepit")}</div>'
                    + '<div style="display: flex; flex-direction: column; line-height: 1.5"><span style="font-weight: 700">輕井澤英迪格酒店</span><span style="font-size: 14px; color: var(--soft)">check-in 15:00・check-out 11:00</span></div>')
        + side_card(f'<h2 style="margin: 0; font-size: 18px; font-weight: 900; display: flex; align-items: center; gap: 8px">{icon("note", 20)}小提醒</h2><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px">{tips}</ul>')
        + '</aside></div>'
        + '</div>' + nav(1) + '<div style="height: 24px"></div></div>')
    return page("行程 12/14 · 2026 東京冬令營", body, (1280, 3150))

def phone_shell(inner, nav_active):
    return (root_open("width: 390px; height: 844px; position: relative; overflow: hidden; box-sizing: border-box;")
            + inner + nav(nav_active, 14) + '</div>')

def phone_trip():
    def mcard(title, note, key, tags):
        tg = ''.join(tag(*x) for x in tags)
        return (f'<article style="background: var(--card); border: 2.5px solid var(--ink); border-top: 7px solid var(--a); border-radius: 20px; overflow: hidden; box-shadow: 0 4px 0 var(--line)">'
                f'<div style="border-bottom: 2px solid var(--ink)">{art(key, "16 / 8")}</div>'
                f'<div style="padding: 12px 14px 14px; display: flex; flex-direction: column; gap: 4px">'
                f'<h3 style="margin: 0; font-size: 17px; font-weight: 900; line-height: 1.35">{title}</h3><p style="margin: 0; font-size: 14px; color: var(--soft); line-height: 1.55">{note}</p>'
                f'<div style="display: flex; gap: 6px; flex-wrap: wrap; margin-top: 4px">{tg}</div></div></article>')
    def mmove(ic, title, note):
        return (f'<div style="display: flex; align-items: center; gap: 12px; padding: 10px 12px; border: 2px dashed var(--soft); border-radius: 16px">'
                f'<span style="width: 36px; height: 36px; flex: none; border-radius: 50%; background: var(--chip); display: grid; place-items: center">{icon(ic, 18)}</span>'
                f'<div style="display: flex; flex-direction: column; line-height: 1.35; min-width: 0"><span style="font-weight: 700; font-size: 15px">{title}</span><span style="font-size: 13px; color: var(--soft)">{note}</span></div></div>')
    rows = [("07:30", mmove("train", "出發 → JR 品川站港南口", "淺草線往品川一帶，約 30 分鐘"), "var(--chip)"),
            ("08:15", mmove("bus", "都巴士「品99」", "「東京出入国在留管理局前」下車"), "var(--chip)"),
            ("08:30", mcard("東京出入國在留管理局", "開門前排隊、辦理手續。平日 9:00–16:00，越早到越好。", "immigration", [("地圖清單地點", "spot"), ("A 組", "a")]), "var(--a)"),
            ("辦完", mmove("train", "JR 山手線到澀谷", "回品川站搭車，約 15 分鐘"), "var(--chip)"),
            ("午後", mcard("Coffee &amp; Cake SHU", "辦完手續後休息，吃午餐或下午茶。", "cake", [("地圖清單地點", "spot")]), "var(--a)")]
    tl = ''.join(tl_row(t, c, d, False, 46) for t, c, d in rows)
    inner = ('<div style="padding: 16px 16px 0; display: flex; flex-direction: column; gap: 14px">'
        + f'<header style="display: flex; align-items: center; justify-content: space-between">{brand(True)}{theme_btn(True)}</header>'
        + f'<div role="group" aria-label="選擇日期" style="display: flex; gap: 6px; overflow: hidden; margin-right: -16px">{day_chips("16", True)}</div>'
        + '<div style="display: flex; align-items: center; gap: 14px; padding: 12px 14px; background: var(--card); border: 2.5px solid var(--ink); border-radius: 20px; box-shadow: 0 4px 0 var(--line)">'
        + seal("16", "12月", 60, "var(--b)", -6)
        + '<div style="display: flex; flex-direction: column; gap: 4px; min-width: 0"><span style="font-size: 12px; font-weight: 700; color: var(--accent); letter-spacing: 0.1em">DAY 4 ・ 12/16（三）</span>'
        + '<h1 style="margin: 0; font-size: 24px; font-weight: 900; line-height: 1.2">分組日</h1><span style="font-size: 13px; color: var(--soft)">A 入管局・SHU・Tower Records／B 明治神宮・中目黑</span></div></div>'
        + '<div role="group" aria-label="切換組別" style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); padding: 4px; border: 2px solid var(--ink); border-radius: 999px; background: var(--card)">'
        + '<button type="button" aria-pressed="true" style="min-height: 40px; border: 0; border-radius: 999px; background: var(--a); color: var(--onaccent); font: inherit; font-weight: 900; font-size: 15px">A 組・入管局 → 澀谷</button>'
        + '<button type="button" aria-pressed="false" style="min-height: 40px; border: 0; border-radius: 999px; background: transparent; color: var(--soft); font: inherit; font-weight: 700; font-size: 15px">B 組・神宮 → 中目黑</button></div>'
        + f'<div style="display: flex; flex-direction: column; gap: 16px">{tl}</div></div>')
    body = phone_shell(inner, 1)
    return page("手機・行程 12/16（深色）", body, (390, 844), dark_default=True)

def phone_pack():
    cats = [("出國", ["護照","入境簽證 / 健康許可證明","外幣現金","eSIM","當地運輸票券","旅平險","機場接送費用","當地機場快捷票券","購物優惠券","電壓檢查","伴手禮","頸枕","真空袋","真空幫浦"], 8),
            ("必需品", ["家裡鑰匙","鼻噴劑","個人藥品","通血透骨膏"], 1)]
    html = ''
    for ci, (name, items, done) in enumerate(cats):
        cells = ''
        for i, it in enumerate(items):
            on = i < done
            cells += (f'<label for="pk{ci}-{i}" style="display: flex; align-items: center; gap: 10px; min-height: 44px; padding: 4px 10px; background: var(--card); border: 2px solid var(--ink); border-radius: 14px; cursor: pointer">'
                      f'<input type="checkbox" id="pk{ci}-{i}" {"checked" if on else ""} style="position: absolute; opacity: 0; width: 1px; height: 1px">'
                      f'<span style="width: 22px; height: 22px; flex: none; border: 2.2px solid var(--ink); border-radius: 7px; display: grid; place-items: center; background: {"var(--pinebg)" if on else "var(--paper)"}">{icon("check", 14, "var(--onaccent)", 3.4) if on else ""}</span>'
                      f'<span style="font-size: 14px; font-weight: 500; line-height: 1.3; {"text-decoration: line-through; color: var(--soft);" if on else ""}">{it}</span></label>')
        html += (f'<section style="display: flex; flex-direction: column; gap: 10px">'
                 f'<h2 style="margin: 0; display: flex; align-items: center; gap: 10px; font-size: 17px; font-weight: 900">'
                 f'<span style="width: 28px; height: 28px; border-radius: 50%; background: var(--accentbg); color: var(--onaccent); border: 2px solid var(--ink); display: grid; place-items: center; font-size: 13px">{ci+1}</span>{name}'
                 f'<span style="font-size: 12px; font-weight: 500; color: var(--soft); background: var(--chip); padding: 2px 10px; border-radius: 999px">{done} / {len(items)}</span></h2>'
                 f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px">{cells}</div></section>')
    inner = ('<div style="padding: 16px 16px 0; display: flex; flex-direction: column; gap: 18px">'
        + f'<header style="display: flex; align-items: center; justify-content: space-between">{brand(True)}{theme_btn(True)}</header>'
        + '<div style="position: relative; display: flex; gap: 14px; align-items: center; padding: 10px; background: var(--card); border: 2.5px solid var(--ink); border-radius: 22px; box-shadow: 0 4px 0 var(--line)">'
        + tape("-11px", "calc(100% - 92px)", 6, 64)
        + f'<div style="width: 118px; flex: none; border: 2px solid var(--ink); border-radius: 14px; overflow: hidden">{art("suitcase", "1 / 1")}</div>'
        + '<div style="display: flex; flex-direction: column; gap: 6px; min-width: 0; flex: 1"><h1 style="margin: 0; font-size: 24px; font-weight: 900; line-height: 1.2">打包清單</h1>'
        + '<span style="font-size: 13px; color: var(--soft)">7 大類、共 69 項。裝進行李就打勾。</span>'
        + '<div style="display: flex; align-items: center; gap: 8px"><div style="flex: 1; height: 12px; border: 2px solid var(--ink); border-radius: 999px; overflow: hidden; background: var(--paper)"><div style="width: 26%; height: 100%; background: var(--pinebg)"></div></div>'
        + '<span style="font-size: 13px; font-weight: 700; font-variant-numeric: tabular-nums">18 / 69</span></div></div></div>'
        + html + '</div>')
    return page("手機・打包清單", phone_shell(inner, 4), (390, 844))

def sheet():
    items = [("tokyostation", "東京車站", "12/14・12/15"), ("shinkansen", "北陸新幹線", "12/14・12/15"), ("applepie", "APPLE PIE lab", "12/14"),
             ("street", "舊輕井澤銀座通", "12/14"), ("stonechurch", "石之教會", "12/14"), ("woodchurch", "高原教會燭光夜", "12/14"),
             ("harunire", "榆樹街小鎮", "12/14"), ("firepit", "英迪格焚火庭園", "12/14・12/15"), ("immigration", "入管局", "12/16 A 組"),
             ("records", "Tower Records", "12/16 A 組"), ("torii", "明治神宮", "12/16 B 組"), ("roastery", "星巴克烘焙工坊", "12/16 B 組"),
             ("todai", "東京大學赤門", "12/17"), ("teamlab", "teamLab Borderless", "12/17"), ("ginza", "銀座夜景", "12/13・12/18"), ("plane", "返程", "12/19")]
    cells = ''.join(f'<figure style="margin: 0; display: flex; flex-direction: column; gap: 10px">{plate(k, "16 / 10", 8, 18)}'
                    f'<figcaption style="display: flex; justify-content: space-between; align-items: baseline; gap: 8px; padding: 0 4px"><span style="font-weight: 900; font-size: 16px">{n}</span><span style="font-size: 13px; color: var(--soft)">{d}</span></figcaption></figure>'
                    for k, n, d in items)
    body = (root_open("width: 1280px; box-sizing: border-box; padding: 56px 64px 64px; display: flex; flex-direction: column; gap: 36px;")
        + '<div style="display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; flex-wrap: wrap">'
        + '<div style="display: flex; flex-direction: column; gap: 8px"><span style="font-size: 14px; font-weight: 700; letter-spacing: 0.16em; color: var(--accent)">ILLUSTRATIONS</span>'
        + '<h1 style="margin: 0; font-size: 44px; font-weight: 900; letter-spacing: 0.04em">插畫集</h1>'
        + '<p style="margin: 0; font-size: 16px; color: var(--soft); max-width: 40em">每站一張。手繪抖動線條、水彩暈邊、紙紋顆粒，加上陰影面與高光，深色模式自動換成夜景配色。</p></div>'
        + f'{brand()}</div>'
        + f'<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 32px 28px">{cells}</div></div>')
    return page("插畫集 · 2026 東京冬令營", body, (1280, 1180), fluid=False)

BUILD = {"Main": main_home, "Trip": trip_desktop, "PhoneTrip": phone_trip, "PhonePack": phone_pack, "Illustrations": sheet}

if __name__ == "__main__":
    name = sys.argv[1]
    os.makedirs(ROOT, exist_ok=True)
    out = os.path.join(ROOT, f"{name}.dc.html")
    open(out, "w").write(BUILD[name]())
    print(out, os.path.getsize(out))
