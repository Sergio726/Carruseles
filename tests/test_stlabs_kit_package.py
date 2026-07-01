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
    meta = {
        "titulo": "Test Out",
        "fondo": "reticula_fina",
        "familia_visual": "guia_editorial",
        "slides": 1,
        "origen": "original",
        "keyword_portada": "TEST",
    }
    out = kit.package(build, "test-out", meta=meta)
    build_id = meta["id"]
    assert out.resolve() == (tmp_historial / "builds" / build_id).resolve()
    assert (out / "manifest.json").exists()
    manifest = __import__("json").loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["fondo"] == "reticula_fina"
    # Una sola carpeta en builds (sin duplicado out_name)
    dirs = [d for d in (tmp_historial / "builds").iterdir() if d.is_dir()]
    assert len(dirs) == 1


def test_package_rechaza_meta_incompleto(tmp_path, monkeypatch):
    import stlabs_kit as kit

    monkeypatch.setattr(kit, "embedded_fonts_css", lambda: "")
    build = tmp_path / "build"
    build.mkdir()
    (build / "carrusel.html").write_text("<html><style></style></html>", encoding="utf-8")
    with pytest.raises(ValueError, match="faltan"):
        kit.package(build, "x", meta={"fondo": "lino_tela"})
