# -*- coding: utf-8 -*-
"""Memoria operativa para carruseles STLabs."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
HISTORIAL_DIR = REPO_ROOT / "historial"
BUILDS_DIR = REPO_ROOT / "builds"
INDEX_PATH = HISTORIAL_DIR / "carruseles.json"
PLANTILLAS_PATH = HISTORIAL_DIR / "plantillas_copy.json"

FONDOS = [
    "piedra_roca",
    "papel_corrugado",
    "concreto_industrial",
    "reticula_fina",
    "lino_tela",
    "roca_volcanica",
    "gradiente_profundo",
]
FAMILIAS = [
    "manifiesto",
    "blueprint",
    "operator_log",
    "dossier_editorial",
    "before_after",
    "dashboard_minimo",
    "guia_editorial",
]

FEEDBACK_ESTADOS = ("borrador", "publicado", "descartado")
META_REQUERIDOS = ("fondo", "familia_visual", "origen", "slides", "keyword_portada")


def empty_index() -> dict:
    return {"ultimo_id": None, "carruseles": []}


def load_index() -> dict:
    HISTORIAL_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_PATH.exists():
        return empty_index()
    try:
        data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return empty_index()
    if not isinstance(data, dict) or "carruseles" not in data:
        return empty_index()
    data.setdefault("ultimo_id", None)
    return data


def save_index(data: dict) -> None:
    HISTORIAL_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _ultimos(items: list[dict], key: str, n: int = 5) -> list[str]:
    return [c[key] for c in items[-n:] if c.get(key)]


def sugerir_fondo(ventana: int = 5) -> str:
    usados = _ultimos(load_index()["carruseles"], "fondo", ventana)
    for f in FONDOS:
        if f not in usados:
            return f
    return FONDOS[0]


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
    fb = meta.get("feedback", {})
    if fb.get("estado"):
        entrada["feedback_estado"] = fb["estado"]
    idx["carruseles"].append(entrada)
    idx["ultimo_id"] = entrada["id"]
    save_index(idx)


def _sync_index_feedback(build_id: str, feedback: dict) -> None:
    idx = load_index()
    for c in idx["carruseles"]:
        if c["id"] == build_id:
            if feedback.get("estado"):
                c["feedback_estado"] = feedback["estado"]
            break
    save_index(idx)


def ultimo() -> dict | None:
    carruseles = load_index()["carruseles"]
    return carruseles[-1] if carruseles else None


def resumen_para_agente() -> str:
    u = ultimo()
    sf, sfa = sugerir_fondo(), sugerir_familia()
    lines = ["## Memoria STLabs — contexto automático", ""]
    if u:
        fb = u.get("feedback_estado")
        fb_line = f"- Estado: `{fb}`" if fb else ""
        lines += [
            f"**Último carrusel:** `{u['id']}` ({u.get('fecha', '?')})",
            f"- Fondo: `{u.get('fondo')}` · Familia: `{u.get('familia_visual')}`",
            f"- Título: {u.get('titulo') or '(sin título)'}",
        ]
        if fb_line:
            lines.append(fb_line)
        lines.append("")
    else:
        lines += ["_Sin carruseles registrados aún._", ""]
    lines += [
        f"**Sugerencia fondo:** `{sf}`",
        f"**Sugerencia familia:** `{sfa}`",
        "",
        "_Regla: no repetir fondo ni familia del último carrusel salvo indicación explícita._",
    ]
    return "\n".join(lines)


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "carrusel"


def _default_id(titulo: str) -> str:
    return f"{date.today().isoformat()}-{slugify(titulo)}"


def resolve_build_id(meta: dict, fallback_titulo: str) -> str:
    meta.setdefault("titulo", fallback_titulo)
    meta.setdefault("id", _default_id(meta["titulo"]))
    return meta["id"]


def validar_meta(meta: dict) -> None:
    faltantes = [k for k in META_REQUERIDOS if k not in meta or meta[k] in (None, "")]
    if faltantes:
        raise ValueError(f"meta incompleto — faltan: {', '.join(faltantes)}")
    if meta["origen"] not in ("screenshot", "original"):
        raise ValueError("meta['origen'] debe ser 'screenshot' o 'original'")


def load_manifest(build_path: Path) -> dict:
    return json.loads((Path(build_path) / "manifest.json").read_text(encoding="utf-8"))


def registrar_carrusel(build_dir: Path, meta: dict) -> Path:
    build_dir = Path(build_dir)
    meta = dict(meta)
    meta.setdefault("id", _default_id(meta.get("titulo", "carrusel")))
    meta.setdefault("fecha", date.today().isoformat())

    manifest_text = json.dumps(meta, ensure_ascii=False, indent=2)
    (build_dir / "manifest.json").write_text(manifest_text, encoding="utf-8")

    dest = BUILDS_DIR / meta["id"]
    if build_dir.resolve() != dest.resolve():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(build_dir, dest)
    registrar_entrada(meta)
    return dest


def listar_builds(estado: str | None = None) -> list[dict]:
    BUILDS_DIR.mkdir(parents=True, exist_ok=True)
    builds = []
    for d in sorted(BUILDS_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        manifest = d / "manifest.json"
        if manifest.exists():
            m = load_manifest(d)
            if estado is None or m.get("feedback", {}).get("estado") == estado:
                builds.append(m)
    return builds


def actualizar_feedback(build_id: str, feedback: dict) -> None:
    path = BUILDS_DIR / build_id / "manifest.json"
    if not path.exists():
        raise FileNotFoundError(f"No existe build: {build_id}")
    m = load_manifest(BUILDS_DIR / build_id)
    m["feedback"] = {**m.get("feedback", {}), **feedback}
    path.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    _sync_index_feedback(build_id, feedback)


def _default_plantillas() -> dict:
    return {
        "screenshot_clone": {
            "portada": "{KEYWORD} en {TEMA}",
            "cta_final": "Comentá {KEYWORD} y te mando el recurso.",
            "footer_siempre": "sebastian.stlabs.ar",
        },
        "educativo": {
            "portada": "Cómo {ACCION} sin {DOLOR}",
            "paso": "Paso {N}: {TITULO}",
            "cta_final": "Guardá esto para cuando lo necesites.",
        },
    }


def plantilla(nombre: str) -> dict:
    if not PLANTILLAS_PATH.exists():
        return _default_plantillas()[nombre]
    data = json.loads(PLANTILLAS_PATH.read_text(encoding="utf-8"))
    return data[nombre]


def aplicar_plantilla(nombre: str, **kwargs) -> dict:
    tpl = plantilla(nombre)
    return {k: v.format(**kwargs) for k, v in tpl.items()}


def cmd_status() -> int:
    u = ultimo()
    if not u:
        print("Sin carruseles registrados.")
        return 0
    print(f"Último: {u['id']} ({u['fecha']})")
    print(f"  Fondo: {u['fondo']} | Familia: {u['familia_visual']}")
    if u.get("feedback_estado"):
        print(f"  Estado: {u['feedback_estado']}")
    print(f"  Total en índice: {len(load_index()['carruseles'])}")
    return 0


def cmd_list(estado: str | None = None) -> int:
    builds = listar_builds(estado=estado)
    if not builds:
        print("Sin builds registrados." + (f" (filtro: {estado})" if estado else ""))
        return 0
    for m in builds:
        fb = m.get("feedback", {}).get("estado", "—")
        print(f"{m['id']}  {m.get('titulo', '')}  [{fb}]  fondo={m.get('fondo')}")
    return 0


def cmd_suggest() -> int:
    print(resumen_para_agente())
    return 0


def cmd_feedback(build_id: str, estado: str | None, notas: str | None) -> int:
    fb: dict = {}
    if estado:
        if estado not in FEEDBACK_ESTADOS:
            print(f"Estado inválido. Usar: {', '.join(FEEDBACK_ESTADOS)}", file=sys.stderr)
            return 1
        fb["estado"] = estado
    if notas:
        fb["notas"] = notas
    if not fb:
        print("Indicá --estado y/o --notas", file=sys.stderr)
        return 1
    try:
        actualizar_feedback(build_id, fb)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1
    print(f"Feedback actualizado para {build_id}")
    return 0


def cmd_plantilla(nombre: str, kwargs: dict) -> int:
    try:
        result = aplicar_plantilla(nombre, **kwargs)
    except KeyError as e:
        print(f"Plantilla o placeholder desconocido: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    for k, v in result.items():
        print(f"{k}: {v}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Memoria operativa STLabs")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status")
    sub.add_parser("suggest")

    ls = sub.add_parser("list")
    ls.add_argument("--estado", choices=FEEDBACK_ESTADOS)

    fb = sub.add_parser("feedback")
    fb.add_argument("build_id")
    fb.add_argument("--estado", choices=FEEDBACK_ESTADOS)
    fb.add_argument("--notas")

    pl = sub.add_parser("plantilla")
    pl.add_argument("nombre")
    pl.add_argument("kv", nargs="*", help="KEY=valor")

    args = p.parse_args(argv)

    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "suggest":
        return cmd_suggest()
    if args.cmd == "list":
        return cmd_list(args.estado)
    if args.cmd == "feedback":
        return cmd_feedback(args.build_id, args.estado, args.notas)
    if args.cmd == "plantilla":
        kwargs = {}
        for item in args.kv:
            if "=" in item:
                k, v = item.split("=", 1)
                kwargs[k] = v
        return cmd_plantilla(args.nombre, kwargs)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
