#!/usr/bin/env python3
"""ResQRules engine — generic walker + primary-survey OVERRIDE + hemorrhage ESCALATION loop.

Layers, by salience:
  100/90/80  primary-survey OVERRIDES  — danger observations preempt + jump to a protocol.
  50         hem_enter                 — entering hemorrhage starts the semantic tier loop.
  10         hem_apply / hem_decide    — the hemorrhage escalation loop (this build).
  0          walk (baseline)           — generic data-driven chart walker.

HEMORRHAGE ESCALATION (this build) — a SEMANTIC rule, not a drawn edge. The escalation TIER is
a fact `Bleeding(tier=N)` that ACCUMULATES in working memory: each "still bleeding -> yes"
advances N -> N+1 and applies the next intervention; the rule reasons over (current tier +
a re-asserted StillBleeding fact). Tier strictly increases; the tourniquet tier is terminal
(holds, routes to urgent transport — no tier 4, no spin); "controlled" exits to the post-control
path. The baseline walker carries NOT(Bleeding()) so it cedes control while the loop runs and
resumes for the exit/transport leaf. Interventions/recheck text are READ from hemorrhage.json.

NOT in this build: certainty factors, return-stack.
"""
import glob
import json
import os
import sys

from experta import KnowledgeEngine, Rule, Fact, Field, MATCH, AS, TEST, NOT

DANGERS = {"b": "catastrophic_bleeding", "n": "not_breathing",
           "p": "no_pulse", "u": "unconscious"}
SAL = {"catastrophic_bleeding": 100, "not_breathing": 90, "no_pulse": 90, "unconscious": 80}

# Hemorrhage escalation tiers, mapped onto hemorrhage.json's existing nodes (read, not reinvented).
HEM_TIERS = {
    1: {"apply": "hem_01", "recheck": "hem_02"},   # direct pressure / compression / hemostatic dressing
    2: {"apply": "hem_03", "recheck": "hem_04"},   # second compression bandage
    3: {"apply": "hem_05", "recheck": "hem_06"},   # tourniquet (TERMINAL)
}
HEM_TERMINAL = 3
HEM_POST_CONTROL = "hem_08"   # controlled by pressure/dressing (tiers 1-2) -> transport
HEM_URGENT = "hem_07"         # tourniquet outcomes (tier 3) -> urgent transport


class Position(Fact):
    nid = Field(str, mandatory=True)


class Active(Fact):           # GUARD: protocol we are in
    chart = Field(str, mandatory=True)


class Danger(Fact):           # transient paramedic observation
    kind = Field(str, mandatory=True)


class Bleeding(Fact):         # ESCALATION TIER — accumulates across loop passes
    tier = Field(int, mandatory=True)


class StillBleeding(Fact):    # transient recheck answer ("yes"/"no")
    answer = Field(str, mandatory=True)


class SignOfLife(Fact):       # CERTAINTY FACTOR: graded confidence there IS a sign of life
    cf = Field(float, mandatory=True)


class ResQRules(KnowledgeEngine):
    FIRED = []     # override firing log (test_overrides.py)
    TIERS = []     # escalation tiers applied, in order (test proof of strict increase)
    OUTCOME = None # exit node id of the escalation loop
    CF_ROUTE = None  # ("ventilation"|"cpr", next_node, cf) — CF routing log (tests)

    def __init__(self, nodes, node_chart, loaded):
        super().__init__()
        self.nodes = nodes
        self.node_chart = node_chart
        self.loaded = loaded
        self.cur_nid = None
        self.cur_chart = None

    # ---- working-memory transitions ----
    def start(self, entry):
        ch = self.node_chart[entry]
        self.declare(Position(nid=entry))
        self.declare(Active(chart=ch))
        self.cur_nid, self.cur_chart = entry, ch

    def _facts_of(self, cls):
        return [self.facts[i] for i in list(self.facts) if isinstance(self.facts[i], cls)]

    def _clear_loop_state(self):
        for f in self._facts_of(Bleeding) + self._facts_of(StillBleeding):
            self.retract(f)

    def _move(self, p, a, nid):
        self.retract(p)
        self.declare(Position(nid=nid))
        ch = self.node_chart[nid]
        if a["chart"] != ch:
            self.retract(a)
            self.declare(Active(chart=ch))
            self._clear_loop_state()       # leaving a protocol clears its loop facts
        self.cur_nid, self.cur_chart = nid, ch

    def _halt(self, p):
        self.retract(p)
        self.cur_nid = None

    # ---- input ----
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

    def _recheck_prompt(self, rnode, rnid, n):
        print(f"   [{rnid}] {rnode['text']}  (recheck after tier {n})")
        print("   1) yes — still bleeding")
        print("   2) no  — bleeding controlled")
        print("   -- DANGER (type letter): [b]leeding  [n]ot-breathing  no-[p]ulse  [u]nconscious")
        while True:
            r = input("   > ").strip().lower()
            if r == "b":                       # already on the bleeding protocol
                print("   (already managing catastrophic bleeding — continuing escalation)")
                continue
            if r in ("n", "p", "u"):
                return ("danger", DANGERS[r])
            if r == "1":
                return ("still", "yes")
            if r == "2":
                return ("still", "no")
            print("   (enter 1, 2, or danger letter n/p/u)")

    def _cf_prompt(self, node):
        cfg = node["cf"]
        keys = list(cfg["scale"].keys())
        print(f"   ?? {cfg['prompt']}")
        for i, k in enumerate(keys, 1):
            print(f"   {i}) {k}  (CF {cfg['scale'][k]:+.2f})")
        print("   -- DANGER (type letter): [b]leeding  [n]ot-breathing  no-[p]ulse  [u]nconscious")
        while True:
            r = input("   > ").strip().lower()
            if r in DANGERS:
                return ("danger", DANGERS[r])
            if r.isdigit() and 1 <= int(r) <= len(keys):
                return ("cf", float(cfg["scale"][keys[int(r) - 1]]))
            print("   (enter a listed number, or a danger letter b/n/p/u)")

    # ---- BASELINE walker: lowest salience; suppressed while a Bleeding tier is active ----
    @Rule(AS.p << Position(nid=MATCH.nid), AS.a << Active(chart=MATCH.c),
          NOT(Bleeding()), salience=0)
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
        if t == "question" and "cf" in node:          # CERTAINTY-FACTOR decision node
            kind, payload = self._cf_prompt(node)
            if kind == "danger":
                self.declare(Danger(kind=payload))     # override still hard-jumps (binary)
            else:
                self.declare(SignOfLife(cf=payload))   # leave Position; the CF rule thresholds it
            return
        kind, payload = self._prompt(node)
        if kind == "danger":
            self.declare(Danger(kind=payload))
        else:
            self._move(p, a, payload)

    # ---- OVERRIDES: high salience = clinical precedence ----
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
        if active == chart:
            print(f"   !! DANGER [{kind}] (sal {SAL[kind]}): already in '{chart}' — staying, no re-entry")
            self._move(p, a, pn)
        else:
            print(f"   !! DANGER [{kind}] (sal {SAL[kind]}): OVERRIDE -> preempt, jump to '{chart}' entry")
            self._move(p, a, entry)

    # ---- HEMORRHAGE ESCALATION LOOP (semantic; tier accumulates in working memory) ----
    @Rule(Position(nid="hem_01"), Active(chart="hemorrhage"), NOT(Bleeding()), salience=50)
    def hem_enter(self):
        print("   >> entering hemorrhage escalation (semantic tier loop) <<")
        self.declare(Bleeding(tier=1))

    @Rule(AS.b << Bleeding(tier=MATCH.n), NOT(StillBleeding()),
          AS.p << Position(nid=MATCH.pn), AS.a << Active(chart=MATCH.c), salience=10)
    def hem_apply(self, b, p, a, n, pn, c):
        cfg = HEM_TIERS[n]
        inode = self.nodes[cfg["apply"]]
        ResQRules.TIERS.append(n)
        print(f"\n   >> ESCALATION TIER {n}: {inode['text']}  (p.{inode['page']})")
        self._move(p, a, cfg["recheck"])                      # keep a Position so overrides still work
        res = self._recheck_prompt(self.nodes[cfg["recheck"]], cfg["recheck"], n)
        if res[0] == "danger":
            self.declare(Danger(kind=res[1]))                 # override jumps out; _move clears loop state
        else:
            self.declare(StillBleeding(answer=res[1]))

    @Rule(AS.b << Bleeding(tier=MATCH.n), AS.s << StillBleeding(answer=MATCH.ans),
          AS.p << Position(nid=MATCH.pn), AS.a << Active(chart=MATCH.c), salience=10)
    def hem_decide(self, b, s, p, a, n, ans, pn, c):
        self.retract(s)
        if ans == "yes":
            if n < HEM_TERMINAL:
                self.retract(b)
                self.declare(Bleeding(tier=n + 1))            # ACCUMULATE: tier N -> N+1
                print(f"   >> still bleeding -> ADVANCE tier {n} -> {n + 1}")
            else:
                self.retract(b)
                print(f"   >> still bleeding at TERMINAL tier {n} (tourniquet): HOLD, no tier {n + 1} -> urgent transport")
                ResQRules.OUTCOME = HEM_URGENT
                self._move(p, a, HEM_URGENT)
        else:
            self.retract(b)
            out = HEM_POST_CONTROL if n < HEM_TERMINAL else HEM_URGENT
            print(f"   >> bleeding controlled at tier {n} -> exit to {out}")
            ResQRules.OUTCOME = out
            self._move(p, a, out)

    # ---- CERTAINTY FACTOR: threshold an ambiguous sign-of-life assessment ----
    @Rule(AS.s << SignOfLife(cf=MATCH.cf),
          AS.p << Position(nid=MATCH.pn), AS.a << Active(chart=MATCH.c), salience=20)
    def cf_sign_of_life(self, s, p, a, cf, pn, c):
        cfg = self.nodes[pn]["cf"]
        t = cfg["threshold"]
        self.retract(s)
        if cf >= t:                                       # confident there IS a sign of life
            print(f"   ~ CF {cf:+.2f} >= {t:+.2f}: confident sign of life -> ventilation branch")
            ResQRules.CF_ROUTE = ("ventilation", cfg["confident_next"], cf)
            self._move(p, a, cfg["confident_next"])
        else:                                             # doubt / low confidence
            print(f"   ~ CF {cf:+.2f} <  {t:+.2f}: doubt -> CPR branch (if in doubt, compress)")
            ResQRules.CF_ROUTE = ("cpr", cfg["doubt_next"], cf)
            self._move(p, a, cfg["doubt_next"])


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
    ResQRules.FIRED, ResQRules.TIERS, ResQRules.OUTCOME, ResQRules.CF_ROUTE = [], [], None, None
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
