#!/usr/bin/env python3
"""Automated proofs for the inference layer.

  Override layer (3a):
    TEST 1  salience precedence: with two dangers at once, the highest-precedence override
            fires FIRST (catastrophic_bleeding before arrest).
    TEST 2  guard: asserting not_breathing while already in cpr_adult does NOT re-enter.

  Hemorrhage escalation loop (3b):
    TEST 3  tier strictly increases 1->2->3 then TERMINAL holds (no tier 4, no crash/spin).
    TEST 4  early exit: "controlled" at tiers 1, 2 (mid), and 3 each exit cleanly.
    TEST 5  override INTO hemorrhage then the loop runs (same as arriving by normal walk).

Run:  python3 test_overrides.py
"""
import builtins

from engine import ResQRules, Position, Active, Danger, Bleeding, StillBleeding, load_all

NODES, NODE_CHART, LOADED = load_all("data")


def fresh():
    ResQRules.FIRED, ResQRules.TIERS, ResQRules.OUTCOME = [], [], None
    e = ResQRules(NODES, NODE_CHART, LOADED)
    e.reset()
    return e


def drive(e, answers):
    """Run the engine, feeding `answers` to each input(); exhaustion ends the run cleanly."""
    it = iter(answers)

    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError
    old, builtins.input = builtins.input, fake_input
    try:
        e.run()
    except EOFError:
        pass
    finally:
        builtins.input = old


# ---- TEST 1: salience = clinical precedence ----
e = fresh()
e.start("gen_04")
e.declare(Danger(kind="not_breathing"))
e.declare(Danger(kind="catastrophic_bleeding"))
drive(e, [])
print("TEST 1 firing order:", ResQRules.FIRED)
assert ResQRules.FIRED == ["catastrophic_bleeding", "not_breathing"], ResQRules.FIRED
print("  PASS: catastrophic_bleeding (sal 100) preempts arrest (sal 90)\n")

# ---- TEST 2: override guard — no re-entry, fires once ----
e = fresh()
e.start("cpr_05")
e.declare(Danger(kind="not_breathing"))
drive(e, [])
print("TEST 2 after guard: pos", e.cur_nid, "active", e.cur_chart, "fired", ResQRules.FIRED)
assert e.cur_nid == "cpr_05" and e.cur_chart == "cpr_adult"
assert ResQRules.FIRED == ["not_breathing"]
print("  PASS: stayed at cpr_05, no re-entry, fired once\n")

# ---- TEST 3: tier strictly increases, terminal holds ----
e = fresh()
e.start("hem_01")
drive(e, ["1", "1", "1"])                      # still bleeding x3
print("TEST 3 tiers:", ResQRules.TIERS, "outcome:", ResQRules.OUTCOME)
assert ResQRules.TIERS == [1, 2, 3], "tier must strictly increase, each applied once"
assert all(b < a for b, a in zip(ResQRules.TIERS, ResQRules.TIERS[1:])), "strictly increasing"
assert 4 not in ResQRules.TIERS, "no escalation past the terminal tourniquet tier"
assert ResQRules.OUTCOME == "hem_07", "terminal -> urgent transport"
print("  PASS: 1->2->3 strictly increasing, terminal held at 3, routed to hem_07\n")

# ---- TEST 4: early exits at each tier ----
for answers, exp_tiers, exp_out, label in [
    (["2"],            [1],       "hem_08", "tier 1"),
    (["1", "2"],       [1, 2],    "hem_08", "tier 2 (mid)"),
    (["1", "1", "2"],  [1, 2, 3], "hem_07", "tier 3"),
]:
    e = fresh()
    e.start("hem_01")
    drive(e, answers)
    print(f"TEST 4 [{label}] tiers {ResQRules.TIERS} -> {ResQRules.OUTCOME}")
    assert ResQRules.TIERS == exp_tiers and ResQRules.OUTCOME == exp_out
print("  PASS: controlled at tier 1/2/3 each exits cleanly (mid-tier proven)\n")

# ---- TEST 5: override INTO hemorrhage, then the loop runs ----
e = fresh()
e.start("gen_01")
drive(e, ["1", "1", "b", "1", "2"])            # walk, assert bleeding -> jump, tier1 yes, tier2 controlled
print("TEST 5 fired:", ResQRules.FIRED, "tiers:", ResQRules.TIERS, "outcome:", ResQRules.OUTCOME)
assert "catastrophic_bleeding" in ResQRules.FIRED
assert ResQRules.TIERS == [1, 2] and ResQRules.OUTCOME == "hem_08"
assert e.cur_chart == "hemorrhage"
print("  PASS: override jumped into hemorrhage, escalation loop ran identically\n")

print("ALL TESTS PASS")
