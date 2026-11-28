"""Builds assets/projects/urbanix-{dark,light}.svg: a crisp mock of the current urbanix.id home page
(black-grey + red palette, Gajian Sale event, voucher strip, product grid).
Run: python3 scripts/build_urbanix.py path/to/urbanix-logo-dark.png"""
import base64, io, os, sys
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'assets', 'projects')

def mark_png(src, white):
    im = Image.open(src).convert('RGBA')
    im = im.crop(im.getbbox())
    w, h = im.size
    im = im.crop((0, 0, w, int(h * 0.66)))  # the U mark only
    im.thumbnail((120, 120))
    if white:
        a = im.split()[3]
        im = Image.merge('RGBA', (Image.new('L', im.size, 255),) * 3 + (a,))
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode(), im.size

FONT = 'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"'
RED, RED_DARK = '#E30220', '#BE0000'

THEMES = {
    'dark': dict(page='#111111', bar='#191919', surface='#1c1c1c', card='#222222', line='#2e2e2e', ink='#F3F4F6',
                 muted='#9aa0a6', soft='#2a2a2a', chrome='#0d0d0d', chrome_bar='#1a1a1a', btn='#F3F4F6', onbtn='#111111',
                 hero='#1c1c1c', big='#262626', thumb='#2b2b2b', glyph='#4a4a4a'),
    'light': dict(page='#F3F4F6', bar='#191919', surface='#ffffff', card='#ffffff', line='#DDDDDD', ink='#191919',
                  muted='#5B6170', soft='#eceef1', chrome='#e7e8eb', chrome_bar='#d9dbdf', btn='#191919', onbtn='#ffffff',
                  hero='#ffffff', big='#eeeeee', thumb='#f1f2f4', glyph='#c4c7cc'),
}

def camera(x, y, s, c):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{c}" stroke-width="5" stroke-linejoin="round">'
            f'<rect x="4" y="16" width="72" height="48" rx="8"/><path d="M24 16l6-10h20l6 10"/><circle cx="40" cy="40" r="14"/></g>')

def build(theme, logo):
    t = THEMES[theme]
    uri, (lw, lh) = logo
    W, H = 1200, 750
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="urbanix.id home page ({theme})">')
    a(f'<rect width="{W}" height="{H}" fill="{t["page"]}"/>')
    # browser chrome
    a(f'<rect width="{W}" height="44" fill="{t["chrome"]}"/>')
    for i, c in enumerate(('#ff5f57', '#febc2e', '#28c840')):
        a(f'<circle cx="{24 + i * 20}" cy="22" r="6" fill="{c}"/>')
    a(f'<rect x="380" y="10" width="440" height="24" rx="12" fill="{t["chrome_bar"]}"/>')
    a(f'<text x="600" y="27" text-anchor="middle" {FONT} font-size="13" fill="{t["muted"]}">urbanix.id</text>')
    # announcement bar
    a(f'<rect y="44" width="{W}" height="30" fill="{t["bar"]}"/>')
    a(f'<rect x="438" y="51" width="38" height="16" rx="8" fill="{RED}"/><text x="457" y="63" text-anchor="middle" {FONT} font-size="10" font-weight="700" fill="#fff">25</text>')
    a(f'<text x="484" y="64" {FONT} font-size="13" fill="#F3F4F6"><tspan font-weight="700">Gajian Sale</tspan> sedang berlangsung · <tspan text-decoration="underline">Lihat semua diskon</tspan></text>')
    # header
    a(f'<rect y="74" width="{W}" height="72" fill="{t["surface"]}"/><line x1="0" y1="146" x2="{W}" y2="146" stroke="{t["line"]}"/>')
    lh2 = 40; lw2 = lw * lh2 / lh
    a(f'<image href="{uri}" x="40" y="90" width="{lw2:.1f}" height="{lh2}"/>')
    a(f'<text x="{48 + lw2:.0f}" y="108" {FONT} font-size="17" font-weight="800" letter-spacing="3" fill="{t["ink"]}">URBANIX</text>')
    a(f'<text x="{48 + lw2:.0f}" y="124" {FONT} font-size="9" letter-spacing="1" fill="{t["muted"]}">Capture Your Style</text>')
    for x, label in ((222, 'Kategori'), (312, 'Promo'), (384, 'Inspirasi')):
        a(f'<text x="{x}" y="115" {FONT} font-size="14" font-weight="600" fill="{t["ink"]}">{label}</text>')
    a(f'<rect x="500" y="92" width="420" height="38" rx="19" fill="{t["soft"]}"/>')
    a(f'<circle cx="524" cy="110" r="7" fill="none" stroke="{t["muted"]}" stroke-width="2"/><line x1="529" y1="115" x2="534" y2="120" stroke="{t["muted"]}" stroke-width="2"/>')
    a(f'<text x="544" y="116" {FONT} font-size="14" fill="{t["muted"]}">Cari kamera, lensa, mic…</text>')
    for i in range(3):
        a(f'<rect x="{960 + i * 46}" y="96" width="30" height="30" rx="8" fill="none" stroke="{t["ink"]}" stroke-width="1.6"/>')
    a(f'<text x="1110" y="116" {FONT} font-size="12" font-weight="700" fill="{t["ink"]}">ID/EN</text>')
    # hero (event)
    a(f'<rect x="40" y="170" width="720" height="250" rx="22" fill="{t["hero"]}" stroke="{t["line"]}"/>')
    a(f'<text x="560" y="350" {FONT} font-size="200" font-weight="900" fill="{t["big"]}">25</text>')
    a(f'<rect x="72" y="200" width="150" height="24" rx="12" fill="{RED}" opacity=".12"/><circle cx="88" cy="212" r="4" fill="{RED}"/>')
    a(f'<text x="100" y="217" {FONT} font-size="11" font-weight="800" letter-spacing="1.5" fill="{RED}">EVENT TERBATAS</text>')
    a(f'<text x="72" y="276" {FONT} font-size="46" font-weight="800" fill="{t["ink"]}">Gajian Sale</text>')
    a(f'<text x="72" y="308" {FONT} font-size="16" fill="{t["muted"]}">Gajian datang, waktunya upgrade gear: diskon sampai 69%,</text>')
    a(f'<text x="72" y="330" {FONT} font-size="16" fill="{t["muted"]}">original &amp; bergaransi.</text>')
    a(f'<rect x="72" y="352" width="180" height="44" rx="22" fill="{t["btn"]}"/><text x="162" y="380" text-anchor="middle" {FONT} font-size="15" font-weight="700" fill="{t["onbtn"]}">Belanja sekarang →</text>')
    a(f'<text x="276" y="380" {FONT} font-size="13" fill="{t["muted"]}">Berakhir dalam</text>')
    for i, v in enumerate(('02', '14', '37')):
        a(f'<rect x="{376 + i * 42}" y="362" width="34" height="26" rx="6" fill="{t["bar"]}"/><text x="{393 + i * 42}" y="380" text-anchor="middle" {FONT} font-size="13" font-weight="700" fill="#fff">{v}</text>')
    # side: vouchers
    a(f'<text x="790" y="194" {FONT} font-size="18" font-weight="800" fill="{t["ink"]}">Klaim voucher</text>')
    def voucher(y, color, big, title, sub):
        a(f'<rect x="790" y="{y}" width="370" height="98" rx="16" fill="{t["card"]}" stroke="{t["line"]}"/>')
        a(f'<path d="M806 {y}h66v98h-66a16 16 0 0 1-16-16v-66a16 16 0 0 1 16-16z" fill="{color}"/>')
        a(f'<circle cx="872" cy="{y}" r="8" fill="{t["page"]}"/><circle cx="872" cy="{y + 98}" r="8" fill="{t["page"]}"/>')
        a(f'<text x="831" y="{y + 56}" text-anchor="middle" {FONT} font-size="16" font-weight="800" fill="#fff">{big}</text>')
        a(f'<text x="892" y="{y + 36}" {FONT} font-size="15" font-weight="700" fill="{t["ink"]}">{title}</text>')
        a(f'<text x="892" y="{y + 58}" {FONT} font-size="12" fill="{t["muted"]}">{sub}</text>')
        a(f'<rect x="1078" y="{y + 64}" width="66" height="24" rx="12" fill="{t["btn"]}"/><text x="1111" y="{y + 81}" text-anchor="middle" {FONT} font-size="12" font-weight="700" fill="{t["onbtn"]}">Klaim</text>')
    voucher(212, RED, '8%', 'Diskon 8% s/d Rp200.000', 'Min. belanja Rp1.000.000')
    voucher(322, '#191919' if theme == 'light' else '#333333', 'Ongkir', 'Gratis ongkir s/d Rp40.000', 'Tanpa min. belanja')
    # product grid
    a(f'<text x="40" y="462" {FONT} font-size="20" font-weight="800" fill="{t["ink"]}">Gajian Sale 25.11</text>')
    a(f'<text x="1160" y="462" text-anchor="end" {FONT} font-size="14" font-weight="600" fill="{RED}">Lihat semua →</text>')
    disc = ('-25%', '-18%', '-12%', '-30%', '-9%')
    for i in range(5):
        x = 40 + i * 228
        a(f'<rect x="{x}" y="480" width="212" height="250" rx="16" fill="{t["card"]}" stroke="{t["line"]}"/>')
        a(f'<rect x="{x + 10}" y="490" width="192" height="140" rx="10" fill="{t["thumb"]}"/>')
        a(camera(x + 66, 520, 1.0, t['glyph']))
        a(f'<rect x="{x + 18}" y="498" width="44" height="20" rx="10" fill="{RED}"/><text x="{x + 40}" y="512" text-anchor="middle" {FONT} font-size="11" font-weight="800" fill="#fff">{disc[i]}</text>')
        a(f'<rect x="{x + 14}" y="646" width="170" height="10" rx="5" fill="{t["soft"]}"/><rect x="{x + 14}" y="664" width="120" height="10" rx="5" fill="{t["soft"]}"/>')
        a(f'<rect x="{x + 14}" y="688" width="96" height="14" rx="7" fill="{RED}" opacity=".85"/>')
        a(f'<rect x="{x + 14}" y="710" width="60" height="8" rx="4" fill="{t["soft"]}"/>')
    a('</svg>')
    return '\n'.join(o)

if __name__ == '__main__':
    src = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    for theme, white in (('dark', True), ('light', False)):
        svg = build(theme, mark_png(src, white))
        open(os.path.join(OUT, f'urbanix-{theme}.svg'), 'w').write(svg)
        print(theme, len(svg))
