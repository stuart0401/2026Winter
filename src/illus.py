# Picture-book illustration library for the redesign (inline SVG, 320x200).
# Fills use CSS classes (.f-*) defined in each artboard's helmet so light/dark themes recolor them.

def svg(inner, label=None, vb="0 0 320 200"):
    a = 'aria-hidden="true"' if not label else f'role="img" aria-label="{label}"'
    return (f'<svg viewBox="{vb}" preserveAspectRatio="xMidYMid slice" {a} '
            f'style="display: block; width: 100%; height: 100%">'
            f'<g filter="url(#paint)">{inner}</g>'
            f'<rect x="0" y="0" width="320" height="200" filter="url(#grain)" opacity="0.4"></rect>'
            f'</svg>')

DEFS = '''<svg width="0" height="0" style="position: absolute" aria-hidden="true"><defs>
<filter id="paint" x="-4%" y="-4%" width="108%" height="108%"><feTurbulence type="fractalNoise" baseFrequency="0.032" numOctaves="3" seed="7" result="n"></feTurbulence><feDisplacementMap in="SourceGraphic" in2="n" scale="4.2" result="d"></feDisplacementMap><feGaussianBlur in="d" stdDeviation="0.9" result="b"></feGaussianBlur><feBlend in="d" in2="b" mode="multiply"></feBlend></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3"></feTurbulence><feColorMatrix type="matrix" values="0 0 0 0 0.32  0 0 0 0 0.25  0 0 0 0 0.18  0.55 0 0 0 -0.22"></feColorMatrix></filter>
<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(40)"><line x1="0" y1="0" x2="0" y2="6" class="hatch"></line></pattern>
</defs></svg>'''

# ---------- building blocks ----------
def sky(night=False):
    if night:
        return ('<rect class="f-night" x="-10" y="-10" width="340" height="220"></rect>'
                '<path class="f-night2" d="M-10 120 Q160 92 330 118 V210 H-10Z"></path>')
    return ('<rect class="f-sky" x="-10" y="-10" width="340" height="220"></rect>'
            '<path class="f-sky2" d="M-10 112 Q160 86 330 110 V210 H-10Z" opacity="0.8"></path>')

def cloud(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<path class="f-cloud" d="M6 34c-9 0-11-14 0-16 1-12 15-16 22-8 5-12 26-12 28 3 12-3 19 9 12 16 7 3 4 9-3 9H10c-5 0-7-1-4-4z"></path>'
            '<path class="f-sky2" d="M8 34h58c5 0 7-3 4-6-14 5-46 6-62 2z" opacity="0.9"></path>'
            '<path class="ol thin" d="M6 34c-9 0-11-14 0-16 1-12 15-16 22-8 5-12 26-12 28 3 12-3 19 9 12 16 7 3 4 9-3 9H10"></path>'
            '<path class="hl" d="M14 16c2-4 6-6 10-5"></path></g>')

def stars(pts):
    out = ''
    for x, y, r in pts:
        out += f'<path class="f-glow" d="M{x} {y-r}L{x+r*0.3} {y-r*0.3}L{x+r} {y}L{x+r*0.3} {y+r*0.3}L{x} {y+r}L{x-r*0.3} {y+r*0.3}L{x-r} {y}L{x-r*0.3} {y-r*0.3}Z" opacity="0.9"></path>'
    return out

def snow(pts):
    return ''.join(f'<circle class="f-snow" cx="{x}" cy="{y}" r="{r}"></circle>' for x, y, r in pts)

SNOW = snow([(24,22,2.4),(58,52,1.6),(96,18,2),(140,40,1.4),(182,14,2.2),(214,48,1.6),(256,24,2),(292,52,1.6),(306,16,1.4),(40,92,1.6),(122,80,1.2),(200,96,1.6),(276,88,1.2)])

def pine(x, y, s=1.0, snowcap=True):
    caps = ('<path class="f-snow" d="M0 2 L-9 16 Q0 12 9 16Z"></path>'
            '<path class="f-snow" d="M-8 28 Q0 24 8 28 L6 24 Q0 22 -6 24Z" opacity="0.9"></path>') if snowcap else ''
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<rect class="f-brown" x="-4" y="70" width="8" height="13"></rect>'
            '<path class="f-pine" d="M0 0 L-17 27 H-8 L-21 49 H-7 L-24 72 H24 L7 49 H21 L8 27 H17Z"></path>'
            '<path class="sh" d="M0 0 L8 27 H17 L8 27 L21 49 H7 L24 72 H4 Z"></path>'
            f'{caps}'
            '<path class="ol thin" d="M0 0 L-17 27 H-8 L-21 49 H-7 L-24 72 H24 L7 49 H21 L8 27 H17Z"></path></g>')

def tree(x, y, s=1.0, cls="f-green"):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<path class="f-brown" d="M-4 8 L-5 38 H5 L4 8Z"></path>'
            f'<path class="{cls}" d="M0 -24 C14 -24 24 -12 22 2 C24 14 12 22 0 20 C-12 22 -24 14 -22 2 C-24 -12 -14 -24 0 -24Z"></path>'
            '<path class="sh" d="M22 2 C24 14 12 22 0 20 C10 14 16 8 22 2Z"></path>'
            '<path class="hl" d="M-12 -10 C-8 -16 -2 -18 4 -17"></path>'
            '<path class="ol thin" d="M0 -24 C14 -24 24 -12 22 2 C24 14 12 22 0 20 C-12 22 -24 14 -22 2 C-24 -12 -14 -24 0 -24Z"></path></g>')

def ground(cls="f-ground", y=158):
    return (f'<path class="{cls}" d="M-10 {y} Q80 {y-8} 160 {y-2} T330 {y-4} V210 H-10Z"></path>'
            f'<path class="ol thin" d="M-10 {y} Q80 {y-8} 160 {y-2} T330 {y-4}"></path>')

def snowground(y=160):
    return (f'<path class="f-snow" d="M-10 {y} Q90 {y-10} 170 {y-2} T330 {y-6} V210 H-10Z"></path>'
            f'<path class="f-sky2" d="M-10 {y+18} Q120 {y+10} 330 {y+20} V210 H-10Z" opacity="0.6"></path>'
            f'<path class="ol thin" d="M-10 {y} Q90 {y-10} 170 {y-2} T330 {y-6}"></path>')

def win(x, y, w, h, cls="f-glow"):
    return (f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5"></rect>'
            f'<rect class="ol xthin" x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5"></rect>')

def steam(xs, y):
    return ''.join(f'<path class="ol thin" d="M{x} {y} q-6 -9 0 -17 q6 -8 0 -16" opacity="0.7"></path>' for x in xs)

# ---------- scenes ----------
def hero():
    return svg(sky()
        + '<circle class="f-sun" cx="262" cy="46" r="24"></circle><path class="hl" d="M248 36 q6 -8 16 -8"></path><circle class="ol thin" cx="262" cy="46" r="24"></circle>'
        + cloud(18, 22, 1.1) + cloud(170, 44, 0.75)
        + '<path class="f-stone2" d="M-10 132 L52 62 L96 104 L158 40 L226 112 L262 86 L330 128 V170 H-10Z"></path>'
        + '<path class="f-stone" d="M-10 132 L52 62 L70 84 L60 132Z M158 40 L186 72 L172 132 H110Z" opacity="0.9"></path>'
        + '<path class="f-snow" d="M40 76 L52 62 L66 78 L58 82 L52 74 L46 82Z M144 56 L158 40 L176 58 L166 62 L158 52 L152 62Z"></path>'
        + '<path class="ol" d="M-10 132 L52 62 L96 104 L158 40 L226 112 L262 86 L330 128"></path>'
        + pine(22, 96, 0.7) + pine(62, 108, 0.52) + pine(100, 104, 0.6)
        + '<rect class="f-brick" x="140" y="118" width="176" height="52"></rect>'
        + '<path class="sh" d="M140 118 H316 V126 H140Z"></path>'
        + '<path class="f-stone2" d="M156 118 V104 Q174 80 192 104 V118Z M262 118 V104 Q280 80 298 104 V118Z"></path>'
        + '<path class="ol" d="M156 118 V104 Q174 80 192 104 V118 M262 118 V104 Q280 80 298 104 V118"></path>'
        + ''.join(win(150 + i * 20, 132, 8, 12, "f-cloud") for i in range(8))
        + '<rect class="ol" x="140" y="118" width="176" height="52"></rect>'
        + '<path class="f-cloud" d="M-10 168 H220 Q250 168 268 182 L272 190 H-10Z"></path>'
        + '<path class="f-blue" d="M-10 182 H270 L272 190 H-10Z"></path>'
        + '<path class="f-sky" d="M206 172 Q236 172 254 182 H210Z"></path>'
        + '<path class="ol" d="M-10 168 H220 Q250 168 268 182 L272 190 H-10"></path>'
        + ''.join(win(4 + i * 26, 172, 14, 7, "f-sky") for i in range(8))
        + '<rect class="f-ground" x="-10" y="190" width="340" height="20"></rect>'
        + SNOW, "東京車站紅磚站舍、新幹線與輕井澤雪山")

def tokyostation():
    w = ''.join(win(x - 4, 116, 8, 11, "f-cloud") + win(x - 4, 138, 8, 11, "f-cloud") for x in range(24, 300, 22))
    return svg(sky() + cloud(26, 18, 0.9) + cloud(222, 12, 0.8)
        + '<rect class="f-brick" x="8" y="96" width="304" height="66"></rect>'
        + '<path class="f-cloud" d="M8 110 H312 V114 H8Z M8 132 H312 V136 H8Z"></path>'
        + '<path class="f-stone2" d="M34 96 V72 Q62 34 90 72 V96Z M230 96 V72 Q258 34 286 72 V96Z"></path>'
        + '<path class="sh" d="M62 34 Q80 50 90 72 V96 H70 Z M258 34 Q276 50 286 72 V96 H266 Z"></path>'
        + '<path class="ol" d="M34 96 V72 Q62 34 90 72 V96 M230 96 V72 Q258 34 286 72 V96 M62 38 V30 M258 38 V30"></path>'
        + '<rect class="f-brick" x="128" y="78" width="64" height="18"></rect><rect class="ol" x="128" y="78" width="64" height="18"></rect>'
        + w + '<rect class="ol" x="8" y="96" width="304" height="66"></rect>'
        + '<path class="sh" d="M8 96 H312 V102 H8Z"></path>'
        + ground() + tree(8, 150, 0.7, "f-leaf") + tree(312, 150, 0.7, "f-leaf"), "東京車站丸之內站舍")

def shinkansen():
    w = ''.join(win(34 + i * 30, 122, 20, 10, "f-sky") for i in range(6))
    return svg(sky()
        + '<path class="f-stone2" d="M-10 132 L70 52 L118 96 L180 40 L258 110 L330 70 V160 H-10Z"></path>'
        + '<path class="f-snow" d="M58 64 L70 52 L84 66 L76 70 L70 62 L64 70Z M166 54 L180 40 L196 56 L188 60 L180 52 L172 60Z"></path>'
        + '<path class="ol" d="M-10 132 L70 52 L118 96 L180 40 L258 110 L330 70"></path>'
        + pine(30, 92, 0.6) + pine(292, 94, 0.62) + pine(262, 104, 0.45)
        + '<rect class="f-ground" x="-10" y="148" width="340" height="62"></rect><path class="ol" d="M-10 160 H330"></path>'
        + '<path class="f-cloud" d="M16 112 H198 Q272 112 306 142 Q310 150 298 150 H16Z"></path>'
        + '<path class="f-blue" d="M16 138 H302 Q308 144 298 150 H16Z"></path><path class="f-yellow" d="M16 132 H292 L298 137 H16Z"></path>'
        + '<path class="f-sky" d="M222 118 Q258 120 280 134 H226Z"></path><path class="hl" d="M40 116 H190"></path>'
        + w + '<path class="ol" d="M16 112 H198 Q272 112 306 142 Q310 150 298 150 H16Z"></path>'
        + SNOW, "北陸新幹線穿過雪山")

def applepie():
    lat = ''.join(f'<path class="ol thin" d="M{76+i*26} 92 L{112+i*26} 136"></path><path class="ol thin" d="M{70+i*26} 132 L{108+i*26} 90"></path>' for i in range(5))
    return svg('<rect class="f-pink" x="-10" y="-10" width="340" height="220"></rect>'
        + '<path class="f-cloud" d="M-10 150 H330 V210 H-10Z" opacity="0.7"></path>'
        + '<path class="f-cloud" d="M20 150 Q24 132 60 130 H262 Q296 132 300 150 Q300 170 160 172 Q20 170 20 150Z"></path>'
        + '<path class="ol" d="M20 150 Q24 132 60 130 H262 Q296 132 300 150 Q300 170 160 172 Q20 170 20 150Z"></path>'
        + '<ellipse class="f-wood" cx="160" cy="114" rx="104" ry="34"></ellipse>'
        + '<path class="sh" d="M60 120 Q160 160 260 120 Q260 140 160 148 Q60 140 60 120Z"></path>'
        + lat + '<ellipse class="ol" cx="160" cy="114" rx="104" ry="34"></ellipse>'
        + '<path class="hl" d="M84 98 Q120 86 160 84"></path>'
        + '<circle class="f-red" cx="270" cy="56" r="24"></circle><path class="sh" d="M286 40 Q296 60 282 76 Q270 82 258 78 Q282 68 286 40Z"></path><path class="hl" d="M256 46 q6 -8 14 -8"></path><circle class="ol" cx="270" cy="56" r="24"></circle>'
        + '<path class="ol" d="M270 32 Q272 22 278 18"></path><path class="f-green" d="M274 26 Q288 16 296 26 Q284 32 274 26Z"></path><path class="ol thin" d="M274 26 Q288 16 296 26 Q284 32 274 26Z"></path>'
        + '<circle class="f-yellow" cx="46" cy="54" r="20"></circle><path class="hl" d="M34 46 q4 -6 10 -6"></path><circle class="ol" cx="46" cy="54" r="20"></circle><path class="ol" d="M46 34 Q48 26 52 24"></path>',
        "蘋果派")

def bread():
    return svg('<rect class="f-yellow" x="-10" y="-10" width="340" height="220"></rect>'
        + '<path class="f-cloud" d="M-10 140 H330 V210 H-10Z" opacity="0.6"></path>'
        + '<path class="f-brown" d="M40 150 Q30 118 72 112 H248 Q292 118 280 150 Q276 176 160 178 Q44 176 40 150Z"></path>'
        + '<path class="sh" d="M40 150 Q44 176 160 178 Q276 176 280 150 Q240 166 160 166 Q80 166 40 150Z"></path>'
        + '<path class="ol thin" d="M58 132 H262 M72 116 V172 M110 112 V176 M150 112 V178 M190 112 V178 M230 114 V174"></path>'
        + '<path class="ol" d="M40 150 Q30 118 72 112 H248 Q292 118 280 150 Q276 176 160 178 Q44 176 40 150Z"></path>'
        + '<g transform="rotate(-22 150 84)"><rect class="f-wood" x="66" y="68" width="176" height="36" rx="18"></rect><path class="sh" d="M70 92 H238 Q236 104 224 104 H84 Q70 104 70 92Z"></path>'
        + '<path class="f-cloud" d="M96 74 L108 96 M126 72 L138 98 M156 72 L168 98 M186 72 L198 96" style="fill: none; stroke: var(--cloud); stroke-width: 4; stroke-linecap: round"></path>'
        + '<rect class="ol" x="66" y="68" width="176" height="36" rx="18"></rect></g>'
        + '<path class="f-wood" d="M196 108 Q226 62 262 102 Q248 114 230 110 Q214 116 196 108Z"></path><path class="sh" d="M200 108 Q230 118 262 102 Q252 114 230 112 Q214 116 200 108Z"></path>'
        + '<path class="ol" d="M196 108 Q226 62 262 102 Q248 114 230 110 Q214 116 196 108Z M212 104 Q220 84 230 106 M230 106 Q240 86 250 102"></path>',
        "麵包")

def street():
    return svg(sky() + cloud(222, 14, 0.8)
        + pine(24, 62, 0.8) + pine(298, 60, 0.82) + pine(60, 84, 0.5)
        + '<path class="f-wood" d="M48 164 V104 L80 78 L112 104 V164Z"></path><path class="sh" d="M80 78 L112 104 V164 H96 V104Z"></path>'
        + win(64, 116, 30, 22) + '<path class="ol" d="M48 164 V104 L80 78 L112 104 V164"></path>'
        + '<path class="f-cloud" d="M118 164 V94 L154 64 L190 94 V164Z"></path><path class="f-red" d="M118 98 H190 V110 H118Z"></path>'
        + '<path class="ol thin" d="M126 98 L130 110 M140 98 L144 110 M154 98 L158 110 M168 98 L172 110 M182 98 L186 110"></path>'
        + win(132, 120, 44, 28) + '<path class="ol" d="M118 164 V94 L154 64 L190 94 V164"></path>'
        + '<path class="f-blue" d="M196 164 V108 L226 84 L256 108 V164Z"></path><path class="sh" d="M226 84 L256 108 V164 H240 V108Z"></path>'
        + win(210, 120, 32, 22) + '<path class="ol" d="M196 164 V108 L226 84 L256 108 V164"></path>'
        + '<path class="f-snow" d="M44 104 L80 74 L116 104 L108 106 L80 84 L52 106Z M114 94 L154 60 L194 94 L186 96 L154 70 L122 96Z M192 108 L226 80 L260 108 L252 110 L226 90 L200 110Z"></path>'
        + '<path class="ol thin" d="M44 104 L80 74 L116 104 M114 94 L154 60 L194 94 M192 108 L226 80 L260 108"></path>'
        + '<path class="ol thin" d="M100 142 V128 M100 128 h8 v6 h-8"></path>'
        + snowground(162) + SNOW, "舊輕井澤銀座通的冬日街道")

def stonechurch():
    arches = ''.join(f'<path class="{c}" d="M{80+i*15} 166 Q160 {40+i*20} {240-i*15} 166Z"></path><path class="ol" d="M{80+i*15} 166 Q160 {40+i*20} {240-i*15} 166"></path>'
                     for i, c in enumerate(["f-stone2", "f-stone", "f-stone2", "f-stone"]))
    return svg(sky() + cloud(240, 18, 0.7)
        + pine(28, 64, 0.85) + pine(66, 82, 0.6) + pine(292, 66, 0.85) + pine(256, 84, 0.55)
        + arches
        + '<path class="f-sky" d="M136 166 Q160 112 184 166Z"></path><path class="hl" d="M148 150 Q154 132 162 126"></path><path class="ol" d="M136 166 Q160 112 184 166"></path>'
        + '<path class="sh" d="M200 166 Q192 104 160 80 Q206 98 225 166Z"></path>'
        + snowground(164) + snow([(30,24,2),(110,30,1.6),(204,20,2),(258,40,1.6),(300,30,2)]), "石之教會的石拱")

def woodchurch():
    lan = ''.join(f'<path class="ol thin" d="M{x} 164 V150"></path><rect class="f-glow" x="{x-6}" y="138" width="12" height="13" rx="3"></rect><rect class="ol thin" x="{x-6}" y="138" width="12" height="13" rx="3"></rect><circle class="f-glow" cx="{x}" cy="144" r="12" opacity="0.25"></circle>' for x in (54, 80, 240, 266))
    return svg(sky(True) + stars([(30,24,4),(90,46,3),(150,18,3),(226,30,4),(300,52,3),(270,16,2.5)])
        + '<circle class="f-sun" cx="276" cy="40" r="14"></circle><circle class="f-night" cx="283" cy="35" r="12"></circle>'
        + pine(32, 70, 0.85) + pine(290, 70, 0.85)
        + '<path class="f-wood" d="M108 164 V92 L160 42 L212 92 V164Z"></path><path class="sh" d="M160 42 L212 92 V164 H178 V92Z"></path>'
        + '<path class="ol thin" d="M118 106 H202 M118 122 H202 M118 138 H202"></path>'
        + '<circle class="f-glow" cx="160" cy="84" r="11"></circle><circle class="ol thin" cx="160" cy="84" r="11"></circle><path class="ol thin" d="M160 73 V95 M149 84 H171"></path>'
        + '<path class="f-glow" d="M144 164 V128 Q160 114 176 128 V164Z"></path><path class="f-glow" d="M130 164 L144 128 H176 L190 164Z" opacity="0.25"></path><path class="ol" d="M144 164 V128 Q160 114 176 128 V164"></path>'
        + '<path class="ol" d="M108 164 V92 L160 42 L212 92 V164"></path>'
        + '<path class="f-snow" d="M102 94 L160 36 L218 94 L208 96 L160 48 L112 96Z"></path><path class="ol thin" d="M102 94 L160 36 L218 94"></path>'
        + snowground(162) + lan, "輕井澤高原教會的聖誕燭光夜")

def harunire():
    bulbs = ''.join(f'<circle class="f-glow" cx="{x}" cy="{round(44+8*__import__("math").sin(i/1.5),1)}" r="3.6"></circle><circle class="f-glow" cx="{x}" cy="{round(44+8*__import__("math").sin(i/1.5),1)}" r="8" opacity="0.25"></circle>' for i, x in enumerate(range(24, 320, 28)))
    return svg(sky(True) + stars([(40,16,3),(150,12,2.5),(280,20,3)])
        + '<path class="ol thin" d="M8 40 Q80 62 160 44 Q240 26 316 46"></path>' + bulbs
        + '<path class="f-wood" d="M16 122 V82 L54 62 L92 82 V122Z"></path><path class="sh" d="M54 62 L92 82 V122 H74 V82Z"></path>' + win(34, 90, 36, 20)
        + '<path class="ol" d="M16 122 V82 L54 62 L92 82 V122"></path>'
        + '<path class="f-wood" d="M204 122 V80 L246 58 L288 80 V122Z"></path><path class="sh" d="M246 58 L288 80 V122 H266 V80Z"></path>' + win(222, 90, 46, 20)
        + '<path class="ol" d="M204 122 V80 L246 58 L288 80 V122"></path>'
        + '<path class="f-snow" d="M12 84 L54 60 L96 84 L88 86 L54 68 L20 86Z M200 82 L246 56 L292 82 L284 84 L246 64 L208 84Z"></path>'
        + tree(130, 98, 0.8, "f-pine") + tree(168, 92, 0.95, "f-pine")
        + '<path class="f-brown" d="M-10 122 H330 V134 H-10Z"></path><path class="ol thin" d="M-10 122 H330 M-10 134 H330 M20 122 V134 M60 122 V134 M100 122 V134 M140 122 V134 M180 122 V134 M220 122 V134 M260 122 V134 M300 122 V134"></path>'
        + '<path class="f-water" d="M-10 142 Q80 134 160 144 T330 142 V210 H-10Z"></path>'
        + '<path class="f-glow" d="M40 152 h22 M232 156 h30 M120 170 h18" style="stroke: var(--glow); stroke-width: 2.4; opacity: 0.6"></path>'
        + '<path class="ol thin" d="M70 162 q10 -4 20 0 M170 178 q10 -4 20 0 M260 168 q10 -4 20 0"></path>',
        "榆樹街小鎮的燈飾與河畔")

def firepit():
    return svg(sky(True) + stars([(30,26,3),(120,14,2.5),(220,30,3),(290,12,2.5)])
        + pine(36, 52, 0.95) + pine(284, 50, 0.95) + pine(86, 74, 0.6) + pine(238, 72, 0.6)
        + snowground(142)
        + '<circle class="f-glow" cx="160" cy="126" r="46" opacity="0.18"></circle>'
        + '<ellipse class="f-stone2" cx="160" cy="150" rx="54" ry="13"></ellipse><ellipse class="ol" cx="160" cy="150" rx="54" ry="13"></ellipse>'
        + '<path class="f-red" d="M134 146 Q128 114 150 100 Q146 120 158 122 Q158 96 176 86 Q170 114 188 128 Q190 142 182 146Z"></path>'
        + '<path class="f-glow" d="M148 146 Q146 128 160 118 Q166 132 172 128 Q176 140 170 146Z"></path>'
        + '<path class="ol thin" d="M134 146 Q128 114 150 100 Q146 120 158 122 Q158 96 176 86 Q170 114 188 128 Q190 142 182 146"></path>'
        + '<path class="f-blue" d="M56 160 V124 Q56 112 70 112 H96 V160Z"></path><path class="ol" d="M56 160 V124 Q56 112 70 112 H96 V160"></path>'
        + '<path class="f-blue" d="M264 160 V124 Q264 112 250 112 H224 V160Z"></path><path class="ol" d="M264 160 V124 Q264 112 250 112 H224 V160"></path>',
        "森林中的焚火庭園")

def immigration():
    rows = ''.join(win(x, y, 11, 13, "f-sky") for y in (58, 82, 106, 130) for x in (206, 230, 254, 278))
    return svg(sky() + cloud(226, 12, 0.8)
        + '<rect class="f-stone" x="194" y="42" width="106" height="124"></rect><path class="sh" d="M270 42 H300 V166 H270Z"></path>' + rows
        + '<rect class="ol" x="194" y="42" width="106" height="124"></rect>'
        + ground()
        + '<g transform="rotate(-6 92 110)"><rect class="f-cloud" x="36" y="44" width="112" height="132" rx="6"></rect><path class="ol thin" d="M52 72 H130 M52 88 H130 M52 104 H114 M52 120 H130 M52 136 H96"></path><rect class="ol" x="36" y="44" width="112" height="132" rx="6"></rect></g>'
        + '<g transform="rotate(9 154 134)"><rect class="f-pine" x="122" y="96" width="64" height="82" rx="6"></rect><circle class="ol thin" cx="154" cy="128" r="13"></circle><path class="ol thin" d="M141 128 H167 M154 115 Q146 128 154 141 Q162 128 154 115"></path><path class="hl" d="M130 104 H160"></path><rect class="ol" x="122" y="96" width="64" height="82" rx="6"></rect></g>'
        + '<circle class="f-red" cx="104" cy="142" r="15" opacity="0.85"></circle><circle class="ol thin" cx="104" cy="142" r="15"></circle><circle class="ol xthin" cx="104" cy="142" r="10"></circle>',
        "文件、護照與入管局大樓")

def cake():
    return svg('<rect class="f-pink" x="-10" y="-10" width="340" height="220"></rect>'
        + '<path class="f-cloud" d="M-10 150 H330 V210 H-10Z" opacity="0.6"></path>'
        + '<ellipse class="f-cloud" cx="122" cy="152" rx="94" ry="20"></ellipse><ellipse class="ol" cx="122" cy="152" rx="94" ry="20"></ellipse>'
        + '<path class="f-yellow" d="M70 146 V118 L122 74 L184 114 V142 Q132 156 70 146Z"></path>'
        + '<path class="f-cloud" d="M70 118 L122 74 L184 114 Q132 124 70 118Z"></path><path class="f-cloud" d="M70 132 Q130 142 184 128 V134 Q130 148 70 138Z"></path>'
        + '<path class="sh" d="M184 114 V142 Q160 150 140 152 V122Z"></path>'
        + '<path class="ol" d="M70 146 V118 L122 74 L184 114 V142 Q132 156 70 146Z M70 118 Q130 124 184 114"></path>'
        + '<circle class="f-red" cx="124" cy="72" r="11"></circle><path class="hl" d="M118 68 q3 -4 7 -4"></path><circle class="ol thin" cx="124" cy="72" r="11"></circle><path class="f-green" d="M124 61 Q130 52 136 58Z"></path>'
        + '<path class="f-cloud" d="M212 102 H274 V136 Q274 154 256 154 H230 Q212 154 212 136Z"></path><path class="sh" d="M258 102 H274 V136 Q274 154 256 154 Z"></path><path class="ol" d="M212 102 H274 V136 Q274 154 256 154 H230 Q212 154 212 136Z M274 112 Q292 112 290 126 Q288 138 274 136"></path>'
        + '<ellipse class="f-brown" cx="243" cy="104" rx="28" ry="4"></ellipse>' + steam([232, 252], 92),
        "蛋糕與咖啡")

def records():
    return svg('<rect class="f-yellow" x="-10" y="-10" width="340" height="220"></rect>'
        + '<g transform="rotate(-5 90 100)"><rect class="f-red" x="32" y="40" width="116" height="116" rx="4"></rect><path class="sh" d="M118 40 H148 V156 H118Z"></path><circle class="f-cloud" cx="90" cy="98" r="30"></circle><circle class="f-yellow" cx="90" cy="98" r="10"></circle><circle class="ol thin" cx="90" cy="98" r="30"></circle><rect class="ol" x="32" y="40" width="116" height="116" rx="4"></rect></g>'
        + '<circle class="f-ink" cx="206" cy="104" r="64"></circle><circle class="groove" cx="206" cy="104" r="52"></circle><circle class="groove" cx="206" cy="104" r="42"></circle><circle class="groove" cx="206" cy="104" r="32"></circle>'
        + '<path class="hl" d="M168 74 Q182 56 204 52"></path><circle class="f-blue" cx="206" cy="104" r="18"></circle><circle class="ol thin" cx="206" cy="104" r="18"></circle><circle class="f-cloud" cx="206" cy="104" r="3"></circle>'
        + '<path class="ol" d="M282 40 V72 M282 40 L300 34 V64"></path><ellipse class="f-ink" cx="277" cy="72" rx="7" ry="5"></ellipse><ellipse class="f-ink" cx="295" cy="64" rx="7" ry="5"></ellipse>'
        + '<path class="ol" d="M26 176 V160 M26 160 L38 156 V172"></path><ellipse class="f-ink" cx="22" cy="176" rx="5" ry="4"></ellipse><ellipse class="f-ink" cx="34" cy="172" rx="5" ry="4"></ellipse>',
        "黑膠唱片與音符")

def torii():
    return svg(sky() + cloud(130, 10, 0.8)
        + tree(26, 96, 1.5, "f-pine") + tree(78, 88, 1.2, "f-leaf") + tree(246, 90, 1.2, "f-leaf") + tree(296, 98, 1.5, "f-pine")
        + '<path class="f-ground" d="M118 170 L140 120 H180 L202 170Z"></path><path class="ol thin" d="M118 170 L140 120 M180 120 L202 170"></path>'
        + '<path class="f-wood" d="M80 36 Q160 20 240 36 L236 50 Q160 38 84 50Z"></path><path class="sh" d="M84 46 Q160 34 236 46 L236 50 Q160 38 84 50Z"></path>'
        + '<rect class="f-wood" x="100" y="60" width="120" height="10"></rect><rect class="f-wood" x="112" y="50" width="14" height="120"></rect><rect class="f-wood" x="194" y="50" width="14" height="120"></rect>'
        + '<path class="sh" d="M120 50 H126 V170 H120Z M202 50 H208 V170 H202Z"></path>'
        + '<path class="ol" d="M80 36 Q160 20 240 36 L236 50 Q160 38 84 50Z"></path><rect class="ol" x="100" y="60" width="120" height="10"></rect><rect class="ol" x="112" y="50" width="14" height="120"></rect><rect class="ol" x="194" y="50" width="14" height="120"></rect>'
        + '<rect class="f-ground" x="-10" y="168" width="340" height="42"></rect><path class="ol thin" d="M-10 168 H330"></path>'
        + ''.join(f'<circle class="f-stone" cx="{x}" cy="{y}" r="2"></circle>' for x, y in [(40,182),(90,190),(150,186),(220,192),(280,184)]),
        "明治神宮大鳥居與森林")

def roastery():
    rivets = ''.join(f'<circle class="f-ink" cx="{x}" cy="{y}" r="1.6"></circle>' for x in (66, 98, 130) for y in (30, 54, 78, 102, 126, 150))
    beans = ''.join(f'<ellipse class="f-brown" cx="{x}" cy="{y}" rx="8" ry="11" transform="rotate({r} {x} {y})"></ellipse><path class="ol thin" d="M{x} {y-9} Q{x-4} {y} {x} {y+9}" transform="rotate({r} {x} {y})"></path><ellipse class="ol thin" cx="{x}" cy="{y}" rx="8" ry="11" transform="rotate({r} {x} {y})"></ellipse>' for x, y, r in [(272,66,20),(292,88,-15),(262,96,40),(296,58,-30)])
    return svg('<rect class="f-cloud" x="-10" y="-10" width="340" height="220"></rect><rect class="f-wood" x="-10" y="164" width="340" height="50"></rect><path class="ol thin" d="M-10 164 H330"></path>'
        + '<rect class="f-copper" x="54" y="18" width="88" height="148" rx="12"></rect><path class="sh" d="M118 18 H130 Q142 18 142 30 V154 Q142 166 130 166 H118Z"></path><path class="hl" d="M64 30 V150"></path>'
        + ''.join(f'<path class="ol thin" d="M54 {y} H142"></path>' for y in (42, 66, 90, 114, 138)) + rivets
        + '<rect class="ol" x="54" y="18" width="88" height="148" rx="12"></rect>'
        + '<path class="ol" d="M142 44 Q184 44 184 84"></path>'
        + '<path class="f-cloud" d="M182 112 H252 V144 Q252 162 234 162 H200 Q182 162 182 144Z"></path><path class="sh" d="M236 112 H252 V144 Q252 162 234 162Z"></path><path class="ol" d="M182 112 H252 V144 Q252 162 234 162 H200 Q182 162 182 144Z M252 120 Q272 120 270 134 Q268 146 252 144"></path>'
        + '<ellipse class="f-brown" cx="217" cy="114" rx="30" ry="4"></ellipse>' + steam([204, 226], 102) + beans,
        "銅製咖啡豆倉與咖啡")

def teamlab():
    orbs = ''.join(f'<circle class="{c}" cx="{x}" cy="{y}" r="{r}" opacity="0.85"></circle><circle class="f-cloud" cx="{x-r*0.35}" cy="{y-r*0.35}" r="{r*0.25}" opacity="0.6"></circle><circle class="ol thin" cx="{x}" cy="{y}" r="{r}"></circle>'
                   for x, y, r, c in [(40,44,16,"f-pink"),(92,96,24,"f-blue"),(152,42,14,"f-yellow"),(206,114,28,"f-green"),(262,52,18,"f-pink"),(294,128,14,"f-yellow"),(30,138,12,"f-green"),(134,150,17,"f-pink"),(250,170,11,"f-blue")])
    flowers = ''.join(f'<g transform="translate({x} {y})">' + ''.join(f'<ellipse class="f-glow" cx="0" cy="-6" rx="3" ry="6" transform="rotate({a})"></ellipse>' for a in (0, 72, 144, 216, 288)) + '<circle class="f-red" cx="0" cy="0" r="2"></circle></g>' for x, y in [(62,72),(182,72),(236,92),(112,122),(276,94),(170,176)])
    return svg('<rect class="f-night" x="-10" y="-10" width="340" height="220"></rect>'
        + ''.join(f'<circle class="f-glow" cx="{x}" cy="{y}" r="{r}" opacity="0.12"></circle>' for x, y, r in [(92,96,46),(206,114,52),(262,52,36)])
        + orbs + flowers, "teamLab 的光球與花")

def todai():
    leaves = ''.join(f'<path class="f-yellow" d="M{x} {y} q-8 -10 0 -14 q8 4 0 14z"></path><path class="ol xthin" d="M{x} {y} q-8 -10 0 -14 q8 4 0 14z"></path>' for x, y in [(40,182),(72,176),(250,180),(284,186),(150,188),(200,184),(110,192)])
    return svg(sky() + cloud(232, 10, 0.8)
        + tree(30, 96, 1.35, "f-yellow") + tree(292, 96, 1.35, "f-yellow")
        + '<path class="f-red" d="M72 78 Q160 52 248 78 L242 92 H78Z"></path><path class="sh" d="M78 86 H242 L242 92 H78Z"></path><path class="ol" d="M72 78 Q160 52 248 78 L242 92 H78Z"></path>'
        + '<rect class="f-red" x="92" y="92" width="136" height="12"></rect><rect class="ol" x="92" y="92" width="136" height="12"></rect>'
        + '<rect class="f-red" x="98" y="104" width="20" height="62"></rect><rect class="f-red" x="202" y="104" width="20" height="62"></rect><rect class="f-ink" x="118" y="104" width="84" height="62" opacity="0.22"></rect>'
        + '<path class="sh" d="M112 104 H118 V166 H112Z M216 104 H222 V166 H216Z"></path><path class="ol" d="M98 104 V166 M118 104 V166 M202 104 V166 M222 104 V166"></path>'
        + '<rect class="f-ground" x="-10" y="164" width="340" height="46"></rect><path class="ol thin" d="M-10 164 H330"></path>' + leaves,
        "東京大學赤門與銀杏")

def plane():
    return svg(sky() + cloud(16, 30, 1.1) + cloud(214, 112, 0.9) + cloud(250, 14, 0.6)
        + '<circle class="f-sun" cx="272" cy="52" r="18"></circle><circle class="ol thin" cx="272" cy="52" r="18"></circle>'
        + '<path class="ol dash" d="M24 146 Q90 132 130 120"></path>'
        + '<path class="f-cloud" d="M120 118 L232 80 Q266 70 270 84 Q272 96 240 104 L132 136 Q110 140 120 118Z"></path><path class="sh" d="M132 136 L240 104 Q260 98 268 92 Q262 104 240 108 L134 138Z"></path><path class="hl" d="M140 116 L220 88"></path>'
        + '<path class="f-red" d="M178 106 L150 156 L172 156 L218 98Z"></path><path class="f-red" d="M132 120 L116 88 L132 86 L152 112Z"></path>'
        + '<path class="ol" d="M120 118 L232 80 Q266 70 270 84 Q272 96 240 104 L132 136 Q110 140 120 118Z M178 106 L150 156 L172 156 L218 98 M132 120 L116 88 L132 86 L152 112"></path>'
        + ''.join(f'<circle class="f-blue" cx="{x}" cy="{y}" r="3.6"></circle>' for x, y in [(244,86),(218,94),(202,99),(186,104),(170,109)]),
        "飛機")

def ginza():
    wins = ''.join(win(x - 6, y, 13, 15) for y in (82, 106, 130) for x in (118, 142, 166, 190))
    return svg(sky(True) + stars([(30,20,3),(120,30,2.5),(292,24,3),(250,60,2)])
        + '<path class="f-stone" d="M98 168 V76 Q98 60 114 58 H206 Q222 60 222 76 V168Z"></path><path class="sh" d="M190 58 H206 Q222 60 222 76 V168 H190Z"></path>'
        + '<rect class="f-stone" x="144" y="20" width="32" height="40"></rect><path class="f-pine" d="M140 22 Q160 0 180 22Z"></path><path class="ol" d="M140 22 Q160 0 180 22Z"></path><rect class="ol" x="144" y="20" width="32" height="40"></rect>'
        + '<circle class="f-cloud" cx="160" cy="40" r="11"></circle><circle class="ol thin" cx="160" cy="40" r="11"></circle><path class="ol thin" d="M160 33 V40 L166 44"></path>'
        + wins + '<path class="ol" d="M98 168 V76 Q98 60 114 58 H206 Q222 60 222 76 V168"></path>'
        + '<rect class="f-brick" x="12" y="98" width="74" height="70"></rect>' + win(24, 112, 20, 20) + win(54, 112, 20, 20) + '<rect class="ol" x="12" y="98" width="74" height="70"></rect>'
        + '<rect class="f-blue" x="234" y="88" width="76" height="80"></rect>' + win(246, 102, 20, 20) + win(278, 102, 20, 20) + '<rect class="ol" x="234" y="88" width="76" height="80"></rect>'
        + '<rect class="f-ground" x="-10" y="166" width="340" height="44"></rect><path class="ol thin" d="M-10 166 H330"></path>'
        + ''.join(f'<path class="ol thin" d="M{x} 166 V144"></path><circle class="f-glow" cx="{x}" cy="142" r="4"></circle><circle class="f-glow" cx="{x}" cy="142" r="10" opacity="0.25"></circle>' for x in (30, 96, 228, 296)),
        "銀座夜晚的鐘樓街景")

def suitcase():
    return svg(sky() + cloud(226, 22, 0.9) + ground("f-ground", 162)
        + '<rect class="f-red" x="92" y="58" width="100" height="100" rx="14"></rect><path class="sh" d="M162 58 H178 Q192 58 192 72 V144 Q192 158 178 158 H162Z"></path><path class="hl" d="M102 70 V146"></path>'
        + '<path class="ol" d="M122 58 V42 H162 V58 M106 84 H178 M106 108 H178 M106 132 H178"></path><rect class="ol" x="92" y="58" width="100" height="100" rx="14"></rect>'
        + '<circle class="f-ink" cx="110" cy="162" r="6"></circle><circle class="f-ink" cx="174" cy="162" r="6"></circle>'
        + '<g transform="rotate(8 156 80)"><rect class="f-cloud" x="138" y="70" width="36" height="20" rx="3"></rect><rect class="ol thin" x="138" y="70" width="36" height="20" rx="3"></rect><path class="ol xthin" d="M144 78 H168 M144 84 H160"></path></g>'
        + '<rect class="f-yellow" x="202" y="98" width="62" height="60" rx="10"></rect><path class="sh" d="M244 98 H254 Q264 98 264 108 V148 Q264 158 254 158 H244Z"></path><path class="ol" d="M216 98 V86 H250 V98"></path><rect class="ol" x="202" y="98" width="62" height="60" rx="10"></rect>'
        + '<path class="f-pine" d="M44 158 L58 112 L72 158Z"></path><path class="ol thin" d="M44 158 L58 112 L72 158Z"></path>',
        "行李箱")

ALL = {"hero": hero, "tokyostation": tokyostation, "shinkansen": shinkansen, "applepie": applepie, "bread": bread,
       "street": street, "stonechurch": stonechurch, "woodchurch": woodchurch, "harunire": harunire, "firepit": firepit,
       "immigration": immigration, "cake": cake, "records": records, "torii": torii, "roastery": roastery,
       "teamlab": teamlab, "todai": todai, "plane": plane, "ginza": ginza, "suitcase": suitcase}

def stationery():
    return svg('<rect class="f-cloud" x="-10" y="-10" width="340" height="220"></rect><rect class="f-wood" x="-10" y="150" width="340" height="60"></rect><path class="ol thin" d="M-10 150 H330"></path>'
        + '<g transform="rotate(-7 112 100)"><rect class="f-blue" x="50" y="34" width="124" height="124" rx="8"></rect><path class="sh" d="M150 34 H166 Q174 34 174 42 V150 Q174 158 166 158 H150Z"></path><path class="ol thin" d="M66 70 H150 M66 90 H150 M66 110 H132"></path><rect class="ol" x="50" y="34" width="124" height="124" rx="8"></rect><path class="f-red" d="M150 34 V62 L158 56 L166 62 V34Z"></path><path class="ol thin" d="M150 34 V62 L158 56 L166 62 V34"></path></g>'
        + '<g transform="rotate(6 206 100)"><rect class="f-snow" x="150" y="44" width="112" height="112" rx="6"></rect><path class="ol xthin" d="M166 70 H246 M166 88 H246 M166 106 H230 M166 124 H246 M166 142 H210"></path><rect class="ol" x="150" y="44" width="112" height="112" rx="6"></rect></g>'
        + '<g transform="rotate(-32 236 130)"><rect class="f-yellow" x="186" y="122" width="92" height="16"></rect><path class="sh" d="M186 132 H278 V138 H186Z"></path><path class="f-wood" d="M278 122 L298 130 L278 138Z"></path><path class="f-ink" d="M292 128 L298 130 L292 132Z"></path><rect class="f-pink" x="176" y="122" width="12" height="16" rx="3"></rect><path class="ol" d="M176 122 H278 L298 130 L278 138 H176Z"></path></g>'
        + '<g transform="rotate(18 82 168)"><rect class="f-red" x="34" y="160" width="82" height="14" rx="7"></rect><path class="f-stone" d="M116 160 L138 167 L116 174Z"></path><path class="hl" d="M44 164 H100"></path><path class="ol" d="M34 167 Q34 160 41 160 H116 L138 167 L116 174 H41 Q34 174 34 167Z"></path></g>',
        "筆記本與文具")

def day16():
    rows = ''.join(win(x, y, 10, 12, "f-sky") for y in (78, 100, 122) for x in (28, 50, 72))
    return svg(sky() + cloud(120, 8, 0.7)
        + '<rect class="f-stone" x="16" y="58" width="80" height="108"></rect><path class="sh" d="M80 58 H96 V166 H80Z"></path>' + rows + '<rect class="ol" x="16" y="58" width="80" height="108"></rect>'
        + '<circle class="f-red" cx="128" cy="136" r="18" opacity="0.9"></circle><circle class="ol thin" cx="128" cy="136" r="18"></circle><circle class="ol xthin" cx="128" cy="136" r="12"></circle>'
        + '<path class="ol dash" d="M160 18 V186"></path>'
        + tree(196, 104, 1.0, "f-leaf") + tree(300, 100, 1.1, "f-pine")
        + '<path class="f-wood" d="M188 50 Q244 36 300 50 L296 62 Q244 50 192 62Z"></path><rect class="f-wood" x="200" y="70" width="88" height="8"></rect><rect class="f-wood" x="208" y="62" width="11" height="104"></rect><rect class="f-wood" x="270" y="62" width="11" height="104"></rect>'
        + '<path class="sh" d="M214 62 H219 V166 H214Z M276 62 H281 V166 H276Z"></path><path class="ol" d="M188 50 Q244 36 300 50 L296 62 Q244 50 192 62Z M208 62 V166 M219 62 V166 M270 62 V166 M281 62 V166 M200 70 H288 V78 H200Z"></path>'
        + '<rect class="f-ground" x="-10" y="164" width="340" height="46"></rect><path class="ol thin" d="M-10 164 H330"></path>',
        "A 組入管局與 B 組明治神宮")

ALL.update({"stationery": stationery, "day16": day16})

def birch(x, top, bottom=166, w=7):
    marks = ''.join(f'<path class="f-ink" d="M{x-w/2} {y} h{w*0.55} v2.4 h-{w*0.55}Z" opacity="0.75"></path>' for y in range(int(top)+10, bottom-6, 17))
    return (f'<rect class="f-snow" x="{x-w/2}" y="{top}" width="{w}" height="{bottom-top}"></rect>{marks}'
            f'<rect class="ol thin" x="{x-w/2}" y="{top}" width="{w}" height="{bottom-top}"></rect>')

def forestchapel():
    return svg(sky() + cloud(196, 10, 0.7)
        + pine(30, 60, 0.9) + pine(292, 64, 0.85)
        + birch(66, 40) + birch(84, 58, w=5) + birch(246, 44) + birch(266, 62, w=5)
        + '<path class="f-snow" d="M118 164 V98 L160 70 L202 98 V164Z"></path><path class="sh" d="M160 70 L202 98 V164 H176 V98Z"></path>'
        + '<path class="f-wood" d="M110 100 L160 64 L210 100 L202 104 L160 74 L118 104Z"></path><path class="ol" d="M110 100 L160 64 L210 100 L202 104 L160 74 L118 104Z"></path>'
        + '<rect class="f-wood" x="153" y="30" width="14" height="40"></rect><path class="f-wood" d="M148 32 L160 16 L172 32Z"></path><path class="ol thin" d="M148 32 L160 16 L172 32Z M153 32 V70 M167 32 V70"></path>'
        + '<path class="ol thin" d="M160 40 V56 M154 46 H166"></path>'
        + win(130, 112, 12, 20) + win(178, 112, 12, 20)
        + '<path class="f-glow" d="M148 164 V136 Q160 124 172 136 V164Z"></path><path class="ol" d="M148 164 V136 Q160 124 172 136 V164"></path>'
        + '<path class="ol" d="M118 164 V98 M202 98 V164"></path>'
        + snowground(162) + snow([(40,24,2),(120,36,1.6),(214,26,2),(290,40,1.6),(150,52,1.4)]), "白樺林裡的森之教堂")

def artmuseum():
    cols = ''.join(birch(x, 64, 160, 6) for x in (70, 98, 126, 154, 182, 210, 238))
    return svg(sky() + cloud(40, 14, 0.8) + cloud(230, 6, 0.6)
        + '<rect class="f-sky" x="50" y="60" width="210" height="100" opacity="0.55"></rect>'
        + '<path class="hl" d="M60 74 L84 150 M150 74 L170 150"></path>'
        + cols
        + '<rect class="f-snow" x="44" y="52" width="222" height="12"></rect><path class="sh" d="M44 60 H266 V64 H44Z"></path><rect class="ol" x="44" y="52" width="222" height="12"></rect>'
        + '<rect class="ol" x="50" y="64" width="210" height="96"></rect>'
        + '<rect class="f-red" x="134" y="118" width="14" height="30" rx="2" transform="rotate(-8 141 133)"></rect><circle class="f-yellow" cx="176" cy="132" r="10"></circle><circle class="ol thin" cx="176" cy="132" r="10"></circle>'
        + tree(24, 128, 0.8, "f-pine") + tree(294, 126, 0.85, "f-pine")
        + snowground(162), "白色柱林般的輕井澤新藝術博物館")

ALL.update({"forestchapel": forestchapel, "artmuseum": artmuseum})

# ---------- day header scenes (unique, not reused by any itinerary card) ----------
def _plane(x, y, s=1.0, rot=0, body="f-cloud", accent="f-red"):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<path class="{body}" d="M-46 2 L34 -12 Q52 -15 54 -6 Q55 2 36 4 L-40 14 Q-52 15 -46 2Z"></path>'
            '<path class="sh" d="M-40 14 L36 4 Q50 2 54 -4 Q52 6 36 7 L-38 16Z"></path>'
            f'<path class="{accent}" d="M4 0 L-14 32 H-2 L22 -2Z M-36 4 L-48 -18 H-38 L-24 2Z"></path>'
            '<path class="ol" d="M-46 2 L34 -12 Q52 -15 54 -6 Q55 2 36 4 L-40 14 Q-52 15 -46 2Z M4 0 L-14 32 H-2 L22 -2 M-36 4 L-48 -18 H-38 L-24 2"></path>'
            + ''.join(f'<circle class="f-blue" cx="{cx}" cy="{cy}" r="2.4"></circle>' for cx, cy in [(30,-8),(18,-6),(8,-4),(-2,-2),(-12,0)]) + '</g>')

def _suitcase(x, y, w=40, h=46, cls="f-red"):
    return (f'<g transform="translate({x} {y})"><rect class="{cls}" x="0" y="0" width="{w}" height="{h}" rx="7"></rect>'
            f'<path class="sh" d="M{w-10} 0 H{w-7} Q{w} 0 {w} 7 V{h-7} Q{w} {h} {w-7} {h} H{w-10}Z"></path>'
            f'<path class="ol thin" d="M{w*0.3} 0 V-9 H{w*0.7} V0 M6 {h*0.35} H{w-6} M6 {h*0.65} H{w-6}"></path>'
            f'<rect class="ol" x="0" y="0" width="{w}" height="{h}" rx="7"></rect>'
            f'<circle class="f-ink" cx="8" cy="{h+3}" r="3.4"></circle><circle class="f-ink" cx="{w-8}" cy="{h+3}" r="3.4"></circle></g>')

def day_arrive():
    blds = ''
    for x, w, h, c in [(118,30,62,"f-stone"),(150,22,84,"f-blue"),(174,34,54,"f-stone2"),(210,26,72,"f-stone"),(238,30,46,"f-brick"),(270,24,66,"f-blue"),(296,30,40,"f-stone2")]:
        blds += f'<rect class="{c}" x="{x}" y="{166-h}" width="{w}" height="{h}"></rect>'
        blds += ''.join(win(x+5+i*9, 166-h+8+j*14, 5, 7) for j in range(max(1,(h-14)//14)) for i in range(max(1,(w-6)//9)))
        blds += f'<rect class="ol thin" x="{x}" y="{166-h}" width="{w}" height="{h}"></rect>'
    return svg('<rect class="f-pink" x="-10" y="-10" width="340" height="220" opacity="0.55"></rect><rect class="f-sky" x="-10" y="-10" width="340" height="120" opacity="0.8"></rect>'
        + '<circle class="f-sun" cx="246" cy="84" r="22"></circle><circle class="ol thin" cx="246" cy="84" r="22"></circle>'
        + cloud(14, 14, 0.8) + cloud(200, 20, 0.6)
        + '<g class="an an-land"><path class="ol dash" d="M10 40 Q40 46 62 56"></path>' + _plane(96, 66, 0.8, 14) + '</g>'
        + blds
        + '<rect class="f-ground" x="-10" y="164" width="340" height="46"></rect><path class="ol thin" d="M-10 164 H330"></path>'
        + '<g class="an an-bob">' + _suitcase(30, 118, 42, 48, "f-red") + '</g><g class="an an-bob2">' + _suitcase(76, 132, 32, 34, "f-yellow") + '</g>'
        + '<g transform="rotate(-10 60 128)"><rect class="f-cloud" x="48" y="122" width="22" height="13" rx="2"></rect><rect class="ol xthin" x="48" y="122" width="22" height="13" rx="2"></rect></g>',
        "飛機降落，行李箱與傍晚的東京街景")

def day_karuizawa():
    return svg(sky() + cloud(250, 14, 0.7)
        + '<path class="f-stone2" d="M-10 140 Q60 120 120 78 Q150 60 174 60 Q200 60 228 80 Q280 116 330 128 V170 H-10Z"></path>'
        + '<path class="f-snow" d="M120 78 Q150 60 174 60 Q200 60 228 80 L214 88 L200 78 L186 88 L172 76 L158 88 L142 78 L130 86Z"></path>'
        + '<path class="ol" d="M-10 140 Q60 120 120 78 Q150 60 174 60 Q200 60 228 80 Q280 116 330 128"></path>'
        + '<g class="an an-smoke"><path class="f-cloud" d="M170 58 q-6 -12 4 -18 q-2 -12 10 -12 q10 -2 10 10 q10 2 4 12" opacity="0.9"></path><path class="ol thin" d="M170 58 q-6 -12 4 -18 q-2 -12 10 -12 q10 -2 10 10 q10 2 4 12"></path></g>'
        + pine(30, 86, 0.75) + pine(64, 100, 0.55) + pine(286, 88, 0.72) + pine(258, 104, 0.5)
        + snowground(158)
        + '<path class="ol dash" d="M-10 186 Q120 170 330 180"></path>'
        + '<g class="an an-ride"><g transform="translate(150 150)"><circle class="f-cloud" cx="0" cy="22" r="17"></circle><circle class="ol" cx="0" cy="22" r="17"></circle><circle class="f-cloud" cx="62" cy="22" r="17"></circle><circle class="ol" cx="62" cy="22" r="17"></circle>'
        + '<path class="ol" d="M0 22 L20 -2 H48 L62 22 M20 -2 L32 22 H0 M32 22 L48 -2 M18 -8 H28 M48 -2 L44 -12 H54"></path><path class="f-red" d="M14 -12 H30 L28 -6 H16Z"></path><path class="ol thin" d="M14 -12 H30 L28 -6 H16Z"></path>'
        + '<rect class="f-wood" x="40" y="-20" width="20" height="10" rx="2"></rect><rect class="ol thin" x="40" y="-20" width="20" height="10" rx="2"></rect></g></g>'
        + '<g class="an an-snow">' + SNOW + '</g>', "淺間山下的雪地與自行車")

def day_return():
    w = ''.join(win(70 + i * 26, 116, 16, 9, "f-sky") for i in range(6))
    return svg('<rect class="f-sky" x="-10" y="-10" width="170" height="220"></rect><rect class="f-sky2" x="160" y="-10" width="170" height="220"></rect>'
        + '<path class="f-stone2" d="M-10 120 L40 62 L84 104 L120 74 L170 130 V160 H-10Z"></path><path class="f-snow" d="M30 74 L40 62 L52 76 L44 80 L40 72 L36 80Z M112 82 L120 74 L130 86 L122 88Z"></path><path class="ol" d="M-10 120 L40 62 L84 104 L120 74 L170 130"></path>'
        + pine(24, 96, 0.55) + pine(60, 104, 0.45)
        + ''.join(f'<rect class="{c}" x="{x}" y="{y}" width="{bw}" height="{150-y}"></rect><rect class="ol thin" x="{x}" y="{y}" width="{bw}" height="{150-y}"></rect>' for x, y, bw, c in [(196,70,24,"f-stone"),(222,52,20,"f-blue"),(244,80,28,"f-stone2"),(274,60,22,"f-stone"),(298,86,26,"f-brick")])
        + '<circle class="f-sun" cx="44" cy="30" r="12"></circle><circle class="ol thin" cx="44" cy="30" r="12"></circle>' + cloud(230, 14, 0.6)
        + '<rect class="f-ground" x="-10" y="148" width="340" height="62"></rect><path class="ol" d="M-10 156 H330 M-10 162 H330"></path>'
        + '<g class="an an-train"><path class="f-cloud" d="M40 108 H220 Q270 108 296 132 Q300 142 288 142 H40Z"></path>'
        + '<path class="f-blue" d="M40 126 H296 Q300 134 288 142 H40Z"></path><path class="f-copper" d="M40 122 H290 L294 126 H40Z"></path>'
        + '<path class="f-sky" d="M236 112 Q266 116 282 128 H240Z"></path><path class="hl" d="M52 112 H210"></path>'
        + w + '<path class="ol" d="M40 108 H220 Q270 108 296 132 Q300 142 288 142 H40Z"></path>'
        + '<path class="ol thin" d="M8 120 H30 M2 130 H26 M10 140 H32" opacity="0.7"></path></g>',
        "新幹線從雪山開往東京")

def day_split():
    return svg(sky() + cloud(20, 14, 0.7) + cloud(236, 10, 0.65)
        + '<rect class="f-ground" x="-10" y="150" width="340" height="60"></rect><path class="ol thin" d="M-10 150 H330"></path>'
        + ''.join(f'<rect class="f-snow" x="{x}" y="168" width="14" height="30" transform="skewX(-18)"></rect><rect class="ol xthin" x="{x}" y="168" width="14" height="30" transform="skewX(-18)"></rect>' for x in range(96, 300, 26))
        + '<rect class="f-wood" x="154" y="44" width="12" height="122"></rect><path class="sh" d="M161 44 H166 V166 H161Z"></path><rect class="ol" x="154" y="44" width="12" height="122"></rect>'
        + '<g class="an an-swa"><path class="f-afill" d="M60 52 H150 V84 H60 L44 68Z"></path><path class="ol" d="M60 52 H150 V84 H60 L44 68Z"></path>'
        + '<path class="f-bfill" d="M170 94 H262 L278 110 L262 126 H170Z"></path><path class="ol" d="M170 94 H262 L278 110 L262 126 H170Z"></path>'
        + '<circle class="f-snow" cx="128" cy="68" r="11"></circle><circle class="ol thin" cx="128" cy="68" r="11"></circle><path class="ol thin" d="M121 60 Q125 68 121 76 M135 60 Q131 68 135 76" style="stroke:var(--red)"></path>'
        + '<path class="ol thin" d="M78 64 H112 M78 72 H104" opacity="0.8"></path></g>'
        + '<g class="an an-swb"><path class="f-bfill" d="M170 94 H262 L278 110 L262 126 H170Z"></path><path class="ol" d="M170 94 H262 L278 110 L262 126 H170Z"></path>'
        + '<circle class="f-cloud" cx="192" cy="110" r="12"></circle><circle class="ol thin" cx="192" cy="110" r="12"></circle>'
        + ''.join(f'<circle class="f-bfill" cx="{cx}" cy="{cy}" r="3"></circle><path class="f-bfill" d="M{cx-4.6} {cy+9} Q{cx-4.6} {cy+3.6} {cx} {cy+3.6} Q{cx+4.6} {cy+3.6} {cx+4.6} {cy+9}Z"></path>' for cx, cy in [(185.5,106),(198.5,106),(192,101.5)])
        + '<path class="ol thin" d="M212 106 H250 M212 114 H240" opacity="0.8"></path></g>'
        + '<g class="an an-pulse"><path class="f-red" d="M160 28 q-10 -10 -4 -16 q4 -4 4 2 q0 -6 4 -2 q6 6 -4 16z"></path><path class="ol thin" d="M160 28 q-10 -10 -4 -16 q4 -4 4 2 q0 -6 4 -2 q6 6 -4 16z"></path></g>'
        + ''.join(f'<circle class="{c}" cx="{x}" cy="146" r="6"></circle><path class="{c}" d="M{x-7} 166 Q{x-7} 152 {x} 152 Q{x+7} 152 {x+7} 166Z"></path><path class="ol thin" d="M{x-7} 166 Q{x-7} 152 {x} 152 Q{x+7} 152 {x+7} 166"></path><circle class="ol thin" cx="{x}" cy="146" r="6"></circle>'
                  for x, c in [(36,"f-afill"),(54,"f-afill"),(262,"f-bfill"),(280,"f-bfill"),(298,"f-bfill")]).replace('<circle class="f-afill"','<g class="an an-wl"><circle class="f-afill"',1).replace('<circle class="f-bfill" cx="262"','</g><g class="an an-wr"><circle class="f-bfill" cx="262"',1) + '</g>',
        "大邱組與三口組的路標，傍晚會合")

def day_ginkgo_tower():
    leaves = ''.join(f'<path class="f-yellow" d="M{x} {y} q-7 -9 0 -12 q7 3 0 12z"></path><path class="ol xthin" d="M{x} {y} q-7 -9 0 -12 q7 3 0 12z"></path>' for x, y in [(52,70),(98,96),(130,60),(70,128),(118,150),(30,112),(142,118)])
    lights = ''.join(f'<circle class="{c}" cx="{x}" cy="{y}" r="{r}" opacity="0.8"></circle>' for x, y, r, c in [(196,40,4,"f-pink"),(228,24,3,"f-glow"),(300,36,4,"f-blue"),(310,90,3,"f-pink"),(206,96,3,"f-green"),(186,66,2.5,"f-glow"),(292,128,3,"f-yellow")])
    return svg('<rect class="f-sky" x="-10" y="-10" width="190" height="220"></rect><path class="f-night" d="M150 -10 H330 V210 H190Z"></path><path class="ol thin" d="M150 -10 L190 210"></path>'
        + cloud(10, 12, 0.6)
        + '<path class="f-brown" d="M56 166 L60 92 H72 L76 166Z"></path><path class="ol thin" d="M56 166 L60 92 H72 L76 166"></path>'
        + '<path class="f-yellow" d="M66 22 C100 22 122 52 118 82 C120 104 96 116 66 112 C36 116 12 104 14 82 C10 52 32 22 66 22Z"></path><path class="sh" d="M118 82 C120 104 96 116 66 112 C90 102 110 92 118 82Z"></path><path class="hl" d="M34 50 C42 38 54 32 66 32"></path><path class="ol" d="M66 22 C100 22 122 52 118 82 C120 104 96 116 66 112 C36 116 12 104 14 82 C10 52 32 22 66 22Z"></path>'
        + '<g class="an an-fall">' + leaves + '</g><g class="an an-tw">' + lights + '</g>'
        + '<path class="f-red" d="M236 166 L252 70 H260 L276 166Z"></path><path class="f-snow" d="M244 116 H268 L270 126 H242Z M248 90 H264 L265 98 H247Z"></path>'
        + '<path class="ol thin" d="M240 150 L272 150 M244 134 L268 134 M248 110 H264 M252 70 L256 34 L260 70 M246 166 L256 70 L266 166"></path><path class="ol" d="M236 166 L252 70 H260 L276 166"></path>'
        + '<circle class="f-glow" cx="256" cy="80" r="16" opacity="0.25"></circle><circle class="f-glow" cx="256" cy="30" r="3"></circle>'
        + '<rect class="f-ground" x="-10" y="164" width="340" height="46"></rect><path class="ol thin" d="M-10 164 H330"></path>',
        "白天的銀杏樹與夜晚亮燈的東京鐵塔")

def day_shopping():
    bulbs = ''.join(f'<circle class="{c}" cx="{x}" cy="{30+((x//20)%2)*6}" r="4"></circle><circle class="f-glow" cx="{x}" cy="{30+((x//20)%2)*6}" r="9" opacity="0.2"></circle>' for x, c in zip(range(12, 330, 26), ["f-glow","f-red","f-glow","f-blue","f-glow","f-pink","f-glow","f-yellow","f-glow","f-red","f-glow","f-blue","f-glow"]))
    def bag(x, y, w, h, c, rot):
        return (f'<g transform="rotate({rot} {x+w/2} {y+h})"><path class="ol" d="M{x+w*0.28} {y} Q{x+w*0.28} {y-22} {x+w/2} {y-22} Q{x+w*0.72} {y-22} {x+w*0.72} {y}" fill="none"></path>'
                f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"></rect><path class="sh" d="M{x+w-10} {y} H{x+w} V{y+h} H{x+w-10}Z"></path><path class="hl" d="M{x+6} {y+8} V{y+h-8}"></path>'
                f'<rect class="ol" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"></rect></g>')
    return svg(sky(True) + '<path class="ol thin" d="M-10 24 Q160 48 330 24"></path>' + '<g class="an an-tw">' + bulbs + '</g>'
        + '<rect class="f-wood" x="-10" y="150" width="340" height="60"></rect><path class="ol thin" d="M-10 150 H330"></path>'
        + '<g class="an an-drop1">' + bag(40, 92, 62, 64, "f-red", -6) + '</g><g class="an an-drop2">' + bag(106, 78, 70, 78, "f-cloud", 2) + '</g><g class="an an-drop3">' + bag(184, 98, 56, 58, "f-blue", 6) + '</g>'
        + '<rect class="f-yellow" x="244" y="118" width="52" height="40" rx="3"></rect><path class="f-red" d="M266 118 H274 V158 H266Z M244 134 H296 V140 H244Z"></path>'
        + '<path class="f-red" d="M270 118 q-16 -16 -20 -4 q4 8 20 4 q16 4 20 -4 q-4 -12 -20 4z"></path><path class="ol thin" d="M270 118 q-16 -16 -20 -4 q4 8 20 4 q16 4 20 -4 q-4 -12 -20 4z"></path><rect class="ol" x="244" y="118" width="52" height="40" rx="3"></rect>'
        + '<path class="f-yellow" d="M141 100 l3 7 7 1 -5 5 1 7 -6 -3 -6 3 1 -7 -5 -5 7 -1z"></path><path class="ol xthin" d="M141 100 l3 7 7 1 -5 5 1 7 -6 -3 -6 3 1 -7 -5 -5 7 -1z"></path>',
        "購物袋、禮物盒與聖誕燈串")

def day_home():
    return svg('<rect class="f-yellow" x="-10" y="-10" width="340" height="220" opacity="0.45"></rect><rect class="f-pink" x="-10" y="80" width="340" height="130" opacity="0.6"></rect>'
        + '<g class="an an-sink"><circle class="f-sun" cx="80" cy="120" r="34"></circle><circle class="ol thin" cx="80" cy="120" r="34"></circle></g>'
        + cloud(170, 30, 0.7) + cloud(10, 30, 0.55)
        + '<g class="an an-takeoff"><path class="ol dash" d="M110 150 Q170 110 214 76"></path>' + _plane(250, 52, 0.85, -20) + '</g>'
        + '<rect class="f-stone2" x="-10" y="142" width="340" height="68"></rect><path class="ol thin" d="M-10 142 H330"></path>'
        + '<path class="ol dash" d="M-10 172 H330"></path>'
        + ''.join(f'<circle class="f-glow" cx="{x}" cy="150" r="2.6"></circle>' for x in range(6, 330, 22))
        + '<g transform="translate(186 120)"><path class="ol" d="M0 52 H96 M8 52 V12 M88 52 V12 M-6 -8 L8 12" fill="none"></path>'
        + '<circle class="f-ink" cx="16" cy="58" r="5"></circle><circle class="f-ink" cx="80" cy="58" r="5"></circle></g>'
        + _suitcase(198, 120, 38, 46, "f-red") + _suitcase(240, 128, 32, 38, "f-blue")
        + '<g transform="translate(206 98)"><rect class="f-cloud" x="0" y="0" width="56" height="20" rx="4"></rect><rect class="ol thin" x="0" y="0" width="56" height="20" rx="4"></rect><path class="f-red" d="M8 10 q-4 -6 1 -7 q3 0 3 3 q0 -3 3 -3 q5 1 1 7 l-4 4z"></path><path class="ol xthin" d="M22 7 H48 M22 13 H40"></path></g>',
        "夕陽中起飛的飛機與行李推車")

ALL.update({"d_arrive": day_arrive, "d_karuizawa": day_karuizawa, "d_return": day_return, "d_split": day_split,
            "d_ginkgo": day_ginkgo_tower, "d_shopping": day_shopping, "d_home": day_home})


def morning():
    rays = ''.join(f'<path class="f-glow" d="M160 104 L{160+140*__import__("math").cos(a)} {104-140*__import__("math").sin(a)} L{160+140*__import__("math").cos(a+0.12)} {104-140*__import__("math").sin(a+0.12)}Z" opacity="0.28"></path>' for a in [0.35,0.75,1.15,1.55,1.95,2.35,2.75])
    birds = ''.join(f'<path class="ol thin" d="M{x-6} {y} q3 -4 6 0 q3 -4 6 0"></path>' for x, y in [(70,38),(88,30),(232,44),(250,36)])
    mist = ''.join(f'<path class="f-cloud" d="M-10 {y} Q80 {y-8} 170 {y} T330 {y} V{y+10} H-10Z" opacity="{o}"></path>' for y, o in [(112,0.55),(128,0.45)])
    return svg('<rect class="f-sky2" x="-10" y="-10" width="340" height="220"></rect><rect class="f-yellow" x="-10" y="40" width="340" height="80" opacity="0.25"></rect>'
        + rays + '<circle class="f-sun" cx="160" cy="104" r="26"></circle><circle class="f-glow" cx="160" cy="104" r="40" opacity="0.3"></circle><circle class="ol thin" cx="160" cy="104" r="26"></circle>'
        + '<path class="f-stone2" d="M-10 118 Q50 86 104 104 Q130 112 160 100 Q200 84 244 102 Q290 116 330 96 V140 H-10Z" opacity="0.85"></path><path class="ol thin" d="M-10 118 Q50 86 104 104 Q130 112 160 100 Q200 84 244 102 Q290 116 330 96"></path>'
        + mist + birds
        + pine(26, 74, 0.8, False) + pine(60, 92, 0.6, False) + pine(294, 70, 0.85, False) + pine(262, 92, 0.6, False)
        + '<rect class="f-wood" x="-10" y="156" width="340" height="54"></rect><path class="sh" d="M-10 156 H330 V162 H-10Z"></path><path class="ol" d="M-10 156 H330"></path><path class="ol thin" d="M-10 176 H330 M60 156 V210 M160 156 V210 M260 156 V210"></path>'
        + '<g transform="translate(206 120)"><path class="f-cloud" d="M0 8 H34 L31 34 Q30 38 26 38 H8 Q4 38 3 34Z"></path><path class="f-brown" d="M2 12 H32 L31 16 H3Z"></path><path class="ol" d="M34 14 q12 0 10 10 q-2 8 -12 6" fill="none"></path><path class="ol" d="M0 8 H34 L31 34 Q30 38 26 38 H8 Q4 38 3 34Z"></path><path class="hl" d="M7 14 V32"></path></g>'
        + steam([214, 226], 124)
        + '<path class="f-green" d="M86 156 q-14 -18 -2 -30 q10 12 2 30z"></path><path class="ol thin" d="M86 156 q-14 -18 -2 -30 q10 12 2 30z M86 156 Q86 140 84 126"></path><circle class="f-sky" cx="80" cy="134" r="2.4"></circle><circle class="hl" cx="79.4" cy="133.4" r="0.8"></circle>',
        "晨光、薄霧與熱咖啡的清新早晨")

ALL.update({"morning": morning})


def financier():
    cakes = ''.join(f'<g transform="translate({x} {y}) rotate({r})"><path class="f-yellow" d="M0 10 L6 0 H54 L60 10 V22 H0Z"></path><path class="f-copper" d="M0 10 H60 V22 H0Z" opacity="0.55"></path><path class="hl" d="M10 4 H46"></path><path class="ol" d="M0 10 L6 0 H54 L60 10 V22 H0Z M0 10 H60"></path></g>' for x, y, r in [(70,104,-4),(140,96,3),(104,124,-1),(178,122,5)])
    return svg('<rect class="f-cloud" x="-10" y="-10" width="340" height="220"></rect><rect class="f-wood" x="-10" y="150" width="340" height="60"></rect><path class="ol thin" d="M-10 150 H330"></path>'
        + '<ellipse class="f-snow" cx="148" cy="150" rx="118" ry="16"></ellipse><ellipse class="ol thin" cx="148" cy="150" rx="118" ry="16"></ellipse>'
        + cakes
        + '<g transform="rotate(8 268 110)"><rect class="f-blue" x="236" y="70" width="64" height="80" rx="4"></rect><path class="sh" d="M286 70 H300 V150 H286Z"></path><path class="f-yellow" d="M264 70 H272 V150 H264Z"></path><rect class="ol" x="236" y="70" width="64" height="80" rx="4"></rect><path class="f-yellow" d="M268 70 q-16 -16 -20 -4 q4 8 20 4 q16 4 20 -4 q-4 -12 -20 4z"></path><path class="ol thin" d="M268 70 q-16 -16 -20 -4 q4 8 20 4 q16 4 20 -4 q-4 -12 -20 4z"></path></g>'
        + steam([40, 52], 120), "盤子上的費南雪與禮盒")

ALL.update({"financier": financier})

def day_hoshino():
    lanterns = ''.join(f'<g transform="translate({x} {y}) scale(1.25)"><circle class="f-glow" cx="0" cy="-8" r="13" opacity="0.22"></circle><rect class="f-yellow" x="-6" y="-16" width="12" height="15" rx="3"></rect><path class="f-ink" d="M-7 -16 H7 L5 -20 H-5Z"></path><rect class="ol thin" x="-6" y="-16" width="12" height="15" rx="3"></rect><path class="f-sun" d="M0 -12 q-2 3 0 6 q2 -3 0 -6z"></path></g>'
                       for x, y in [(34,178),(70,172),(250,170),(288,176)])
    taxi = ('<g transform="translate(118 116) scale(1.3)">'
            '<path class="f-glow" d="M58 18 L120 6 L120 34 Z" opacity="0.35"></path>'
            '<path class="f-yellow" d="M0 22 V14 Q0 10 4 10 H14 L22 2 H42 L50 10 H58 Q62 10 62 14 V22Z"></path>'
            '<rect class="f-cloud" x="26" y="-4" width="12" height="6" rx="1.5"></rect><rect class="ol xthin" x="26" y="-4" width="12" height="6" rx="1.5"></rect>'
            '<path class="f-sky" d="M24 4 H40 L46 10 H18Z"></path><path class="ol thin" d="M24 4 H40 L46 10 H18Z M32 4 V10"></path>'
            '<path class="ol" d="M0 22 V14 Q0 10 4 10 H14 L22 2 H42 L50 10 H58 Q62 10 62 14 V22Z"></path>'
            '<circle class="f-ink" cx="14" cy="23" r="5"></circle><circle class="f-ink" cx="48" cy="23" r="5"></circle><circle class="f-stone2" cx="14" cy="23" r="2"></circle><circle class="f-stone2" cx="48" cy="23" r="2"></circle>'
            '<circle class="f-glow" cx="59" cy="15" r="2.4"></circle></g>')
    return svg(sky(True)
        + '<g class="an an-tw">' + stars([(30,22,3),(84,40,2.4),(126,16,2.6),(206,30,2.2),(240,14,3),(300,44,2.4)]) + '</g>'
        + '<circle class="f-sun" cx="270" cy="34" r="13"></circle><circle class="f-night" cx="277" cy="29" r="11"></circle>'
        + pine(20, 66, 0.9) + pine(54, 80, 0.7) + pine(88, 72, 0.8) + pine(232, 74, 0.78) + pine(270, 66, 0.9) + pine(304, 80, 0.7)
        + '<path class="f-snow" d="M-10 150 Q80 132 160 140 T330 136 V210 H-10Z"></path><path class="ol thin" d="M-10 150 Q80 132 160 140 T330 136"></path>'
        + '<path class="f-stone2" d="M-10 172 Q100 150 170 156 T330 150 V166 Q240 164 170 170 T-10 188Z" opacity="0.8"></path><path class="ol dash" d="M10 176 Q100 158 170 162 T320 156"></path>'
        + '<g class="an an-drive">' + taxi + '</g>'
        + '<g class="an an-flick">' + lanterns + '</g>'
        + '<g class="an an-snow">' + SNOW + '</g>',
        "星野區雪夜裡的計程車與燭光")

ALL.update({"d_hoshino": day_hoshino})

def walkshoes():
    def shoe(x, y, s, c):
        return (f'<g transform="translate({x} {y}) scale({s})"><path class="{c}" d="M0 30 Q0 8 14 6 L30 4 Q38 4 42 12 L50 20 Q76 22 84 30 Q88 36 82 38 H4 Q0 38 0 30Z"></path>'
                '<path class="f-snow" d="M0 32 H86 Q86 40 78 40 H6 Q0 40 0 32Z"></path><path class="sh" d="M50 20 Q76 22 84 30 Q70 26 52 26Z"></path>'
                '<path class="ol thin" d="M20 10 L36 22 M26 8 L40 20 M14 30 Q40 18 64 28"></path>'
                '<path class="ol" d="M0 30 Q0 8 14 6 L30 4 Q38 4 42 12 L50 20 Q76 22 84 30 Q88 36 82 38 M0 32 H86 Q86 40 78 40 H6 Q0 40 0 32Z"></path></g>')
    return svg('<rect class="f-sky2" x="-10" y="-10" width="340" height="220"></rect><rect class="f-wood" x="-10" y="150" width="340" height="60"></rect><path class="ol thin" d="M-10 150 H330"></path>'
        + '<rect class="f-stone2" x="196" y="96" width="104" height="56" rx="3"></rect><path class="f-stone" d="M190 86 H306 V100 H190Z"></path><path class="ol" d="M196 100 V152 H300 V100 M190 86 H306 V100 H190Z"></path><path class="f-red" d="M236 116 h24 v14 h-24z"></path><path class="ol thin" d="M236 116 h24 v14 h-24z"></path>'
        + shoe(40, 108, 1.3, "f-blue") + shoe(96, 90, 1.05, "f-red")
        + '<path class="ol dash" d="M20 70 Q60 52 100 64 T180 60"></path>', "健走鞋與鞋盒")

ALL.update({"walkshoes": walkshoes})

def dinnerwalk():
    def lantern(x, y):
        return (f'<path class="ol thin" d="M{x} {y-10} V{y-4}"></path>'
                f'<circle class="f-glow" cx="{x}" cy="{y+8}" r="20" opacity="0.22"></circle>'
                f'<rect class="f-red" x="{x-8}" y="{y-4}" width="16" height="24" rx="8"></rect>'
                f'<path class="ol xthin" d="M{x-8} {y+3} H{x+8} M{x-8} {y+9} H{x+8} M{x-8} {y+15} H{x+8}"></path>'
                f'<rect class="ol thin" x="{x-8}" y="{y-4}" width="16" height="24" rx="8"></rect>'
                f'<rect class="f-ink" x="{x-5}" y="{y-6}" width="10" height="3"></rect><rect class="f-ink" x="{x-5}" y="{y+19}" width="10" height="3"></rect>')
    def walker(x, c, h=1.0, step=1):
        y = 166
        hy = y - 34 * h
        leg = f'M{x-2} {y-12*h} L{x-6*step} {y} M{x+2} {y-12*h} L{x+6*step} {y}'
        return (f'<path class="ol" d="{leg}"></path>'
                f'<path class="{c}" d="M{x-8*h} {y-10*h} Q{x-9*h} {hy+8} {x} {hy+7} Q{x+9*h} {hy+8} {x+8*h} {y-10*h}Z"></path>'
                f'<path class="ol thin" d="M{x-8*h} {y-10*h} Q{x-9*h} {hy+8} {x} {hy+7} Q{x+9*h} {hy+8} {x+8*h} {y-10*h}Z"></path>'
                f'<circle class="f-pink" cx="{x}" cy="{hy}" r="{6.5*h}"></circle><circle class="ol thin" cx="{x}" cy="{hy}" r="{6.5*h}"></circle>'
                f'<path class="f-ink" d="M{x-6.5*h} {hy-1} Q{x} {hy-10*h} {x+6.5*h} {hy-1} Q{x} {hy-5*h} {x-6.5*h} {hy-1}Z"></path>')
    noren = ''.join(f'<rect class="f-blue" x="{x}" y="96" width="17" height="30"></rect><rect class="ol xthin" x="{x}" y="96" width="17" height="30"></rect>' for x in (196, 214, 232, 250))
    return svg(sky(True) + stars([(26,22,3),(84,14,2.2),(150,30,2.6),(118,60,1.8),(60,52,1.6)])
        + '<circle class="f-snow" cx="200" cy="30" r="11"></circle><circle class="f-night" cx="205" cy="26" r="10"></circle>'
        + '<rect class="f-stone" x="-10" y="70" width="70" height="98"></rect>' + win(4, 84, 16, 18) + win(30, 84, 16, 18) + win(4, 116, 16, 18) + win(30, 116, 16, 18, "f-sky") + '<rect class="ol" x="-10" y="70" width="70" height="98"></rect>'
        + '<path class="f-wood" d="M176 62 H300 V168 H176Z"></path><path class="sh" d="M282 62 H300 V168 H282Z"></path>'
        + '<path class="f-brown" d="M168 64 L238 44 L308 64Z"></path><path class="ol" d="M168 64 L238 44 L308 64Z"></path>'
        + '<rect class="f-glow" x="190" y="96" width="82" height="72"></rect><rect class="f-glow" x="190" y="96" width="82" height="72" opacity="0.4"></rect>'
        + noren + '<path class="ol thin" d="M192 96 H272"></path><circle class="f-snow" cx="231" cy="111" r="7"></circle><circle class="ol xthin" cx="231" cy="111" r="7"></circle>'
        + '<rect class="ol" x="176" y="62" width="124" height="106"></rect><path class="ol" d="M190 168 V96 H272 V168"></path>'
        + '<rect class="f-cloud" x="206" y="70" width="50" height="16" rx="2"></rect><rect class="ol thin" x="206" y="70" width="50" height="16" rx="2"></rect><path class="ol xthin" d="M214 78 H248"></path>'
        + lantern(184, 76) + lantern(290, 76)
        + steam([216, 246], 126)
        + '<rect class="f-ground" x="-10" y="166" width="340" height="44"></rect><path class="ol thin" d="M-10 166 H330"></path>'
        + '<circle class="f-glow" cx="130" cy="186" r="38" opacity="0.18"></circle>'
        + '<path class="ol thin" d="M150 166 V100"></path><circle class="f-glow" cx="150" cy="98" r="5"></circle><circle class="f-glow" cx="150" cy="98" r="13" opacity="0.25"></circle><path class="ol thin" d="M144 94 H156"></path>'
        + walker(72, "f-red", 1.35, 1) + walker(102, "f-blue", 1.45, -1) + walker(130, "f-yellow", 1.1, 1),
        "夜晚銀座街頭散步，走向掛著燈籠的小餐館")

ALL.update({"dinnerwalk": dinnerwalk})

def ledger():
    coin = lambda x, y, r: (f'<circle class="f-yellow" cx="{x}" cy="{y}" r="{r}"></circle><circle class="sh" cx="{x+r*0.25}" cy="{y+r*0.2}" r="{r*0.8}" opacity="0.08"></circle>'
                            f'<circle class="ol thin" cx="{x}" cy="{y}" r="{r}"></circle><circle class="ol xthin" cx="{x}" cy="{y}" r="{r*0.7}"></circle>'
                            f'<path class="ol thin" d="M{x-r*0.32} {y-r*0.42} L{x} {y} L{x+r*0.32} {y-r*0.42} M{x} {y} V{y+r*0.45} M{x-r*0.32} {y+r*0.05} H{x+r*0.32} M{x-r*0.32} {y+r*0.25} H{x+r*0.32}"></path>')
    lines = ''.join(f'<path class="ol xthin" d="M{x0} {y} H{x0+44}"></path><path class="ol xthin" d="M{x0+52} {y} H{x0+68}"></path>'
                    for x0 in (86, 166) for y in (74, 90, 106, 122))
    return svg('<rect class="f-cloud" x="-10" y="-10" width="340" height="220"></rect>'
        + '<rect class="f-wood" x="-10" y="148" width="340" height="62"></rect><path class="ol thin" d="M-10 148 H330"></path>'
        + '<path class="sh" d="M80 150 L246 150 L250 158 L76 158Z"></path>'
        + '<path class="f-snow" d="M78 54 Q118 46 160 56 Q202 46 242 54 V146 Q202 138 160 148 Q118 138 78 146Z"></path>'
        + '<path class="f-sky2" d="M160 56 Q202 46 242 54 V146 Q202 138 160 148Z" opacity="0.6"></path>'
        + lines
        + '<path class="ol" d="M78 54 Q118 46 160 56 Q202 46 242 54 V146 Q202 138 160 148 Q118 138 78 146Z M160 56 V148"></path>'
        + '<path class="f-red" d="M196 44 H206 V64 L201 59 L196 64Z"></path><path class="ol thin" d="M196 44 H206 V64 L201 59 L196 64Z"></path>'
        + '<g transform="rotate(-8 40 112)"><path class="f-snow" d="M22 64 H60 V150 L55 146 L50 150 L45 146 L40 150 L35 146 L30 150 L26 146 L22 150Z"></path>'
        + '<path class="ol thin" d="M22 64 H60 V150 L55 146 L50 150 L45 146 L40 150 L35 146 L30 150 L26 146 L22 150Z"></path>'
        + '<path class="ol xthin" d="M28 76 H54 M28 86 H46 M28 96 H54 M28 106 H42 M28 124 H54"></path><path class="ol thin" d="M28 134 H54"></path></g>'
        + '<g transform="rotate(32 262 112)"><rect class="f-blue" x="256" y="62" width="11" height="78" rx="2"></rect><path class="f-cloud" d="M256 140 L261.5 156 L267 140Z"></path>'
        + '<rect class="ol thin" x="256" y="62" width="11" height="78" rx="2"></rect><path class="ol thin" d="M256 140 L261.5 156 L267 140"></path><path class="hl" d="M259 70 V128"></path></g>'
        + coin(272, 168, 15) + coin(298, 176, 11) + coin(246, 180, 10)
        + '<path class="f-green" d="M100 164 H186 V186 H100Z"></path><path class="ol thin" d="M100 164 H186 V186 H100Z"></path><circle class="ol xthin" cx="143" cy="175" r="7"></circle>'
        + '<path class="f-pink" d="M112 170 H204 V192 H112Z" opacity="0.95"></path><path class="ol thin" d="M112 170 H204 V192 H112Z"></path><circle class="ol xthin" cx="158" cy="181" r="7"></circle>',
        "攤開的記帳本、收據、筆、紙鈔和日圓硬幣")

ALL.update({"ledger": ledger})

def tokyotower():
    # dusk sky, Tokyo Tower in the middle, low buildings and trees at its feet
    def hw(y):  # half width of the tower at height y (svg y grows downward)
        pts = [(18, 1.2), (56, 5.5), (98, 13), (132, 24), (166, 40)]
        for (y0, w0), (y1, w1) in zip(pts, pts[1:]):
            if y0 <= y <= y1:
                t = (y - y0) / (y1 - y0); return w0 + (w1 - w0) * (t ** 1.15)
        return pts[-1][1]
    cx = 160
    ys = list(range(18, 167, 4)) + [166]
    outline = ' '.join(f'L{cx - hw(y):.1f} {y}' for y in ys)
    outline = f'M{cx} 12 ' + outline + ' ' + ' '.join(f'L{cx + hw(y):.1f} {y}' for y in reversed(ys)) + 'Z'
    bands = ''
    for y0, y1 in ((118, 126), (74, 80), (40, 44)):
        bands += (f'<path class="f-cloud" d="M{cx-hw(y0):.1f} {y0} L{cx+hw(y0):.1f} {y0} L{cx+hw(y1):.1f} {y1} L{cx-hw(y1):.1f} {y1}Z"></path>')
    lattice = ''
    for y in range(26, 160, 10):
        a, b = cx - hw(y), cx + hw(y); a2, b2 = cx - hw(y + 10), cx + hw(y + 10)
        lattice += f'<path class="ol xthin" d="M{a:.1f} {y} L{b2:.1f} {y+10} M{b:.1f} {y} L{a2:.1f} {y+10}"></path>'
    deck = (f'<rect class="f-cloud" x="{cx-19}" y="92" width="38" height="12" rx="2"></rect>'
            + ''.join(f'<rect class="f-glow" x="{cx-16+i*6.5}" y="95" width="4" height="5" rx="1"></rect>' for i in range(5))
            + f'<rect class="ol thin" x="{cx-19}" y="92" width="38" height="12" rx="2"></rect>'
            + f'<rect class="f-cloud" x="{cx-8}" y="50" width="16" height="7" rx="2"></rect><rect class="f-glow" x="{cx-5}" y="52" width="10" height="3" rx="1"></rect><rect class="ol thin" x="{cx-8}" y="50" width="16" height="7" rx="2"></rect>')
    arch = f'<path class="f-sky2" d="M{cx-24} 166 Q{cx} 128 {cx+24} 166Z"></path><path class="ol thin" d="M{cx-24} 166 Q{cx} 128 {cx+24} 166"></path>'
    blds = ''
    for x, w, h, c in [(-6, 34, 44, "f-stone2"), (30, 26, 30, "f-stone"), (58, 30, 52, "f-blue"), (226, 28, 40, "f-stone"), (256, 34, 58, "f-stone2"), (292, 34, 34, "f-brick")]:
        blds += f'<rect class="{c}" x="{x}" y="{166-h}" width="{w}" height="{h}"></rect>'
        blds += ''.join(win(x + 5 + i * 9, 166 - h + 7 + j * 12, 4, 5) for j in range(max(1, (h - 12) // 12)) for i in range(max(1, (w - 6) // 9)))
        blds += f'<rect class="ol thin" x="{x}" y="{166-h}" width="{w}" height="{h}"></rect>'
    return svg(sky()
        + '<rect class="f-pink" x="-10" y="70" width="340" height="100" opacity="0.55"></rect><rect class="f-sun" x="-10" y="120" width="340" height="50" opacity="0.35"></rect>'
        + '<circle class="f-sun" cx="262" cy="112" r="18"></circle><circle class="ol thin" cx="262" cy="112" r="18"></circle>'
        + cloud(18, 24, 0.7) + cloud(218, 30, 0.55)
        + blds
        + f'<path class="f-red" d="{outline}"></path>'
        + '<path class="sh" d="M' + ' L'.join(f'{cx + hw(y):.1f} {y}' for y in ys) + ' L' + ' L'.join(f'{cx + hw(y)*0.35:.1f} {y}' for y in reversed(ys)) + 'Z"></path>'
        + bands + lattice + deck + arch
        + f'<path class="ol" d="{outline}"></path><path class="ol thin" d="M{cx} 4 V14"></path>'
        + tree(104, 150, 0.7, "f-green") + tree(214, 152, 0.65, "f-leaf") + tree(124, 156, 0.5, "f-leaf")
        + '<rect class="f-ground" x="-10" y="164" width="340" height="46"></rect><path class="ol thin" d="M-10 164 H330"></path>',
        "傍晚的東京鐵塔，腳下是小樓房和樹")

ALL.update({"tokyotower": tokyotower})
