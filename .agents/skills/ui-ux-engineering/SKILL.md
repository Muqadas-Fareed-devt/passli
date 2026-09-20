---
name: ui-ux-engineering
description: >-
  Modern frontend styling, glassmorphism, responsive design, micro-animations,
  and accessible UI/UX components. Use when designing, styling, or refining HTML/CSS templates
  and frontend interfaces.
---

# UI/UX Engineering & Modern Aesthetics Workflow

This skill ensures interfaces are visually stunning, responsive, accessible, and delight users with micro-interactions.

## Design Principles

### 1. Aesthetic Polish & Color Palette
- **Palette**: Use curated HSL/RGB custom properties for background, surfaces, borders, primary accent, and text hierarchy.
- **Glassmorphism & Depth**: Utilize multi-layered subtle shadows and backdrop blurs:
  ```css
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  ```
- **Modern Typography**: Pair clean sans-serif typefaces (e.g. Inter, Outfit, system modern) with clear weight distinctions (400, 500, 600, 700).

### 2. Micro-Interactions & Transitions
- Add smooth transitions on interactive elements (`transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);`).
- Add subtle hover states on buttons, cards, and list items (e.g., slight elevation, border glow, icon translation).
- Provide visual feedback for loading states and form submissions (spinners, disabled state styling).

### 3. Responsive Layouts & Accessibility
- Mobile-first CSS Grid and Flexbox layouts.
- Semantic HTML tags (`<main>`, `<nav>`, `<article>`, `<section>`, `<aside>`).
- Accessible forms: clear `<label>` associations, visible `:focus-visible` outlines, and ARIA attributes for dynamic components.
