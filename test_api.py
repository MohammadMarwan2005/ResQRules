#!/usr/bin/env python3
"""Automated proofs for the API adapter layer (api/session_runner.py).

These drive the SessionRunner DIRECTLY (no HTTP / TestClient needed) — the same
queue-based engine adapter the FastAPI routes use — and assert on the
(ScreenState, OverrideEvent) contract the mobile app will consume.

  TEST 1  Bleeding-key on a hem screen = GUARD (the fix).
          A hemorrhage session opens on a hem_question (tier 1). Pressing the
          Bleeding danger key 'b' must NOT be read as "no — controlled"; it must
          raise a guard override (already in hemorrhage) and stay on a hem screen.
  TEST 2  Arrest override OUT of hemorrhage. Pressing 'n' on a hem screen jumps to
          cpr_adult with a non-guard override event (and clears hemorrhage state).
  TEST 3  Normal recheck sanity: "yes" escalates the tier, "no" exits to terminal.

Run:  python3 test_api.py
"""
from api.session_runner import SessionRunner


def boot(chart_id):
    return SessionRunner(session_id="test", chart_id=chart_id)


# ── TEST 1: Bleeding key on a hem screen is a guard, not "controlled" ─────────
r = boot("hemorrhage")
s0 = r.current_screen
print("TEST 1 open:", s0.type, "tier", s0.hem_tier.current if s0.hem_tier else None)
assert s0.type == "hem_question", f"hemorrhage should open on a hem_question, got {s0.type}"
assert s0.hem_tier.current == 1, f"should open at tier 1, got {s0.hem_tier.current}"

screen, override = r.submit("b")
print("TEST 1 after 'b':", screen.type,
      "| override:", None if override is None else
      (override.kind, override.guard_fired, override.jumped_to_chart))
assert override is not None, "pressing 'b' must produce an override_event (guard), not be swallowed"
assert override.kind == "catastrophic_bleeding"
assert override.guard_fired is True, "already in hemorrhage -> guard"
assert override.jumped_to_chart is None, "guard does not jump"
assert screen.type == "hem_question", "after the guard we stay on a hem recheck screen"
assert screen.chart_id == "hemorrhage"
r.stop()
print("  PASS: 'b' on a hem screen guards (no false 'controlled' exit)\n")


# ── TEST 2: arrest override OUT of hemorrhage (regression) ────────────────────
r = boot("hemorrhage")
assert r.current_screen.type == "hem_question"
screen, override = r.submit("n")
print("TEST 2 after 'n':", screen.type, screen.chart_id,
      "| override:", (override.kind, override.guard_fired, override.jumped_to_chart))
assert override is not None
assert override.kind == "not_breathing"
assert override.guard_fired is False, "leaving hemorrhage -> real jump, not a guard"
assert override.jumped_to_chart == "cpr_adult"
assert screen.chart_id == "cpr_adult", "body should now be the CPR protocol"
r.stop()
print("  PASS: 'n' on a hem screen jumps to cpr_adult (non-guard)\n")


# ── TEST 3: normal recheck — escalate then exit ──────────────────────────────
r = boot("hemorrhage")
assert r.current_screen.hem_tier.current == 1
screen, override = r.submit("1")               # yes — still bleeding -> tier 2
print("TEST 3 after '1':", screen.type, "tier", screen.hem_tier.current)
assert override is None, "a normal recheck answer is not an override"
assert screen.type == "hem_question" and screen.hem_tier.current == 2, "still bleeding -> escalate to tier 2"

screen, override = r.submit("2")               # no — controlled -> terminal
print("TEST 3 after '2':", screen.type, "terminal", screen.is_terminal, "alive", r.alive)
assert screen.type == "action" and screen.is_terminal is True, "controlled -> terminal action"
assert screen.chart_id == "hemorrhage"
assert r.alive is False, "terminal leaf ends the session"
r.stop()
print("  PASS: recheck yes->escalate, no->terminal exit\n")


print("ALL API TESTS PASS")
