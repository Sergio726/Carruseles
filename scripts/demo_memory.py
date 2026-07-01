#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Demo end-to-end de memoria STLabs sin Playwright ni fuentes embebidas."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import stlabs_kit as kit
from stlabs_memory import (
    BUILDS_DIR,
    INDEX_PATH,
    load_index,
    load_manifest,
    sugerir_familia,
    sugerir_fondo,
)


def main() -> int:
    fondo = sugerir_fondo()
    familia = sugerir_familia()
    print(f"Sugerencia fondo: {fondo}")
    print(f"Sugerencia familia: {familia}")

    cover = (
        '<div style="position:absolute;inset:0;display:flex;flex-direction:column;'
        'justify-content:center;align-items:center;text-align:center;padding:0 60px;">'
        '<h1 style="font-family:var(--disp);font-size:120px;color:#fff;">DEMO '
        '<span class="gr">MEMORIA</span></h1></div>'
    )
    slides = [
        kit.chrome(1, cover, total=1, bridges=None, paper=True),
    ]

    work = REPO / "_demo_work"
    work.mkdir(exist_ok=True)
    kit.write_html(slides, work / "carrusel.html")

    meta = {
        "titulo": "Demo Memoria STLabs",
        "slides": 1,
        "fondo": fondo,
        "familia_visual": familia,
        "origen": "original",
        "keyword_portada": "MEMORIA",
    }

    # Mock fonts para Windows / entornos sin /usr/share/fonts
    _orig = kit.embedded_fonts_css
    kit.embedded_fonts_css = lambda: ""
    try:
        out = kit.package(work, "demo-memoria", meta=meta)
    finally:
        kit.embedded_fonts_css = _orig

    build_id = meta["id"]
    manifest_path = BUILDS_DIR / build_id / "manifest.json"
    assert manifest_path.exists(), f"Falta manifest en {manifest_path}"
    assert out.resolve() == (BUILDS_DIR / build_id).resolve()

    idx = load_index()
    assert idx["ultimo_id"] == build_id
    m = load_manifest(BUILDS_DIR / build_id)
    print(f"OK — build registrado: {build_id}")
    print(f"  manifest: {manifest_path}")
    print(f"  índice: {INDEX_PATH} ({len(idx['carruseles'])} carruseles)")
    print(json.dumps(m, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
