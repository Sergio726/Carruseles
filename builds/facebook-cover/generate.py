# -*- coding: utf-8 -*-
"""Portada Facebook STLabs — 1640×624 (retina de 820×312)."""
from __future__ import annotations

import base64
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BUILD = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))

from stlabs_kit import embedded_fonts_css

SEB_URI = f"data:image/jpeg;base64,{base64.b64encode((REPO / 'seb.jpg').read_bytes()).decode()}"

CSS = """
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
body{background:#000;}
:root{--verde:#00FFB2;--blanco:#F2F2F2;--gray:#9aa39c;
 --mono:'IBM Plex Mono',monospace;--cond:'Barlow Condensed',sans-serif;
 --disp:'Bebas Neue',sans-serif;--pop:'Poppins',sans-serif;}
.fb-cover{position:relative;width:1640px;height:624px;overflow:hidden;color:var(--blanco);
 background:radial-gradient(42% 80% at 88% 50%, rgba(0,255,178,.14), transparent 55%),
  radial-gradient(30% 60% at 12% 80%, rgba(0,255,178,.06), transparent 50%),
  linear-gradient(105deg,#0a0a0a 0%,#0d0f0e 45%,#080808 100%);}
.fb-cover::before{content:'';position:absolute;inset:0;opacity:.35;pointer-events:none;
 background-image:linear-gradient(rgba(255,255,255,.02) 1px,transparent 1px),
  linear-gradient(90deg,rgba(255,255,255,.02) 1px,transparent 1px);background-size:48px 48px;}
.deco{position:absolute;inset:0;pointer-events:none;z-index:2;}
.deco-line{position:absolute;background:linear-gradient(90deg,transparent,rgba(0,255,178,.55),transparent);
 height:1px;transform-origin:left center;}
.deco-l1{top:88px;left:60px;width:340px;transform:rotate(-8deg);}
.deco-l2{bottom:120px;left:80px;width:280px;transform:rotate(5deg);opacity:.6;}
.deco-arc{position:absolute;right:18%;top:12%;width:180px;height:180px;border:1px solid rgba(0,255,178,.25);
 border-radius:50%;border-left-color:transparent;border-bottom-color:transparent;transform:rotate(-25deg);}
.deco-dot{position:absolute;width:6px;height:6px;border-radius:50%;background:var(--verde);
 box-shadow:0 0 12px rgba(0,255,178,.8);}
.deco-d1{top:56px;left:48px;} .deco-d2{bottom:48px;right:42%;} .deco-d3{top:42%;left:38%;}
.bk{position:absolute;width:28px;height:28px;border:2px solid rgba(0,255,178,.45);z-index:3;}
.bk-tl{top:28px;left:28px;border-right:none;border-bottom:none;}
.bk-br{bottom:28px;right:28px;border-left:none;border-top:none;}
.content{position:relative;z-index:4;padding:72px 0 0 88px;max-width:58%;}
.name1{font-family:var(--pop);font-weight:800;font-size:52px;letter-spacing:1px;line-height:1;}
.name2{font-family:var(--disp);font-size:118px;line-height:.88;color:var(--verde);letter-spacing:2px;
 text-shadow:0 0 40px rgba(0,255,178,.25);}
.role{margin-top:18px;font-family:var(--cond);font-size:28px;letter-spacing:3px;color:var(--blanco);}
.role span{color:var(--verde);font-weight:600;}
.role-line{width:320px;height:2px;margin-top:14px;background:linear-gradient(90deg,var(--verde),transparent);}
.services{margin-top:28px;display:flex;gap:28px;flex-wrap:wrap;}
.svc{display:flex;align-items:center;gap:10px;}
.svc-hex{width:36px;height:36px;clip-path:polygon(25% 6%,75% 6%,100% 50%,75% 94%,25% 94%,0 50%);
 background:rgba(0,255,178,.12);border:1px solid rgba(0,255,178,.35);display:flex;align-items:center;
 justify-content:center;font-family:var(--mono);font-size:14px;color:var(--verde);}
.svc span{font-family:var(--mono);font-size:13px;letter-spacing:1px;color:var(--gray);}
.photo{position:absolute;right:0;top:0;bottom:0;width:52%;z-index:1;}
.photo img{position:absolute;right:-4%;bottom:0;height:108%;width:auto;max-width:none;object-fit:cover;
 object-position:60% 20%;filter:brightness(.88) contrast(1.08) saturate(.85);}
.photo-scrim{position:absolute;inset:0;
 background:linear-gradient(90deg,#0a0a0a 0%,rgba(10,10,10,.92) 18%,rgba(10,10,10,.35) 42%,rgba(10,10,10,.08) 62%,transparent 78%),
  linear-gradient(180deg,rgba(10,10,10,.55) 0%,transparent 28%,transparent 72%,rgba(10,10,10,.75) 100%);}
.photo-glow{position:absolute;right:22%;top:18%;width:280px;height:280px;border-radius:50%;
 background:radial-gradient(circle,rgba(0,255,178,.18),transparent 70%);z-index:0;}
.url{position:absolute;left:88px;bottom:32px;z-index:5;font-family:var(--mono);font-size:18px;
 letter-spacing:2px;color:var(--verde);opacity:.85;}
"""

HTML = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<style>{embedded_fonts_css()}{CSS}</style></head><body>
<section class="fb-cover">
  <div class="photo-glow"></div>
  <div class="photo">
    <img src="{SEB_URI}" alt="Sebastián García">
    <div class="photo-scrim"></div>
  </div>
  <div class="deco">
    <div class="deco-line deco-l1"></div>
    <div class="deco-line deco-l2"></div>
    <div class="deco-arc"></div>
    <span class="deco-dot deco-d1"></span>
    <span class="deco-dot deco-d2"></span>
    <span class="deco-dot deco-d3"></span>
  </div>
  <span class="bk bk-tl"></span>
  <span class="bk bk-br"></span>
  <div class="content">
    <div class="name1">SEBASTIÁN</div>
    <div class="name2">GARCÍA</div>
    <div class="role">ARQUITECTO DE <span>SOLUCIONES DE IA</span></div>
    <div class="role-line"></div>
    <div class="services">
      <div class="svc"><span class="svc-hex">▣</span><span>ARQUITECTURA DE SISTEMAS</span></div>
      <div class="svc"><span class="svc-hex">◎</span><span>AGENTES INTELIGENTES</span></div>
      <div class="svc"><span class="svc-hex">▤</span><span>AUTOMATIZACIÓN CON IA</span></div>
      <div class="svc"><span class="svc-hex">◉</span><span>SOLUCIONES ESCALABLES</span></div>
    </div>
  </div>
  <div class="url">sebastian.stlabs.ar</div>
</section>
</body></html>"""


def render(out_png: Path) -> Path:
    from playwright.sync_api import sync_playwright

    html_path = BUILD / "cover.html"
    html_path.write_text(HTML, encoding="utf-8")
    out_png.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        pg = br.new_page(viewport={"width": 1640, "height": 624}, device_scale_factor=2)
        pg.goto(html_path.as_uri())
        pg.wait_for_function("document.fonts.ready")
        pg.wait_for_timeout(3500)
        pg.locator(".fb-cover").screenshot(path=str(out_png))
        br.close()
    return out_png


def main() -> int:
    dest = Path(r"C:\Users\Sebastian\Downloads\recusos carrousel\facebook-cover-stlabs.png")
    out = render(dest)
    # Copia estándar para subir directo
    std = dest.with_name("facebook-cover-820.png")
    from PIL import Image

    im = Image.open(out)
    im.resize((1640, 624), Image.Resampling.LANCZOS).save(out)
    im.resize((820, 312), Image.Resampling.LANCZOS).save(std)
    print("Listo:")
    print(" ", out)
    print(" ", std)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
