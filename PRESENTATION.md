# ResQRules — Unified Content Plan: Report + 15-min Presentation

> Approved plan for the two course deliverables: (1) a thorough written **report**, (2) a
> **~15-min slide presentation**, visual and demo-driven. Same skeleton, different depth.
> Audience = KBS professors grading on: knowledge/inference separation, forward chaining,
> working memory, conflict resolution, salience, certainty factors — always tied back to
> **Experta primitives** (`Fact`, `KnowledgeEngine`, `@Rule`, salience, `declare`/`retract`).
>
> Workflow gates: this plan ✅ → ONE theme test slide (approve) → full deck + report.

---

## 0. Verified corrections to the domain framing (IMPORTANT)

Every stage claim was checked against actual `text_en` in the five JSONs. Presenting the
uncorrected version in front of the professor who owns the source charts is the biggest
avoidable risk in the deck.

| Draft said | What the JSON actually says | How we present it |
|---|---|---|
| Pre-first-aid = **DRS** (Danger, Response, Send for help) | **SSS = Safety → Scene → Situation** (`gen_01`–`gen_03`); chart calls it "Preliminary Assessment". "DRS" appears nowhere; no "send for help" step exists (closest: "Need reinforcement?" in `gen_02`) | Use **SSS / Preliminary Assessment**. If DRS is mentioned at all: "other doctrines call this DRS; SARC uses SSS" — spoken aside, not on-slide |
| Primary survey **ABC**, flips to **CAB** in critical circulation cases | Only **ABCDE** appears (`gen_06`). "CAB"/"C-ABC" appear nowhere — BUT the *structure* encodes circulation-first: `gen_04` "Life threatening bleeding?" → jump to hemorrhage sits **before** the ABCDE node | Say: "the chart hard-codes the exception *structurally* — catastrophic bleeding is checked **before** ABCDE." Stronger than a mnemonic: the knowledge encodes precedence positionally, and our salience values (100 > 90) encode the same precedence in the engine. Don't put "CAB" on a slide |
| Secondary survey = **DE** (Disability, Exposure) | **D and E are the tail of ABCDE inside the *Primary* Assessment** (`gen_06`). Secondary Assessment (`gen_10`) = SAMPLER, OPQRST, vital signs, GCS, PERRLA | Present four chart swim-lanes as drawn (per `meta.notes`): **Preliminary (SSS) → Primary (AVPU + ABCDE) → Secondary (history + vitals) → Continuous Assessment** (`gen_11`) |

Other verified facts this plan relies on:
- Charts say "**Assessment**", never "survey" — match their vocabulary on slides.
- `engine.py` **defaults `LANG = "ar"`** (line 28) — demo prep must set it explicitly either way.
- Engine surface: 8 `@Rule`s (walk 0; overrides 100/90/80; hem_enter 50; cf 20; hem_apply/decide 10),
  6 `Fact` subclasses; the terminal literally prints salience and rule firings
  (`!! DANGER [kind] (sal 90): OVERRIDE…`, `>> ESCALATION TIER 2…`, `~ CF +0.20 < +0.50: doubt -> CPR branch`)
  — the engine narrates its own inference; the demo exploits this.
- The **production Flutter app is `~/AndroidStudioProjects/resq_rules`** (Clean Architecture,
  Cubit, Retrofit/Dio, get_it, freezed, ARB l10n). This repo's `mobile/` is the earlier
  prototype (raw `http` + `provider`) — mention as "we prototyped, then rebuilt properly", nothing more.
- App rendering is server-driven: `ScreenType` enum switches one widget per node `type`; the
  shell (AppBar + loading bar + **danger panel**) never changes. The danger panel IS inference
  layer 3a as UI.
- Real endpoints (for report §8): `GET /charts`, `POST /sessions`, `GET /sessions/{id}`,
  `POST /sessions/{id}/step`, `/reset`, `DELETE`.
- App defaults to hosted backend `https://resqrules.duckdns.org` — demo-day network dependency.
- **No logo asset exists**: identity = "ResQRules" wordmark, white on `#CC0000`; the Red
  Cross/Crescent emblem is *deliberately never drawn* (protected symbol — one spoken compliance
  line). Launcher icon is still stock Flutter — polish before projecting a real phone.

---

## 1. Merged outline

### 1a. Report — table of contents

1. **Introduction** — problem, what ResQRules is, stakeholders (SARC responders/trainees, KBS course).
2. **Domain background: how a paramedic thinks** — four assessment phases as drawn on chart #1; the circulation-first structural exception.
3. **KBS background** — brief Experta primer: facts/WM, RETE, forward chaining, salience/conflict resolution, CF concept (and that Experta lacks native CF — sets up §6).
4. **Knowledge acquisition & representation** — sources (SARC PDFs + team paramedic), visual-only extraction @180 DPI ("the arrows ARE the logic"), the JSON schema, provenance audit trail (58/59 `source`), `validate.py`.
5. **Architecture (the centerpiece)** — rejected design (one `@Rule` per node = "web app with static hardcoded pages, no database") vs. chosen design (knowledge/logic separation = the textbook KBS definition). 8 rules / 59 nodes / 5 charts.
6. **The inference engine** — generic walker as declare/match/fire loop; three inference layers mapped to Experta primitives: 3a salience overrides + conflict resolution, 3b working-memory tier accumulation, 3c CF-as-data + thresholding rule.
7. **Complete flow walkthrough** — the slide trace as figures with WM tables per step.
8. **System integration** — FastAPI wrapper + stability guarantee (contract driven by node `type` from JSON, not by rules); Flutter app; bilingual design (routing is language-independent).
9. **Testing & validation** — the 11 automated tests and which KBS property each proves.
10. **Limitations & future work** — no return-stack (jumps one-way); `unconscious` routes to CPR entry (airway-first refinement pending); Phase-2 charts = JSON only, zero engine change.
11. **Conclusion** — the central KBS lesson: knowledge/logic separation.
12. **Acknowledgments** — supervisor (Miss Omama, official title TBC) + team.
- **Appendices**: schema reference; chart inventory + provenance stats; API summary; full engine trace transcripts (EN + AR).

### 1b. Slide map (~15 min → 18 logical slides, ~27 physical)

| # | Sec | Slide | Time | Phys |
|---|-----|-------|------|------|
| 1 | A | Title + wordmark | 0:20 | 1 |
| 2 | A | The problem: paper can't re-route | 1:00 | 1 |
| 3 | A | What ResQRules is + stakeholders | 0:45 | 1 |
| 4 | B | How a paramedic thinks (4 phases, corrected) | 1:15 | 2 |
| 5 | D1 | Knowledge sources | 0:30 | 1 |
| 6 | D2 | The design we rejected | 1:00 | 1 |
| 7 | D3 | The design we built (CENTERPIECE) | 1:15 | 2 |
| 8 | D4 | PDF → JSON: extraction + provenance | 0:45 | 1 |
| 9 | D5 | The engine in Experta terms | 1:00 | 1 |
| 10 | D5 | Inference I: salience + conflict resolution | 1:00 | 1 |
| 11 | D5 | Inference II: certainty factor at cpr_11 | 0:45 | 1 |
| 12 | C | **Flow walkthrough trace** (script §5) | 2:00 | ~9 |
| 13 | D6 | FastAPI in one slide | 0:30 | 1 |
| 14 | D7 | The Flutter app | 0:45 | 1 |
| 15 | D8 | **Demo (placeholder — video slot)** | 1:30 | 1 |
| 16 | F1 | Journey recap + thesis | 0:30 | 1 |
| 17 | F2 | Team | 0:20 | 1 |
| 18 | F3 | Thanks (Miss Omama) + Questions | 0:10 | 1 |
| | | **Total** | **≈14:30** | ~27 |

**Cut levers → 12 min:** merge 5 into 8 (−30s); merge 11 into 10 (−30s); demo → 60s recording (−30s); fold 3 into 2 (−30s).
**Stretch → 20 min:** re-add a Testing slide (after 12); extend demo with CF live; offer the "add a 6th chart live, zero code change" stunt in Q&A.

---

## 2. Per-slide guidance (key message · what to say · one visual)

1. **Title** · *ResQRules exists.* · "A knowledge-based system that walks a first responder through Red Crescent protocols." · Visual: wordmark white-on-`#CC0000`.
2. **The problem** · *The patient doesn't follow the flowchart.* · SARC SOP = 12 paper charts; under adrenaline you must find the right box and follow arrows — while the patient deteriorates mid-protocol; paper can't re-route. · Visual: real hemorrhage PDF page, red "you are here… but the patient stopped breathing" annotation.
3. **What it is + stakeholders** · *Protocols as software that reacts.* · Terminal engine → API → mobile app; for responders, trainees, and (this room) a KBS case study. · Visual: phone screenshot + terminal screenshot side by side.
4. **How a paramedic thinks** · *Four assessment phases — and one structural exception.* · Preliminary (SSS) → Primary (AVPU + ABCDE) → Secondary (SAMPLER/OPQRST/vitals) → Continuous. Build 2: "before ABCDE, one question — *life-threatening bleeding?* — circulation-first as *structure*; our engine encodes the same precedence as *salience*." (Seeds slide 10.) · Visual: 4 swim-lanes redrawn from chart #1, exception arrow in danger red.
5. **Knowledge sources** · *Expert-validated knowledge, not our invention.* · SARC official flowcharts + a paramedic **on the team** (M.GH) as living expert for ambiguities. · Visual: PDF thumbnails + expert-in-the-loop icon.
6. **The design we rejected** · *One `@Rule` per box = no knowledge base.* · 59 hand-coded rules; medical revision = code change; Experta as flowchart costume; "exactly like a web app with static hardcoded data and no database." · Visual: a wall of 59 tiny `@Rule` snippets, crossed out.
7. **The design we built (CENTERPIECE)** · *Knowledge is data; inference is generic — that's what "KBS" means.* · JSON knowledge base ↔ small generic engine; **8 rules walk 59 nodes across 5 charts**; falsifiable: chart #6 = drop a JSON file, zero code change. Build 2: 3-layer diagram with API/app above. · Visual: KB/engine separation diagram — the diagram of the talk.
8. **PDF → JSON** · *Faithfulness is engineered, not promised.* · Visual-only extraction ("the arrows ARE the logic"); every node cites its page; provenance `source`/`derived`/`added` = 58/59 `source`; `validate.py` fails loudly. · Visual: chart box photo morphing into its JSON node, provenance badge.
9. **The engine in Experta terms** · *Forward chaining = declare → match → fire.* · `KnowledgeEngine` subclass; `Position`/`Active` facts = working memory; the `walk` rule (salience 0) matches `Position`, renders the node from JSON, `retract`s old / `declare`s new → RETE chains. One line: every inference behavior is test-proven (11 tests). · Visual: the actual `walk` rule signature + declare/match/fire loop.
10. **Inference I: salience + conflict resolution** · *Salience encodes clinical precedence.* · At every prompt the paramedic can assert a `Danger` fact instead of answering (b/n/p/u); overrides at 100/90/80 preempt the walk (0); two dangers at once → conflict resolution fires bleeding before arrest (proven, TEST 1); guards: `retract` once-only + `Active` no-re-entry. "A paper chart cannot accept an asynchronous fact." · Visual: salience ladder 100/90/80/0 as a triage board.
11. **Inference II: certainty factor** · *Uncertainty is data too.* · `cpr_11` "Sign of life?" — gasping ≠ breathing; Experta has no native CF, so: `SignOfLife(cf)` fact + one thresholding rule; scale certain 1.0 / likely 0.6 / **unsure 0.2** / none −1.0, threshold 0.5 → "if in doubt, compress"; the bias lives in the *scale*, endpoints match binary. · Visual: 4 answer buttons on a confidence dial with the 0.5 cut line.
12. **Flow walkthrough** · *Watch working memory drive the walk.* · Progressive-reveal trace, script §5.
13. **FastAPI** · *The API contract is a consequence of the architecture.* · Response shapes driven by node `type` from JSON — new rules: zero API change; new chart: auto-discovered; every response bilingual. No internals. · Visual: one JSON response with `type` highlighted feeding a screen wireframe.
14. **Flutter app** · *The same knowledge, in a responder's pocket.* · Thin client: one widget per server node `type` (`ScreenType` switch — the KBS drives the UI); persistent **danger panel** (= slide 10's overrides as UI); instant EN↔AR, zero server round-trip; RTL flips locally. One breath on stack: Clean Architecture, Cubit, Retrofit. · Visual: 3 phone screens (question / override toast showing its salience / action leaf).
15. **Demo (placeholder for now — decided)** · *The engine narrates its own inference.* · Slide ships as a styled placeholder with an embedded-video slot (HTML deck plays video natively). When the video is recorded, the recommended content: **60s terminal** (`LANG="en"`) — the engine prints the KBS evidence verbatim; press `b` mid-assessment, watch the preempt (`!! DANGER [catastrophic_bleeding] (sal 100): OVERRIDE`) — then **30s Flutter app** as product closer. Ready-made scripts: `presentation/traces/override_bleeding_en.txt` and `cf_unsure_en.txt`.
16. **Journey recap + thesis** · *One picture, one sentence.* · PDFs → JSON → Experta engine → FastAPI → Flutter; "Paper can't react; knowledge as data + a small inference engine can." Spoken aside: limitations (one-way jumps; Phase-2 = JSON only). · Visual: 5-icon pipeline (reused as report cover figure).
17. **Team** · *Journey order = people order.* · M.GH (knowledge/paramedic) → M.SH (AI/engine) → M.JA (FastAPI) → M.Y.D (Flutter/design) → M.Marwan (Flutter/UI/DevOps). Full names swapped in before generation. · Visual: 5 avatars ON the slide-16 pipeline.
18. **Thanks + Questions** · Sincere one-liner for our supervisor **Miss Omama** · Visual: wordmark + "Questions?".

---

## 3. Topics ADDED (and why)

1. **Conflict-resolution moment (slide 10, TEST 1)** — named grading criterion; literal proof exists (two simultaneous `Danger` facts → salience order decides). Costs 15s.
2. **Provenance / faithfulness engineering (slide 8)** — knowledge acquisition is a graded KBS phase; `source/derived/added` + page citations + loud validation is the most defensible originality claim; pre-answers "did you invent medical content?"
3. **CF as its own slide (11)** — named rubric line; CF-as-data workaround (Experta has none natively) is a design contribution.
4. **The falsifiable claim (slide 7 + Q&A stunt)** — "chart #6 is a JSON drop, zero code change" turns the architecture argument from adjective into experiment.
5. **Limitations & future work (report §10; aside on slide 16)** — academic honesty is graded; ours are honest and documented (one-way jumps, unconscious→CPR simplification, flagged terminal-hold divergence).
6. **Testing (report §9; one line on slide 9)** — 11 tests mapped to KBS properties; full table in report; own slide only in the 20-min variant.
7. **Bilingual architecture (inside slides 13–14, 20s)** — routing language-independent, display parallel `_en`/`_ar`; locally relevant, and the data-driven design paying off again.

## 4. Topics CUT or kept shallow (and why)

1. **FastAPI internals** — professors grade KBS, not web plumbing; one slide = the stability guarantee only; details → report §8 + appendix.
2. **Flutter widget/state details** — one slide; no widget trees or cubit diagrams; report gets one paragraph + screenshot figure.
3. **Design system / DevOps / hosting** — visible in demo + team slide; zero dedicated slides.
4. **`rasterize.py` mechanics** — one bullet inside slide 8.
5. **Schema field-by-field** — report appendix only; slides show a single JSON node example.
6. **Experta/RETE theory lecture** — professors teach it; concepts introduced only through our code (slides 9–11); compact primer in report §3.
7. **Arabic engine UI mechanics** — demo flag only; details in report.

---

## 5. Section C walkthrough — ~2-minute script (slide 12, ~9 physical)

**Chart choice: `general_assessment`, branch at `gen_04`, yes-branch continuing into `hemorrhage`.**
Why: (a) the ROOT chart — the trace re-teaches section B's four phases free; (b) the
audience-choice question "Life threatening bleeding?" is dramatic and binary; (c) the yes-branch
shows the two best KBS moments in one path: a cross-chart `jump` + `Bleeding(tier=N)` WM
accumulation; (d) depth fits (3 lead-in steps + branch + ≤5 steps). Runner-up `cpr_adult` (CF
node) rejected: 8-node lead-in to `cpr_11` is too deep — CF gets slide 11 + demo instead.

**Slide format:** left ~70% = tree, visited path lit, current node pulsing; right ~30% =
engine-state sidebar, exactly three rows: **WM facts** (real syntax), **rule fired** (+ salience),
**Δ** (retracted/declared this step, highlighted).

| Phys | Show | Say (abridged) |
|---|---|---|
| C1 | Tree grayed; `gen_01` lit. Sidebar: `Position(nid=gen_01)`, `Active(chart=general_assessment)`; `walk (sal 0)` | "Two facts in working memory. One generic rule matches them and renders this node *from the JSON* — the engine knows nothing about this chart." |
| C2 | `gen_01→gen_02` | "Answer = retract old `Position`, declare new one. RETE re-matches, `walk` fires again. *That is forward chaining* — Safety, then Scene." |
| C3 | `gen_02→gen_03→gen_04` (one build) | "Situation check — that was the Preliminary phase, SSS. Now the chart asks its most important question…" |
| **C4** | `gen_04` **"Life threatening bleeding?"** — two large hyperlink buttons YES / NO | **Audience choice.** "You arrive at a motorbike crash; blood is spreading fast on the asphalt. Show of hands — yes or no?" |
| C5y | `gen_05` jump; sidebar: `Active` flips to `hemorrhage`, `Position(nid=hem_01)` | "A `jump` node — the KB is 5 separate trees; the engine resolves the transfer. Note ABCDE never ran: circulation-first, as structure." |
| C6y | `hem_enter (sal 50)` fires; **`Bleeding(tier=1)` appears in WM** | "A NEW kind of fact. Not position — *state*. The escalation tier now lives in working memory." |
| C7y | Tier 1 applied (direct pressure), recheck → still bleeding; Δ: `retract Bleeding(1)`, `declare Bleeding(2)` | "The rule reasons over tier + answer: escalate. It never re-asks tier 1 — the fact remembers." |
| C8y | Tier 2 → still bleeding → **tier 3 tourniquet**; note the flagged divergence (chart draws an infinite re-apply loop; we cap at terminal) | "Highest tier. If still bleeding now: HOLD — no tier 4, urgent transport. The engine refuses to spin." |
| C9y | Controlled → `hem_07` leaf; leaf banner | "Leaf reached. Every step was one generic rule + facts — zero chart-specific code." |
| C10 | "The road not taken": no-branch as one compressed strip (`gen_06` ABCDE → stable/unstable → secondary → continuous) | 10-second flyover so the audience sees their unchosen branch existed for real. |

**The rehearsed click:** C4 has two on-slide hyperlink buttons (YES → C5y, NO → C5n strip) —
in the HTML deck these are plain internal anchor links, rehearsal-proof.
Ordering trick: C5y…C9y sit immediately after C4, so plain "next" = YES branch; a real
hyperlink click is needed only if the room votes NO (NO button → C5n strip → link back to C10).
Rehearse both; steer narration toward YES. Timing: C1–C3 ≈ 35s · C4 ≈ 20s · branch ≈ 50s ·
C10 ≈ 15s ⇒ ~2:00.

**Accuracy rule:** sidebar contents are generated from a real engine session
(`LANG="en"`, scripted input — transcripts in `presentation/traces/`), never hand-invented.

---

## 6. Decisions (answered) + remaining open items

**Decided (2026-07-02):**
1. **Time limit: 15 min** — deck stays sized to 14:30 with the cut/stretch levers in §1b.
2. **English slides + Arabic narration** — LTR deck, Noto Sans primary; no RTL build needed. Clinical terms stay in the charts' own English vocabulary (matches the source PDFs the professors know).
3. **Report in English.**
4. **Demo = external** — slide 15 is a styled interstitial only; the presenter Alt-Tabs to a video or a live terminal/app demo (nothing embedded). Traces + suggested 90s script ready in `presentation/traces/`.
5. **Supervisor: "Miss Omama" — no title, no surname on slides or report.**
6. **Slide tool: single-file HTML deck** (chosen as "best for our case"): exact brand tokens + Noto fonts, C4 audience-branch = plain internal anchor links, native `<video>` embed for the demo slide, presents full-screen in any browser, versionable in this repo. The approved theme test slide (`presentation/theme_test_slide.html`) is already built in this exact medium — the deck inherits it 1:1.
7. **Report is delivered with the project to a review committee later** (not presented) ⇒ **slides are generated first**; the report is written standalone — it must not assume the reader saw the talk, and its conclusion/acknowledgments are formal committee-facing prose.

**Still open (user will edit later, not blockers):**
- Team member nicknames/initials stay in BOTH deck and report; the user swaps in full names later.
- Whether the demo will be a video or live (slide 15 interstitial works either way).

---

## E. Visual identity — theme test slide

One test slide, light theme, subject = **physical slide C7y** (exercises every palette role:
background, heading, body, accent, danger/safe pair, sidebar code text). Body ≥18pt; any
identity color that fails on white gets a flagged adjusted variant.

**Identity tokens** (from the app's `ds/tokens/*.css`, byte-identical to this repo's design bundle):
- **Palette:** primary `#CC0000` (dark `#990000`, light `#FF3333`, tint `#FFEAEA`) · success `#2D6A4F` (tint `#F0FAF5`) · warning `#E85D04` (tint `#FFF3EB`) · text `#1A1A1A` / `#4A4A4A` · border `#E0E0E0` · surface `#F5F5F5` · card/page `#FFFFFF`. Single light theme.
- **Trace-slide semantics:** danger/still-bleeding = `#CC0000`; safe/controlled = `#2D6A4F`; current node = `#FFEAEA` + `#CC0000` border (or filled); visited = `#4A4A4A`; unvisited = `#E0E0E0`.
- **Type:** Noto Sans + Noto Sans Arabic (metrics-matched), weights 400/600/700 only; deck defines larger sizes, keeps family/weights; body ≥18pt.
- **Shape:** 8dp grid; radius 6/8/12; flat, subtle shadows, **no gradients, no decorative imagery**.
- **Logo:** none — "ResQRules" wordmark white-on-`#CC0000`; **never draw a red cross/crescent emblem**.
- **Projector flags:** `#E85D04` on white ≈ 3.5:1 → badges/large type only, darkened text variant ~`#B54A00`; 100-tints wash out → always pair with border/label; `#CC0000` on white ≈ 5.9:1 → headings/accents OK; body stays `#1A1A1A`.

---

## Execution checklist

1. ✅ This plan in repo.
2. ✅ Real engine traces captured (`LANG="en"`) → `presentation/traces/` — yes-branch, no-branch, `b`-override (sal 100 line), CF-unsure (doubt line + graceful jump stub). Accuracy source for C1–C10, slide 11, and the demo video.
3. ✅ Theme test slide built → `presentation/theme_test_slide.html` (open in a browser; annotations below the canvas). **User approval gates the full deck.**
4. Full HTML deck first (per decision 7), then the standalone committee report.
5. Demo video (optional): record terminal session per `presentation/traces/override_bleeding_en.txt` + 30s app closer; drop into slide 15's video slot. If recording on a phone screen, replace the stock Flutter launcher icon first.
6. Rehearse to 14:30; dry-run the C4 anchor click both ways; test-project the theme slide (or view from 2–3 m).
