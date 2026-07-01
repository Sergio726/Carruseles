from stlabs_memory import (
    FONDOS,
    FAMILIAS,
    aplicar_plantilla,
    actualizar_feedback,
    empty_index,
    listar_builds,
    load_index,
    registrar_carrusel,
    registrar_entrada,
    resumen_para_agente,
    slugify,
    sugerir_familia,
    sugerir_fondo,
    load_manifest,
    cmd_status,
    cmd_suggest,
    cmd_feedback,
)


def test_catalogos_tienen_items_del_sistema_diseno():
    assert len(FONDOS) >= 7
    assert len(FAMILIAS) == 7
    assert "papel_corrugado" in FONDOS
    assert "operator_log" in FAMILIAS


def test_load_index_crea_vacio_si_no_existe(tmp_historial):
    idx = load_index()
    assert idx == empty_index()


def test_sugerir_fondo_evita_ultimo_usado(tmp_historial):
    registrar_entrada(
        {"id": "a", "fondo": "papel_corrugado", "familia_visual": "manifiesto"}
    )
    assert sugerir_fondo() != "papel_corrugado"


def test_sugerir_familia_evita_ultima_usada(tmp_historial):
    registrar_entrada(
        {"id": "a", "fondo": "lino_tela", "familia_visual": "operator_log"}
    )
    assert sugerir_familia() != "operator_log"


def test_sugerir_rota_cuando_todos_usados(tmp_historial):
    fondos = [
        "piedra_roca",
        "papel_corrugado",
        "concreto_industrial",
        "reticula_fina",
        "lino_tela",
        "roca_volcanica",
        "gradiente_profundo",
    ]
    for i, f in enumerate(fondos):
        registrar_entrada({"id": f"c{i}", "fondo": f, "familia_visual": "manifiesto"})
    assert sugerir_fondo() == "piedra_roca"


def test_resumen_incluye_sugerencias(tmp_historial):
    registrar_entrada(
        {
            "id": "test-1",
            "fondo": "papel_corrugado",
            "familia_visual": "blueprint",
            "titulo": "Demo",
        }
    )
    txt = resumen_para_agente()
    assert "papel_corrugado" in txt
    assert "blueprint" in txt
    assert "Sugerencia fondo" in txt
    assert "Sugerencia familia" in txt


def test_slugify():
    assert slugify("IA en RevOps 2026!") == "ia-en-revops-2026"


def test_registrar_carrusel_copia_outputs(tmp_historial, tmp_path):
    build = tmp_path / "out"
    build.mkdir()
    (build / "carrusel.html").write_text("<html></html>", encoding="utf-8")
    png_dir = build / "png"
    png_dir.mkdir()
    (png_dir / "slide-01.png").write_bytes(b"png")
    meta = {
        "titulo": "Test Carrusel",
        "slides": 1,
        "fondo": "lino_tela",
        "familia_visual": "manifiesto",
        "origen": "original",
        "keyword_portada": "TEST",
    }
    dest = registrar_carrusel(build, meta)
    assert dest.exists()
    assert (dest / "manifest.json").exists()
    assert (dest / "png" / "slide-01.png").exists()
    m = load_manifest(dest)
    assert m["titulo"] == "Test Carrusel"
    assert m["keyword_portada"] == "TEST"


def test_actualizar_feedback(tmp_historial, tmp_path):
    build = tmp_path / "out"
    build.mkdir()
    (build / "carrusel.html").write_text("<html></html>", encoding="utf-8")
    meta = {
        "id": "test-fb",
        "titulo": "FB Test",
        "slides": 1,
        "fondo": "lino_tela",
        "familia_visual": "manifiesto",
    }
    registrar_carrusel(build, meta)
    actualizar_feedback("test-fb", {"estado": "publicado", "notas": "ok"})
    m = load_manifest(tmp_historial / "builds" / "test-fb")
    assert m["feedback"]["estado"] == "publicado"
    assert m["feedback"]["notas"] == "ok"
    publicados = listar_builds(estado="publicado")
    assert len(publicados) == 1


def test_aplicar_plantilla(tmp_historial):
    result = aplicar_plantilla("educativo", ACCION="automatizar", DOLOR="perder leads", N="1", TITULO="Setup")
    assert "automatizar" in result["portada"]
    assert "Paso 1" in result["paso"]


def test_cmd_status_sin_datos(tmp_historial, capsys):
    assert cmd_status() == 0
    assert "Sin carruseles" in capsys.readouterr().out


def test_cmd_suggest_imprime_sugerencias(tmp_historial, capsys):
    assert cmd_suggest() == 0
    out = capsys.readouterr().out
    assert "Sugerencia fondo" in out


def test_cmd_feedback_invalido(tmp_historial):
    assert cmd_feedback("no-existe", "publicado", None) == 1
