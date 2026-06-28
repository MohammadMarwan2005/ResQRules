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
  - **3a — primary-survey override [BUILT].** Hybrid input + 4 danger overrides + salience + guard.
  - **3b — hemorrhage escalation loop [BUILT].** Semantic tier fact that accumulates in working memory.
  - **3c — not built yet:** certainty factors; cross-protocol return-stack.

## Inference layer 3a — primary-survey override (BUILT)

### Hybrid input model
The user is a **paramedic**. By default the engine walks the current chart and asks the next
question (the low-salience baseline `walk` rule). But at **every** prompt a fixed menu of
**danger observations** is offered; asserting one (instead of answering) declares a `Danger`
fact that a high-salience override rule acts on, preempting the current node and jumping to the
correct protocol. This asynchronous assertion is the headline feature — a rules engine can do it,
a static flowchart cannot. (We do NOT parse free-text observations — fixed menu only.)

Menu keys → danger → target protocol entry:
| key | danger observation | jumps to |
|----|--------------------|----------|
| `b` | catastrophic_bleeding | `hemorrhage` (hem_01) |
| `n` | not_breathing | `cpr_adult` (cpr_01) |
| `p` | no_pulse | `cpr_adult` (cpr_01) |
| `u` | unconscious | `cpr_adult` (cpr_01) |

`unconscious` airway-first note: clinically an unconscious patient *with* pulse/breathing should
route airway-first; per the fixed spec menu we send `unconscious` to the CPR-adult entry (whose
first step is the unresponsive/airway assessment). A finer airway-vs-CPR split is a future refinement.

### Salience = clinical precedence (rubric point)
Each override is a high-salience `@Rule` matching a `Danger` fact; the walker is the low-salience
baseline. Salience values encode the C-ABC trauma precedence:
| rule | salience | rationale |
|------|---------:|-----------|
| `ov_bleeding` | **100** | catastrophic "C" — bleed-out kills fastest (C before A in C-ABC trauma) |
| `ov_arrest` (not_breathing / no_pulse) | **90** | airway / breathing / circulation arrest |
| `ov_unconscious` | **80** | disability / consciousness |
| `walk` (normal traversal) | **0** | baseline, lowest |

Conflict resolution: when more than one danger is live, Experta's salience strategy fires the
highest first (proven in `test_overrides.py` TEST 1: bleeding fires before arrest).

### Guard (the real bug risk: fire-once + no re-entry)
An `Active(chart=…)` fact tracks the current protocol. Every override (1) `retract`s the `Danger`
it handled, so it fires **once** per assertion, and (2) if we are **already in** the target
protocol, it does **not** jump — it re-prompts the current node (no re-entry, no loop). Proven in
`test_overrides.py` TEST 2 and live session (c): re-asserting `not_breathing` inside CPR keeps the
position and never restarts the protocol.

## Inference layer 3b — hemorrhage escalation loop (BUILT)

### What it demonstrates (distinct rubric point — see table)
**Accumulation of state in working memory across rule firings.** The escalation *tier* is a fact
`Bleeding(tier=N)` that advances each pass; the rule reasons over **(current tier + a re-asserted
`StillBleeding` fact)** to choose the next action. This is the engine reasoning over working
memory — not a flowchart sending control back to the same box. (Contrast 3a, which is about
salience/conflict-resolution.)

### The escalation (tiers mapped onto `hemorrhage.json`'s existing nodes — read, not reinvented)
| tier | intervention node | recheck node | terminal? |
|----:|-------------------|--------------|-----------|
| 1 | `hem_01` direct pressure / compression / hemostatic dressing | `hem_02` | |
| 2 | `hem_03` second compression bandage | `hem_04` | |
| 3 | `hem_05` tourniquet | `hem_06` | **yes** |

Rules: `hem_enter` (sal 50) starts the loop on arrival at `hem_01` (works whether reached by normal
walk via `gen_05` **or** by the catastrophic_bleeding override); `hem_apply` (sal 10) applies the
tier-N intervention, moves `Position` to the recheck node (so the override menu still works), and
prompts; `hem_decide` (sal 10) reasons over tier + `StillBleeding`:
- **still bleeding & N < 3** → retract `Bleeding(N)`, declare `Bleeding(N+1)` (**ADVANCE**, never re-asks N).
- **still bleeding & N = 3 (terminal)** → **HOLD** (no tier 4), route to urgent transport (`hem_07`).
- **controlled** → exit to post-control transport (`hem_08` for tiers 1-2; `hem_07` after tourniquet).

The baseline `walk` rule carries `NOT(Bleeding())`, so it cedes control while the loop owns the
patient and resumes only for the terminal transport leaf. `_move` clears loop facts on a protocol
change, so a danger asserted mid-loop (n/p/u) jumps out cleanly with no stale tier.

### Guards proven (`test_overrides.py` TEST 3-5, live sessions a/b/c)
- **Advance, don't spin:** tiers visited = `[1,2,3]`, strictly increasing, each once.
- **Terminal holds:** "still bleeding" at the tourniquet tier produces no tier 4 / no crash / no
  infinite loop — it routes to urgent transport. (Note: the chart *draws* a re-apply loop
  `hem_06.yes -> hem_05`; the semantic model intentionally caps at the terminal tier and routes to
  urgent transport instead of looping forever — flagged as a deliberate divergence from the drawn edge.)
- **Early exit:** "controlled" at tier 1, 2 (mid), and 3 each exit cleanly.
- **Integration:** override-into-hemorrhage then loop behaves identically to arriving by normal walk.

## KBS rubric → where it lives
| KBS concept | In ResQRules |
|-------------|--------------|
| **Facts (working memory)** | `Current(nid=…)` = where we are; later patient facts (`Conscious`, `Bleeding`, `SpO2`) asserted as answers accumulate. |
| **Forward chaining** | Experta RETE matches the `Current` fact, fires the generic walk rule, asserts the next `Current` → chains forward through the tree. |
| **Salience** | [BUILT 3a] primary-survey overrides get high salience (100/90/80) so they pre-empt the normal walk (0) regardless of current node — salience = clinical precedence (see table above). |
| **Conflict resolution** | [BUILT 3a] when several rules are eligible (override vs. walk, or two dangers at once), salience + Experta's strategy decide which fires — proven in `test_overrides.py`, not hand-sequenced. |
| **Working-memory state accumulation** | [BUILT 3b] the hemorrhage escalation tier is a fact `Bleeding(tier=N)` that advances across rule firings; the rule reasons over current tier + a re-asserted `StillBleeding` fact (semantic loop, not a drawn back-edge). |
| **Certainty factors** | Phase 3: `certainty` on nodes where the source implies "if unsure…"; combine CFs along a path to express confidence in the recommendation. |
| **Hubs / sub-routines** | `jump` nodes (#8 Airway, #10 Hemorrhage, CPR) modelled as cross-tree transfers; Phase 2 return-stack lets a sub-routine return. |
