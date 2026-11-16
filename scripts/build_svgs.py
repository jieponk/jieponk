"""Generates the README section SVGs in assets/sections/ (same look as assets/banner.svg).
Run: python3 scripts/build_svgs.py"""
import os, html
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sections')
os.makedirs(OUT, exist_ok=True)
E = html.escape

STYLE = '''<style>
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono","DejaVu Sans Mono",monospace}
.sans{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}
.sweep{animation:sweep 5s ease-in-out infinite}@keyframes sweep{0%{transform:translateX(-260px)}60%,100%{transform:translateX(1260px)}}
.pulse{animation:pulse 2s ease-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes pulse{0%{transform:scale(1);opacity:.7}100%{transform:scale(3);opacity:0}}
.hl{animation:hl 7s steps(1) infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>'''

def lights(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="6" fill="#ff5f57"/><circle cx="{x+20}" cy="{y}" r="6" fill="#febc2e"/>'
            f'<circle cx="{x+40}" cy="{y}" r="6" fill="#28c840"/>')

def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{E(label)}">'
            f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#39d353" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="#b7ffc4"/><stop offset="1" stop-color="#39d353" stop-opacity="0"/></linearGradient></defs>'
            f'{STYLE}{body}</svg>')

# ---------- section header: VS Code-like tab strip ----------
ICON = {'js': ('#f1e05a', 'JS'), 'md': ('#519aba', 'MD'), 'sh': ('#89e051', '$_'), 'json': ('#cbcb41', '{}'), 'log': ('#8b949e', '≡')}
def header(name, file, kind, note):
    color, glyph = ICON[kind]
    tw = 70 + len(file) * 9.2
    nw = (len(name) + 2) * 10.4
    body = f'''
<rect x=".5" y=".5" width="1199" height="63" rx="10" fill="#0d1117" stroke="#30363d"/>
<path d="M10.5 .5h1179a10 10 0 0 1 10 10V26H.5V10.5a10 10 0 0 1 10-10z" fill="#161b22"/>
<line x1="0" y1="26" x2="1200" y2="26" stroke="#30363d"/>
{lights(22, 14)}
<g transform="translate(90,0)">
  <rect x="0" y="3" width="{tw}" height="24" fill="#0d1117"/>
  <line x1="0" y1="3" x2="0" y2="26" stroke="#30363d"/><line x1="{tw}" y1="3" x2="{tw}" y2="26" stroke="#30363d"/>
  <rect x="0" y="3" width="{tw}" height="2" fill="#0a84ff"/>
  <text x="14" y="19" class="mono" font-size="10" font-weight="700" fill="{color}">{E(glyph)}</text>
  <text x="38" y="19" class="mono" font-size="12" fill="#e6edf3">{E(file)}</text>
</g>
<text x="24" y="52" class="mono" font-size="17" font-weight="700" textLength="{nw:.0f}" lengthAdjust="spacingAndGlyphs"><tspan fill="#39d353">❯</tspan><tspan fill="#e6edf3"> {E(name)}</tspan></text>
<rect class="blink" x="{24 + nw + 6:.0f}" y="38" width="8" height="17" fill="#39d353"/>
<text x="1176" y="51" text-anchor="end" class="mono" font-size="13" fill="#6a9955">// {E(note)}</text>
<rect class="sweep" x="0" y="62" width="240" height="2" fill="url(#g)"/>'''
    return svg(1200, 64, body, name)

SECTIONS = [
    ('about', 'whoami', 'whoami.js', 'js', 'who I am & where I have been'),
    ('projects', 'featured.projects', 'projects.md', 'md', 'shipped & in use'),
    ('stack', 'stack', 'stack.json', 'json', 'tools I actually use'),
    ('stats', 'github.stats', 'stats.log', 'log', 'updated daily by Actions'),
]
for slug, name, file, kind, note in SECTIONS:
    open(os.path.join(OUT, f'{slug}.svg'), 'w').write(header(name, file, kind, note))

# ---------- about: whoami.js + career.log in one window ----------
def T(parts):  # [(color, text)] -> tspans
    return ''.join(f'<tspan fill="{c}">{E(t)}</tspan>' for c, t in parts)
K, F, S, P, C, N, D = '#ff7b72', '#d2a8ff', '#a5d6ff', '#e6edf3', '#6a9955', '#79c0ff', '#484f58'
code = [
    [(K, 'const '), (F, 'rudi'), (P, ' = {')],
    [(P, '  role:    '), (S, '"E-Commerce Specialist"'), (P, ',')],
    [(P, '  company: '), (S, '"PT Koolsnap Multi Retailindo"'), (P, ',')],
    [(P, '  stores:  ['), (S, '"Aneka Foto"'), (P, ', '), (S, '"Urbanix"'), (P, ', '), (S, '"GearNest"'), (P, '],')],
    [(P, '  base:    '), (S, '"Jakarta, Indonesia"'), (P, ',')],
    [(P, '  award:   '), (S, '"Shopee Award 2024 · Best Seller"'), (P, ',')],
    [(P, '};')],
    [(C, '// building systems for repetitive workflows')],
]
lines = ''.join(f'<text x="44" y="{100+i*24}" class="mono" font-size="14.5" xml:space="preserve">'
                f'<tspan fill="{D}">{i+1:>2}  </tspan>{T(l)}</text>' for i, l in enumerate(code))
career = [
    ('2026 → now', 'E-Commerce Specialist', 'PT Koolsnap Multi Retailindo', '#39d353'),
    ('2024', 'Shopee Award · Best Seller', 'marketplace achievement', '#ffd166'),
    ('2023 → 2026', 'E-Commerce Specialist', 'PT Sinar Agung Indotama', '#70a5fd'),
    ('2019 → 2023', 'Retail & store operations', '', '#8b949e'),
    ('2017 → 2019', 'Marketplace Admin', '', '#8b949e'),
]
tl = ['<line x1="660" y1="96" x2="660" y2="262" stroke="#30363d" stroke-width="2"/>']
for i, (yr, role, org, col) in enumerate(career):
    y = 96 + i * 41
    pulse = f'<circle class="pulse" cx="660" cy="{y}" r="5" fill="{col}"/>' if i == 0 else ''
    tl.append(f'<circle cx="660" cy="{y}" r="5" fill="{col}"/>{pulse}'
              f'<text x="680" y="{y+5}" class="mono" font-size="13" fill="{col}">{E(yr)}</text>'
              f'<text x="800" y="{y+5}" class="sans" font-size="14.5" font-weight="600" fill="#e6edf3">{E(role)}</text>'
              + (f'<text x="800" y="{y+22}" class="sans" font-size="12" fill="#8b949e">{E(org)}</text>' if org else ''))
hl = ('<rect x="30" y="0" width="560" height="22" rx="4" fill="#0a84ff" fill-opacity=".10">'
      '<animate attributeName="y" values="' + ';'.join(str(83 + i*24) for i in range(8)) + f'" dur="8s" calcMode="discrete" repeatCount="indefinite"/></rect>')
about = f'''
<rect x=".5" y=".5" width="1199" height="299" rx="14" fill="#0d1117" stroke="#30363d"/>
<path d="M14.5 .5h1171a14 14 0 0 1 14 14V34H.5V14.5a14 14 0 0 1 14-14z" fill="#161b22"/>
{lights(22, 17)}
<text x="600" y="22" text-anchor="middle" class="mono" font-size="12.5" fill="#8b949e">~/rudi — whoami.js · career.log</text>
<line x1="0" y1="34" x2="1200" y2="34" stroke="#30363d"/>
<line x1="610" y1="34" x2="610" y2="300" stroke="#30363d"/>
<text x="30" y="60" class="mono" font-size="12" fill="#8b949e">WHOAMI.JS</text>
<text x="640" y="60" class="mono" font-size="12" fill="#8b949e">CAREER.LOG</text>
{hl}{lines}{''.join(tl)}'''
open(os.path.join(OUT, 'about.svg'), 'w').write(svg(1200, 300, about, 'whoami and career log'))

# ---------- footer: ./status terminal ----------
status = [('[✓]', 'building systems'), ('[✓]', 'automating workflows'), ('[✓]', 'shipping projects'),
          ('[✓]', 'breaking things'), ('[✓]', 'fixing them again'), ('[→]', 'keep building...')]
n = len(status); cycle = 10
rows = []
for i, (mark, txt) in enumerate(status):
    t0 = (0.6 + i * 0.55) / cycle
    col = '#39d353' if mark == '[✓]' else '#ffd166'
    rows.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t0:.3f};{t0+0.02:.3f};.96;1" dur="{cycle}s" repeatCount="indefinite"/>'
                f'<text x="{40 + (i % 3) * 380}" y="{108 + (i // 3) * 30}" class="mono" font-size="15"><tspan fill="{col}">{mark}</tspan><tspan fill="#e6edf3"> {E(txt)}</tspan></text></g>')
footer = f'''
<rect x=".5" y=".5" width="1199" height="199" rx="14" fill="#0d1117" stroke="#30363d"/>
<path d="M14.5 .5h1171a14 14 0 0 1 14 14V34H.5V14.5a14 14 0 0 1 14-14z" fill="#161b22"/>
{lights(22, 17)}
<text x="600" y="22" text-anchor="middle" class="mono" font-size="12.5" fill="#8b949e">jieponk@github: ~ — zsh</text>
<line x1="0" y1="34" x2="1200" y2="34" stroke="#30363d"/>
<text x="40" y="72" class="mono" font-size="15"><tspan fill="#39d353">jieponk@github</tspan><tspan fill="#8b949e">:~$ </tspan><tspan fill="#e6edf3">./status</tspan></text>
{''.join(rows)}
<text x="40" y="178" class="mono" font-size="15"><tspan fill="#39d353">jieponk@github</tspan><tspan fill="#8b949e">:~$ </tspan></text>
<rect class="blink" x="203" y="164" width="9" height="17" fill="#39d353"/>
<text x="1160" y="178" text-anchor="end" class="mono" font-size="14" font-weight="700" fill="#6a9955">// code. coffee. ship. repeat.</text>
<path d="M.5 176h1199v9.5a14 14 0 0 1-14 14H14.5a14 14 0 0 1-14-14z" fill="#161b22" opacity="0"/>'''
open(os.path.join(OUT, 'footer.svg'), 'w').write(svg(1200, 200, footer, 'status: building systems, automating workflows, shipping projects. code. coffee. ship. repeat.'))
print('ok')
