# -*- coding: utf-8 -*-
"""
STLabs Carousel Kit — sistema de diseño reutilizable para carruseles de Sebastián García.
Uso típico desde un build nuevo:

    from stlabs_kit import *
    slides = [chrome(1, cover_html, bridges="right", footer=True), ...]
    write_html(slides, "/home/claude/buildX/carrusel.html")
    render("/home/claude/buildX")                 # -> png/slide-XX.png (retina 2160x2700)
    package("/home/claude/buildX", "STLabs-MiCarrusel")  # -> /mnt/user-data/outputs/...

Reglas de marca: ver SISTEMA-DISENO-CARRUSELES-STLABS.md
"""
import base64, pathlib, shutil, zipfile

# ─────────────────────────────────────────────────────────────────────────────
# 1. TOKENS DE MARCA
# ─────────────────────────────────────────────────────────────────────────────
VERDE="#00FFB2"; RED="#FF5247"; AMBER="#FF9D3C"
NEG="#0A0A0A"; GRAF="#141414"; GRIS="#1E1E1E"; BLANCO="#F2F2F2"; GRAY="#9aa39c"

STLABS = "/usr/share/fonts/truetype/stlabs/"
GFONTS = "/usr/share/fonts/truetype/google-fonts/"

# (familia, archivo, peso, estilo)
FONT_FACES = [
    ("Poppins", GFONTS+"Poppins-Bold.ttf", 700, "normal"),
    ("Poppins", GFONTS+"Poppins-Bold.ttf", 800, "normal"),
    ("Bebas Neue", STLABS+"BebasNeue-Regular.ttf", 400, "normal"),
    ("IBM Plex Mono", STLABS+"IBMPlexMono-Regular.ttf", 400, "normal"),
    ("IBM Plex Mono", STLABS+"IBMPlexMono-Medium.ttf", 500, "normal"),
    ("IBM Plex Mono", STLABS+"IBMPlexMono-SemiBold.ttf", 600, "normal"),
    ("Barlow Condensed", STLABS+"BarlowCondensed-Regular.ttf", 400, "normal"),
    ("Barlow Condensed", STLABS+"BarlowCondensed-Medium.ttf", 500, "normal"),
    ("Barlow Condensed", STLABS+"BarlowCondensed-SemiBold.ttf", 600, "normal"),
    ("Barlow Condensed", STLABS+"BarlowCondensed-Bold.ttf", 700, "normal"),
    ("Lora", GFONTS+"Lora-Italic-Variable.ttf", "400 700", "italic"),
]

def _face(fam, path, w, style):
    d = base64.b64encode(pathlib.Path(path).read_bytes()).decode()
    return (f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{w};"
            f"font-display:block;src:url(data:font/ttf;base64,{d}) format('truetype');}}")

def embedded_fonts_css():
    """Devuelve el bloque @font-face con TODAS las fuentes de marca en base64."""
    return "".join(_face(*f) for f in FONT_FACES)

# ─────────────────────────────────────────────────────────────────────────────
# 2. CSS BASE (tokens + chrome + componentes + mecánicas)
# ─────────────────────────────────────────────────────────────────────────────
BASE_CSS = """
:root{--verde:#00FFB2;--red:#FF5247;--am:#FF9D3C;--neg:#0A0A0A;--graf:#141414;--gris:#1E1E1E;
 --blanco:#F2F2F2;--gray:#9aa39c;
 --mono:'IBM Plex Mono',monospace;--cond:'Barlow Condensed',sans-serif;--disp:'Bebas Neue',sans-serif;
 --pop:'Poppins',sans-serif;--serif:'Lora',serif;}
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
body{background:#000;}
.sheet{display:flex;flex-direction:column;gap:48px;padding:48px;background:#000;}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;color:var(--blanco);
 background:radial-gradient(58% 36% at 84% 6%, rgba(0,255,178,.07), transparent 60%),
            radial-gradient(50% 36% at 12% 96%, rgba(0,255,178,.05), transparent 60%),
            linear-gradient(165deg,#0d0d0d,#070707 60%,#0b0b0b);}
.slide>*{position:relative;z-index:2;}
.gr{color:var(--verde);} .red{color:var(--red);} .am{color:var(--am);}
.ac{font-family:var(--serif);font-style:italic;font-weight:600;color:var(--verde);}
b{font-weight:700;color:#fff;}

/* retícula sutil opcional */
.grid::before{content:'';position:absolute;inset:0;z-index:0;opacity:.4;
 background-image:linear-gradient(rgba(255,255,255,.016) 1px,transparent 1px),
  linear-gradient(90deg,rgba(255,255,255,.016) 1px,transparent 1px);background-size:60px 60px;}

/* textura papel corrugado — .paper (notoria) / .paper.sutil */
.paper::after{content:'';position:absolute;inset:0;z-index:1;pointer-events:none;opacity:.8;mix-blend-mode:overlay;
 background:repeating-linear-gradient(90deg,
   rgba(255,255,255,.11) 0px, rgba(255,255,255,.11) 1.5px,
   rgba(255,255,255,0) 3px, rgba(255,255,255,0) 10px,
   rgba(0,0,0,.5) 12px, rgba(0,0,0,.5) 13.5px, rgba(255,255,255,0) 15px);}
.paper.sutil::after{opacity:.45;}

/* footer firma (obligatorio) */
.web{position:absolute;left:0;right:0;bottom:70px;text-align:center;z-index:6;font-family:var(--mono);
 font-size:25px;letter-spacing:2px;color:var(--verde);opacity:.9;}

/* contador, corchetes, puntitos (opcionales) */
.snum{position:absolute;top:64px;right:84px;z-index:8;font-family:var(--mono);font-size:21px;color:var(--verde);}
.bk{position:absolute;width:34px;height:34px;border:2px solid rgba(0,255,178,.55);z-index:6;}
.bk-tl{top:40px;left:40px;border-right:none;border-bottom:none;}
.bk-tr{top:40px;right:40px;border-left:none;border-bottom:none;}
.bk-bl{bottom:40px;left:40px;border-right:none;border-top:none;}
.bk-br{bottom:40px;right:40px;border-left:none;border-top:none;}
.dc{position:absolute;z-index:7;display:flex;gap:6px;}
.dc i{width:7px;height:7px;border-radius:50%;background:var(--verde);box-shadow:0 0 7px rgba(0,255,178,.6);}
.dc-tr{top:60px;right:88px;} .dc-bl{bottom:60px;left:88px;}

/* barra de progreso (opcional) */
.prog{position:absolute;left:84px;right:84px;bottom:120px;height:3px;background:#1c1c1c;z-index:8;border-radius:3px;overflow:hidden;}
.prog span{display:block;height:100%;background:var(--verde);box-shadow:0 0 10px rgba(0,255,178,.5);}

/* ── MECÁNICA: nodo-flecha partido por la costura ── */
.brnode{position:absolute;top:597px;width:156px;height:156px;border-radius:50%;z-index:8;
 background:radial-gradient(circle at 50% 45%,#151515,#0b0b0b);border:2px solid var(--verde);
 box-shadow:0 0 30px rgba(0,255,178,.3), inset 0 0 22px rgba(0,0,0,.6);
 display:flex;align-items:center;justify-content:center;}
.brnode span{font-family:var(--pop);font-weight:800;font-size:74px;color:var(--verde);line-height:1;}
.br-r{left:1002px;} .br-l{left:-78px;}

/* ── MECÁNICA: iPhone realista (entero) ── */
.iphone{position:relative;width:600px;height:1240px;padding:15px;border-radius:100px;
 background:linear-gradient(125deg,#4a4e54 0%,#1b1d20 15%,#0b0c0e 38%,#101113 52%,#1b1d20 78%,#52565c 100%);
 box-shadow:0 75px 150px rgba(0,0,0,.82),0 0 0 1.5px #000,inset 0 2px 4px rgba(255,255,255,.4),
  inset 0 -2px 4px rgba(255,255,255,.12),inset 3px 0 4px rgba(255,255,255,.18),inset -3px 0 4px rgba(255,255,255,.18);
 transform:perspective(2500px) rotateX(5deg) rotateY(-16deg) rotateZ(-7deg);transform-origin:center center;}
.ip-bezel{width:100%;height:100%;background:#050505;border-radius:86px;padding:13px;box-shadow:inset 0 0 0 2px #202225;}
.ip-screen{position:relative;width:100%;height:100%;border-radius:75px;overflow:hidden;
 background:radial-gradient(120% 80% at 50% 0%, #11140f, #070707);}
.ip-island{position:absolute;top:48px;left:50%;transform:translateX(-50%);width:132px;height:38px;background:#000;border-radius:22px;z-index:8;}
.ip-cam{position:absolute;right:20px;top:50%;transform:translateY(-50%);width:14px;height:14px;border-radius:50%;
 background:radial-gradient(circle at 38% 32%,#26333d,#03060a);}
.ip-reflect{position:absolute;inset:0;z-index:9;pointer-events:none;
 background:linear-gradient(118deg,rgba(255,255,255,.13) 0%,rgba(255,255,255,0) 19%,rgba(255,255,255,0) 70%,rgba(255,255,255,.06) 100%);}
.ip-side{position:absolute;background:linear-gradient(90deg,#3a3d42,#0d0e10);border-radius:5px;z-index:2;}
.ip-pwr{right:-7px;top:392px;width:8px;height:168px;}.ip-vu{left:-7px;top:356px;width:8px;height:104px;}
.ip-vd{left:-7px;top:480px;width:8px;height:104px;}.ip-act{left:-7px;top:252px;width:8px;height:60px;}
/* para partir el teléfono por la costura */
.phone-bridge{position:absolute;top:372px;width:600px;height:1320px;z-index:4;}
.pb-right{left:780px;} .pb-left{left:-300px;}

/* ── MECÁNICA: foto real integrada al negro ── */
.ph-bg{position:absolute;inset:0;z-index:0;width:100%;height:100%;object-fit:cover;
 filter:brightness(.55) contrast(1.05) saturate(.75);}
.ph-scrim{position:absolute;inset:0;z-index:1;
 background:radial-gradient(60% 40% at 80% 8%, rgba(0,255,178,.07), transparent 55%),
            linear-gradient(180deg, rgba(7,7,7,.32) 0%, rgba(7,7,7,.12) 34%, rgba(7,7,7,.82) 66%, #070707 92%);}
"""

# ─────────────────────────────────────────────────────────────────────────────
# 3. COMPONENTES / HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def web_footer():
    return '<div class="web">sebastian.stlabs.ar</div>'

def bridge(kind):
    """kind: 'right' | 'left' | 'both' | None"""
    n = ""
    if kind in ("right", "both"): n += '<div class="brnode br-r"><span>→</span></div>'
    if kind in ("left", "both"):  n += '<div class="brnode br-l"><span>→</span></div>'
    return n

def donut(year, rank, ia):
    """Dona de porcentaje: verde=IA, gris=humanos, arranca a las 12."""
    hu = round(100 - ia, 1); ia = round(ia, 1)
    return (f'<div class="cc"><div class="cc-top"><span class="cc-y">{year}</span>'
            f'<span class="cc-r">#{rank}</span></div>'
            f'<div class="donut" style="background:conic-gradient(from 0deg, var(--verde) 0 {ia}%, '
            f'#2c2c2c {ia}% 100%)"><i></i></div>'
            f'<div class="mbar"><span style="width:{ia}%"></span></div>'
            f'<div class="cc-lab"><span>Humanos {hu}%</span><span class="gr">IA {ia}%</span></div></div>')

DONUT_CSS = """
.cc{background:#121212;border:1px solid #242424;border-radius:16px;padding:18px 16px;display:flex;flex-direction:column;align-items:center;}
.cc-top{width:100%;display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}
.cc-y{font-family:var(--pop);font-weight:700;font-size:30px;color:#fff;}
.cc-r{font-family:var(--mono);font-size:18px;color:#666;}
.donut{width:132px;height:132px;border-radius:50%;display:flex;align-items:center;justify-content:center;}
.donut i{width:80px;height:80px;border-radius:50%;background:#121212;}
.mbar{width:100%;height:7px;background:#262626;border-radius:5px;margin-top:14px;overflow:hidden;}
.mbar span{display:block;height:100%;background:var(--verde);}
.cc-lab{width:100%;display:flex;justify-content:space-between;margin-top:10px;font-family:var(--mono);font-size:17px;color:#9a9a9a;}
"""

def phone(head="STLABS", badge="PREDICTIVO · 97% PRECISIÓN", hl='Tu trabajo tiene<br><span class="gr">los días contados.</span>',
          sub="Cuántos años le quedan a tu profesión.", placeholder="Escribí tu profesión…", btn="Analizar →"):
    return (f'<div class="iphone"><div class="ip-bezel"><div class="ip-screen">'
            f'<div class="ui"><div class="ui-head"><span class="ui-bolt">⚡</span>{head}</div>'
            f'<div class="ui-badge">{badge}</div><div class="ui-hl">{hl}</div>'
            f'<div class="ui-sub">{sub}</div><div class="ui-input">{placeholder}</div>'
            f'<div class="ui-btn">{btn}</div></div>'
            f'<div class="ip-island"><span class="ip-cam"></span></div><div class="ip-reflect"></div>'
            f'</div></div><span class="ip-side ip-act"></span><span class="ip-side ip-vu"></span>'
            f'<span class="ip-side ip-vd"></span><span class="ip-side ip-pwr"></span></div>')

PHONE_UI_CSS = """
.ui{padding:128px 58px 0;display:flex;flex-direction:column;align-items:center;text-align:center;}
.ui-head{display:flex;align-items:center;gap:12px;font-family:var(--cond);font-weight:700;font-size:48px;letter-spacing:3px;color:#fff;}
.ui-bolt{color:var(--verde);}
.ui-badge{margin-top:26px;font-family:var(--mono);font-size:15px;color:var(--verde);border:1px solid rgba(0,255,178,.5);border-radius:30px;padding:9px 17px;}
.ui-hl{margin-top:30px;font-family:var(--pop);font-weight:800;font-size:50px;line-height:1.02;color:#fff;}
.ui-sub{margin-top:20px;font-family:var(--cond);font-size:26px;color:#9aa39c;}
.ui-input{width:100%;margin-top:36px;background:#141414;border:1px solid #2e2e2e;border-radius:18px;padding:26px;font-family:var(--cond);font-size:36px;color:#6a6a6a;text-align:left;}
.ui-btn{width:100%;margin-top:16px;background:var(--verde);color:#04130b;border-radius:18px;font-family:var(--cond);font-weight:700;font-size:38px;padding:26px;box-shadow:0 0 44px rgba(0,255,178,.5);}
"""

def chrome(idx, inner, total=10, bridges="both", footer=True, counter=False, brackets=False, dots=False, paper=False):
    """Envuelve el contenido de un slide con el chrome estándar + mecánicas opcionales."""
    cls = "slide" + (" paper" if paper else "")
    parts = [f'<section class="{cls}">', inner]
    if counter:  parts.append(f'<div class="snum">{idx:02d}/{total:02d}</div>')
    if brackets: parts.append(''.join(f'<span class="bk bk-{c}"></span>' for c in ("tl","tr","bl","br")))
    if dots:     parts.append('<span class="dc dc-tr"><i></i><i></i><i></i></span><span class="dc dc-bl"><i></i><i></i><i></i></span>')
    if footer:   parts.append(web_footer())
    parts.append(bridge(bridges))
    parts.append('</section>')
    return ''.join(parts)

# ─────────────────────────────────────────────────────────────────────────────
# 4. ENSAMBLE / RENDER / PACKAGE
# ─────────────────────────────────────────────────────────────────────────────
def full_css(extra=""):
    return BASE_CSS + DONUT_CSS + PHONE_UI_CSS + extra

def write_html(slides, path, extra_css=""):
    """Escribe el HTML de trabajo (sin fuentes embebidas — se embeben en package)."""
    html = (f'<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">'
            f'<style>{full_css(extra_css)}</style></head>'
            f'<body><div class="sheet">{"".join(slides)}</div></body></html>')
    p = pathlib.Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8"); return p

def render(build_dir, html_name="carrusel.html"):
    """Playwright → png/slide-XX.png retina (2160x2700). Requiere playwright + chromium."""
    from playwright.sync_api import sync_playwright
    B = pathlib.Path(build_dir); (B/"png").mkdir(exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage"])
        pg = br.new_page(viewport={"width":1180,"height":1450}, device_scale_factor=2)
        pg.goto((B/html_name).as_uri())
        pg.wait_for_function("document.fonts.ready"); pg.wait_for_timeout(4000)
        for i, el in enumerate(pg.query_selector_all(".slide"), 1):
            el.screenshot(path=str(B/f"png/slide-{i:02d}.png"))
        br.close()
    return sorted((B/"png").glob("slide-*.png"))

def package(build_dir, out_name, html_name="carrusel.html"):
    """Embebe fuentes base64, copia PNGs, arma tira de preview + ZIP a /mnt/user-data/outputs/<out_name>/."""
    B = pathlib.Path(build_dir)
    html = (B/html_name).read_text(encoding="utf-8").replace("<style>", "<style>"+embedded_fonts_css(), 1)
    OUT = pathlib.Path("/mnt/user-data/outputs")/out_name; OUT.mkdir(parents=True, exist_ok=True)
    final_html = OUT/f"{out_name}.html"; final_html.write_text(html, encoding="utf-8")
    pngs = sorted((B/"png").glob("slide-*.png"))
    for p in pngs: shutil.copy(p, OUT/p.name)
    from PIL import Image
    ims=[Image.open(p) for p in pngs]; w,h=ims[0].size; sc=400
    strip=Image.new("RGB",(sc*len(ims),int(h*sc/w)),(10,10,10))
    for i,im in enumerate(ims): strip.paste(im.resize((sc,int(h*sc/w))),(i*sc,0))
    strip.save(OUT/"_preview-tira.png")
    with zipfile.ZipFile(OUT/f"{out_name}.zip","w",zipfile.ZIP_DEFLATED) as zf:
        for p in pngs: zf.write(p,p.name)
        zf.write(final_html, final_html.name)
    return OUT

# Demo mínima
if __name__ == "__main__":
    cover = ('<div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;'
             'align-items:center;text-align:center;padding:0 60px;z-index:5;">'
             '<h1 style="font-family:var(--disp);font-size:150px;line-height:.86;color:#fff;">DEMO '
             '<span class="gr">STLABS</span></h1></div>')
    s = [chrome(1, cover, total=2, bridges="right", paper=True),
         chrome(2, cover, total=2, bridges="left", paper=True)]
    write_html(s, "/home/claude/demo/carrusel.html")
    print("demo HTML escrito")
