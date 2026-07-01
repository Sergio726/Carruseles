from pathlib import Path

import pytest


def test_package_llama_registrar_con_meta(tmp_historial, tmp_path, monkeypatch):
    import stlabs_kit as kit
    import stlabs_memory as mem

    monkeypatch.setattr(kit, "embedded_fonts_css", lambda: "")
    monkeypatch.setattr(mem, "REPO_ROOT", tmp_historial)
    monkeypatch.setattr(mem, "HISTORIAL_DIR", tmp_historial / "historial")
    monkeypatch.setattr(mem, "BUILDS_DIR", tmp_historial / "builds")
    monkeypatch.setattr(mem, "INDEX_PATH", tmp_historial / "historial" / "carruseles.json")

    build = tmp_path / "build"
    build.mkdir()
    (build / "carrusel.html").write_text(
        "<html><style></style><body><div class='slide'></div></body></html>",
        encoding="utf-8",
    )
    out = kit.package(
        build,
        "test-out",
        output_dir=tmp_path / "out",
        meta={
            "fondo": "reticula_fina",
            "familia_visual": "guia_editorial",
            "slides": 1,
            "origen": "original",
        },
    )
    assert (out / "manifest.json").exists()
    manifest = __import__("json").loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["fondo"] == "reticula_fina"
