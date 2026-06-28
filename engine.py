#!/usr/bin/env python3
"""ResQRules engine — generic data-driven walker + primary-survey OVERRIDE layer.

BASELINE (low salience): ONE generic rule walks any chart JSON, forward-chaining on a
single `Position` fact (handles question / instruction / action / jump).

INFERENCE LAYER (this build): the user is a paramedic. At EVERY prompt they may, instead of
answering, assert one of a FIXED menu of DANGER OBSERVATIONS (b/n/p/u). A high-salience
override @Rule per danger PREEMPTS the current node and jumps to the correct protocol.
Salience encodes clinical precedence (see PLAN.md):
    catastrophic_bleeding 100  >  not_breathing/no_pulse 90  >  unconscious 80  >  walk 0.

GUARD: an `Active(chart=...)` fact tracks the current protocol; each override retracts the
Danger it handled (so it fires ONCE) and, if we are ALREADY in the target protocol, it does
NOT jump — it just re-prompts the current node (no re-entry, no loop).

NOT in this build: hemorrhage re-check loop, certainty factors, return-stack.
"""
import glob
import json
import os
import sys

from experta import KnowledgeEngine, Rule, Fact, Field, MATCH, AS, TEST

# danger letter (menu key) -> danger kind asserted as a fact
DANGERS = {"b": "catastrophic_bleeding", "n": "not_breathing",
           "p": "no_pulse", "u": "unconscious"}
# salience = clinical precedence (documented in PLAN.md)
SAL = {"catastrophic_bleeding": 100, "not_breathing": 90, "no_pulse": 90, "unconscious": 80}


class Position(Fact):
    """Where we are. Exactly one at a time."""
    nid = Field(str, mandatory=True)


class Active(Fact):
    """GUARD: the protocol/chart we are currently in. Exactly one at a time."""
    chart = Field(str, mandatory=True)


class Danger(Fact):
    """A paramedic danger observation; transient — retracted once an override handles it."""
    kind = Field(str, mandatory=True)


class ResQRules(KnowledgeEngine):
    FIRED = []  # class-level log of override firings (used by test_overrides.py)

    def __init__(self, nodes, node_chart, loaded):
        super().__init__()
        self.nodes = nodes
        self.node_chart = node_chart
        self.loaded = loaded
        self.cur_nid = None          # plain mirror of Position, for test introspection
        self.cur_chart = None

    # ---- working-memory transitions (keep exactly one Position + one Active) ----
    def start(self, entry):
        ch = self.node_chart[entry]
        self.declare(Position(nid=entry))
        self.declare(Active(chart=ch))
        self.cur_nid, self.cur_chart = entry, ch

    def _move(self, p, a, nid):
        self.retract(p)
        self.declare(Position(nid=nid))
        ch = self.node_chart[nid]
        if a["chart"] != ch:
            self.retract(a)
            self.declare(Active(chart=ch))
        self.cur_nid, self.cur_chart = nid, ch

    def _halt(self, p):
        self.retract(p)
        self.cur_nid = None

    # ---- input (the hybrid menu: normal choices + the fixed danger menu) ----
    def _prompt(self, node):
        if node["type"] == "question":
            normal = [(o["answer"], o["next"]) for o in node["options"]]
        else:
            normal = [("(continue)", node["next"])]
        for i, (lab, _) in enumerate(normal, 1):
            print(f"   {i}) {lab}")
        print("   -- DANGER (type letter): [b]leeding  [n]ot-breathing  no-[p]ulse  [u]nconscious")
        while True:
            r = input("   > ").strip().lower()
            if r in DANGERS:
                return ("danger", DANGERS[r])
            if r.isdigit() and 1 <= int(r) <= len(normal):
                return ("advance", normal[int(r) - 1][1])
            print("   (enter a listed number, or a danger letter b/n/p/u)")

    # ---- BASELINE walker: LOWEST salience ----
    @Rule(AS.p << Position(nid=MATCH.nid), AS.a << Active(chart=MATCH.c), salience=0)
    def walk(self, p, a, nid, c):
        node = self.nodes[nid]
        print(f"\n[{nid}] {node['text']}  (p.{node['page']})")
        t = node["type"]
        if t == "action":
            self._halt(p)
            print("=== END (action / leaf) ===")
            return
        if t == "jump":
            tc, tn = node["target_chart"], node.get("target_node", "entry")
            if tc in self.loaded:
                print(f"   >> JUMP to chart '{tc}' (node '{tn}') <<")
                self._move(p, a, tn)
            else:
                self._halt(p)
                print(f"   >> would transfer to chart '{tc}' (node '{tn}') — not loaded <<")
                print("=== END (jump stub) ===")
            return
        kind, payload = self._prompt(node)
        if kind == "danger":
            self.declare(Danger(kind=payload))     # leave Position; an override (high salience) handles it
        else:
            self._move(p, a, payload)

    # ---- OVERRIDES: HIGH salience = clinical precedence ----
    @Rule(AS.d << Danger(kind="catastrophic_bleeding"),
          AS.p << Position(nid=MATCH.pn), AS.a << Active(chart=MATCH.c), salience=100)
    def ov_bleeding(self, d, p, a, pn, c):
        self.retract(d)
        self._override(p, a, pn, c, "catastrophic_bleeding", "hemorrhage", "hem_01")

    @Rule(AS.d << Danger(kind=MATCH.k),
          AS.p << Position(nid=MATCH.pn), AS.a << Active(chart=MATCH.c),
          TEST(lambda k: k in ("not_breathing", "no_pulse")), salience=90)
    def ov_arrest(self, d, p, a, pn, c, k):
        self.retract(d)
        self._override(p, a, pn, c, k, "cpr_adult", "cpr_01")

    @Rule(AS.d << Danger(kind="unconscious"),
          AS.p << Position(nid=MATCH.pn), AS.a << Active(chart=MATCH.c), salience=80)
    def ov_unconscious(self, d, p, a, pn, c):
        self.retract(d)
        self._override(p, a, pn, c, "unconscious", "cpr_adult", "cpr_01")

    def _override(self, p, a, pn, active, kind, chart, entry):
        ResQRules.FIRED.append(kind)
        if active == chart:                        # GUARD: already in target protocol
            print(f"   !! DANGER [{kind}] (sal {SAL[kind]}): already in '{chart}' — staying, no re-entry")
            self._move(p, a, pn)                    # re-prompt current node; NO jump to entry
        else:
            print(f"   !! DANGER [{kind}] (sal {SAL[kind]}): OVERRIDE -> preempt, jump to '{chart}' entry")
            self._move(p, a, entry)


def load_all(data_dir="data"):
    nodes, node_chart, loaded = {}, {}, set()
    for f in glob.glob(os.path.join(data_dir, "*.json")):
        c = json.load(open(f))
        cid = c["meta"]["chart_id"]
        loaded.add(cid)
        for nid, nd in c["nodes"].items():
            nodes[nid] = nd
            node_chart[nid] = cid
    return nodes, node_chart, loaded


def main(path):
    chart = json.load(open(path))
    nodes, node_chart, loaded = load_all(os.path.dirname(path) or "data")
    print(f"=== {chart['meta']['title']}  ({chart['meta']['chart_id']}) ===")
    print(f"(loaded charts: {', '.join(sorted(loaded))})")
    e = ResQRules(nodes, node_chart, loaded)
    e.reset()
    e.start(chart["entry"])
    try:
        e.run()
    except (EOFError, KeyboardInterrupt):
        print("\n=== aborted (no more input) ===")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/choking.json")
