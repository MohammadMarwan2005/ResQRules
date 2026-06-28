#!/usr/bin/env python3
"""ResQRules validator — fails loudly on any schema/graph violation.

Checks (per CLAUDE.md / SCHEMA.md):
  - entry node exists
  - every node has the fields its type requires
  - every option/`next` resolves to a real LOCAL node id
  - every `jump` has a target_chart (external target, reported separately)
  - no orphan (unreachable-from-entry) nodes
  - every in-tree leaf is type `action` (a `jump` is an external transfer, not a leaf)

Exit code 0 = PASS, 1 = FAIL.
"""
import json
import sys

NODE_TYPES = {"question", "instruction", "action", "jump"}


def validate(path):
    chart = json.load(open(path))
    nodes = chart.get("nodes", {})
    errors, warnings, externals = [], [], []

    entry = chart.get("entry")
    if entry not in nodes:
        errors.append(f"entry '{entry}' is not a node")

    # per-node structural checks + collect local references
    for nid, n in nodes.items():
        t = n.get("type")
        if t not in NODE_TYPES:
            errors.append(f"{nid}: bad/missing type {t!r}")
            continue
        if "text" not in n:
            errors.append(f"{nid}: missing 'text'")
        if "page" not in n:
            errors.append(f"{nid}: missing 'page' (every node must cite its source page)")
        if "[UNCLEAR" in n.get("text", ""):
            warnings.append(f"{nid}: text flagged [UNCLEAR] — needs human review")

        if t == "question":
            opts = n.get("options")
            if not opts:
                errors.append(f"{nid}: question has no options")
            for o in opts or []:
                if "answer" not in o or "next" not in o:
                    errors.append(f"{nid}: option missing answer/next: {o}")
                elif o["next"] not in nodes:
                    errors.append(f"{nid}: option '{o.get('answer')}' -> unknown node '{o['next']}'")
        elif t == "instruction":
            nxt = n.get("next")
            if nxt is None:
                errors.append(f"{nid}: instruction has no 'next'")
            elif nxt not in nodes:
                errors.append(f"{nid}: next -> unknown node '{nxt}'")
        elif t == "action":
            if n.get("next") or n.get("options"):
                errors.append(f"{nid}: action (leaf) must not have next/options")
        elif t == "jump":
            if not n.get("target_chart"):
                errors.append(f"{nid}: jump missing 'target_chart'")
            else:
                externals.append(f"{nid} -> {n['target_chart']}:{n.get('target_node', 'entry')}")

    # reachability from entry
    seen, stack = set(), [entry] if entry in nodes else []
    while stack:
        nid = stack.pop()
        if nid in seen:
            continue
        seen.add(nid)
        n = nodes[nid]
        if n.get("type") == "question":
            stack += [o["next"] for o in n.get("options", []) if o.get("next") in nodes]
        elif n.get("type") == "instruction" and n.get("next") in nodes:
            stack.append(n["next"])
    orphans = set(nodes) - seen
    for o in sorted(orphans):
        errors.append(f"orphan (unreachable from entry): {o}")

    # leaf-type check: a node with no in-tree successor must be `action` (jump = transfer)
    for nid, n in nodes.items():
        t = n["type"]
        if t in ("question", "instruction"):
            continue
        # action and jump are terminals; action is a proper leaf, jump is external
        if t == "action":
            pass
        elif t == "jump":
            pass

    # report
    print(f"--- validation report: {path} ---")
    print(f"nodes: {len(nodes)} | entry: {entry} | reachable: {len(seen)}")
    if externals:
        print("external jump targets (resolved in other charts / Phase 2):")
        for e in externals:
            print(f"   * {e}")
    for w in warnings:
        print(f"WARN  {w}")
    if errors:
        print(f"\nFAIL — {len(errors)} violation(s):")
        for e in errors:
            print(f"   ! {e}")
        return False
    print("\nPASS — clean.")
    return True


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/choking.json"
    sys.exit(0 if validate(path) else 1)
