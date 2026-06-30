# ResQRules — Design System

> Mobile first-aid clinical decision-support for Red Cross / Red Crescent field paramedics.
> This repository is the **foundation layer**: tokens, type, spacing, elevation, and every
> reusable primitive. No full screens — those are a separate pass built on top of this.

---

## 1. Product context

**ResQRules** is a phone-sized decision-support tool a paramedic holds in one hand, often
outdoors, in poor light, under acute stress — a collapsing patient, catastrophic bleeding,
no pulse. It walks a responder through certainty-factor (CF) clinical charts: a question,
a set of answers, an intervention, an escalation tier. The interface is the opposite of a
consumer app — **every decision serves legibility and speed, never delight.**

Design consequences that drive every token below:
- **Big targets.** 56dp minimum on everything tappable; the danger panel zones are 64dp.
- **Loud status.** Red is *action*, not alarm-wallpaper. Green = controlled/terminal,
  orange = ambiguous/urgent. Color is a clinical signal, used sparingly and consistently.
- **Bilingual, zero reflow.** Noto Sans (Latin) and Noto Sans Arabic share metrics, so a
  responder can flip EN ↔ AR mid-protocol and the layout does not move a pixel.
- **Calm surfaces.** White cards, one soft shadow, generous padding. Nothing competes with
  the clinical text.

### Sources

This system was authored **from a written specification only** — there was no attached
codebase, Figma file, or screenshot set. All token values, component states, and bilingual
specimens come verbatim from the ResQRules foundation brief. If a canonical Figma or Flutter
codebase exists, link it here so future passes reconcile against ground truth:

- Figma: _(none provided — add link)_
- Codebase: _(none provided — add repo)_

Because there is no upstream source, treat the values in `tokens/` as authoritative.

---

## 2. Content fundamentals

The voice is a **calm clinical instructor**, not a brand. Copy is terse, imperative, and
unambiguous — it tells the responder exactly what to do next.

- **Casing:** Sentence case for instructions and questions ("Apply firm pressure"). Title
  Case for screen/section titles and button labels ("End Session", "Back to Home"). ALL-CAPS
  reserved for urgency badges only ("CRITICAL").
- **Person:** Second-person imperative — verbs lead, the "you" is implied. Answers are bare
  ("yes", "no", "no — bleeding controlled"). No pronoun warmth, no "please".
- **Numbers:** Always Latin numerals — even in Arabic mode (`p.7`, `Tier 2 / 3`, `CF +0.60`).
  Clinical acronyms stay Latin everywhere: **CPR, AED, BVM, SpO₂, SpCO** — never transliterated
  into Arabic script, even mid-sentence.
- **Bilingual pairing:** Specimens are written as `English / العربية` so designers always see
  both. In product they are never shown together — the language toggle swaps them.
- **No emoji as voice.** The clinical glyphs (bleeding, no-pulse, etc.) are *icons*, not emoji
  (see §5). Copy itself never uses emoji, exclamation spam, or marketing tone.
- **Tone examples:**
  - Question: "Is the bleeding catastrophic?" / "هل النزيف كارثي؟"
  - Action: "End Session" / "إنهاء الجلسة"
  - Status: "✓ Already in CPR Adult — continuing"
  - Error: "Connection error — tap to retry"

---

## 3. Visual foundations

**Overall vibe:** clinical, flat, high-contrast, utilitarian. Closer to a medical device
readout than a lifestyle app. Whitespace and type weight carry the hierarchy; ornament is
absent by policy.

- **Color.** Red Cross red (`#CC0000`) is the single brand anchor — used for the AppBar, the
  primary action, and the danger panel, never as decoration. Status is a three-note chord:
  **green** (`#2D6A4F`, controlled/terminal), **orange** (`#E85D04`, ambiguous/high-urgency),
  **neutral grey** (`#4A4A4A`, standard). Surfaces are white on white with grey hairlines.
  Tints (`primary-100`, `success-100`, `warning-100`) are barely-there washes for card
  backgrounds — never saturated.
- **Type.** Noto Sans / Noto Sans Arabic, weights 400/600/700 only — **never lighter than 400.**
  Seven sizes (22 → 12). Hierarchy comes from weight + size, not color. Body text (16px / 1.6)
  is tuned for reading dense instructions one-handed.
- **Spacing.** Strict 8dp grid (4 / 8 / 12 / 16 / 20 / 24 / 32). 16dp screen margins, 20dp card
  padding, 12dp between options. The rhythm is roomy — fingers, not cursors.
- **Backgrounds.** Flat fills only. **No gradients, no imagery, no texture, no blur.** The page
  is white; the danger panel and AppBar are solid red. A scrim (black 45%) backs bottom sheets.
- **Elevation.** Exactly three shadows. Cards cast a soft downward `level-1`. Bottom panels and
  sheets cast **upward** (`level-2`, `level-3`) because they rise from the bottom edge. No
  decorative or layered shadows anywhere.
- **Corners.** 6dp (badges/dots), 8dp (buttons/inputs), 12dp (cards/sheets), full pill
  (language toggle, urgency badges). Cards = 12dp radius + `level-1` shadow + white fill;
  accent variants add a 4dp left border and a faint tint, nothing else.
- **Borders.** Outlined buttons use a 1.5dp stroke in their semantic color. Dividers and input
  borders are 1dp `neutral-300`. Borders carry color meaning (CF confidence buttons recolor
  their entire border + label).
- **Motion.** Minimal and functional. Override toast slides in 200ms ease-out / out 200ms
  ease-in. Loading bar is an indeterminate left-to-right sweep. Language toggle's active pill
  slides between segments. **No bounces, no parallax, no decorative loops.** Respect
  `prefers-reduced-motion`.
- **Hover / press.** Mobile-first, so press is primary: filled buttons darken one step
  (`600 → 700`); outlined buttons drop to ~90% opacity; danger zones darken individually.
  Hover (tablet/web) lightens primary to `400`. Disabled = `neutral-300` fill + `neutral-600`
  text, no shadow.
- **Transparency / blur.** Used almost nowhere — only the loading-lock state (danger panel at
  60% opacity) and the bottom-sheet scrim. No frosted glass.

---

## 4. Spacing, elevation & radius — see tokens

All foundation values live in `tokens/` and are the single source of truth:
`colors.css · typography.css · spacing.css · elevation.css · radius.css · fonts.css`.
The root `styles.css` is an `@import` manifest — consumers link that one file.

---

## 5. Iconography

There is **no bespoke icon set** in the source spec — the brief uses emoji (💧 💨 ❤ 👤 ⚡ ✓)
as placeholders for clinical glyphs. Emoji are unacceptable in the real product: they render
differently per platform, can't be recolored to white on the red danger panel, and read as
casual. **This system substitutes [Lucide](https://lucide.dev) line icons** (consistent
1.5–2px stroke, rounded caps) — appropriate for a clinical instrument and CDN-available.

> ⚠️ **Substitution flag:** the spec's emoji were replaced with Lucide equivalents. If the real
> ResQRules app ships a specific medical icon set, drop the SVGs into `assets/icons/` and remap
> the `<Icon>` component — the names below are the contract.

Mapping (spec → Lucide name):

| Meaning | Spec emoji | Lucide `name` |
| --- | --- | --- |
| Catastrophic bleeding | 💧 | `droplet` |
| Not breathing | 💨 | `wind` |
| No pulse | ❤ | `activity` |
| Unconscious | 👤 | `user` |
| Override / switched | ⚡ | `zap` |
| Guard / already-in | ✓ | `check` |
| Back (LTR) | ← | `arrow-left` |
| Back (RTL) | → | `arrow-right` |
| Reset session | ↺ | `rotate-ccw` |

**Implementation:** the `Icon` component renders a real inline `<svg>` whose Lucide
path geometry is embedded in the component (no network fetch), stroked with `currentColor`
so any icon recolors to white/red/green by inheriting text color. This is offline-safe.
(An earlier CSS `mask-image` approach was abandoned because cross-origin SVGs are silently
dropped as masks by the browser.) Sizes: 20dp (buttons, danger zones), 16dp (inline). Latin
numerals and clinical acronyms are typographic, never iconographic. To add an icon, copy its
inner markup from [lucide.dev](https://lucide.dev) into the `ICONS` map.

No raster logo asset was provided; "ResQRules" is set as a wordmark in `heading` weight white
on the AppBar. Add a real logo to `assets/` when available.

---

## 6. Index / manifest

```
styles.css                  ← global entry (link this) — @import manifest only
tokens/
  fonts.css                 Noto Sans + Noto Sans Arabic (Google Fonts CDN)
  colors.css                primary / semantic / neutral / on-color / urgency + aliases
  typography.css            families, weights, 7-step scale, RTL helper
  spacing.css               8dp scale + layout aliases + touch targets
  elevation.css             3 shadow levels
  radius.css                4 radii
guidelines/                 foundation specimen cards (Design System tab)
components/
  core/                     Icon (shared primitive)
  actions/                  Button, OutlinedButton, CfButton, LangToggle
  content/                  Card, UrgencyBadge, PageCitation, TierBadge
  feedback/                 OverrideToast, LoadingBar, Snackbar
  surfaces/                 DangerPanel, BottomSheet, AppBar
SKILL.md                    portable Agent-Skill wrapper
```

**Component inventory (14 primitives + Icon):** Button (Primary), OutlinedButton (4 variants),
CfButton (4 CF levels), Card (4 variants), UrgencyBadge (3), PageCitation, TierBadge (4 states),
DangerPanel (3 states), LangToggle, OverrideToast (2 variants), LoadingBar, Snackbar,
BottomSheet (Reset), AppBar (Home + Session). Every text-bearing component ships EN + AR.

**Namespace:** components are exposed at `window.ResQRulesDesignSystem_3e3070.<Name>` once the
bundle is loaded — see any component card for the mount pattern.
