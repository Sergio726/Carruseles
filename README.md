# Carruseles STLabs

Creación de carruseles de Instagram para la marca Sebastián García (STLabs).

## Instalación

```bash
pip install -r requirements.txt
playwright install chromium
```

## Memoria operativa

Antes de cada carrusel:

```bash
python stlabs_memory.py suggest
python stlabs_memory.py status
```

Después de publicar:

```bash
python stlabs_memory.py feedback <id> --estado publicado --notas "opcional"
```

Plantillas de copy:

```bash
python stlabs_memory.py plantilla educativo ACCION=automatizar DOLOR=perder_leads N=1 TITULO=Setup
```

## Flujo de trabajo

1. Consultar memoria (`suggest`)
2. `write_html()` + `render()` con [stlabs_kit.py](stlabs_kit.py)
3. `package(build_dir, out_name, meta={...})` — registra en `builds/` e `historial/`

## Documentación

- Sistema de diseño: [SISTEMA-DISENO-CARRUSELES-STLABS.md](SISTEMA-DISENO-CARRUSELES-STLABS.md)
- Plan de memoria: [docs/plans/2026-07-01-memoria-operativa-carruseles.md](docs/plans/2026-07-01-memoria-operativa-carruseles.md)

## Tests

```bash
pytest tests/ -v
```
