# Knowledge tree schema (every `data/*.json` conforms to this)

One JSON file per chart. The engine treats this file as *knowledge* — it never hard-codes
chart logic.

```jsonc
{
  "meta": {
    "chart_id": "choking",            // stable id, also the JSON filename stem
    "title_en": "Heimlich Maneuver",  // English title — source-of-truth anchor
    "title_ar": "مناورة هايملك",      // Arabic parallel (OPTIONAL; falls back to title_en)
    "source": "SARC SOP",
    "source_pages": [7],              // chart number / page(s) in the master 12-chart deck
    "notes": ["..."]                  // OPTIONAL: chart-level footnotes that aren't a flow box
  },
  "entry": "<node_id>",               // id of the first node to walk (language-independent)
  "nodes": {
    "<node_id>": {
      "type": "question | instruction | action | jump",
      "text_en": "faithful text transcribed from the chart",   // REQUIRED — source-of-truth
      "text_ar": "النص بالعربية",                              // OPTIONAL parallel; engine falls back to text_en + [en] flag
      "page": 7,                      // source page for THIS node (required)
      "provenance": "source",         // REQUIRED: source | derived | added (audit trail, language-independent)

      // type == "question" only:
      "options": [ { "answer_en": "yes", "answer_ar": "نعم",  // answer_en REQUIRED; answer_ar OPTIONAL
                     "next": "<node_id>",                       // node ids are language-independent
                     "provenance": "derived" }, ... ],          // OPTIONAL per-edge provenance override

      // type == "instruction" only:
      "next": "<node_id>",

      // type == "jump" only:
      "target_chart": "cpr_adult",    // language-independent
      "target_node": "entry",         // language-independent

      // type == "action": no "next"/"options" (it is a leaf)

      // CF block (question nodes with graded confidence only — see cpr_11):
      "cf": {
        "prompt_en": "English CF question",  // REQUIRED if cf present
        "prompt_ar": "سؤال CF بالعربية",     // OPTIONAL parallel; falls back to prompt_en + [en]
        "scale": { "certain": 1.0, "likely": 0.6, "unsure": 0.2, "none": -1.0 },  // keys are programmatic (always English)
        "threshold": 0.5,
        "confident_next": "<node_id>",
        "doubt_next": "<node_id>"
      }
    }
  }
}
```

## Language support (`LANG = "en" | "ar"`)

The engine reads a module-level `LANG` flag. All displayed text goes through helpers:
- `txt(node)` → `node[f"text_{LANG}"]`, falling back to `node["text_en"] + "  [en]"`.
- `ans(option)` → `option[f"answer_{LANG}"]`, same fallback.
- `cf_prompt_text(cfg)` → `cfg[f"prompt_{LANG}"]`, same fallback.
- `meta_title(meta)` → `meta[f"title_{LANG}"]`, same fallback.
- Engine UI strings (menus, trace lines, END messages) come from `UI[LANG]` dict.

**Language-independence guarantees:**
- Node ids, `next`, `target_chart`, `target_node`, `entry` — never translated; routing is language-free.
- `provenance` — structural audit field; language-free.
- `validate.py` checks `text_en` (required) and reports Arabic coverage separately; validation PASS/FAIL is language-independent.
- CF scale keys (`certain`/`likely`/`unsure`/`none`) are programmatic dict keys (always English); display labels come from `UI[LANG]["cf_labels"]`.

## Node types
| type | meaning | continuation |
|------|---------|--------------|
| `question`    | a decision diamond | `options[]`; each option `next` → a local node id |
| `instruction` | a do-this step that flows on | single `next` → a local node id |
| `action`      | a terminal leaf (stop) | none |
| `jump`        | one-way cross-tree / hub transfer | `target_chart` (+ `target_node`); resolved in another file |

## Provenance (faithfulness audit trail) — REQUIRED on every node
Every node carries `provenance`; an individual `option` may override it for one edge.
| value | meaning |
|-------|---------|
| `source`  | transcribed directly from a box/arrow drawn on the chart |
| `derived` | the literal meaning of a drawn box, but not itself a drawn box/arrow — e.g. a "repeat the cycles until…" loop-back edge |
| `added`   | tool-added for navigation only, NOT on the chart — e.g. a safe-exit so a one-armed decision diamond is walkable |

Rules:
- A `derived`/`added` node or option must never carry invented **clinical** content; it only
  encodes navigation/structure. Anything `added`/`derived` is also called out in the
  extraction report.
- When the *node* is a real box but one *edge* off it is derived/added, keep the node
  `source` and set `provenance` on that single `option`.

## SHALLOW charts
A chart may be modelled SHALLOW (e.g. #8 Upper Airway — a hub reference point). Capture the
top-level decisions and outbound jumps; consolidate deep sub-branches into a single
`instruction`/`action`, and note the consolidation in the report. Consolidated nodes stay
`source` (they transcribe real boxes, merged) — the merge is a modelling choice, not invented
content.

## Conventions
- **Node ids**: short chart prefix + number, e.g. `chk_01`, `chk_02` (avoids cross-chart
  collisions when hubs reference each other).
- **`action` = leaf.** A leaf must be `type: action`. A `jump` is *not* a leaf — it is a
  transfer to another chart, validated separately.
- **`jump` targets are external**: `target_chart` may name a chart that isn't loaded /
  isn't extracted yet. The engine prints `would transfer to <target_chart>` and stops
  (a graceful stub). Phase 2 wires a real return-stack.
- **Fan-out connectors → `question` nodes.** Where a chart represents a decision as a plain
  arrow that splits to several labelled boxes (no diamond drawn), model it as one `question`
  whose `options[].answer` are those box labels. This is faithful and keeps the tree clean.
- **Added / derived edges** (a safe-exit for a one-armed diamond; a "repeat until…" loop-back)
  are allowed only when needed to make the tree walkable, and MUST be flagged in the
  extraction report. They never carry invented *clinical* content.
- **`meta.notes`** (optional extension) preserves chart footnotes that are not themselves
  flow boxes (e.g. general technique reminders), so fidelity isn't lost.
- **`certainty`** is reserved for the Phase-3 certainty-factor layer; include it only where
  the chart itself implies uncertainty ("if unsure…"). Omit otherwise.
