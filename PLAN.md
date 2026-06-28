# ResQRules — plan

## Goal
A terminal first-aid expert system that walks a responder through SARC / Red Crescent
first-responder SOP algorithms via interactive Q&A, built on the **Experta** forward-chaining
rules engine, for a university Knowledge-Based-Systems course.

## In scope (v1 — exactly 5 charts)
- **#1 General Intervention Process & Patient Assessment** — the ROOT / spine (SSS → ABCDE).
- **#3 Cardio-Respiratory Arrest – Adult** — flagship emergency.
- **#7 Heimlich / Choking** — jumps into CPR when the patient goes unconscious. *(extracted)*
- **#10 Catastrophic Hemorrhage** — hub; branches off #1; escalation re-check loop.
- **#8 Upper Airway Management** — hub called by #3 and #7; modelled SHALLOW.

## Out of scope (Phase 2 = add JSON only, don't build now)
#2, #4, #5, #6, #9, #11, #12, plus two referenced-but-absent charts (**Oxygen**, **Seizure**).
Any jump into one of these is a graceful `jump` stub today.

## Architecture
1. **Knowledge** — JSON trees in `data/` (see `SCHEMA.md`).
2. **Generic engine** (`engine.py`) — a small set of generic Experta rules walk *any* tree by
   asserting/matching a `Current` fact. No per-node rules.
3. **Domain rules** (Phase 3) — a few REAL rules layered on top. This is the graded inference
   work; the data-driven core exists to make room for it.

## Phases
- **Phase 1 (this run):** scaffold (`CLAUDE.md`, `SCHEMA.md`, `PLAN.md`), schema, extract
  **#7 Choking** → `data/choking.json`, build `engine.py` + `validate.py`, run end-to-end
  (leaf path **and** jump-to-CPR-stub path). ✅
- **Phase 2:** extract the other 4 in-scope charts (#1, #3, #8 shallow, #10), wire hub jumps
  between them and a return-stack so a `jump` can come back.
- **Phase 3:** the real inference layer — see rubric mapping below.

## KBS rubric → where it lives
| KBS concept | In ResQRules |
|-------------|--------------|
| **Facts (working memory)** | `Current(nid=…)` = where we are; later patient facts (`Conscious`, `Bleeding`, `SpO2`) asserted as answers accumulate. |
| **Forward chaining** | Experta RETE matches the `Current` fact, fires the generic walk rule, asserts the next `Current` → chains forward through the tree. |
| **Salience** | Phase 3: primary-survey overrides ("life-threatening bleeding" / "no breathing") get high salience so they pre-empt the normal walk regardless of current node. |
| **Conflict resolution** | When several rules are eligible (e.g. an override vs. the normal walk), salience + Experta's strategy decide which fires — demonstrable, not hand-sequenced. |
| **Certainty factors** | Phase 3: `certainty` on nodes where the source implies "if unsure…"; combine CFs along a path to express confidence in the recommendation. |
| **Hubs / sub-routines** | `jump` nodes (#8 Airway, #10 Hemorrhage, CPR) modelled as cross-tree transfers; Phase 2 return-stack lets a sub-routine return. |
