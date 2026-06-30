# Handoff: ResQRules — Mobile First-Aid Clinical Decision-Support

## Overview

ResQRules is a phone-sized clinical decision-support app for Red Cross / Red Crescent field
paramedics. It walks a responder through emergency protocols (catastrophic hemorrhage, cardiac
arrest, choking, airway, general assessment) as an interactive Q&A driven by a rules engine.
The responder taps through questions, instructions, and escalation steps; a persistent
**danger panel** lets them jump to a life-threat protocol at any moment.

This package contains two design references and the design-system source they are built on.

- **ResQRules.dc.html** — the runnable, iOS-framed prototype (splash → home → live session).
- **Showcase.dc.html** — a component reference: every component in English + Arabic states.

## About the Design Files

The files in this bundle are **design references created in HTML** — prototypes that show the
intended look and behavior. **They are not production code to ship directly.** The task is to
**recreate these designs in the target codebase's environment** using its established patterns
and libraries.

The app's spec is mobile-native (it is written in "dp"/"sp" units, references the system
navigation bar, and ships bilingual EN/Arabic). The most likely production targets are
**Flutter** or **React Native**; if no app environment exists yet, choose the framework that
best fits the team. The HTML prototype uses a small custom component runtime ("Design
Components") — **do not port that runtime.** Port the *visual + behavioral spec* below into the
target framework's idioms.

## Fidelity

**High-fidelity (hifi).** Colors, typography, spacing, radii, shadows, motion, and copy are all
final and exact (values in Design Tokens below). Recreate the UI faithfully using the codebase's
existing UI primitives. The one thing to treat as *representative* is the **clinical copy** — the
question/instruction text was authored for UI demonstration from the spec's examples and is **not
medical guidance**. Replace it with the real protocol content from the rules engine.

---

## Information Architecture

The app has exactly **two screens** plus a splash. No bottom navigation, no onboarding, no dark
mode (all explicitly out of scope).

1. **Splash** — brief wordmark + indeterminate loading bar, auto-advances (~1.3s) or on tap.
2. **Home** — AppBar + scrollable list of 5 protocol cards.
3. **Session** — AppBar + swappable node body + persistent DangerPanel. The body changes by
   "node type" (6 variants); the shell never changes.

Navigation: tap a card on Home → Session (enters at that chart's entry node). Back arrow or
Reset (↺) on Session → confirmation bottom sheet → Home. Danger-panel zone → jump to the
matching life-threat protocol (or a "guard" toast if already in it).

---

## Screens / Views

### SCREEN 1 — Home (chart selector)

**Purpose:** the responder picks which emergency protocol to run.

**Layout:**
- Status-bar spacer (54dp) over a red AppBar (`#CC0000`).
- **AppBar (home variant, 56dp):** wordmark **"ResQRules"** left (white, 18sp/600). Language
  toggle top-right (`[EN | ع]`).
- **Body:** vertical scroll list, 16dp screen margins, **14dp gap** between cards
  (comfortable) or 8dp (compact — an exploration toggle). Background white.
- 5 ChartCards in fixed order, then a 34dp bottom spacer for the home indicator.

**ChartCard** (component 01):
- White card, **12dp radius**, `level-1` shadow (`0 2 8 rgba(0,0,0,0.10)`).
- **4dp left border accent** colored by urgency: critical `#CC0000`, high `#E85D04`,
  standard `#4A4A4A`. (In Arabic the accent flips to the right edge — use logical
  `border-inline-start`.)
- 16dp padding. Entire card is one tap target → Session. **No chevron, no icon.**
- **Urgency badge** top-right: pill, 6dp radius, urgency-colored background, white text,
  11sp/600, all-caps, letter-spacing ~0.06em. Labels: `CRITICAL / HIGH / STANDARD`
  (Arabic: `حرج / عالي / عادي`).
- **Primary title** = active language, 17sp/600, `#1A1A1A`.
- **Secondary title** = the other language, 14sp/400, `#4A4A4A`, on the line below.
  In EN mode the Arabic secondary is right-aligned; in AR mode the English secondary is
  left-aligned.
- Pressed state: background → `#F5F5F5`.

Cards (order, English title / Arabic title / urgency):
1. Catastrophic Hemorrhage / النزيف الكارثي — **CRITICAL**
2. Cardio-Respiratory Arrest Adult / السكتة القلبية التنفسية (بالغ) — **CRITICAL**
3. Heimlich Maneuver / مناورة هايمليك — **CRITICAL**
4. Upper Airway Management / إدارة المجرى الهوائي العلوي — **HIGH**
5. General Intervention Process & Patient Assessment / عملية التدخل العام وتقييم المريض — **STANDARD**

### SCREEN 2 — Session (protocol walkthrough)

**Purpose:** run the active protocol; the body swaps per node type while the shell stays fixed.

**Fixed shell, top to bottom:**
- Status-bar spacer (54dp) over red.
- **AppBar (session variant, 56dp):** back arrow (`arrow-left`, flips to `arrow-right` in RTL) →
  opens reset confirmation; chart title (white, 17sp/600, truncated to 1 line); language toggle;
  reset button (`rotate-ccw`, 40dp tap target). All controls white on red.
- **Loading bar lane (3dp):** an indeterminate `#CC0000` sweep appears here during any
  transition; otherwise empty. Sits directly below the AppBar.
- **Body area:** 16dp side padding, 12dp top. Scrolls if content overflows. The
  **page citation** ("p.7", caption 12sp/`#4A4A4A`) is the first element of every body.
- **OverrideToast** overlays the top of the body area (see Interactions).
- **Error Snackbar** docks above the DangerPanel when present.
- **DangerPanel (64dp):** always visible (see component 09).
- 34dp red home-indicator safe-area below the panel.

---

## Node Type Components (the 6 body variants)

All share: 16dp side / 12dp top padding; page citation at the very top; text left-aligned in EN,
right-aligned in AR. Cards are 12dp radius + `level-1` shadow + 20dp inner padding unless noted.

### A) NodeInstruction (component 02)
A "do this" step that flows on after Continue.
- Page citation → white Card with instruction text (16sp/400, **1.6 line-height**, may be
  multi-paragraph) → flexible spacer → full-width primary **Continue** button (red, 56dp) pinned
  to the bottom.

### B) NodeQuestion (component 03)
A decision point with 2–4 options.
- Page citation → white Card with question text (16sp/600, 1.5 lh) → 16dp gap → stacked
  full-width **OutlinedButtons** (red border + text, 56dp, **12dp gap** between). Text labels
  only, no icons. Supports a 4-option variant (e.g. the ABCD primary-survey question).

### C) NodeCFQuestion — Certainty Factor (component 04)
One screen: the CPR "Sign of life present?" assessment. Conservative bias — ambiguous answers
go to CPR.
- Page citation → white Card: question text (16sp/600) + 1dp divider + CF prompt (14sp/400,
  `#4A4A4A`, 1.5 lh) → 16dp gap → **4 CfButtons** (56dp, **10dp gap**):
  - Certain `+1.00`, Likely `+0.60` — green border/text (`#2D6A4F`)
  - Unsure `+0.20` — amber border/text (`#E85D04`)
  - None `−1.00` — red border/text (`#CC0000`)
- The CF value renders as small secondary text (11sp) inline with the label, on the trailing
  side (right in LTR, left in RTL). Color rule: CF ≥ 0.5 → green; 0 < CF < 0.5 → amber;
  CF ≤ 0 → red.

### D) NodeHemQuestion — Hemorrhage Escalation (component 05)
The "still bleeding?" recheck after each hemorrhage tier. Shows BOTH what was just done AND the
escalate decision.
- Row: page citation (leading) + **TierBadge** (trailing).
- **Intervention callout** = `callout` Card variant (4dp red left accent, faint tint): a 12sp/600
  uppercase label "Intervention applied" + the text of what was done (14sp/400, 1.5 lh).
- 16dp gap → recheck-question Card: "Active bleeding?" / "هل النزيف نشط؟" (16sp/600).
- 16dp gap → two OutlinedButtons (56dp, 12dp gap): **"yes — still bleeding"** (red) and
  **"no — bleeding controlled"** (success green `#2D6A4F`).

### TierBadge (component 06, standalone)
3 dots in a row, 8dp diameter, 6dp gap:
- Applied tiers (1..current−1): filled `#CC0000`.
- Current tier: filled `#CC0000` with a white ring + subtle pulse.
- Not-yet-applied: empty circle, 1dp `#E0E0E0` border.
- Below the dots: "Tier N / 3" caption (Latin numerals even in Arabic; Arabic label "المستوى").
- States to support: tier 1 (`● ○ ○`), tier 2 (`● ● ○`), tier 3 (`● ● ●`), and complete.

### E) NodeAction — Terminal (component 07)
End of protocol; final instruction, no further choices.
- Card uses the **success** variant: very light green tint `#F0FAF5`, 4dp left accent `#2D6A4F`.
  Final action text 16sp/600.
- Flexible spacer → **"End Session"** (ghost/outlined green, 56dp) → 8dp gap → **"Start Again"**
  (elevated red, 56dp).

### F) NodeJumpStub — Unavailable Transfer (component 08)
Protocol needs to transfer to a chart not yet in the system.
- Card uses the **stub** variant: grey background `#F5F5F5`. Transfer note (16sp/400, e.g.
  "Oxygen algorithm.") + 1dp divider + "Protocol not yet available" (14sp/400, `#4A4A4A`).
- Flexible spacer → full-width **"Back to Home"** (neutral OutlinedButton, 56dp).

---

## Persistent & Feedback Components

### DangerPanel (component 09)
- Fixed 64dp bar at the bottom of Session, solid `#CC0000`, **upward** shadow
  (`0 -2 12 rgba(0,0,0,0.20)`). Always visible across all node types.
- **4 equal-width tap targets**, no inter-button borders. Each: a 20dp white Lucide icon
  centered, a 10sp/600 white label below.
- Zones (LTR order): **Catastrophic Bleeding** (`droplet`) · **Not Breathing** (`wind`) ·
  **No Pulse** (`activity`) · **Unconscious** (`user`). Arabic mirrors the order:
  Unconscious | No Pulse | Not Breathing | Bleeding.
- Press: each zone darkens individually. **Loading-lock state:** whole panel → 60% opacity,
  non-interactive, during any pending transition.

### OverrideToast (component 10)
Full-width banner that slides down from under the AppBar over the body when the rules engine
returns a non-null `override_event`. `#CC0000` bg, white 14sp/600, 12dp vertical / 16dp
horizontal padding. Slides down 200ms ease-out, holds 2.5s, slides up 200ms ease-in.
- **Jump** (guard_fired=false): `⚡ Switched to: [Chart]  (Salience [N])` — icon `zap`.
  Arabic: `⚡ تحويل إلى: [البروتوكول]  (الأولوية [N])`.
- **Guard** (guard_fired=true): `✓ Already in [Chart] — continuing` — icon `check`.
  Arabic: `✓ أنت في [البروتوكول] بالفعل — استمرار`.

### LoadingBar (feedback)
3dp indeterminate left-to-right `#CC0000` sweep, pinned below the AppBar. The only loading
indicator — no spinner overlay; clinical text stays readable. Should feel instant (<300ms).

### Snackbar — error (feedback)
Non-blocking bar docked at the bottom (above DangerPanel): `#1A1A1A` bg, white 14sp,
"Connection error — tap to retry" (Arabic equivalent). Tapping it retries the last action.
Never a full-screen error — the last clinical content stays visible behind it.

### ResetSheet / BottomSheet (component 11)
Bottom sheet (not a dialog), rises from the bottom with `level-3` upward shadow over a black-45%
scrim. Handle bar at top; title "Reset session" (17sp/600); two 64dp full-height rows:
**"Reset this chart"** (current chart name in `#4A4A4A` below) and **"Choose a different chart"**
("Return to chart list" below); centered **"Cancel"** text button at the bottom.

### LangToggle (component 12)
Segmented control, **72dp × 32dp**, two segments `[EN] [ع]`. On the red AppBar: 1dp white border,
white text; active segment = white background + red text; inactive = transparent + white text.
The active pill slides between segments on change. A standalone (on-white) variant also exists.

### AppBar (component 14)
56dp, solid `#CC0000`, **no shadow**. Home variant = wordmark + lang toggle. Session variant =
back + truncated title + lang toggle + reset.

---

## Interactions & Behavior

- **Card tap → Session:** enter at the chart's `entry` node.
- **Every in-session transition routes through a 300ms "loading" gate:** set loading=true →
  show LoadingBar + lock DangerPanel (60%) + fade/slide the body out → after ~300ms apply the
  node change → loading=false → body animates in. This models the rules-engine round-trip.
- **Node body transition (exploration, default "slide"):** body fades + translates ~14px on the
  leading axis (direction-aware: +X in LTR, −X in RTL). Other options: "fade" (opacity only),
  "instant". **Important:** drive visibility off the reliable `loading` boolean, not a separate
  settle timer, so a body can never get stuck invisible under rapid taps.
- **Option select:** if the option has a `jump` target → switch charts (and toast); else advance
  to `next` node.
- **Danger-panel zone:** map zone → chart (bleeding→hemorrhage, breathing→airway,
  pulse→CPR, unconscious→CPR). If already in that chart → **guard** toast; else switch to its
  entry node → **jump** toast (with salience number).
- **Back / Reset (↺):** open ResetSheet. "Reset this chart" → re-enter entry node. "Choose a
  different chart" → Home. "Cancel" → dismiss.
- **Terminal NodeAction:** "End Session" → Home; "Start Again" → re-enter entry node.
- **Live language toggle:** flips all copy AND mirrors layout (text alignment, option order,
  back-arrow direction, danger-zone order, CF-value side). **Latin acronyms (CPR, AED, BVM,
  SpO₂) and all numerals stay Latin in Arabic mode.** Because Noto Sans + Noto Sans Arabic share
  metrics, the layout must not reflow on toggle.
- **Error retry:** when a transition "fails" (simulated via a flag in the prototype), show the
  Snackbar; tapping it re-runs the pending action.
- **Motion:** respect `prefers-reduced-motion` (disable the splash/loop animations).

---

## State Management

Single session state object:
- `screen`: `'splash' | 'home' | 'session'`
- `chartId`: which protocol is active
- `nodeId`: current node within the chart
- `lang`: `'en' | 'ar'` (also sets document `dir`)
- `loading`: boolean — gates LoadingBar, DangerPanel lock, and body visibility
- `toast`: `{ visible, variant: 'jump'|'guard', message }`
- `error`: `{ visible }` + a stored "pending action" to retry
- `resetOpen`: boolean

**Protocol graph data model** (drives the engine; see `ResQRules.dc.html` logic for the full 5
graphs). Each chart: `{ id, urgency, titleEn, titleAr, entry, nodes }`. Each node by type:
- instruction: `{ type, page, text:{en,ar}, next }`
- question: `{ type, page, text:{en,ar}, options:[{ id, label:{en,ar}, variant?, next | jump }] }`
- cf: `{ type, page, text, cfPrompt, options:[{ id, label, level:'certain'|'likely'|'unsure'|'none', next }] }`
- hem: `{ type, page, tier, intervention:{en,ar}, text, options:[yes→next, no→next] }`
- action (terminal): `{ type, page, text }`
- jumpstub: `{ type, page, stubNote:{en,ar} }`

Salience map (for jump toasts): hemorrhage 100, CPR 95, Heimlich 90, airway 80, general 50.

**Real integration:** replace the mocked graph + 300ms timer with the actual rules-engine API.
Each response yields the next node and an optional `override_event` (`{ guard_fired, chart_name,
salience }`) that drives the OverrideToast.

---

## Design Tokens

Authoritative source: `ds/tokens/*.css` (also copied into this bundle). Key values:

**Color**
- Primary `#CC0000`, Primary Dark `#990000`, Primary Light `#FF3333`
- Success `#2D6A4F`, Warning (amber-red) `#E85D04`
- Text Primary `#1A1A1A`, Text Secondary `#4A4A4A`
- Background `#FFFFFF`, Surface `#F5F5F5`, Border `#E0E0E0`, Divider `#F0F0F0`
- On-Primary `#FFFFFF`
- Urgency: critical `#CC0000`, high `#E85D04`, standard `#4A4A4A`
- Tints (card backgrounds, barely-there): success tint `#F0FAF5`, plus primary/warning 100s
- Press = one step darker (600→700); hover (web/tablet) = lighter (→400); disabled =
  `#E0E0E0` fill + `#4A4A4A` text, no shadow

**Typography** — Noto Sans (Latin) + Noto Sans Arabic (identical metrics). Weights **400/600/700
only, never < 400.**
- Display 22 / 700 — chart & section titles
- Heading 18 / 600 — AppBar title
- Body 16 / 400, **line-height 1.6** — clinical instruction text
- Label 15 / 600 — button labels
- Caption 12 / 400, `#4A4A4A` — node ID, page citation

**Spacing** — strict 8dp grid: 4 / 8 / 12 / 16 / 20 / 24 / 32. Screen margin 16, card padding 20,
option gap 12, CF-button gap 10.

**Radius** — 6 (badges, tier dots) · 8 (buttons, inputs) · 12 (cards, sheets) · full pill
(lang toggle, urgency badges).

**Elevation** — exactly 3, no decorative shadows:
- `level-1` cards: `0 2 8 rgba(0,0,0,0.10)` (downward)
- `level-2` bottom panel: `0 -2 12 rgba(0,0,0,0.20)` (upward)
- `level-3` bottom sheet (upward, slightly stronger)

**Touch targets** — 56dp minimum on everything tappable; DangerPanel zones 64dp.

**Hard "do nots":** no gradients, no background imagery/texture/blur (except the loading-lock
60% opacity and the sheet scrim), no decorative icons on content cards, no shadows on text,
no bottom nav, no splash beyond the minimal wordmark, no dark mode.

---

## Assets / Icons

No bespoke icon set or logo was provided. Icons are **Lucide** line icons (1.5–2px stroke,
rounded caps), recolored via `currentColor`. Mapping used:

- Catastrophic bleeding → `droplet`
- Not breathing → `wind`
- No pulse → `activity`
- Unconscious → `user`
- Override / switched → `zap`
- Guard / already-in → `check`
- Back (LTR / RTL) → `arrow-left` / `arrow-right`
- Reset session → `rotate-ccw`

The "ResQRules" wordmark is type only (Noto Sans 700, white on red). **The Red Cross / Red
Crescent emblem is a protected symbol and was deliberately NOT drawn** — brand identity is
carried by the `#CC0000` system + wordmark. If your org is authorized to use the emblem, add the
official asset; otherwise keep it out.

Fonts load from Google Fonts (Noto Sans + Noto Sans Arabic). In production, self-host the woff2
files.

---

## Files

In this bundle (`design_files/`):
- `ResQRules.dc.html` — the runnable prototype (all screens, all node types, all states, full
  bilingual state machine, the 5 protocol graphs). **Primary reference.**
- `Showcase.dc.html` — every component in EN + AR states, plus a foundations panel.
- `ChartCard.dc.html`, `NodeInstruction.dc.html`, `NodeQuestion.dc.html`,
  `NodeCFQuestion.dc.html`, `NodeHemQuestion.dc.html`, `NodeAction.dc.html`,
  `NodeJumpStub.dc.html` — the individual composed components.

In `design_system/`:
- `ds/tokens/*.css` — the authoritative token values (colors, typography, spacing, elevation,
  radius, fonts, motion).
- `component-apis.md` — the prop contract (`.d.ts` summary) for all 15 design-system primitives,
  so you can see each component's inputs without the HTML runtime.

> The `.dc.html` files use a custom component runtime for the prototype only. Read them for
> structure, composition, copy, and exact values — but implement in your target framework's
> idioms (e.g. Flutter widgets / RN components), not by porting the runtime.

## How to use this with Claude Code

1. Unzip into (or beside) your app repo.
2. Point Claude Code at `design_handoff_resqrules/README.md` and `design_files/ResQRules.dc.html`.
3. Ask it to implement screen-by-screen in your stack, starting with tokens → ChartCard → Home,
   then the Session shell → each node type → DangerPanel/toasts/sheet.
4. Open the `.dc.html` files in a browser to see the intended look/behavior as you build.
