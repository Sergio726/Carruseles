# Memoria Operativa STLabs — Implementation Plan

> **For Claude:** Use bite-sized tasks below in order. Cada fase es un checkpoint: no avanzar a la siguiente sin tests verdes.

**Goal:** Agregar memoria operativa local al proyecto Carruseles STLabs para recordar fondos, familias visuales y entregas pasadas, sin ML ni base de datos externa.

**Architecture:** Módulo `stlabs_memory.py` lee/escribe JSON en `historial/` y archiva cada entrega en `builds/<slug>/`. `stlabs_kit.package()` acepta metadata opcional y delega el registro. CLI expone `status` y `suggest`. Regla Cursor obliga al agente a consultar memoria al inicio de cada carrusel.

**Tech Stack:** Python 3.10+, stdlib (`json`, `pathlib`, `argparse`, `datetime`), `stlabs_kit.py` existente, `pytest` para tests, Cursor rules (`.mdc`).

---

## Contexto del codebase (leer antes de empezar)

| Archivo | Rol actual |
|---|---|
| `stlabs_kit.py` | Kit de diseño + `write_html`, `render`, `package` |
| `SISTEMA-DISENO-CARRUSELES-STLABS.md` | Reglas de marca; secciones 4 (fondos) y 5 (familias) son la fuente de catálogos |
| `seb.jpg` | Asset de foto; no tocar en esta feature |
| `carrusel-studio.skill` | Skill genérico Ruva; fuera de alcance |

**Paths a parametrizar:** `package()` hoy escribe a `/mnt/user-data/outputs/` (entorno Claude). La memoria debe usar paths relativos al repo (`builds/`, `historial/`) y un `output_dir` configurable.

---

## Estructura final del repo

```
Carruseles/
├── stlabs_kit.py                 # modificado: output_dir + hook memoria
├── stlabs_memory.py              # NUEVO
├── historial/
│   ├── carruseles.json           # índice ligero
│   └── plantillas_copy.json      # Fase 3
├── builds/
│   └── <slug>/
│       ├── manifest.json
│       ├── carrusel.html
│       ├── png/
│       ├── _preview-tira.png
│       └── <slug>.zip
├── tests/
│   ├── test_stlabs_memory.py
│   └── conftest.py
├── .cursor/rules/
│   └── carruseles-memoria.mdc    # Fase 3
├── docs/plans/
│   └── 2026-07-01-memoria-operativa-carruseles.md  # este archivo
├── requirements.txt              # playwright, pillow, pytest
└── SISTEMA-DISENO-CARRUSELES-STLABS.md  # + sección 8
```

---

# FASE 1 — MVP: índice + sugerencias (estimado: 2–3 h)

## Task 1: Bootstrap de tests y dependencias

**Files:**
- Create: `requirements.txt`
- Create: `tests/conftest.py`
- Create: `tests/__init__.py`

**Step 1: Crear `requirements.txt`**

```
playwright>=1.40.0
Pillow>=10.0.0
pytest>=8.0.0
```

**Step 2: Crear `tests/conftest.py`**

```python
import json
import pytest
from pathlib import Path

@pytest.fixture
def tmp_historial(tmp_path, monkeypatch):
    """Redirige REPO_ROOT e HISTORIAL a directorio temporal."""
    import stlabs_memory as mem
    monkeypatch.setattr(mem, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(mem, "HISTORIAL_DIR", tmp_path / "historial")
    monkeypatch.setattr(mem, "BUILDS_DIR", tmp_path / "builds")
    (tmp_path / "historial").mkdir()
    (tmp_path / "builds").mkdir()
    yield tmp_path
```

**Step 3: Instalar y verificar pytest**

```bash
pip install -r requirements.txt
pytest --version
```

Expected: versión de pytest impresa sin error.

**Step 4: Commit**

```bash
git add requirements.txt tests/
git commit -m "chore: bootstrap pytest y fixtures para memoria STLabs"
```

---

## Task 2: Catálogos y lectura del índice vacío

**Files:**
- Create: `stlabs_memory.py`
- Create: `historial/carruseles.json`
- Create: `tests/test_stlabs_memory.py`

**Step 1: Escribir test que falla**

```python
# tests/test_stlabs_memory.py
from stlabs_memory import FONDOS, FAMILIAS, load_index, empty_index

def test_catalogos_tienen_items_del_sistema_diseno():
    assert len(FONDOS) >= 7
    assert len(FAMILIAS) == 7
    assert "papel_corrugado" in FONDOS
    assert "operator_log" in FAMILIAS

def test_load_index_crea_vacio_si_no_existe(tmp_historial):
    idx = load_index()
    assert idx == empty_index()
```

**Step 2: Correr test — debe fallar**

```bash
pytest tests/test_stlabs_memory.py::test_catalogos_tienen_items_del_sistema_diseno -v
```

Expected: `ModuleNotFoundError: stlabs_memory`

**Step 3: Implementar mínimo en `stlabs_memory.py`**

```python
# -*- coding: utf-8 -*-
"""Memoria operativa para carruseles STLabs."""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
HISTORIAL_DIR = REPO_ROOT / "historial"
BUILDS_DIR = REPO_ROOT / "builds"
INDEX_PATH = HISTORIAL_DIR / "carruseles.json"

FONDOS = [
    "piedra_roca", "papel_corrugado", "concreto_industrial",
    "reticula_fina", "lino_tela", "roca_volcanica", "gradiente_profundo",
]
FAMILIAS = [
    "manifiesto", "blueprint", "operator_log", "dossier_editorial",
    "before_after", "dashboard_minimo", "guia_editorial",
]

def empty_index() -> dict:
    return {"ultimo_id": None, "carruseles": []}

def load_index() -> dict:
    HISTORIAL_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_PATH.exists():
        return empty_index()
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))

def save_index(data: dict) -> None:
    HISTORIAL_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
```

**Step 4: Crear `historial/carruseles.json` inicial**

```json
{
  "ultimo_id": null,
  "carruseles": []
}
```

**Step 5: Correr tests — deben pasar**

```bash
pytest tests/test_stlabs_memory.py::test_catalogos_tienen_items_del_sistema_diseno tests/test_stlabs_memory.py::test_load_index_crea_vacio_si_no_existe -v
```

**Step 6: Commit**

```bash
git add stlabs_memory.py historial/carruseles.json tests/test_stlabs_memory.py
git commit -m "feat(fase1): catálogos y carga de índice de memoria"
```

---

## Task 3: Sugerencias de fondo y familia (rotación)

**Files:**
- Modify: `stlabs_memory.py`
- Modify: `tests/test_stlabs_memory.py`

**Step 1: Tests que fallan**

```python
from stlabs_memory import sugerir_fondo, sugerir_familia, registrar_entrada

def test_sugerir_fondo_evita_ultimo_usado(tmp_historial):
    registrar_entrada({"id": "a", "fondo": "papel_corrugado", "familia_visual": "manifiesto"})
    assert sugerir_fondo() != "papel_corrugado"

def test_sugerir_familia_evita_ultima_usada(tmp_historial):
    registrar_entrada({"id": "a", "fondo": "lino_tela", "familia_visual": "operator_log"})
    assert sugerir_familia() != "operator_log"

def test_sugerir_rota_cuando_todos_usados(tmp_historial):
    for i, f in enumerate(["piedra_roca", "papel_corrugado", "concreto_industrial",
                            "reticula_fina", "lino_tela", "roca_volcanica", "gradiente_profundo"]):
        registrar_entrada({"id": f"c{i}", "fondo": f, "familia_visual": "manifiesto"})
    # Con todos usados recientemente, devuelve el menos reciente (el primero registrado)
    assert sugerir_fondo() == "piedra_roca"
```

**Step 2: Implementar**

```python
def _ultimos(items: list[dict], key: str, n: int = 5) -> list[str]:
    return [c[key] for c in items[-n:] if c.get(key)]

def sugerir_fondo(ventana: int = 5) -> str:
    usados = _ultimos(load_index()["carruseles"], "fondo", ventana)
    for f in FONDOS:
        if f not in usados:
            return f
    return FONDOS[0]  # todos usados: rotar al más antiguo del catálogo

def sugerir_familia(ventana: int = 5) -> str:
    usados = _ultimos(load_index()["carruseles"], "familia_visual", ventana)
    for f in FAMILIAS:
        if f not in usados:
            return f
    return FAMILIAS[0]

def registrar_entrada(meta: dict) -> None:
    idx = load_index()
    entrada = {
        "id": meta["id"],
        "fecha": meta.get("fecha", date.today().isoformat()),
        "titulo": meta.get("titulo", ""),
        "slides": meta.get("slides"),
        "fondo": meta["fondo"],
        "familia_visual": meta["familia_visual"],
    }
    idx["carruseles"].append(entrada)
    idx["ultimo_id"] = entrada["id"]
    save_index(idx)
```

**Step 3: Correr tests**

```bash
pytest tests/test_stlabs_memory.py -v -k "sugerir"
```

**Step 4: Commit**

```bash
git add stlabs_memory.py tests/test_stlabs_memory.py
git commit -m "feat(fase1): sugerir fondo y familia con rotación"
```

---

## Task 4: Resumen para agente

**Files:**
- Modify: `stlabs_memory.py`
- Modify: `tests/test_stlabs_memory.py`

**Step 1: Test**

```python
from stlabs_memory import resumen_para_agente, registrar_entrada

def test_resumen_incluye_sugerencias(tmp_historial):
    registrar_entrada({"id": "test-1", "fondo": "papel_corrugado", "familia_visual": "blueprint", "titulo": "Demo"})
    txt = resumen_para_agente()
    assert "papel_corrugado" in txt
    assert "blueprint" in txt
    assert "Sugerencia fondo" in txt
    assert "Sugerencia familia" in txt
```

**Step 2: Implementar**

```python
def ultimo() -> dict | None:
    carruseles = load_index()["carruseles"]
    return carruseles[-1] if carruseles else None

def resumen_para_agente() -> str:
    u = ultimo()
    sf, sfa = sugerir_fondo(), sugerir_familia()
    lines = ["## Memoria STLabs — contexto automático", ""]
    if u:
        lines += [
            f"**Último carrusel:** `{u['id']}` ({u.get('fecha', '?')})",
            f"- Fondo: `{u.get('fondo')}` · Familia: `{u.get('familia_visual')}`",
            f"- Título: {u.get('titulo') or '(sin título)'}",
            "",
        ]
    else:
        lines += ["_Sin carruseles registrados aún._", ""]
    lines += [
        f"**Sugerencia fondo:** `{sf}`",
        f"**Sugerencia familia:** `{sfa}`",
        "",
        "_Regla: no repetir fondo ni familia del último carrusel salvo indicación explícita._",
    ]
    return "\n".join(lines)
```

**Step 3: pytest + commit**

```bash
pytest tests/test_stlabs_memory.py::test_resumen_incluye_sugerencias -v
git add stlabs_memory.py tests/test_stlabs_memory.py
git commit -m "feat(fase1): resumen markdown para agente"
```

---

## Task 5: Documentar sección 8 en sistema de diseño

**Files:**
- Modify: `SISTEMA-DISENO-CARRUSELES-STLABS.md` (append after sección 7)

**Contenido a agregar:**

```markdown
---

## 8. Memoria operativa (obligatorio)

Antes de crear cualquier carrusel:
1. Leer `historial/carruseles.json` o ejecutar `python stlabs_memory.py suggest`
2. Usar fondo y familia sugeridos (distintos al último salvo pedido explícito)
3. Al empaquetar, pasar `meta=` a `package()` con manifest completo

Campos mínimos del manifest: `id`, `titulo`, `slides`, `fondo`, `familia_visual`, `origen` (`screenshot`|`original`), `keyword_portada`.
```

**Commit:**

```bash
git add SISTEMA-DISENO-CARRUSELES-STLABS.md
git commit -m "docs: sección 8 memoria operativa en sistema de diseño"
```

---

### Checkpoint Fase 1

```bash
pytest tests/test_stlabs_memory.py -v
python -c "from stlabs_memory import resumen_para_agente; print(resumen_para_agente())"
```

Expected: todos los tests PASS; resumen impreso con sugerencias.

---

# FASE 2 — Builds archivados + CLI + hook en package (estimado: 3–4 h)

## Task 6: `registrar_carrusel` y slug automático

**Files:**
- Modify: `stlabs_memory.py`
- Modify: `tests/test_stlabs_memory.py`

**Step 1: Tests**

```python
from pathlib import Path
from stlabs_memory import slugify, registrar_carrusel, load_manifest

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
```

**Step 2: Implementar**

```python
import re
import shutil
from datetime import date

def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "carrusel"

def _default_id(titulo: str) -> str:
    return f"{date.today().isoformat()}-{slugify(titulo)}"

def registrar_carrusel(build_dir: Path, meta: dict) -> Path:
    build_dir = Path(build_dir)
    meta = dict(meta)
    meta.setdefault("id", _default_id(meta.get("titulo", "carrusel")))
    meta.setdefault("fecha", date.today().isoformat())

    dest = BUILDS_DIR / meta["id"]
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(build_dir, dest)

    (dest / "manifest.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    registrar_entrada(meta)
    return dest

def load_manifest(build_path: Path) -> dict:
    return json.loads((Path(build_path) / "manifest.json").read_text(encoding="utf-8"))
```

**Step 3: pytest + commit**

```bash
pytest tests/test_stlabs_memory.py -v -k "slugify or registrar_carrusel"
git commit -am "feat(fase2): registrar carrusel en builds/ con manifest"
```

---

## Task 7: Parametrizar `package()` y conectar memoria

**Files:**
- Modify: `stlabs_kit.py:235-251`
- Create: `tests/test_stlabs_kit_package.py`
- Modify: `tests/conftest.py` (mock fonts si hace falta)

**Step 1: Cambiar firma de `package`**

```python
def package(build_dir, out_name, html_name="carrusel.html", output_dir=None, meta=None):
    """
    Embebe fuentes, copia PNGs, arma tira + ZIP.
    output_dir: destino (default REPO/builds/<out_name> o legado /mnt/user-data/outputs)
    meta: dict opcional → dispara registrar_carrusel() al finalizar
    """
    from stlabs_memory import REPO_ROOT, registrar_carrusel
    B = pathlib.Path(build_dir)
    html = (B/html_name).read_text(encoding="utf-8").replace("<style>", "<style>"+embedded_fonts_css(), 1)

    if output_dir is None:
        output_dir = REPO_ROOT / "builds" / out_name
    OUT = pathlib.Path(output_dir)
    OUT.mkdir(parents=True, exist_ok=True)
    # ... resto igual (final_html, pngs, strip, zip) ...

    if meta is not None:
        meta.setdefault("titulo", out_name)
        registrar_carrusel(OUT, meta)
    return OUT
```

**Nota implementación:** `embedded_fonts_css()` falla en Windows si no hay fuentes en `/usr/share/fonts/`. Para tests, mockear `embedded_fonts_css` retornando `""` o saltar test de package si fonts no existen:

```python
@pytest.mark.skipif(not Path("/usr/share/fonts").exists(), reason="fuentes STLabs no instaladas")
```

**Step 2: Test de integración ligero (mock fonts)**

```python
def test_package_llama_registrar_con_meta(tmp_historial, tmp_path, monkeypatch):
    import stlabs_kit as kit
    monkeypatch.setattr(kit, "embedded_fonts_css", lambda: "")
    build = tmp_path / "build"
    build.mkdir()
    (build / "carrusel.html").write_text("<html><style></style><body><div class='slide'></div></body></html>")
    # Sin render real; package solo necesita html + png opcional
    out = kit.package(build, "test-out", output_dir=tmp_path/"out", meta={
        "fondo": "reticula_fina", "familia_visual": "guia_editorial", "slides": 1, "origen": "original"
    })
    assert (out / "manifest.json").exists()
```

**Step 3: pytest + commit**

```bash
pytest tests/test_stlabs_kit_package.py -v
git commit -am "feat(fase2): package() con output_dir local y hook de memoria"
```

---

## Task 8: CLI `stlabs_memory.py`

**Files:**
- Modify: `stlabs_memory.py` (append `main()`)
- Modify: `tests/test_stlabs_memory.py`

**Step 1: Tests CLI**

```python
from stlabs_memory import cmd_status, cmd_suggest

def test_cmd_status_sin_datos(tmp_historial, capsys):
    assert cmd_status() == 0
    assert "Sin carruseles" in capsys.readouterr().out

def test_cmd_suggest_imprime_sugerencias(tmp_historial, capsys):
    assert cmd_suggest() == 0
    out = capsys.readouterr().out
    assert "Sugerencia fondo" in out
```

**Step 2: Implementar**

```python
def cmd_status() -> int:
    u = ultimo()
    if not u:
        print("Sin carruseles registrados.")
        return 0
    print(f"Último: {u['id']} ({u['fecha']})")
    print(f"  Fondo: {u['fondo']} | Familia: {u['familia_visual']}")
    print(f"  Total en índice: {len(load_index()['carruseles'])}")
    return 0

def cmd_suggest() -> int:
    print(resumen_para_agente())
    return 0

def main():
    import argparse
    p = argparse.ArgumentParser(description="Memoria operativa STLabs")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("suggest")
    args = p.parse_args()
    if args.cmd == "status":
        raise SystemExit(cmd_status())
    if args.cmd == "suggest":
        raise SystemExit(cmd_suggest())

if __name__ == "__main__":
    main()
```

**Step 3: Verificar manualmente**

```bash
python stlabs_memory.py suggest
python stlabs_memory.py status
```

**Step 4: Commit**

```bash
git add stlabs_memory.py tests/test_stlabs_memory.py
git commit -m "feat(fase2): CLI status y suggest"
```

---

## Task 9: Actualizar checklist sección 7

**Files:**
- Modify: `SISTEMA-DISENO-CARRUSELES-STLABS.md` sección 7

Reemplazar paso 3 por:

```
3. Ejecutar `python stlabs_memory.py suggest` → elegir fondo/familia sugeridos
```

Agregar paso 9:

```
9. `package(..., meta={...})` registra en builds/ e historial/
```

**Commit:** `docs: checklist actualizado con memoria y package meta`

---

### Checkpoint Fase 2

```bash
pytest tests/ -v
python stlabs_memory.py status
```

Expected: índice y builds coherentes tras un package de prueba.

---

# FASE 3 — Memoria rica + reglas agente + plantillas (estimado: 2–3 h)

## Task 10: Campo `feedback` y listado de builds

**Files:**
- Modify: `stlabs_memory.py`
- Modify: `tests/test_stlabs_memory.py`

**Esquema extendido de manifest:**

```json
{
  "feedback": {
    "estado": "borrador | publicado | descartado",
    "notas": "",
    "metricas": { "saves": null, "shares": null, "comentarios": null }
  }
}
```

**Funciones:**

```python
def actualizar_feedback(build_id: str, feedback: dict) -> None:
    path = BUILDS_DIR / build_id / "manifest.json"
    m = json.loads(path.read_text(encoding="utf-8"))
    m["feedback"] = {**m.get("feedback", {}), **feedback}
    path.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")

def listar_builds(estado: str | None = None) -> list[dict]:
    builds = []
    for d in sorted(BUILDS_DIR.iterdir()):
        if (d / "manifest.json").exists():
            m = load_manifest(d)
            if estado is None or m.get("feedback", {}).get("estado") == estado:
                builds.append(m)
    return builds
```

**CLI:** subcomando `feedback <id> --estado publicado --notas "..."`

**Tests:** registrar build → actualizar feedback → listar filtrado.

**Commit:** `feat(fase3): feedback manual y listado de builds`

---

## Task 11: Plantillas de copy reutilizables

**Files:**
- Create: `historial/plantillas_copy.json`
- Modify: `stlabs_memory.py`
- Modify: `tests/test_stlabs_memory.py`

**Contenido inicial `plantillas_copy.json`:**

```json
{
  "screenshot_clone": {
    "portada": "{KEYWORD} en {TEMA}",
    "cta_final": "Comentá {KEYWORD} y te mando el recurso.",
    "footer_siempre": "sebastian.stlabs.ar"
  },
  "educativo": {
    "portada": "Cómo {ACCION} sin {DOLOR}",
    "paso": "Paso {N}: {TITULO}",
    "cta_final": "Guardá esto para cuando lo necesites."
  }
}
```

**Funciones:**

```python
def plantilla(nombre: str) -> dict:
    path = HISTORIAL_DIR / "plantillas_copy.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data[nombre]

def aplicar_plantilla(nombre: str, **kwargs) -> dict:
    tpl = plantilla(nombre)
    return {k: v.format(**kwargs) for k, v in tpl.items()}
```

**CLI:** `python stlabs_memory.py plantilla educativo --ACCION automatizar --DOLOR perder leads`

**Commit:** `feat(fase3): plantillas de copy con placeholders`

---

## Task 12: Regla Cursor para el agente

**Files:**
- Create: `.cursor/rules/carruseles-memoria.mdc`

```markdown
---
description: Memoria operativa STLabs — consultar antes de cada carrusel
globs: "**/*"
alwaysApply: true
---

# Carruseles STLabs — Memoria obligatoria

Al iniciar trabajo de carrusel en este repo:

1. Ejecutar `python stlabs_memory.py suggest` o leer `historial/carruseles.json`
2. Proponer fondo y familia distintos al último carrusel (salvo pedido explícito)
3. Al finalizar `package()`, pasar `meta` completo con: id, titulo, slides, fondo, familia_visual, origen, keyword_portada
4. Si el carrusel se publica, registrar feedback con `python stlabs_memory.py feedback <id> --estado publicado`

Referencia: `SISTEMA-DISENO-CARRUSELES-STLABS.md` secciones 7 y 8.
```

**Commit:** `chore(fase3): regla Cursor para memoria STLabs`

---

## Task 13: README del proyecto

**Files:**
- Modify: `README.md`

Incluir:
- Qué es el proyecto
- Instalación (`pip install -r requirements.txt`, `playwright install chromium`)
- Comandos de memoria (`suggest`, `status`, `feedback`)
- Flujo resumido generate → render → package(meta=...)
- Link a `SISTEMA-DISENO-CARRUSELES-STLABS.md`

**Commit:** `docs: README con memoria operativa y flujo de trabajo`

---

## Task 14: `.gitignore` para builds pesados (opcional)

**Files:**
- Create: `.gitignore`

```
builds/**/png/
builds/**/*.zip
__pycache__/
.pytest_cache/
_skill_extract/
```

**Decisión:** commitear `manifest.json` y `historial/*.json`; ignorar PNGs/ZIPs si son muy pesados. Ajustar según preferencia del equipo.

**Commit:** `chore: gitignore para outputs binarios`

---

### Checkpoint Fase 3 (final)

```bash
pytest tests/ -v
python stlabs_memory.py suggest
python stlabs_memory.py status
python stlabs_memory.py feedback <id-test> --estado publicado
```

Manual: abrir Cursor en el repo y verificar que la regla `carruseles-memoria` aparece activa.

---

## Orden de ejecución y commits sugeridos

| # | Commit message | Fase |
|---|---|---|
| 1 | `chore: bootstrap pytest y fixtures` | 1 |
| 2 | `feat(fase1): catálogos e índice` | 1 |
| 3 | `feat(fase1): sugerencias rotación` | 1 |
| 4 | `feat(fase1): resumen para agente` | 1 |
| 5 | `docs: sección 8 memoria` | 1 |
| 6 | `feat(fase2): registrar en builds/` | 2 |
| 7 | `feat(fase2): package con meta` | 2 |
| 8 | `feat(fase2): CLI status/suggest` | 2 |
| 9 | `docs: checklist con memoria` | 2 |
| 10 | `feat(fase3): feedback y listado` | 3 |
| 11 | `feat(fase3): plantillas copy` | 3 |
| 12 | `chore(fase3): regla Cursor` | 3 |
| 13 | `docs: README completo` | 3 |
| 14 | `chore: gitignore outputs` | 3 |

---

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Fuentes no existen en Windows | `output_dir` local; tests mockean `embedded_fonts_css` |
| Paths Claude `/mnt/user-data/` | `package(output_dir=REPO/builds/...)` por defecto en repo |
| Índice corrupto | `load_index()` valida schema mínimo; si falla, backup + `empty_index()` |
| Repetición de fondos con pocos carruseles | ventana configurable (`ventana=5`) en `sugerir_*` |

---

## Fuera de alcance (YAGNI)

- Supabase / Postgres
- Embeddings o búsqueda semántica
- Dashboard web
- Scraping de métricas de Instagram
- Sincronización multi-usuario en tiempo real

---

## Estimación total

| Fase | Tiempo | Entregable |
|---|---|---|
| 1 | 2–3 h | Índice + sugerencias + resumen agente |
| 2 | 3–4 h | builds/ + package hook + CLI |
| 3 | 2–3 h | feedback + plantillas + regla Cursor + README |
| **Total** | **7–10 h** | Memoria operativa completa |

---

## Criterios de aceptación global

- [ ] `pytest tests/ -v` → 100% PASS
- [ ] Tras un carrusel de prueba, `builds/<slug>/manifest.json` existe
- [ ] `historial/carruseles.json` actualizado con último carrusel
- [ ] `python stlabs_memory.py suggest` propone fondo/familia distintos al último
- [ ] Agente Cursor lee regla y consulta memoria al iniciar
- [ ] `SISTEMA-DISENO-CARRUSELES-STLABS.md` documenta flujo en secciones 7 y 8
