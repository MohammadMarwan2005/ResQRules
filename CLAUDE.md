# ResQRules — repo guardrails (read before touching anything)

ResQRules is a terminal first-aid **knowledge-based system** (university KBS course).
It walks a responder through SARC / Red Crescent first-responder SOP flowcharts via
interactive Q&A, using the **Experta** forward-chaining rules engine.

## The one architectural rule that matters
**Data-driven, NOT one-`@Rule`-per-node.** The flowcharts are *knowledge* (JSON trees);
a *small* set of generic Experta rules walks any tree. Writing one hand-coded rule per
box turns Experta into a flowchart costume and demonstrates no inference — do not do it.

Layers:
1. **Knowledge** — one JSON tree per chart in `data/`, conforming to `SCHEMA.md`.
2. **Generic engine** — `engine.py`: a handful of rules that assert/match facts to walk
   ANY conforming tree.
3. **Domain rules (Phase 3, later)** — a few REAL rules on top: high-salience primary-survey
   overrides, hub jumps, hemorrhage "still bleeding?" re-check loops, certainty factors.
   This is the graded inference work. **Leave room for it; never bake routing into per-node rules.**

## File layout
```
CLAUDE.md  PLAN.md  SCHEMA.md      # docs / guardrails
data/<chart_id>.json              # one knowledge tree per chart
engine.py                         # generic Experta walker (loads ONE chart, walks it)
validate.py                       # schema + graph validation, fails loudly
rasterize.py                      # PDF page -> PNG @180 DPI (extraction aid)
build/png/                        # rasterized images (gitignored, regenerate anytime)
```
PDFs are **not** in a single folder. They live at the repo root and in `Traumatic/` and
`Non-Traumatic/`. Do not move them (preserves the author's categorisation). The 5 in-scope:
| chart | file |
|-------|------|
| #1 General Intervention Process & Patient Assessment | `General Intervention Process & Pat Assessment.pdf` |
| #3 Cardio-Respiratory Arrest – Adult | `Non-Traumatic/Cardio-Respiratory Arrest Adult_validated.pdf` |
| #7 Heimlich / Choking | `Non-Traumatic/Heimlich Maneuver_validated.pdf` |
| #8 Upper Airway Management | `Non-Traumatic/Upper Airway Management_validated.pdf` |
| #10 Catastrophic Hemorrhage | `Traumatic/Catastrophic Hemorrhage_validated.pdf` |

## Extraction rules (HARD constraints)
- **VISUAL ONLY.** Rasterize the page to PNG @ ~180 DPI and *read the image*
  (`python rasterize.py`). NEVER use `pdftotext` / text-layer extraction — it scrambles
  box labels and drops the arrows, which ARE the logic.
- **Never invent, infer, or "improve" medical content.** Transcribe only what the box shows.
  Unreadable/ambiguous → `"text": "[UNCLEAR: best guess]"` and list it for human review.
- **Every node cites its source page** (`"page": <n>`).
- Any edge you add that is **not drawn on the chart** (e.g. a safe-exit so a one-armed
  decision diamond is walkable, or a "repeat until…" loop-back) must be flagged in the
  extraction report as ADDED/DERIVED. Do not bury it.
- Cross-tree / hub transfers, and any jump to an out-of-scope or absent chart, are modelled
  as a `jump` node that **degrades gracefully** (engine prints `would transfer to <X>`)
  instead of crashing.

## Always validate after extraction
Run `python validate.py data/<chart>.json`. It must PASS:
entry exists · every option/`next` resolves to a real local node OR a `jump` target ·
no orphan (unreachable) nodes · every in-tree leaf is `type: action` (`jump` = external
transfer, reported separately). Validation **fails loudly** (non-zero exit) on any violation.

## Definition of done (per chart)
`data/<chart>.json` validates clean **and** `engine.py` walks it entry → leaf in the
terminal, including at least one `jump` path. Then stop for human review.

## Scope
v1 = exactly 5 charts: #1, #3, #7, #8 (model SHALLOW), #10.
Phase 2 = add JSON only for #2, #4, #5, #6, #9, #11, #12 + two referenced-but-absent
charts (Oxygen, Seizure). Do not build Phase-2 charts unless asked.
