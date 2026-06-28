# Knowledge tree schema (every `data/*.json` conforms to this)

One JSON file per chart. The engine treats this file as *knowledge* — it never hard-codes
chart logic.

```jsonc
{
  "meta": {
    "chart_id": "choking",            // stable id, also the JSON filename stem
    "title": "Heimlich Maneuver",     // chart title, transcribed
    "source": "SARC SOP",
    "source_pages": [7],              // chart number / page(s) in the master 12-chart deck
    "notes": ["..."]                  // OPTIONAL: chart-level footnotes that aren't a flow box
  },
  "entry": "<node_id>",               // id of the first node to walk
  "nodes": {
    "<node_id>": {
      "type": "question | instruction | action | jump",
      "text": "faithful text transcribed from the chart",
      "page": 7,                      // source page for THIS node (required)

      // type == "question" only:
      "options": [ { "answer": "yes", "next": "<node_id>" }, ... ],

      // type == "instruction" only:
      "next": "<node_id>",

      // type == "jump" only:
      "target_chart": "cpr_adult",
      "target_node": "entry",

      // type == "action": no "next"/"options" (it is a leaf)

      "certainty": 0.0                // OPTIONAL; only where the source implies "if unsure…"
    }
  }
}
```

## Node types
| type | meaning | continuation |
|------|---------|--------------|
| `question`    | a decision diamond | `options[]`; each option `next` → a local node id |
| `instruction` | a do-this step that flows on | single `next` → a local node id |
| `action`      | a terminal leaf (stop) | none |
| `jump`        | one-way cross-tree / hub transfer | `target_chart` (+ `target_node`); resolved in another file |

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
