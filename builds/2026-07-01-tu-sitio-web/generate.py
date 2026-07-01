# -*- coding: utf-8 -*-
"""Clon fiel Vilma (sitios web) → STLabs / Sebastián García."""
from __future__ import annotations

import base64
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BUILD = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))

from stlabs_kit import chrome, write_html, render, package

CTA_KEYWORD = "WEB"
SEB_URI = f"data:image/jpeg;base64,{base64.b64encode((REPO / 'seb.jpg').read_bytes()).decode()}"
SLIDE6_PATH = REPO / "assets" / "slide6-hero.png"
SLIDE6_URI = f"data:image/png;base64,{base64.b64encode(SLIDE6_PATH.read_bytes()).decode()}"
SLIDE1_PATH = REPO / "assets" / "slide1-hero.png"
SLIDE1_URI = f"data:image/png;base64,{base64.b64encode(SLIDE1_PATH.read_bytes()).decode()}"

EXTRA_CSS = """
.sheet .slide::after{content:'';position:absolute;inset:0;z-index:1;pointer-events:none;opacity:.55;mix-blend-mode:overlay;
 background:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E");
}
.hl-box{display:inline-block;background:rgba(0,255,178,.1);border:1px solid rgba(0,255,178,.4);
 padding:10px 20px;margin-top:24px;font-family:var(--cond);font-size:28px;}
.s-label{font-family:var(--mono);font-size:20px;color:var(--verde);letter-spacing:2px;margin-bottom:14px;}
.s-title{font-family:var(--pop);font-weight:800;font-size:50px;line-height:1.1;color:var(--blanco);margin-bottom:20px;}
.s-body{font-family:var(--cond);font-size:29px;line-height:1.4;color:var(--gray);max-width:920px;}
.s-body b{color:var(--blanco);}

.s1-wrap{position:relative;height:100%;overflow:hidden;}
.s1-head{position:relative;z-index:3;padding:72px 84px 0;}
.s1-t1{font-family:var(--cond);font-size:44px;color:var(--blanco);}
.s1-t2{font-family:var(--disp);font-size:132px;line-height:.86;color:var(--blanco);margin:6px 0;
 text-shadow:0 4px 32px rgba(0,0,0,.9);}
.s1-t3{font-family:var(--cond);font-size:44px;color:var(--blanco);}
.s1-head .hl-box{margin-top:20px;}
.s1-stage{position:absolute;inset:0;z-index:1;}
.s1-hero{position:absolute;inset:0;}
.s1-hero img{width:100%;height:100%;object-fit:contain;object-position:center bottom;}
.s1-scrim{position:absolute;inset:0;z-index:2;pointer-events:none;
 background:linear-gradient(180deg,rgba(10,10,10,.55) 0%,rgba(10,10,10,.12) 38%,rgba(10,10,10,0) 58%);}

.s2-grid{padding:88px 84px 0;display:grid;grid-template-columns:1fr 300px;gap:32px;}
.s2-side{font-family:var(--cond);font-size:32px;line-height:1.35;color:var(--gray);padding-top:30px;}
.s2-side b{color:var(--blanco);}
.lap-scene{position:relative;height:760px;margin-top:16px;}
.lap{width:500px;height:300px;background:linear-gradient(145deg,#4a4e54,#1b1d20);border-radius:14px;padding:10px;
 transform:perspective(700px) rotateX(7deg);}
.lap-sc{background:#0a0a0a;border-radius:8px;height:100%;}
.scroll-out{position:absolute;left:30px;top:260px;width:420px;border:1px solid #2a2a2a;border-radius:8px;overflow:hidden;
 box-shadow:0 28px 56px rgba(0,0,0,.8);}
.so-dark{background:#0d0d0d;padding:24px;text-align:center;}
.so-dark h4{font-family:var(--disp);font-size:36px;color:var(--verde);}
.so-mid{display:flex;gap:14px;padding:18px;background:#141414;align-items:center;}
.so-mid img{width:72px;height:72px;border-radius:50%;object-fit:cover;border:2px solid rgba(0,255,178,.4);}
.so-mid div{font-family:var(--cond);font-size:17px;color:var(--gray);}
.so-mid b{display:block;color:var(--verde);font-size:20px;margin-bottom:4px;}
.so-foot{background:#0a0a0a;padding:18px;font-family:var(--mono);font-size:13px;color:var(--gray);text-align:center;}

.s3-wrap{padding:76px 84px 0;}
.cards{position:relative;height:600px;margin-top:24px;}
.fc{position:absolute;width:190px;background:#141414;border:1px solid #2a2a2a;border-radius:10px;padding:14px;
 box-shadow:0 16px 32px rgba(0,0,0,.55);}
.fc1{left:100px;top:70px;transform:rotate(-7deg);}
.fc2{left:270px;top:30px;transform:rotate(3deg);z-index:2;}
.fc3{right:120px;top:90px;transform:rotate(5deg);}
.fc h5{font-family:var(--mono);font-size:13px;color:var(--verde);}
.fc p{font-family:var(--cond);font-size:15px;color:var(--gray);margin-top:6px;}
.lap3{position:absolute;left:50%;bottom:0;transform:translateX(-50%);width:540px;height:280px;
 background:linear-gradient(145deg,#4a4e54,#1b1d20);border-radius:12px;padding:8px;}
.lap3-sc{background:#0a0a0a;border-radius:6px;height:100%;}

.s4-wrap{padding:76px 84px 0;}
.phone-scene{position:absolute;right:70px;bottom:110px;width:300px;}
.pphone{background:linear-gradient(145deg,#4a4e54,#1b1d20);border-radius:32px;padding:10px;
 box-shadow:0 36px 72px rgba(0,0,0,.7);transform:perspective(500px) rotateY(-10deg);}
.pscr{background:#0a0a0a;border-radius:24px;height:460px;display:flex;flex-direction:column;
 align-items:center;justify-content:center;text-align:center;padding:20px;position:relative;}
.pscr::before{content:'';position:absolute;inset:16px;border:2px dashed rgba(0,255,178,.22);border-radius:16px;}
.pscr h4{font-family:var(--disp);font-size:30px;color:var(--verde);line-height:1.1;position:relative;z-index:1;}
.pscr span{font-family:var(--mono);font-size:12px;color:var(--gray);margin-top:10px;position:relative;z-index:1;}

.s5-top{padding:64px 84px 24px;height:46%;}
.s5-bot{position:absolute;left:0;right:0;bottom:0;height:54%;background:linear-gradient(180deg,#0a0a0a,#101820);}
.s5-scene{position:absolute;left:50%;bottom:90px;transform:translateX(-50%);width:880px;height:400px;}
.s5-lap{position:absolute;left:30px;bottom:0;width:460px;height:260px;background:linear-gradient(145deg,#4a4e54,#1b1d20);
 border-radius:10px;padding:8px;transform:perspective(500px) rotateY(6deg);}
.s5-lap-sc{background:#0a0a0a;border-radius:6px;height:100%;padding:20px;}
.s5-lap-sc h4{font-family:var(--disp);font-size:34px;color:var(--verde);}
.s5-lap-sc p{font-family:var(--cond);font-size:15px;color:var(--gray);margin-top:8px;}
.s5-photo{position:absolute;right:50px;bottom:10px;width:300px;height:370px;border-radius:14px;overflow:hidden;
 border:2px solid rgba(0,255,178,.35);box-shadow:0 24px 48px rgba(0,0,0,.65);}
.s5-photo img{width:100%;height:100%;object-fit:cover;filter:brightness(.5) contrast(1.05);}

.s6-wrap{position:relative;height:100%;overflow:hidden;}
.s6-head{position:relative;z-index:5;padding:44px 72px 0;text-align:center;}
.s6-h{font-family:var(--pop);font-weight:800;font-size:40px;line-height:1.1;max-width:900px;margin:0 auto;color:var(--blanco);
 text-shadow:0 2px 24px rgba(0,0,0,.85);}
.s6-cta{position:relative;margin:14px auto 0;background:rgba(8,8,8,.94);border:2px solid rgba(0,255,178,.28);
 border-radius:12px;padding:16px 28px;max-width:780px;backdrop-filter:blur(8px);
 box-shadow:0 12px 40px rgba(0,0,0,.65),0 0 0 1px rgba(0,255,178,.08) inset;}
.s6-cta::before,.s6-cta::after{content:'';position:absolute;width:18px;height:18px;border:2px solid var(--verde);opacity:.75;}
.s6-cta::before{top:-6px;left:-6px;border-right:none;border-bottom:none;}
.s6-cta::after{bottom:-6px;right:-6px;border-left:none;border-top:none;}
.s6-cta p{font-family:var(--cond);font-size:26px;color:var(--blanco);line-height:1.35;}
.s6-cta .kw{color:var(--verde);font-family:var(--pop);font-weight:800;}
.s6-stage{position:absolute;left:0;right:0;top:200px;bottom:88px;z-index:1;}
.s6-hero{position:absolute;inset:0;z-index:1;}
.s6-hero img{width:100%;height:100%;object-fit:contain;object-position:center bottom;}
.s6-scrim{position:absolute;inset:0;z-index:2;pointer-events:none;
 background:linear-gradient(180deg,rgba(10,10,10,.72) 0%,rgba(10,10,10,.08) 22%,rgba(10,10,10,0) 42%,
 rgba(10,10,10,.15) 72%,rgba(10,10,10,.88) 100%);}
.s6-mock{position:absolute;z-index:4;width:118px;background:#0d0d0d;border:1px solid rgba(0,255,178,.35);
 border-radius:10px;overflow:hidden;box-shadow:0 20px 48px rgba(0,0,0,.75),0 0 24px rgba(0,255,178,.12);}
.s6-mock-bar{height:22px;background:#1a1a1a;border-bottom:1px solid #2a2a2a;display:flex;align-items:center;gap:5px;padding:0 8px;}
.s6-mock-bar i{width:7px;height:7px;border-radius:50%;background:#333;}
.s6-mock-bar i:nth-child(1){background:#ff5f57;}
.s6-mock-bar i:nth-child(2){background:#febc2e;}
.s6-mock-bar i:nth-child(3){background:#28c840;}
.s6-mock-body{padding:10px 8px 12px;}
.s6-mock-hero{height:52px;border-radius:6px;background:linear-gradient(135deg,rgba(0,255,178,.22),rgba(0,255,178,.04));
 border:1px solid rgba(0,255,178,.25);display:flex;align-items:center;justify-content:center;text-align:center;
 font-family:var(--mono);font-size:9px;line-height:1.2;color:var(--verde);letter-spacing:.5px;}
.s6-mock-line{height:6px;border-radius:3px;background:#222;margin-top:7px;}
.s6-mock-line.w60{width:60%;}
.s6-mock-line.w80{width:80%;}
.s6-mock-line.w40{width:40%;}
.s6-mock-chart{margin-top:10px;height:44px;display:flex;align-items:flex-end;gap:4px;padding:0 2px;}
.s6-mock-chart span{flex:1;background:rgba(0,255,178,.35);border-radius:2px 2px 0 0;}
.s6-mock-l{left:28px;top:18%;transform:rotate(-8deg);}
.s6-mock-r{right:28px;top:22%;transform:rotate(7deg);}
.s6-chip{position:absolute;z-index:4;font-family:var(--mono);font-size:11px;color:var(--verde);
 background:rgba(10,10,10,.88);border:1px solid rgba(0,255,178,.4);border-radius:999px;padding:6px 12px;
 box-shadow:0 8px 24px rgba(0,0,0,.6);}
.s6-chip-a{left:50%;top:8%;transform:translateX(-50%);}
.s6-chip-b{right:18%;bottom:28%;}
.s6-chip-c{left:16%;bottom:32%;}
"""


def slide1():
    return chrome(1, f"""
<div class="s1-wrap">
  <div class="s1-stage">
    <div class="s1-hero"><img src="{SLIDE1_URI}" alt="Monitor y dashboard web"></div>
    <div class="s1-scrim"></div>
  </div>
  <div class="s1-head">
    <div class="s1-t1">Tu sitio web</div>
    <div class="s1-t2">NO ES</div>
    <div class="s1-t3">una tarjeta de presentación.</div>
    <div class="hl-box">O al menos, <b>no debería serlo.</b></div>
  </div>
</div>""", bridges="right", paper=False)


def slide2():
    return chrome(2, f"""
<div class="s2-grid">
  <div>
    <div class="s-title">Una web que trabaja por vos no nace del diseño.</div>
    <div class="lap-scene">
      <div class="lap"><div class="lap-sc"></div></div>
      <div class="scroll-out">
        <div class="so-dark"><h4>VUÉLVETE IRREMPLAZABLE</h4></div>
        <div class="so-mid"><img src="{SEB_URI}" alt=""><div><b>SOY SEBASTIÁN</b>RevOps · CRM · IA. Mentoría y sistemas que escalan.</div></div>
        <div class="so-foot">LA EDUCACIÓN ES LA SOLUCIÓN</div>
      </div>
    </div>
  </div>
  <div class="s2-side">Nace de la estrategia. Estos son <b>3 pilares</b> que la separan de una tarjeta digital.</div>
</div>""", bridges="both", paper=False)


def slide3():
    return chrome(3, """
<div class="s3-wrap">
  <div class="s-label">01</div>
  <div class="s-title">Arquetipo digital</div>
  <div class="s-body">No todas las webs sirven para lo mismo. Primero definís <b>qué tipo de sitio necesita tu modelo de negocio</b> y después diseñás.</div>
  <div class="cards">
    <div class="fc fc1"><h5>LANDING</h5><p>Captura · oferta clara</p></div>
    <div class="fc fc2"><h5>AUTORIDAD</h5><p>Contenido · confianza</p></div>
    <div class="fc fc3"><h5>VENTA</h5><p>Producto · conversión</p></div>
    <div class="lap3"><div class="lap3-sc"></div></div>
  </div>
</div>""", bridges="both", paper=False)


def slide4():
    return chrome(4, """
<div class="s4-wrap">
  <div class="s-label">02</div>
  <div class="s-title">Arquitectura estratégica</div>
  <div class="s-body">Las páginas, la estructura y el copy de cada sección no son decoración. Son el camino que guía al visitante hacia la acción. <b>Sin arquitectura, tu web es linda, pero se pierde.</b></div>
</div>
<div class="phone-scene"><div class="pphone"><div class="pscr">
  <h4>WEBSITE<br>UNDER<br>CONSTRUCTION</h4>
  <span>Armando estructura · secciones · copy</span>
</div></div></div>""", bridges="both", paper=False)


def slide5():
    return chrome(5, f"""
<div class="s5-top">
  <div class="s-label">03</div>
  <div class="s-title">Psicología web</div>
  <div class="s-body">Un sitio que convierte aplica neuromarketing: disparadores que generan confianza y mueven a la acción, sin ser invasivos. <b>La diferencia entre "qué lindo" y "quiero esto" está acá.</b></div>
</div>
<div class="s5-bot"><div class="s5-scene">
  <div class="s5-lap"><div class="s5-lap-sc"><h4>CONVERTÍ MÁS</h4><p>Disparadores mentales aplicados a tu web.</p></div></div>
  <div class="s5-photo"><img src="{SEB_URI}" alt="Sebastián García"></div>
</div></div>""", bridges="both", paper=False)


def slide6():
    return chrome(6, f"""
<div class="s6-wrap">
  <div class="s6-head">
    <div class="s6-h">Quiero enseñarte a construir la tuya.</div>
    <div class="s6-cta"><p>Comentá <span class="kw">{CTA_KEYWORD}</span> y te mando el acceso directo.</p></div>
  </div>
  <div class="s6-stage">
    <div class="s6-hero"><img src="{SLIDE6_URI}" alt="Sebastián"></div>
    <div class="s6-scrim"></div>
    <div class="s6-mock s6-mock-l">
      <div class="s6-mock-bar"><i></i><i></i><i></i></div>
      <div class="s6-mock-body">
        <div class="s6-mock-hero">TU<br>MARCA</div>
        <div class="s6-mock-line w80"></div>
        <div class="s6-mock-line w60"></div>
        <div class="s6-mock-line w40"></div>
      </div>
    </div>
    <div class="s6-mock s6-mock-r">
      <div class="s6-mock-bar"><i></i><i></i><i></i></div>
      <div class="s6-mock-body">
        <div class="s6-mock-hero">LANDING<br>+ CTA</div>
        <div class="s6-mock-chart"><span style="height:28px"></span><span style="height:40px"></span>
         <span style="height:22px"></span><span style="height:36px"></span><span style="height:30px"></span></div>
        <div class="s6-mock-line w80"></div>
      </div>
    </div>
    <span class="s6-chip s6-chip-a">// acceso directo</span>
    <span class="s6-chip s6-chip-b">conversión ↑</span>
    <span class="s6-chip s6-chip-c">estrategia web</span>
  </div>
</div>""", bridges="left", paper=False)


def main():
    slides = [slide1(), slide2(), slide3(), slide4(), slide5(), slide6()]
    write_html(slides, BUILD / "carrusel.html", extra_css=EXTRA_CSS)
    render(BUILD)
    out_dir = Path(r"C:\Users\Sebastian\Downloads\recusos carrousel\CARRUSEL-FINAL")
    meta = {
        "titulo": "Tu Sitio Web No Es Una Tarjeta",
        "slides": 6,
        "fondo": "concreto_industrial",
        "familia_visual": "operator_log",
        "origen": "screenshot",
        "keyword_portada": "WEB",
        "keyword_cta": CTA_KEYWORD,
        "handle_original": "vilma",
    }
    out = package(BUILD, "STLabs-Tu-Sitio-Web", output_dir=out_dir, meta=meta)
    print("Listo:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
