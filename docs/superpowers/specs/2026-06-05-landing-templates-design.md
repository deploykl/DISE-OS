# Design Spec: Landing Page Templates Collection
**Date:** 2026-06-05  
**Stack:** HTML + Tailwind CSS (CDN) + Vanilla JS  
**Status:** Approved

---

## Overview

A collection of 5 complete, styled landing pages in HTML + Tailwind, each with a distinct visual identity. Accessible via a central gallery (`index.html`) that lets the user preview and open any template instantly.

**Goal:** Have a ready-to-pick library of elegant, modern landing pages for any future project.

---

## File Structure

```
D:\PROGRAMACION\DISEÑOS\
├── index.html              ← gallery (open this first)
├── landing-glass.html      ← Style 1: Glassmorphism Dark
├── landing-minimal.html    ← Style 2: Elegant Minimalism
├── landing-dark.html       ← Style 3: Dark Premium Gold
├── landing-neon.html       ← Style 4: Neon Cyberpunk
└── landing-pastel.html     ← Style 5: Soft Pastel Modern
```

---

## Gallery — `index.html`

- Dark neutral background so card colors don't clash
- 5 cards, one per template
- Each card: style name, short description, color swatch strip, "Ver plantilla" button (opens in new tab)
- Responsive: 1 col mobile → 2 col tablet → 3 col desktop

---

## Sections (all 5 landings share the same structure)

| # | Section | Details |
|---|---------|---------|
| 1 | **Navbar** | Logo left, nav links center, CTA button right. Sticky on scroll. |
| 2 | **Hero** | Large headline, subheadline, 2 CTA buttons (primary + outline), decorative SVG/gradient shape |
| 3 | **Features** | 3-column grid, 6 features each with SVG icon + title + description |
| 4 | **Stats** | 4 highlighted numbers (e.g. 10K+ Users, 500+ Projects, 99% Uptime, 24/7 Support) |
| 5 | **Testimonials** | 3 cards: avatar circle, name, role, quote text |
| 6 | **Pricing** | 3 plans (Free / Pro / Enterprise). Pro card visually highlighted. Feature checklist per plan. |
| 7 | **FAQ** | 5 questions, accordion (toggle open/close with vanilla JS) |
| 8 | **CTA Banner** | Full-width section, headline + subtext + single CTA button |
| 9 | **Footer** | Logo, 3 link columns, social icons (SVG), copyright line |

---

## The 5 Styles

### 1. Glassmorphism Dark — `landing-glass.html`
- **Background:** Deep navy/purple gradient (`#0f0c29` → `#302b63` → `#24243e`)
- **Cards:** `bg-white/10 backdrop-blur border border-white/20` frosted glass
- **Accent:** Electric blue/violet (`#7c3aed`, `#4f46e5`)
- **Typography:** Inter (Google Fonts) — white headings, `text-white/70` body
- **Effects:** Blur orbs in hero background, subtle glow on CTA button

### 2. Elegant Minimalism — `landing-minimal.html`
- **Background:** Pure white `#ffffff`, sections alternate with `#f8f9fa`
- **Cards:** White with `border border-gray-100 shadow-sm`
- **Accent:** Deep slate (`#0f172a`) + coral/terracotta (`#e85d4a`)
- **Typography:** Playfair Display (headings) + Inter (body)
- **Effects:** Generous whitespace, thin dividers, no decorative gradients

### 3. Dark Premium Gold — `landing-dark.html`
- **Background:** Deep black (`#0a0a0a`, `#111111`)
- **Cards:** `bg-zinc-900 border border-zinc-800`
- **Accent:** Gold (`#d4af37`, `#f5c842`)
- **Typography:** Cormorant Garamond (headings) + Inter (body) — white text
- **Effects:** Gold gradient on headline text, subtle gold glow on hover states

### 4. Neon Cyberpunk — `landing-neon.html`
- **Background:** Pure black `#000000` with dark grid pattern overlay
- **Cards:** `bg-black border border-green-500/30`
- **Accent:** Neon green (`#00ff41`) + hot pink (`#ff006e`)
- **Typography:** Space Grotesk (headings) + mono for stats/numbers
- **Effects:** Neon glow (`box-shadow: 0 0 20px #00ff41`), scanline texture, glitch hover on hero title

### 5. Soft Pastel Modern — `landing-pastel.html`
- **Background:** Warm cream `#faf8f5`, sections in `#f0ece8` / soft lavender `#ede9fe`
- **Cards:** White with `rounded-3xl shadow-md border-0`
- **Accent:** Dusty rose (`#e879a0`) + lavender (`#8b5cf6`) + mint (`#34d399`)
- **Typography:** DM Sans (headings) + DM Sans (body) — warm dark text `#2d2d2d`
- **Effects:** Soft shadows, pill-shaped buttons, blob shapes in hero

---

## Technical Constraints

- **No build step** — all files open directly in browser
- **Tailwind via CDN** — `<script src="https://cdn.tailwindcss.com"></script>`
- **Google Fonts via `<link>`** — no local font files
- **JS inline** — accordion FAQ uses ~10 lines of vanilla JS per file
- **No images** — placeholders use SVG shapes, gradient divs, or Tailwind utilities
- **Icons** — inline SVG only (no external icon library CDN required)

---

## Anti-Patterns to Avoid

- No emoji used as icons
- No layout shift on hover (no scale transforms on cards)
- No content hidden behind navbar (padding-top on first section)
- No horizontal scroll on mobile
- Sufficient contrast ratio on all text (4.5:1 minimum)
