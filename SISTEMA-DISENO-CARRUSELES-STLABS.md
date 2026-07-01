# Sistema de Diseño de Carruseles — STLabs / Sebastián García
> **Estándar absoluto del proyecto.** Todo chat nuevo arranca aquí.
> Marca: Sebastián García (RevOps · CRM · IA). Firma: **sebastian.stlabs.ar**

---

## 0. WORKFLOW PRINCIPAL (leer primero)

Cuando Yuli sube imágenes, la tarea por defecto es **clonar el carrusel** con la identidad de Sebastián.

### Reglas de clonado — sin excepción

| # | Regla |
|---|---|
| 1 | **REEMPLAZAR** todo @handle o cuenta de Instagram del original → `sebastian.stlabs.ar` en IBM Plex Mono verde |
| 2 | **ELIMINAR** el contador de slides (2/8, 3/8…) que traen los screenshots — no reproducirlo |
| 3 | **SIEMPRE recrear** imágenes de referencia internas (fotos, mockups, gráficos, capturas, ilustraciones) — nunca reemplazar por texto ni omitir |
| 4 | **MANTENER** imagen/logo de Claude exactamente igual si aparece en el original |
| 5 | **Aplicar paleta STLabs** (#0A0A0A fondo, #00FFB2 verde, #9aa39c gris, #F2F2F2 blanco) y tipografías de marca |
| 6 | **VARIEDAD DE FONDOS OBLIGATORIA** — ver sección 5 |

---

## 1. Identidad de marca

### Paleta
| Token | HEX | Uso |
|---|---|---|
| Verde neón | `#00FFB2` | Acento principal. 1–2 usos fuertes por slide. |
| Negro mineral | `#0A0A0A` | Base de todos los fondos. |
| Grafito | `#141414` / `#1E1E1E` | Cards, cajas. |
| Blanco cálido | `#F2F2F2` | Texto principal. |
| Gris | `#9aa39c` | Texto secundario. |
| Rojo | `#FF5247` | SOLO riesgo/peligro. Nunca decorativo. |
| Ámbar | `#FF9D3C` | Solo énfasis negativo puntual. |

### Tipografías (todas base64-embebidas — CDN inaccesible en entorno bash)
| Familia | Peso | Rol |
|---|---|---|
| Bebas Neue | 400 | Display, portada, números gigantes |
| Poppins | 700 / 800 | Titulares de paso |
| Barlow Condensed | 400–700 | Cuerpo, bullets, claims |
| IBM Plex Mono | 400–600 | Labels, PASO, footer, URL |
| Lora *itálica* | 400–700 | Palabras-acento editoriales, siempre en verde |

Rutas: `/usr/share/fonts/truetype/stlabs/` y `/usr/share/fonts/truetype/google-fonts/`

### Voz
Español argentino, voseo: Empezá, Elegí, Dejá, Hacé, Creá, Conectá, Comentá, Deslizá.
Sin emojis. Sin inglés. Mayúsculas en display. Copy corto y punchy.

### Firma (obligatoria, cada slide)
`sebastian.stlabs.ar` · IBM Plex Mono · verde · centrado · `bottom: 70px`
NUNCA @handle de Instagram ni handles de terceros.

---

## 2. Pipeline técnico (HTML → PNG con Playwright)

Estructura `/home/claude/buildN/`:
- `generate.py` → HTML + CSS con tokens de marca
- `render.py` → Playwright screenshot por .slide
- `package.py` → fuentes base64 + ZIP + tira preview → `/mnt/user-data/outputs/`

Parámetros render: lienzo 1080×1350px · viewport 1180 · device_scale_factor=2 → PNG retina 2160×2700
Crítico: `page.wait_for_function("document.fonts.ready")` + `wait_for_timeout(4000)` antes del screenshot.
Entrega siempre: tira de preview → ZIP → slides retina → HTML editable.
Kit reutilizable: `stlabs_kit.py` (tokens, fuentes base64, componentes chrome/bridge/donut/phone, helpers render/package).

---

## 3. Mecánicas visuales reutilizables (parámetros exactos)

### Nodo-flecha partido por la costura
Círculo verde diám.156 con → Poppins800 74px, top:597.
`.br-r { left:1002px }` en slide N (borde derecho).
`.br-l { left:-78px }` en slide N+1 (borde izquierdo).
Portada: solo right · Último slide: solo left · Intermedios: both.

### iPhone realista CSS puro
Marco titanio: linear-gradient(125deg, #4a4e54, #1b1d20, #0b0c0e, #101113, #1b1d20, #52565c).
Tilt: transform: perspective(2500px) rotateX(5deg) rotateY(-16deg) rotateZ(-7deg).
Dynamic island + cámara + brillo .ip-reflect + botones laterales.
Partido por costura: pb-right{left:780px} / pb-left{left:-300px}.

### Donas de porcentaje
background: conic-gradient(from 0deg, var(--verde) 0 X%, #2c2c2c X% 100%)
Verde=IA, gris=humanos. Arrancan desde las 12. Hueco interno = color de la card.

### Fotos reales integradas al negro
object-fit:cover + filter:brightness(.5) contrast(1.05) saturate(.7) + scrim gradiente vertical.
Título sobre scrim inferior. Foto real de Sebastián/familia > cualquier render de IA.

---

## 4. VARIEDAD DE FONDOS (regla crítica — leer siempre)

PROHIBIDO: todos los carruseles con fondo negro plano + texto pequeño + título grande a la izquierda.
OBLIGATORIO: cada carrusel usa un fondo y composición diferentes.

Catálogo de texturas disponibles en CSS puro:

**Piedra/roca:** SVG feTurbulence baseFrequency~0.65 + feColorMatrix desaturado + overlay rgba(7,7,7,.88)
**Papel corrugado:** repeating-linear-gradient(90deg, rgba(255,255,255,.11) 0 1.5px, transparent 3px 10px, rgba(0,0,0,.5) 12px 13.5px, transparent 15px) · opacity .8 · mix-blend-mode:overlay
**Concreto industrial:** SVG feTurbulence baseFrequency~0.9 tipo fractalNoise + overlay muy oscuro
**Retícula fina:** linear-gradient(rgba(255,255,255,.016) 1px, transparent 1px) + 90deg · size 60px
**Lino/tela:** repeating-linear-gradient cruzado en 0deg y 90deg · opacidad baja
**Roca volcánica:** SVG noise alta frecuencia + alto contraste + filter oscuro + glow verde sutil en esquina
**Gradiente profundo:** radial-gradient desde foco verde muy tenue en una esquina, resto negro puro

La textura va en ::before o ::after del .slide, mix-blend-mode:overlay.
El fondo base siempre es negro mineral #0A0A0A.
La composición también varía: centrada, asimétrica, dividida, full-foto, etc.

---

## 5. Familias visuales (rotar entre carruseles)

1. Manifiesto — Bebas enorme + dato/badge
2. Blueprint — proceso en grid / pasos numerados
3. Operator log — flujo paso a paso con microprueba
4. Dossier editorial — foto full + texto monumental
5. Before/After — dos columnas, riesgo/seguro
6. Dashboard mínimo — donas, barras, métricas
7. Guía editorial — corchetes, número gigante de paso, barra de progreso

---

## 6. Reglas absolutas

SÍ: contraste fuerte · textura física diferente por carrusel · escala monumental · composición asimétrica · microdetalles auténticos · keyword literal en portada · foto real de Sebastián · recrear imágenes de referencia internas · mantener logo Claude si aparece.

NO: robots/cerebros/circuitos · 3D plástico · estética SaaS genérica · simetría perfecta · glow excesivo · verde disperso · emojis · inglés · @handle de Instagram · contador de slides del screenshot · reemplazar imágenes de referencia por texto.

---

## 7. Checklist de arranque (todo carrusel)

1. ¿Viene de screenshot? → aplicar reglas de clonado (sección 0) primero
2. Copiar stlabs_kit.py a /home/claude/buildN/
3. Ejecutar `python stlabs_memory.py suggest` → elegir fondo/familia sugeridos (secciones 4 y 5)
4. Definir contenido slide a slide: voseo, keyword literal, 1–2 verdes por slide
5. generate.py → render.py → seam tests → ajustar → package.py
6. Verificar: sebastian.stlabs.ar en todos · sin @Instagram · sin contador de slides
7. Entregar: tira preview → ZIP → slides → HTML
8. `package(..., meta={...})` registra en builds/ e historial/
9. Si se publica: `python stlabs_memory.py feedback <id> --estado publicado`

---

## 8. Memoria operativa (obligatorio)

Antes de crear cualquier carrusel:
1. Leer `historial/carruseles.json` o ejecutar `python stlabs_memory.py suggest`
2. Usar fondo y familia sugeridos (distintos al último salvo pedido explícito)
3. Al empaquetar, pasar `meta=` a `package()` con manifest completo

Campos mínimos del manifest: `id`, `titulo`, `slides`, `fondo`, `familia_visual`, `origen` (`screenshot`|`original`), `keyword_portada`.
