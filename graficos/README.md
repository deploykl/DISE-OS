# Catálogo de gráficos

Inventario de todos los gráficos disponibles en esta carpeta para poder
reutilizarlos rápido en cualquier proyecto.

## Estructura

| Archivo | Contenido |
|---|---|
| `index.html` | Catálogo único con los **61 gráficos** numerados (#1–#61), cada uno en su propia sección `id="chart-N"` con un badge `#N — nombre (tipo, tema)`. Incluye Chart.js 4.4.0 (una sola vez), Tailwind, Tabler icons, Font Awesome y fuentes. |
| `catalogo.json` | Lista de 61 entradas (una por gráfico) con metadatos + el `anchor` correspondiente dentro de `index.html`. |

Las 5 galerías originales (`arctic-charts.html`, `vibiz-charts.html`,
`graficos.html`, `barras2.html`, `tendencia.html`) fueron consolidadas en
`index.html`, cada una con sus ids/CSS/JS aislados (prefijos `arctic-`,
`vibiz-`, `graficos-`, `barras2-`, `tendencia-`, CSS scoped por tema e
IIFEs por script) para evitar colisiones entre gráficos.

## `catalogo.json`

Lista de **61 entradas**, una por cada gráfico individual. Cada entrada tiene:

```json
{
  "id": "vibiz-charts__c-donut",
  "nombre": "Doughnut",
  "descripcion": "Market share por categoría",
  "tipo": "doughnut",
  "archivo": "index.html",
  "canvas_id": "c-donut",
  "tema": "Vibiz (light, tabler icons)",
  "nota": "...",
  "anchor": "chart-34"
}
```

`anchor` es el `id` de la sección dentro de `index.html` (`#chart-34` para
este ejemplo) y se corresponde 1 a 1 con el número de badge visible en la
tarjeta (`#34 — Doughnut (...)`).

## Cómo reutilizar un gráfico

1. Dime su número (ej. "usemos el #23") o su nombre/descripción.
2. Busco la entrada en `catalogo.json` → obtengo el `anchor` (`chart-N`).
3. Te doy el bloque HTML+JS de esa sección de `index.html` ya con sus ids/CSS
   reales (sin los prefijos de scoping si lo vas a usar solo, o con ellos si
   lo necesitas dentro de `index.html`).
