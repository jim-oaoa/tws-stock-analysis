# Dashboard Redesign — Design Specification

**Project:** tws-stock-analysis  
**Product Type:** Financial Dashboard (per ui-ux-pro-max matrix)  
**Style System:** Dark Mode (OLED) + Data-Dense + Dimensional Layering  
**Date:** 2026-05-28

---

## 1. Design Tokens (CSS Custom Properties)

### Colors — OLED Dark Palette
```
--bg-root:        #0a0e0f       deepest background
--bg-surface:     #12161a       card backgrounds
--bg-elevated:    #1a1f24       hover/popover
--bg-input:       #1e2429       search input
--border-default: #2a3038       card borders
--border-active:  #3b82f6       focus/active borders

--text-primary:   #e6edf3       main content
--text-secondary: #8b949e       labels, muted
--text-dim:       #5c6570       very muted

--accent-blue:    #3b82f6       primary CTA, trust, links
--accent-cyan:    #22d3ee       chart lines, highlights

--profit:         #22c55e       bullish, gains, undervalued
--profit-dim:     #1a3a2a       profit background tint
--loss:           #ef4444       bearish, losses, overvalued
--loss-dim:       #3a1a1a       loss background tint
--warning:        #d29922       hold/neutral, fish body
--warning-dim:    #3a2e0a       warning background tint

--fish-head:      #22c55e       FISH_HEAD zone color
--fish-body:      #d29922       FISH_BODY zone color
--fish-tail:      #f0883e       FISH_TAIL zone color
--fish-bone:      #ef4444       FISH_BONE zone color
--bone-broken:    #5c6570       BONE_BROKEN zone color
```

### Typography
```
Font Stack: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
Mono: 'JetBrains Mono', 'Fira Code', monospace

Scale:
--text-xs:   0.75rem     labels, badges
--text-sm:   0.875rem    secondary data, table cells
--text-base: 1rem        body
--text-lg:   1.125rem    card titles
--text-xl:   1.25rem     section headers
--text-2xl:  1.5rem      KPI values
--text-3xl:  2rem        hero price
--text-4xl:  2.5rem      signal display

Weights:
--font-normal:  400
--font-medium:  500
--font-semibold: 600
--font-bold:    700
--font-black:   900     signal only
```

### Spacing & Elevation
```
Grid Gap: 16px (cards), 24px (sections)
Card Padding: 20px (compact), 24px (standard)

Elevation (z-index scale: 10, 20, 30, 50):
--elevation-0: none                        flat
--elevation-1: 0 1px 3px rgb(0 0 0 / 0.4)  base card
--elevation-2: 0 4px 12px rgb(0 0 0 / 0.5) hover
--elevation-3: 0 8px 24px rgb(0 0 0 / 0.6) modal/popover

Border Radius:
--radius-sm: 6px    inputs, buttons
--radius-md: 10px   compact cards
--radius-lg: 16px   main cards
--radius-xl: 24px   hero cards
```

### Animation Tokens
```
--duration-fast:   150ms   hover, focus
--duration-normal: 250ms   card hover lift, transitions
--duration-slow:   500ms   reveal animations, count-up
--easing:          cubic-bezier(0.4, 0, 0.2, 1)

Respect: @media (prefers-reduced-motion: reduce)
```

---

## 2. Layout Architecture

### Bento Box Grid (Apple-style modular)

```
┌─────────────────────────────────────────────────────┐
│  HEADER: Logo + Search Bar                  24px h  │
├───────────────┬─────────────────────────────────────┤
│               │                                     │
│  SIGNAL       │  PRICE HERO                         │
│  CARD         │  (large, spans 2 cols)              │
│  (1 col)      │  NT$ 2,270                          │
│               │  Zone indicator + sparkline         │
│               │                                     │
├───────────────┤                                     │
│               │                                     │
│  METRICS      │                                     │
│  GRID         │                                     │
│  (2x2 mini)   │                                     │
│               │                                     │
├───────────────┴─────────────────────────────────────┤
│                                                     │
│  VALUATION CHART (full width, 400px)                │
│  Fish-Bone curve with zone overlay                  │
│                                                     │
├───────────────┬─────────────────────────────────────┤
│               │                                     │
│  TECHNICAL    │  QUARTERLY GRID TABLE               │
│  INDICATORS   │  (scrollable, sticky header)        │
│  (1 col)      │                                     │
│               │                                     │
└───────────────┴─────────────────────────────────────┘
```

### Responsive Breakpoints
- **Desktop (lg+)**: 3-col bento grid as shown above
- **Tablet (md)**: 2-col, chart full width
- **Mobile (sm)**: single column stack

---

## 3. Component Specifications

### 3.1 Header
```
- Logo: "Fish-Bone" text + subtle fish icon (SVG)
- Subtitle: "Taiwan Stock Valuation Dashboard"
- Search: pill-shaped input with icon, glow on focus
- Live indicator dot (pulsing green = connected)
```

### 3.2 Price Hero Card (spans 2 cols)
```
- Massive price: "NT$ 2,270" (text-4xl, font-black)
- Price change delta (if available): +45 (+2.0%) in profit-green
- Zone badge: pill with zone color bg
- Sparkline mini-chart (last 20 periods trend)
- Background: subtle gradient or noise texture
- Border: 1px --border-default, --elevation-1
- Hover: --elevation-2, subtle scale(1.01)
```

### 3.3 Hybrid Signal Card
```
- Glassmorphism effect: backdrop-blur, translucent bg
- Signal text: massive, font-black, color-coded
  - STRONG_BUY/BUY → --profit (#22c55e)
  - HOLD → --warning (#d29922)
  - SELL/STRONG_SELL → --loss (#ef4444)
- Action text below with divider
- Animated pulse ring on signal change
- Border color matches signal
```

### 3.4 Metrics Grid (2x2 in sidebar)
```
- Current Price (large number)
- Net Value (large number)
- Fundamental Zone (colored badge)
- Valuation Zone (colored badge)
- Each cell: subtle border-bottom, hover: bg-elevated
```

### 3.5 Valuation Chart (full width)
```
- Dark themed Lightweight Charts
- Background: --bg-surface
- Grid lines: rgba(255,255,255,0.05)
- Line color: --accent-cyan (#22d3ee)
- Zone price lines: colored dashed lines
  - Fish Head: --fish-head green
  - Fish Body: --fish-body yellow
  - Fish Tail: --fish-tail orange
  - Fish Bone: --fish-bone red
- Current price marker: blue dashed vertical line
- Tooltip: dark bg, high contrast text
```

### 3.6 Technical Indicators Card
```
- Fish Bone Value (price level)
- Bias percentage with progress bar
  - Green: -10% to +10% (neutral)
  - Yellow: ±10-20%
  - Red: >±20%
- ADX with traffic light
  - ADX > 25: green dot + "Trending"
  - ADX < 25: grey dot + "Ranging"
- State label with zone color
```

### 3.7 Quarterly Grid Table
```
- Sticky header row
- Alternating row colors (subtle)
- EPS column: right-aligned, monospace
- Accum. Net Value column: highlighted (accent-blue)
- Row hover: --bg-elevated
- Horizontal scroll on mobile
```

---

## 4. Interaction & Animation Spec

### Loading State
```
- Skeleton screens (not spinner):
  - Price: 2rem height pulse block
  - Chart: 400px pulse block
  - Table: 7 row pulse blocks
  - Cards: matching card-height pulse blocks
- Transition: fade 250ms from skeleton to content
```

### Data Refresh
```
- Subtle shimmer when new data arrives
- Number count-up animation on price change (500ms ease-out)
- Zone change: badge color transition (300ms)
```

### Error State
```
- Card-level error messages (not full-page takeovers)
- Retry button in the affected card
- Chart error → ErrorBoundary fallback with retry
```

### Micro-interactions
```
- Card hover: translateY(-2px), shadow increase, 250ms
- Button press: scale(0.97), 150ms
- Search focus: glow ring, 250ms
- Row hover: bg change, 150ms
- Signal change: pulse ring animation, 600ms
```

---

## 5. Accessibility (WCAG AA Minimum)

- All text contrast ≥ 4.5:1 against background
- Focus rings visible (2px --accent-blue) on all interactive elements
- Table headers properly scoped
- Form inputs have labels (aria-label if icon-only)
- Signal colors paired with text (not color-only)
- Keyboard: Tab through search → analyze → table (if sortable)
- `prefers-reduced-motion` respected

---

## 6. Implementation Plan

### Phase 1: Design System Foundation
1. Create `src/styles/tokens.css` — all CSS custom properties
2. Update `src/index.css` — import tokens, set Tailwind v4 theme
3. Remove unused `App.css` boilerplate
4. Add Inter + JetBrains Mono fonts via Google Fonts CDN in `index.html`

### Phase 2: Core Components (by priority)
1. `PriceHero.tsx` — large price + zone badge + sparkline
2. `SignalCard.tsx` — glassmorphism signal card
3. `MetricsGrid.tsx` — 2x2 KPI grid
4. `Header.tsx` — logo + search bar with live indicator
5. `ValuationChart.tsx` — enhanced dark-themed chart
6. `TechnicalCard.tsx` — ADX/Bias indicators
7. `QuarterlyTable.tsx` — enhanced data table
8. `SkeletonLoader.tsx` — skeleton components for loading
9. `ErrorCard.tsx` — card-level error display

### Phase 3: Integration
1. Rewrite `App.tsx` with new layout and components
2. Update `types/valuation.ts` if needed
3. Add utility hooks (`useCountUp`, `useMediaQuery`)
4. Final polish: transitions, hover states, responsive

---

## 7. Implementation Rules

- **Use existing API contracts** — no backend changes
- **Tailwind CSS v4 (CSS-first)** — use `@theme` block, NOT `tailwind.config.js`
- **React + TypeScript** — strict mode, proper typing
- **Component isolation** — each component in its own file
- **ErrorBoundary** — wrap chart and data-dependent components
- **No new dependencies** unless absolutely necessary (lightweight-charts is already installed)
- **Mobile-first responsive** — design for 375px → scale up
