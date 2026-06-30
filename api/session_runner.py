from __future__ import annotations

import glob
import json
import os
import sys
import threading
from queue import Queue, Empty
from typing import Optional

# Ensure project root is importable regardless of how uvicorn is launched
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from engine import (
    ResQRules, load_all,
    DANGERS, SAL, HEM_TIERS, HEM_TERMINAL,
)
from api.models import (
    ScreenState, BilingualText, OptionItem,
    CFChoice, CFConfig, HemTierInfo,
    DangerPanelItem, OverrideEvent,
)

# ─── knowledge base: loaded once at import time ───────────────────────────────

_DATA_DIR = os.path.join(_ROOT, "data")

NODES, NODE_CHART, LOADED = load_all(_DATA_DIR)

CHARTS_META: dict[str, dict] = {}
CHART_ENTRY: dict[str, str] = {}

for _f in sorted(glob.glob(os.path.join(_DATA_DIR, "*.json"))):
    _c = json.load(open(_f))
    _cid = _c["meta"]["chart_id"]
    CHARTS_META[_cid] = _c["meta"]
    CHART_ENTRY[_cid] = _c["entry"]

CHART_URGENCY: dict[str, str] = {
    "hemorrhage":         "critical",
    "cpr_adult":          "critical",
    "choking":            "critical",
    "airway":             "high",
    "general_assessment": "standard",
}

DANGER_PANEL: list[DangerPanelItem] = [
    DangerPanelItem(key="b", label=BilingualText(en="Catastrophic Bleeding", ar="نزيف كارثي"),  severity="critical"),
    DangerPanelItem(key="n", label=BilingualText(en="Not Breathing",         ar="لا يتنفس"),   severity="critical"),
    DangerPanelItem(key="p", label=BilingualText(en="No Pulse",              ar="لا نبض"),     severity="critical"),
    DangerPanelItem(key="u", label=BilingualText(en="Unconscious",           ar="فاقد الوعي"), severity="high"),
]

_CF_EN = {"certain": "Certain", "likely": "Likely", "unsure": "Unsure", "none": "None"}
_CF_AR = {"certain": "متأكد",   "likely": "محتمل",  "unsure": "غير متأكد", "none": "لا شيء"}

SESSIONS: dict[str, SessionRunner] = {}


# ─── I/O adapter (subclass — engine.py is never touched) ─────────────────────

class ResQAPIAdapter(ResQRules):
    """Subclass of ResQRules: replaces terminal I/O with queue-based exchange."""

    def __init__(self, nodes, node_chart, loaded, iq: Queue, oq: Queue):
        super().__init__(nodes, node_chart, loaded)
        self._iq = iq
        self._oq = oq

    # ── internal builders ─────────────────────────────────────────────────────

    def _bil(self, node: dict) -> BilingualText:
        return BilingualText(en=node.get("text_en", ""), ar=node.get("text_ar", ""))

    def _chart_title(self, chart_id: str) -> BilingualText:
        m = CHARTS_META.get(chart_id, {})
        return BilingualText(en=m.get("title_en", chart_id), ar=m.get("title_ar", ""))

    def _base(self, nid: str, node: dict) -> dict:
        cid = self.node_chart.get(nid, "")
        return dict(
            node_id=nid,
            chart_id=cid,
            chart_title=self._chart_title(cid),
            page=node.get("page", 0),
            text=self._bil(node),
        )

    def _emit(self, s: ScreenState) -> None:
        self._oq.put(s)

    def _recv(self) -> str:
        return self._iq.get()

    # ── I/O overrides ─────────────────────────────────────────────────────────

    def _prompt(self, node) -> tuple:
        nid = self.cur_nid
        base = self._base(nid, node)
        if node["type"] == "question":
            options = [
                OptionItem(id=i + 1, label=BilingualText(
                    en=o.get("answer_en", ""), ar=o.get("answer_ar", "")))
                for i, o in enumerate(node["options"])
            ]
            nexts = [o["next"] for o in node["options"]]
            self._emit(ScreenState(type="question", options=options, **base))
        else:
            options = [OptionItem(id=1, label=BilingualText(en="Continue", ar="متابعة"))]
            nexts = [node["next"]]
            self._emit(ScreenState(type="instruction", options=options, **base))

        raw = self._recv()
        if raw in DANGERS:
            return ("danger", DANGERS[raw])
        if raw.isdigit() and 1 <= int(raw) <= len(nexts):
            return ("advance", nexts[int(raw) - 1])
        return ("advance", nexts[0])  # fallback: first option

    def _recheck_prompt(self, rnode, rnid, n) -> tuple:
        apply_nid = HEM_TIERS[n]["apply"]
        hem = HemTierInfo(
            current=n,
            max_tier=HEM_TERMINAL,
            terminal=(n == HEM_TERMINAL),
            intervention=self._bil(self.nodes[apply_nid]),
        )
        options = [
            OptionItem(id=1, label=BilingualText(en="yes — still bleeding",    ar="نعم — النزيف مستمر")),
            OptionItem(id=2, label=BilingualText(en="no — bleeding controlled", ar="لا — النزيف متوقف")),
        ]
        self._emit(ScreenState(
            type="hem_question",
            options=options,
            hem_tier=hem,
            **self._base(rnid, rnode),
        ))
        raw = self._recv()
        if raw in DANGERS:  # include "b": bleeding on a hem screen = guard, not "no, controlled"
            return ("danger", DANGERS[raw])
        if raw == "1":
            return ("still", "yes")
        return ("still", "no")

    def _cf_prompt(self, node) -> tuple:
        nid = self.cur_nid
        cfg = node["cf"]
        keys = list(cfg["scale"].keys())
        choices = [
            CFChoice(
                id=i + 1, key=k,
                label=BilingualText(en=_CF_EN.get(k, k), ar=_CF_AR.get(k, k)),
                cf_value=cfg["scale"][k],
            )
            for i, k in enumerate(keys)
        ]
        cf_cfg = CFConfig(
            prompt=BilingualText(en=cfg.get("prompt_en", ""), ar=cfg.get("prompt_ar", "")),
            choices=choices,
            threshold=cfg["threshold"],
        )
        self._emit(ScreenState(type="cf_question", cf=cf_cfg, **self._base(nid, node)))
        raw = self._recv()
        if raw in DANGERS:
            return ("danger", DANGERS[raw])
        if raw.isdigit() and 1 <= int(raw) <= len(keys):
            return ("cf", float(cfg["scale"][keys[int(raw) - 1]]))
        return ("cf", float(cfg["scale"]["none"]))  # doubt → CPR

    def _halt(self, p):
        """Capture terminal screen before Position is retracted."""
        nid = self.cur_nid  # must read BEFORE super() sets it to None
        if nid and nid in self.nodes:
            node = self.nodes[nid]
            t = node.get("type")
            base = self._base(nid, node)
            if t == "action":
                self._emit(ScreenState(type="action", is_terminal=True, **base))
            elif t == "jump":
                self._emit(ScreenState(
                    type="jump_stub",
                    stub_target=node.get("target_chart"),
                    is_terminal=True,
                    **base,
                ))
        super()._halt(p)


# ─── session runner ───────────────────────────────────────────────────────────

class SessionRunner:
    def __init__(self, session_id: str, chart_id: str):
        if chart_id not in CHART_ENTRY:
            raise ValueError(f"Unknown chart_id: {chart_id!r}")
        self.session_id = session_id
        self.chart_id = chart_id
        self.alive = True
        self.current_screen: Optional[ScreenState] = None
        self._iq: Queue = Queue()
        self._oq: Queue = Queue()
        self._adapter, self._thread = self._boot(CHART_ENTRY[chart_id])
        self.current_screen = self._oq.get(timeout=15)

    # ── internals ─────────────────────────────────────────────────────────────

    def _boot(self, entry: str) -> tuple[ResQAPIAdapter, threading.Thread]:
        # Reset class-level diagnostics for this session
        ResQRules.FIRED    = []
        ResQRules.TIERS    = []
        ResQRules.OUTCOME  = None
        ResQRules.CF_ROUTE = None

        adapter = ResQAPIAdapter(NODES, NODE_CHART, LOADED, self._iq, self._oq)
        adapter.reset()

        runner_ref = self

        def _run():
            try:
                adapter.start(entry)
                adapter.run()
            except Exception:
                pass
            finally:
                runner_ref.alive = False

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        return adapter, t

    @staticmethod
    def _target_chart(kind: str) -> str:
        return "hemorrhage" if kind == "catastrophic_bleeding" else "cpr_adult"

    # ── public interface ──────────────────────────────────────────────────────

    def submit(self, raw: str) -> tuple[ScreenState, Optional[OverrideEvent]]:
        """Submit an answer; block until the engine produces the next screen."""
        fired_before = len(ResQRules.FIRED)
        chart_before = self._adapter.cur_chart
        self._iq.put(raw)
        try:
            screen = self._oq.get(timeout=15)
        except Empty:
            self.alive = False
            raise RuntimeError("Engine did not respond — session ended unexpectedly")
        self.current_screen = screen
        if not self._thread.is_alive():
            self.alive = False

        override: Optional[OverrideEvent] = None
        if len(ResQRules.FIRED) > fired_before:
            kind  = ResQRules.FIRED[fired_before]
            tgt   = self._target_chart(kind)
            guard = (chart_before == tgt)
            override = OverrideEvent(
                kind=kind,
                salience=SAL.get(kind, 0),
                jumped_to_chart=None if guard else tgt,
                guard_fired=guard,
            )
        return screen, override

    def reset(self, chart_id: Optional[str] = None) -> ScreenState:
        """Restart session on same or new chart; session_id stays the same."""
        self.alive = False
        new_chart = chart_id or self.chart_id
        if new_chart not in CHART_ENTRY:
            raise ValueError(f"Unknown chart_id: {new_chart!r}")
        self.chart_id = new_chart
        self._iq = Queue()
        self._oq = Queue()
        self._adapter, self._thread = self._boot(CHART_ENTRY[new_chart])
        self.alive = True
        self.current_screen = self._oq.get(timeout=15)
        return self.current_screen

    def stop(self) -> None:
        self.alive = False
