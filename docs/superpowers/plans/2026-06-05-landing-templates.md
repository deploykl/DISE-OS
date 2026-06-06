# Landing Page Templates Collection — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 5 complete styled landing pages in HTML + Tailwind CSS plus a gallery `index.html` for browsing and selecting templates.

**Architecture:** 6 standalone HTML files, no build step. Each landing page is self-contained: Tailwind via CDN, Google Fonts via `<link>`, inline SVG icons, and a single `<script>` block (~15 lines) for the FAQ accordion. The gallery links to all 5 templates via `target="_blank"`.

**Tech Stack:** HTML5, Tailwind CSS CDN v3, Google Fonts, Vanilla JS (inline), inline SVG.

---

## Shared HTML Skeleton (used by all 5 landings)

Every landing file follows this exact structure. Only colors, fonts, and decorative effects change per style.

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[Style Name] — Landing</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="[GOOGLE FONTS URL]" rel="stylesheet" />
  <style>/* custom effects per style */</style>
</head>
<body class="[body classes]">
  <!-- 1. Navbar -->
  <!-- 2. Hero -->
  <!-- 3. Features -->
  <!-- 4. Stats -->
  <!-- 5. Testimonials -->
  <!-- 6. Pricing -->
  <!-- 7. FAQ -->
  <!-- 8. CTA Banner -->
  <!-- 9. Footer -->
  <script>/* FAQ accordion */</script>
</body>
</html>
```

## Shared FAQ Accordion JS (copy identically into all 5 files)

```js
document.querySelectorAll('[data-faq-btn]').forEach(btn => {
  btn.addEventListener('click', () => {
    const answer = btn.nextElementSibling;
    const icon = btn.querySelector('[data-faq-icon]');
    const isOpen = answer.style.maxHeight;
    document.querySelectorAll('[data-faq-answer]').forEach(a => a.style.maxHeight = '');
    document.querySelectorAll('[data-faq-icon]').forEach(i => i.style.transform = 'rotate(0deg)');
    if (!isOpen) {
      answer.style.maxHeight = answer.scrollHeight + 'px';
      icon.style.transform = 'rotate(45deg)';
    }
  });
});
```

## Shared FAQ HTML Pattern (adapt colors per style)

```html
<section id="faq">
  <h2>Preguntas frecuentes</h2>
  <div class="space-y-4 max-w-2xl mx-auto">
    <div class="[card classes]">
      <button data-faq-btn class="w-full flex justify-between items-center p-5 text-left">
        <span>¿Cuánto cuesta el plan Pro?</span>
        <span data-faq-icon class="transition-transform duration-200 text-2xl font-light">+</span>
      </button>
      <div data-faq-answer style="max-height:0;overflow:hidden;transition:max-height .3s ease">
        <p class="px-5 pb-5 [text classes]">El plan Pro cuesta $29/mes e incluye todas las funcionalidades premium...</p>
      </div>
    </div>
    <!-- repeat for 4 more questions -->
  </div>
</section>
```

## Shared Pricing Card Pattern (3 columns: Free / Pro / Enterprise)

```html
<section id="pricing">
  <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
    <!-- Free -->
    <div class="[card-base]">
      <h3>Free</h3>
      <p class="text-4xl font-bold">$0<span class="text-base font-normal">/mes</span></p>
      <ul class="space-y-3 my-6">
        <li>✓ 5 proyectos</li>
        <li>✓ 1 usuario</li>
        <li>✗ Soporte prioritario</li>
      </ul>
      <a href="#" class="[btn-outline]">Empezar gratis</a>
    </div>
    <!-- Pro — highlighted -->
    <div class="[card-highlighted] scale-105">
      <span class="[badge]">Popular</span>
      <h3>Pro</h3>
      <p class="text-4xl font-bold">$29<span class="text-base font-normal">/mes</span></p>
      <ul class="space-y-3 my-6">
        <li>✓ Proyectos ilimitados</li>
        <li>✓ 10 usuarios</li>
        <li>✓ Soporte prioritario</li>
      </ul>
      <a href="#" class="[btn-primary]">Comenzar ahora</a>
    </div>
    <!-- Enterprise -->
    <div class="[card-base]">
      <h3>Enterprise</h3>
      <p class="text-4xl font-bold">Custom</p>
      <ul class="space-y-3 my-6">
        <li>✓ Todo en Pro</li>
        <li>✓ Usuarios ilimitados</li>
        <li>✓ SLA dedicado</li>
      </ul>
      <a href="#" class="[btn-outline]">Contactar ventas</a>
    </div>
  </div>
</section>
```

---

## Task 1: Glassmorphism Dark — `landing-glass.html`

**Files:**
- Create: `D:\PROGRAMACION\DISEÑOS\landing-glass.html`

**Design tokens:**
- Body bg: `style="background: linear-gradient(135deg, #0f0c29, #302b63, #24243e)"`
- Font: `Outfit` — `https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap`
- Body class: `font-['Outfit'] text-white min-h-screen`
- Accent: `#7c3aed` (violet-600), `#4f46e5` (indigo-600)
- Glass card: `bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl`
- CTA btn primary: `bg-violet-600 hover:bg-violet-500 text-white px-8 py-3 rounded-full transition-all duration-200 shadow-lg shadow-violet-500/30`
- CTA btn outline: `border border-white/40 hover:bg-white/10 text-white px-8 py-3 rounded-full transition-all duration-200`
- Navbar: `fixed top-4 left-4 right-4 z-50 bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl px-6 py-4`
- Section padding: `py-24 px-4`

**Hero background orbs (add inside `<style>`):**
```css
.orb { position:absolute; border-radius:50%; filter:blur(80px); pointer-events:none; }
.orb-1 { width:400px; height:400px; background:#7c3aed44; top:-100px; right:-100px; }
.orb-2 { width:300px; height:300px; background:#4f46e544; bottom:0; left:-50px; }
```

**Navbar SVG logo icon (16x16 diamond shape):**
```html
<svg width="32" height="32" viewBox="0 0 32 32" fill="none">
  <path d="M16 2L30 16L16 30L2 16Z" fill="url(#g1)"/>
  <defs><linearGradient id="g1" x1="2" y1="2" x2="30" y2="30" gradientUnits="userSpaceOnUse">
    <stop stop-color="#7c3aed"/><stop offset="1" stop-color="#4f46e5"/>
  </linearGradient></defs>
</svg>
```

**Stats numbers:** `10K+ Usuarios`, `500+ Proyectos`, `99.9% Uptime`, `24/7 Soporte`
Stats value class: `text-5xl font-bold bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent`

**Feature icons:** 6 inline SVG icons (24x24), color `#a78bfa` (violet-400). Topics: Velocidad, Seguridad, Análisis, Colaboración, Integraciones, Soporte.

- [ ] **Step 1: Create `landing-glass.html` with complete all 9 sections**

  Build the full file using the shared skeleton + shared FAQ JS + glass design tokens above. All 9 sections must be present.

- [ ] **Step 2: Verify in browser**

  Open `landing-glass.html` in browser. Check:
  - Navbar is sticky and frosted
  - Hero shows gradient background with orbs
  - All 9 sections render without horizontal scroll
  - FAQ accordion opens/closes on click

---

## Task 2: Elegant Minimalism — `landing-minimal.html`

**Files:**
- Create: `D:\PROGRAMACION\DISEÑOS\landing-minimal.html`

**Design tokens:**
- Body bg: `bg-white`
- Font: `Playfair Display` (headings) + `Inter` (body)
  ```
  https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;500;600&display=swap
  ```
- Heading class: `font-['Playfair_Display']`
- Body class: `font-['Inter'] text-slate-800 bg-white`
- Accent: `#e85d4a` (coral/terracotta)
- Cards: `bg-white border border-gray-100 shadow-sm rounded-xl`
- CTA btn primary: `bg-slate-900 hover:bg-slate-700 text-white px-8 py-3 rounded-sm transition-colors duration-200`
- CTA btn outline: `border-2 border-slate-900 hover:bg-slate-900 hover:text-white text-slate-900 px-8 py-3 rounded-sm transition-all duration-200`
- Navbar: `sticky top-0 z-50 bg-white border-b border-gray-100 px-6 py-4`
- Section alternate bg: odd sections `bg-white`, even sections `bg-gray-50`
- Accent color usage: coral `#e85d4a` on nav active link, section number labels, pricing badge, CTA button hover underline
- Section padding: `py-24 px-4 max-w-6xl mx-auto`

**Hero special:** Large serif headline split into two lines with thin font-weight subtitle. No gradient, no orbs. Just generous whitespace and a thin coral underline under the main CTA button.

**Stats:** Same 4 metrics. Value class: `text-5xl font-bold text-slate-900`, label: `text-sm uppercase tracking-widest text-slate-400`.

**Thin horizontal dividers between sections:** `<hr class="border-gray-100" />`

- [ ] **Step 1: Create `landing-minimal.html` with all 9 sections**

- [ ] **Step 2: Verify in browser**

  Open `landing-minimal.html`. Check: clean whitespace, serif headings, coral accents visible, no extra shadows or gradients bleeding into sections.

---

## Task 3: Dark Premium Gold — `landing-dark.html`

**Files:**
- Create: `D:\PROGRAMACION\DISEÑOS\landing-dark.html`

**Design tokens:**
- Body bg: `style="background:#0a0a0a"` + `text-zinc-100`
- Font: `Cormorant Garamond` (headings) + `Inter` (body)
  ```
  https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500&display=swap
  ```
- Heading class: `font-['Cormorant_Garamond'] tracking-wide`
- Accent: Gold `#d4af37` / `#f5c842`
- Cards: `bg-zinc-900 border border-zinc-800 rounded-xl`
- CTA btn primary: `border border-yellow-500 text-yellow-400 hover:bg-yellow-500 hover:text-black px-8 py-3 transition-all duration-200`
- Navbar: `fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur border-b border-zinc-800 px-8 py-5`
- Gold gradient text (hero headline):
  ```css
  .gold-text { background: linear-gradient(90deg, #d4af37, #f5c842, #d4af37); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  ```
- Gold glow on hover (add in `<style>`):
  ```css
  .gold-glow:hover { box-shadow: 0 0 20px #d4af3755; }
  ```
- Section divider: thin gold line `<div class="w-16 h-px bg-yellow-500 mx-auto my-4"></div>`
- Section padding: `py-28 px-4 max-w-6xl mx-auto`

**Stats:** Value class: `text-5xl font-bold text-yellow-400`, label: `text-xs uppercase tracking-widest text-zinc-500`

**Testimonial avatar:** circle with gold border `w-12 h-12 rounded-full bg-zinc-700 border-2 border-yellow-500`

- [ ] **Step 1: Create `landing-dark.html` with all 9 sections**

- [ ] **Step 2: Verify in browser**

  Check: gold accents visible, text legible on dark background, gold gradient renders on hero headline.

---

## Task 4: Neon Cyberpunk — `landing-neon.html`

**Files:**
- Create: `D:\PROGRAMACION\DISEÑOS\landing-neon.html`

**Design tokens:**
- Body bg: `bg-black text-white`
- Font: `Space Grotesk` (all text) + mono for stats
  ```
  https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700;800&display=swap
  ```
- Body class: `font-['Space_Grotesk'] bg-black text-white`
- Accent primary: Neon green `#00ff41`
- Accent secondary: Hot pink `#ff006e`
- Cards: `bg-black border border-green-500/30 rounded-lg`
- CTA btn primary: `border border-green-400 text-green-400 hover:bg-green-400 hover:text-black px-8 py-3 transition-all duration-200 uppercase tracking-widest text-sm`
- Navbar: `fixed top-0 left-0 right-0 z-50 bg-black border-b border-green-500/20 px-8 py-4`
- Grid overlay (add to `<style>`):
  ```css
  .grid-bg {
    background-image: linear-gradient(#00ff4108 1px, transparent 1px), linear-gradient(90deg, #00ff4108 1px, transparent 1px);
    background-size: 40px 40px;
  }
  .neon-glow { text-shadow: 0 0 10px #00ff41, 0 0 30px #00ff4188; }
  .neon-border { box-shadow: 0 0 10px #00ff4133, inset 0 0 10px #00ff4111; }
  .pink-glow { text-shadow: 0 0 10px #ff006e, 0 0 30px #ff006e88; }
  ```
- Hero section: add `grid-bg` class to hero wrapper
- Stats value: `text-5xl font-bold text-green-400 neon-glow font-mono`
- Section label prefix: `<span class="text-green-400 font-mono text-sm">// </span>`

**Glitch effect on hero title (add to `<style>`):**
```css
@keyframes glitch {
  0%,100% { transform: translate(0); }
  20% { transform: translate(-2px,1px); }
  40% { transform: translate(2px,-1px); }
  60% { transform: translate(-1px,2px); }
  80% { transform: translate(1px,-2px); }
}
.glitch:hover { animation: glitch .3s steps(1) infinite; }
```

**Feature icon color alternation:** first 3 features use `text-green-400`, last 3 use `text-pink-500`

- [ ] **Step 1: Create `landing-neon.html` with all 9 sections**

- [ ] **Step 2: Verify in browser**

  Check: grid background visible in hero, green neon text glow, glitch on hero title hover, pink and green accents alternate in features.

---

## Task 5: Soft Pastel Modern — `landing-pastel.html`

**Files:**
- Create: `D:\PROGRAMACION\DISEÑOS\landing-pastel.html`

**Design tokens:**
- Body bg: `style="background:#faf8f5"` + `text-gray-800`
- Font: `DM Sans`
  ```
  https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap
  ```
- Body class: `font-['DM_Sans']`
- Accent: Dusty rose `#e879a0`, Lavender `#8b5cf6`, Mint `#34d399`
- Cards: `bg-white rounded-3xl shadow-md`
- CTA btn primary: `bg-violet-500 hover:bg-violet-400 text-white px-8 py-3 rounded-full transition-colors duration-200`
- CTA btn outline: `border-2 border-violet-300 hover:border-violet-500 text-violet-600 px-8 py-3 rounded-full transition-all duration-200`
- Navbar: `sticky top-0 z-50 bg-white/80 backdrop-blur border-b border-rose-100 px-6 py-4`
- Blob shapes in hero (add to `<style>`):
  ```css
  .blob { position:absolute; border-radius:50%; opacity:0.5; filter:blur(60px); pointer-events:none; }
  .blob-1 { width:350px; height:350px; background:#e879a044; top:-50px; right:5%; }
  .blob-2 { width:250px; height:250px; background:#8b5cf633; bottom:0; left:10%; }
  .blob-3 { width:200px; height:200px; background:#34d39933; top:30%; left:40%; }
  ```
- Section alternating bg: `#faf8f5` → `#f0ece8` → `#ede9fe` (lavender tint) → back
- Stats value: `text-5xl font-bold text-violet-600`
- Feature icon bg circles: `w-12 h-12 rounded-full flex items-center justify-center` with alternating bg: `bg-rose-100`, `bg-violet-100`, `bg-green-100`

**Pill badges on pricing:** `<span class="bg-violet-100 text-violet-700 text-xs font-medium px-3 py-1 rounded-full">Popular</span>`

- [ ] **Step 1: Create `landing-pastel.html` with all 9 sections**

- [ ] **Step 2: Verify in browser**

  Check: warm cream background, pastel blobs visible in hero, rounded pill shapes everywhere, multi-accent colors (rose/violet/mint) balanced across sections.

---

## Task 6: Gallery — `index.html`

**Files:**
- Create: `D:\PROGRAMACION\DISEÑOS\index.html`

**Design:**
- Body bg: `style="background:#111827"` (gray-900), `text-white`, `font-['Inter']`
- Font: `Inter` via Google Fonts
- Page layout: centered, `max-w-5xl mx-auto px-6 py-16`
- Header: large title "Design Templates", subtitle "Selecciona un diseño para ver la plantilla completa"
- 5 template cards in a responsive grid: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`

**Each card structure:**
```html
<div class="bg-gray-800 border border-gray-700 rounded-2xl overflow-hidden hover:border-gray-500 transition-colors duration-200 cursor-pointer">
  <!-- Color swatch strip -->
  <div class="h-2 w-full" style="background: linear-gradient(90deg, [color1], [color2], [color3])"></div>
  <!-- Card body -->
  <div class="p-6">
    <div class="flex items-center justify-between mb-2">
      <h3 class="font-semibold text-lg">[Style Name]</h3>
      <span class="text-xs text-gray-400 bg-gray-700 px-2 py-1 rounded">[tag]</span>
    </div>
    <p class="text-gray-400 text-sm mb-5">[short description]</p>
    <!-- Small color dots -->
    <div class="flex gap-2 mb-5">
      <div class="w-4 h-4 rounded-full" style="background:[color1]"></div>
      <div class="w-4 h-4 rounded-full" style="background:[color2]"></div>
      <div class="w-4 h-4 rounded-full" style="background:[color3]"></div>
    </div>
    <a href="[filename]" target="_blank" class="block text-center bg-gray-700 hover:bg-gray-600 text-white py-2.5 rounded-xl text-sm transition-colors duration-200">
      Ver plantilla →
    </a>
  </div>
</div>
```

**5 card data:**

| Style | File | Swatch colors | Tag | Description |
|-------|------|--------------|-----|-------------|
| Glassmorphism Dark | `landing-glass.html` | `#7c3aed`, `#4f46e5`, `#0f0c29` | Dark | Capas translúcidas sobre gradiente oscuro |
| Minimalismo Elegante | `landing-minimal.html` | `#0f172a`, `#e85d4a`, `#f8f9fa` | Light | Tipografía serif, espacios amplios |
| Dark Premium Gold | `landing-dark.html` | `#0a0a0a`, `#d4af37`, `#f5c842` | Dark | Lujo oscuro con detalles dorados |
| Neón Cyberpunk | `landing-neon.html` | `#000000`, `#00ff41`, `#ff006e` | Dark | Grid oscuro con acentos neón |
| Soft Pastel Modern | `landing-pastel.html` | `#e879a0`, `#8b5cf6`, `#34d399` | Light | Colores suaves, formas redondeadas |

- [ ] **Step 1: Create `index.html` gallery**

  Build the gallery page with all 5 cards following the structure and data above. Add a small "9 secciones" tag on each card.

- [ ] **Step 2: Verify in browser**

  Open `index.html`. Check: all 5 cards show with correct swatches, "Ver plantilla →" opens each landing in a new tab, page is responsive at mobile width.

---

## Spec Coverage Check

| Spec Requirement | Covered By |
|-----------------|-----------|
| 5 landing pages HTML + Tailwind | Tasks 1–5 |
| Glassmorphism Dark style | Task 1 |
| Elegant Minimalism style | Task 2 |
| Dark Premium Gold style | Task 3 |
| Neon Cyberpunk style | Task 4 |
| Soft Pastel Modern style | Task 5 |
| index.html gallery | Task 6 |
| Navbar + Hero + Features + Stats + Testimonials + Pricing + FAQ + CTA + Footer | Tasks 1–5 (all 9 sections) |
| FAQ accordion (vanilla JS) | Shared JS block in Tasks 1–5 |
| No build step, opens in browser | All tasks use CDN only |
| No emoji icons (inline SVG) | All tasks specify SVG |
| No horizontal scroll | Verified in each Step 2 |
| Sufficient contrast | Design tokens specify correct values |
