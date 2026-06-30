# ResQRules API — Reference

Base URL (laptop): `http://localhost:8000`  
Base URL (device on same LAN): `http://<your-machine-ip>:8000`  
Future (cloud): set in `mobile/lib/config/api_config.dart`

All requests and responses are JSON. No authentication (additive in a future stage).

---

## Stability guarantee

The response contract is driven by **node `type` from the JSON knowledge files**, not by internal Experta rules, facts, or salience. This means:
- Adding / changing rules → zero API change
- Adding a new chart (`data/*.json`) → auto-discovered by `GET /charts`, no code change
- Adding auth later → middleware only, response shapes unchanged
- Adding DB later → storage only, response shapes unchanged

---

## Bilingual support

Every text field in every response is **bilingual** — both `en` and `ar` are always returned. The client picks which to display based on a local `lang` setting. No server round-trip is needed to switch languages.

```json
{ "en": "yes", "ar": "نعم" }
```

---

## Error shape

All **hand-raised** errors return a machine-readable body so the client can branch on a stable
`code` instead of string-matching the message:

```json
{ "detail": { "code": "session_ended", "message": "Session has ended — use POST /reset to restart" } }
```

| `code` | Status | Meaning | Client should |
|--------|--------|---------|---------------|
| `chart_not_found`    | 404 | unknown `chart_id` | fix the request |
| `session_not_found`  | 404 | unknown / expired `session_id` | start a new session |
| `session_ended`      | 410 | `alive=false` (terminal reached) | `POST /reset`, do not retry `/step` |
| `invalid_input`      | 422 | `input` not in `{1..4, b, n, p, u}` | ignore / re-prompt |
| `engine_unavailable` | 503 / 400 | engine failed to boot (create / reset) | retry, then surface the error Snackbar |
| `engine_timeout`     | 503 | engine did not respond to `/step` | retry via the error Snackbar |

> **Note:** FastAPI's *automatic* request-validation errors (malformed JSON, missing `input`
> field) use the framework default shape `{"detail": [ … ]}` (a list), **not** `{code, message}`.
> Only the hand-raised errors above carry a `code`. The client should treat any non-2xx without a
> `detail.code` as a generic "connection/validation error → retry".

---

## Endpoints

### `GET /charts`

List all available clinical protocol charts.

**Response 200**
```json
[
  {
    "chart_id": "choking",
    "title": { "en": "Heimlich Maneuver", "ar": "مناورة هايملك" },
    "urgency": "critical"
  },
  {
    "chart_id": "cpr_adult",
    "title": { "en": "Cardio-Respiratory Arrest Adult (signs of puberty are visible)", "ar": "السكتة القلبية التنفسية للبالغين (مع ظهور علامات البلوغ)" },
    "urgency": "critical"
  },
  {
    "chart_id": "hemorrhage",
    "title": { "en": "Catastrophic Hemorrhage", "ar": "النزيف الكارثي" },
    "urgency": "critical"
  },
  {
    "chart_id": "airway",
    "title": { "en": "Upper Airway Management", "ar": "إدارة الجهاز التنفسي العلوي" },
    "urgency": "high"
  },
  {
    "chart_id": "general_assessment",
    "title": { "en": "General Intervention Process & Patient Assessment", "ar": "عملية التدخل العامة وتقييم المريض" },
    "urgency": "standard"
  }
]
```

`urgency` values: `"critical"` | `"high"` | `"standard"`

---

### `POST /sessions`

Start a new clinical session on a chosen protocol chart. Returns the first screen.

**Request body**
```json
{ "chart_id": "choking" }
```

**Response 201**
```json
{
  "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "alive": true,
  "screen": { ... ScreenState ... },
  "override_event": null,
  "danger_panel": [
    { "key": "b", "label": { "en": "Catastrophic Bleeding", "ar": "نزيف كارثي" }, "severity": "critical" },
    { "key": "n", "label": { "en": "Not Breathing",         "ar": "لا يتنفس"  }, "severity": "critical" },
    { "key": "p", "label": { "en": "No Pulse",              "ar": "لا نبض"    }, "severity": "critical" },
    { "key": "u", "label": { "en": "Unconscious",           "ar": "فاقد الوعي"}, "severity": "high"     }
  ]
}
```

**Errors** (body is `{detail:{code,message}}` — see [Error shape](#error-shape))
| Status | `code` | Meaning |
|--------|--------|---------|
| 404 | `chart_not_found` | `chart_id` not found |
| 503 | `engine_unavailable` | Engine failed to start |

---

### `GET /sessions/{session_id}`

Fetch the current screen without advancing. Use to reconnect after app goes to background.

**Response 200** — same shape as `POST /sessions`

**Errors**
| Status | `code` | Meaning |
|--------|--------|---------|
| 404 | `session_not_found` | Session not found |

---

### `POST /sessions/{session_id}/step`

Submit a user answer and receive the next screen. Handles both option selections and danger-key activations.

**Request body**
```json
{ "input": "1" }
```

`input` values:
| Value | Meaning |
|-------|---------|
| `"1"` – `"4"` | Select numbered option (most screens have 2; CF screen has 4) |
| `"b"` | Catastrophic bleeding — override to hemorrhage protocol (salience 100) |
| `"n"` | Not breathing — override to CPR protocol (salience 90) |
| `"p"` | No pulse — override to CPR protocol (salience 90) |
| `"u"` | Unconscious — override to CPR protocol (salience 80) |

**Response 200** — same shape as `POST /sessions`

`override_event` will be non-null when a danger key caused a protocol jump (see [Override Events](#override-events)).

**Errors**
| Status | `code` | Meaning |
|--------|--------|---------|
| 404 | `session_not_found` | Session not found |
| 410 | `session_ended` | Session has ended (alive=false) — use POST /reset |
| 422 | `invalid_input` | Invalid input value (not in `{1..4, b, n, p, u}`) |
| 503 | `engine_timeout` | Engine timeout |

---

### `POST /sessions/{session_id}/reset`

Restart the session on the same or a different chart. The session_id is preserved.

**Request body**
```json
{ "chart_id": "cpr_adult" }
```

`chart_id` is optional. If omitted, resets to the same chart.

**Response 200** — first screen of the chosen chart

**Errors**
| Status | `code` | Meaning |
|--------|--------|---------|
| 404 | `session_not_found` / `chart_not_found` | Session or chart_id not found |
| 400 | `engine_unavailable` | Reset failed (bad chart_id or engine boot) |

---

### `DELETE /sessions/{session_id}`

End the session and free server resources.

**Response 200**
```json
{ "ok": true }
```

---

## ScreenState — the stable screen contract

Every response contains a `screen` object. The `type` field is the discriminator — the client renders a different UI component for each type.

### Common fields (always present on every screen type)

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Screen type — see values below |
| `node_id` | string | Knowledge graph node ID (e.g. `"chk_01"`) |
| `chart_id` | string | Protocol chart (e.g. `"choking"`) |
| `chart_title` | BilingualText | Chart name in EN + AR |
| `page` | int | Source page in the SARC SOP document |
| `text` | BilingualText | Main clinical text of this node |
| `is_terminal` | bool | True when session is over (action leaf or stub) |
| `options` | OptionItem[] or null | Selectable answers |
| `cf` | CFConfig or null | Certainty-factor config — only on `cf_question` screens |
| `hem_tier` | HemTierInfo or null | Hemorrhage tier info — only on `hem_question` screens |
| `stub_target` | string or null | Target chart name — only on `jump_stub` screens |

### `type` values

#### `"instruction"`
A do-this step. One option: `id=1`, label "Continue / متابعة".

```json
{
  "type": "instruction",
  "node_id": "cpr_01",
  "chart_id": "cpr_adult",
  "chart_title": { "en": "Cardio-Respiratory Arrest Adult (signs of puberty are visible)", "ar": "السكتة القلبية التنفسية للبالغين" },
  "page": 3,
  "text": {
    "en": "Patient evaluation: no sign of life. (Unresponsive; open the airway chin lift / jaw thrust; check-listen-feel max 10 sec...)",
    "ar": "تقييم المريض: لا توجد علامة حياة. (لا يستجيب؛ افتح مجرى الهواء...)"
  },
  "is_terminal": false,
  "options": [{ "id": 1, "label": { "en": "Continue", "ar": "متابعة" } }],
  "cf": null,
  "hem_tier": null,
  "stub_target": null
}
```

**Flutter renders:** Clinical text card + full-width red "Continue" button.

---

#### `"question"`
A decision diamond with 2–4 options.

```json
{
  "type": "question",
  "node_id": "chk_01",
  "chart_id": "choking",
  "chart_title": { "en": "Heimlich Maneuver", "ar": "مناورة هايملك" },
  "page": 7,
  "text": {
    "en": "Suspect foreign body obstruction?",
    "ar": "هل يُشتبه في انسداد جسم غريب؟"
  },
  "is_terminal": false,
  "options": [
    { "id": 1, "label": { "en": "yes", "ar": "نعم" } },
    { "id": 2, "label": { "en": "no",  "ar": "لا"  } }
  ],
  "cf": null,
  "hem_tier": null,
  "stub_target": null
}
```

**Flutter renders:** Question text card + N outlined option buttons (full-width, red border).

---

#### `"cf_question"`
A graded-confidence question (certainty factor). The user picks a confidence level; the engine thresholds it internally and routes to the appropriate branch.

```json
{
  "type": "cf_question",
  "node_id": "cpr_11",
  "chart_id": "cpr_adult",
  "chart_title": { "en": "Cardio-Respiratory Arrest Adult", "ar": "..." },
  "page": 3,
  "text": { "en": "[1] Sign of life?", "ar": "[1] علامة حياة؟" },
  "is_terminal": false,
  "options": [
    { "id": 1, "label": { "en": "Certain",    "ar": "متأكد"      } },
    { "id": 2, "label": { "en": "Likely",     "ar": "محتمل"      } },
    { "id": 3, "label": { "en": "Unsure",     "ar": "غير متأكد"  } },
    { "id": 4, "label": { "en": "None",       "ar": "لا شيء"     } }
  ],
  "cf": {
    "prompt": {
      "en": "Confidence the patient has a SIGN OF LIFE (breathing/pulse)? — gasping is NOT efficient breathing; do not rely on a doubtful pulse.",
      "ar": "ما مدى ثقتك بأن المريض لديه علامة حياة (تنفس/نبض)؟ — اللهث ليس تنفساً فعّالاً؛ لا تعتمد على نبض مشكوك فيه."
    },
    "choices": [
      { "id": 1, "key": "certain", "label": { "en": "Certain",   "ar": "متأكد"     }, "cf_value":  1.0 },
      { "id": 2, "key": "likely",  "label": { "en": "Likely",    "ar": "محتمل"     }, "cf_value":  0.6 },
      { "id": 3, "key": "unsure",  "label": { "en": "Unsure",    "ar": "غير متأكد" }, "cf_value":  0.2 },
      { "id": 4, "key": "none",    "label": { "en": "None",      "ar": "لا شيء"    }, "cf_value": -1.0 }
    ],
    "threshold": 0.5
  },
  "hem_tier": null,
  "stub_target": null
}
```

**Clinical note:** CF >= 0.5 → ventilation branch. CF < 0.5 → CPR branch. "Unsure" (CF=0.2) tips to CPR — conservative bias ("if in doubt, compress").

**Flutter renders:** Question text + CF prompt text + 4 colored confidence buttons (green/amber/red tinted by CF value).

---

#### `"hem_question"`
Hemorrhage escalation recheck. Shown after each tier intervention is applied. Carries the tier progress indicator and the text of the intervention just applied.

```json
{
  "type": "hem_question",
  "node_id": "hem_02",
  "chart_id": "hemorrhage",
  "chart_title": { "en": "Catastrophic Hemorrhage", "ar": "النزيف الكارثي" },
  "page": 10,
  "text": { "en": "Active bleeding?", "ar": "هل النزيف نشط؟" },
  "is_terminal": false,
  "options": [
    { "id": 1, "label": { "en": "yes — still bleeding",    "ar": "نعم — النزيف مستمر" } },
    { "id": 2, "label": { "en": "no — bleeding controlled", "ar": "لا — النزيف متوقف" } }
  ],
  "cf": null,
  "hem_tier": {
    "current": 1,
    "max_tier": 3,
    "terminal": false,
    "intervention": {
      "en": "Control of external bleeding: direct compression on the wound; compression dressing; if available, hemostatic compression dressing.",
      "ar": "السيطرة على النزيف الخارجي: ضغط مباشر على الجرح؛ ضمادة ضاغطة؛ إذا توفرت، ضمادة ضاغطة مرقئة للدم."
    }
  },
  "stub_target": null
}
```

`hem_tier` fields:
| Field | Type | Description |
|-------|------|-------------|
| `current` | int | Tier just applied (1, 2, or 3) |
| `max_tier` | int | Always 3 (tourniquet = terminal) |
| `terminal` | bool | True when current == 3 (tourniquet — cannot escalate further) |
| `intervention` | BilingualText | What was just applied at this tier |

Tier progression: 1 = direct pressure/compression, 2 = second compression bandage, 3 = tourniquet (terminal). If `still bleeding` at tier 3 → urgent transport. If `controlled` at any tier → normal transport.

**Flutter renders:** Intervention text callout + tier progress dots (3 steps) + 2 answer buttons.

---

#### `"action"`
Terminal leaf. The protocol is complete.

```json
{
  "type": "action",
  "node_id": "chk_03",
  "chart_id": "choking",
  "chart_title": { "en": "Heimlich Maneuver", "ar": "مناورة هايملك" },
  "page": 7,
  "text": { "en": "Encourage coughing. Continuous assessment.", "ar": "شجّع على السعال. التقييم المستمر." },
  "is_terminal": true,
  "options": null,
  "cf": null,
  "hem_tier": null,
  "stub_target": null
}
```

**Flutter renders:** Green-bordered card + "End / End Session" button that returns to home.

---

#### `"jump_stub"`
The protocol requires a transfer to a chart not currently loaded.

```json
{
  "type": "jump_stub",
  "node_id": "air_08",
  "chart_id": "airway",
  "chart_title": { "en": "Upper Airway Management", "ar": "إدارة الجهاز التنفسي العلوي" },
  "page": 8,
  "text": { "en": "Oxygen algorithm.", "ar": "خوارزمية الأكسجين." },
  "is_terminal": true,
  "options": null,
  "cf": null,
  "hem_tier": null,
  "stub_target": "oxygen"
}
```

`stub_target` is the chart_id that would be loaded in a future phase.

**Flutter renders:** Grey transfer card explaining the protocol would continue in a chart not yet available.

> **Note on transparent jumps:** When a jump target IS loaded (e.g. choking → CPR adult when patient goes unconscious), the engine follows the jump silently and the next screen is simply the first screen of the target chart. The client detects the protocol change by comparing `chart_id` between consecutive responses.
>
> **These option-driven jumps return `override_event: null` — they are silent (no toast).** Only a **danger-key** press (`b`/`n`/`p`/`u`) produces a non-null `override_event`. So the toast UI is driven exclusively by `override_event`; a chart switch with `override_event == null` should swap the body without announcing it.

---

## Override events

When a danger key (`b`, `n`, `p`, `u`) triggers a protocol jump, the response includes `override_event`:

```json
{
  "kind": "catastrophic_bleeding",
  "salience": 100,
  "jumped_to_chart": "hemorrhage",
  "guard_fired": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `kind` | string | Danger kind: `catastrophic_bleeding` / `not_breathing` / `no_pulse` / `unconscious` |
| `salience` | int | Clinical priority: bleeding=100, arrest=90, unconscious=80 |
| `jumped_to_chart` | string or null | Chart jumped to; null if `guard_fired=true` |
| `guard_fired` | bool | True = already in the target protocol; stayed put |

**Guard case** (e.g., pressing `n` while already in CPR):
```json
{
  "kind": "not_breathing",
  "salience": 90,
  "jumped_to_chart": null,
  "guard_fired": true
}
```

> **Danger keys work on every interactive screen — including `hem_question` rechecks.** Pressing
> `b` (catastrophic bleeding) while already in the hemorrhage protocol returns a **guard**
> (`guard_fired:true`, `jumped_to_chart:null`) and stays on the current recheck — it is no longer
> mis-read as "no — bleeding controlled".

Override salience hierarchy (highest wins):
| Danger key | Kind | Salience | Jumps to |
|------------|------|----------|----------|
| `b` | catastrophic_bleeding | 100 | hemorrhage |
| `n` | not_breathing | 90 | cpr_adult |
| `p` | no_pulse | 90 | cpr_adult |
| `u` | unconscious | 80 | cpr_adult |

---

## Type reference

### BilingualText
```json
{ "en": "string", "ar": "string" }
```

### OptionItem
```json
{ "id": 1, "label": { "en": "yes", "ar": "نعم" } }
```

### CFChoice
```json
{
  "id": 1,
  "key": "certain",
  "label": { "en": "Certain", "ar": "متأكد" },
  "cf_value": 1.0
}
```

### CFConfig
```json
{
  "prompt": { "en": "...", "ar": "..." },
  "choices": [ ... CFChoice[] ... ],
  "threshold": 0.5
}
```

### HemTierInfo
```json
{
  "current": 1,
  "max_tier": 3,
  "terminal": false,
  "intervention": { "en": "...", "ar": "..." }
}
```

### DangerPanelItem
```json
{
  "key": "b",
  "label": { "en": "Catastrophic Bleeding", "ar": "نزيف كارثي" },
  "severity": "critical"
}
```
`severity`: `"critical"` | `"high"`

### SessionResponse (full envelope)
```json
{
  "session_id": "uuid-v4",
  "alive": true,
  "screen": { ... ScreenState ... },
  "override_event": null,
  "danger_panel": [ ... DangerPanelItem[] ... ]
}
```

---

## Quick start (curl)

```bash
# 1. List charts
curl http://localhost:8000/charts

# 2. Start a choking session
curl -s -X POST http://localhost:8000/sessions \
  -H "Content-Type: application/json" \
  -d '{"chart_id":"choking"}'
# → copy session_id from the response

SID=<your-session-id>

# 3. Step through (answer "yes" to first question)
curl -s -X POST http://localhost:8000/sessions/$SID/step \
  -H "Content-Type: application/json" \
  -d '{"input":"1"}'

# 4. Trigger a danger override (catastrophic bleeding)
curl -s -X POST http://localhost:8000/sessions/$SID/step \
  -H "Content-Type: application/json" \
  -d '{"input":"b"}'
# → response.screen.type == "hem_question"
# → response.override_event.kind == "catastrophic_bleeding"

# 5. Reset to CPR chart
curl -s -X POST http://localhost:8000/sessions/$SID/reset \
  -H "Content-Type: application/json" \
  -d '{"chart_id":"cpr_adult"}'

# 6. End session
curl -X DELETE http://localhost:8000/sessions/$SID
```

---

## Starting the server

```bash
cd /path/to/AlgorithmsAdult
pip3 install fastapi "uvicorn[standard]" pydantic

# Development (auto-reload on code changes)
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Interactive docs (Swagger UI)
open http://localhost:8000/docs
```
