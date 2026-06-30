# ResQRules Design System — Component API Reference

The prop contract for all 15 primitives, extracted from the design system's TypeScript
definitions. Use this to understand each component's inputs without reading the HTML runtime.
Recreate these as native components in your target framework — the prop shapes are the contract.

Every text-bearing component takes `dir?: 'ltr' | 'rtl'` (and usually `lang?: 'en' | 'ar'`).
All numerals + clinical acronyms (CPR, AED, BVM, SpO₂) stay Latin even in Arabic.

---

## Actions

### Button — primary elevated action
Full-width, 56dp, red fill, white label.
- `children: ReactNode` — label
- `onClick?`, `disabled?` (→ neutral-300 fill, neutral-600 text, no shadow)
- `loading?` — red fill, centered white spinner, no label, non-interactive
- `fullWidth?` (default true), `dir?`

### OutlinedButton — full-width 56dp, 1.5dp border, transparent fill
Variant sets border + text color; pressed → −10% opacity.
- `children`, `onClick?`, `disabled?`, `fullWidth?`, `dir?`
- `variant?: 'primary'(red) | 'success'(green) | 'warning'(orange) | 'neutral'(near-black ghost)`

### CfButton — certainty-factor confidence button
Outlined, full-width, 56dp; label on one side, CF value on the other; color encodes confidence.
- `children`, `onClick?`, `disabled?`, `fullWidth?`, `dir?`
- `level?: 'certain'(+1.00,green) | 'likely'(+0.60,green) | 'unsure'(+0.20,orange) | 'none'(−1.00,red)`
- `cf?: string` — override the CF display string (defaults from level)

### LangToggle — EN / ع segmented pill (72×32)
Active filled pill slides between segments.
- `value?: 'en' | 'ar'`, `onChange?: (value) => void`
- `variant?: 'onPrimary'(white-on-red, AppBar) | 'standalone'(red-on-white)`

---

## Content

### Card — content surface
radius-lg, level-1 shadow, white, 20dp padding. Accent variants add a 4dp inline-start border
(flips side in RTL).
- `children`, `dir?`
- `variant?: 'default' | 'success'(green accent + tint) | 'stub'(grey, no shadow) | 'callout'(red accent)`

### UrgencyBadge — inline urgency pill
Caption all-caps, white on the urgency color.
- `level?: 'critical'(red) | 'high'(orange) | 'standard'(grey)`
- `children?` — override label (e.g. Arabic "حرج"); defaults to the English level name
- `dir?`

### TierBadge — hemorrhage escalation progress
3 dots + "Tier N / 3" caption.
- `current?: 0 | 1 | 2 | 3` — active tier (0 = all pending, entering tier 1)
- `complete?: boolean` — all tiers applied: every dot filled, no ring
- `lang?` (Latin numerals regardless), `label?: string` (override caption), `dir?`

### PageCitation — source page reference, e.g. "p.7"
Caption style, Latin numerals always.
- `page?: number | string`, `children?` (override full text), `dir?`
- `absolute?: boolean` — pin 16dp from the top screen edge (left in LTR, right in RTL)

---

## Feedback

### LoadingBar — 3dp indeterminate bar, sits directly below the AppBar
- `frozen?: boolean` — static mid-sweep frame for docs/print
- `trackColor?: string` — track behind the moving segment (default transparent)

### OverrideToast — banner that slides down to announce a protocol override
- `variant?: 'jump'(protocol switch ⚡) | 'guard'(already-in confirmation ✓)`
- `visible?: boolean` — drives slide in/out
- `children?` (override message), `lang?`, `dir?`

### Snackbar — full-width tap-to-retry error bar (neutral-900), docks above DangerPanel
- `children?` (override message)
- `onRetry?: (e) => void` — fired when tapped
- `lang?`, `dir?`

---

## Surfaces

### AppBar — top bar (56dp, red, no shadow)
Home = wordmark + LangToggle. Session = back arrow + ellipsised title + LangToggle + reset.
- `variant?: 'home' | 'session'`
- `title?: string` — session variant, ellipsised to 1 line
- `lang?`, `onLangChange?: (value) => void`
- `onBack?: () => void` — session; arrow flips to → and to the right edge in RTL
- `onReset?: () => void` — session reset (↺)
- `dir?`, `statusBar?: boolean` (render a 24px status-bar spacer above)

### DangerPanel — fixed bottom emergency bar, 4 tap zones
Red, 64dp, upward shadow. RTL flips zone order.
- `lang?`, `dir?`
- `locked?: boolean` — loading-lock: all zones to 60% opacity, non-interactive
- `onZone?: (key) => void` where key is `'bleeding' | 'breathing' | 'pulse' | 'unconscious'`

### BottomSheet — Reset Session sheet
Handle, title, two tappable rows, Cancel. radius-lg top corners, level-3 shadow.
- `lang?`, `dir?`
- `chartName?: string` — sub-label under "Reset this chart"
- `onResetChart?`, `onChooseChart?`, `onCancel?: () => void`
- `overlay?: boolean` — render scrim + slide-up wrapper (fills nearest positioned ancestor)
- `visible?: boolean` — with overlay: drives slide/scrim in & out

---

## Core

### Icon — inline Lucide line icon
Strokes in `currentColor` so it recolors cleanly (white on red panel; red/green/orange inline).
Offline-safe (geometry embedded, no network fetch).
- `name: string` — `droplet · wind · activity · user · zap · check · arrow-left · arrow-right · rotate-ccw`
- `size?: number | string` (default 20), `color?: string` (default currentColor)
- `strokeWidth?: number` (default 2), `title?: string` (accessible label; omitted → decorative)
