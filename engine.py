#!/usr/bin/env python3
"""ResQRules engine — a generic, data-driven Experta walker for SARC SOP charts.

A SMALL set of generic rules walks ANY chart JSON (see SCHEMA.md). There are NO
per-node rules: the single `walk` rule matches the `Current` fact, prints the node,
and asserts the next `Current` — forward chaining through the tree.

All charts in data/ are loaded into one node map (node-id prefixes avoid collisions),
so a one-way `jump` into an in-scope chart is FOLLOWED; a jump to an absent / out-of-scope
chart degrades to a stub. Coming back from a sub-routine (return-stack) is Phase 2.
"""
import glob
import json
import os
import sys

from experta import KnowledgeEngine, Rule, Fact, Field, MATCH, AS


class Current(Fact):
    """The single 'where we are' fact the generic rule chains on."""
    nid = Field(str, mandatory=True)


class ResQRules(KnowledgeEngine):
    def __init__(self, nodes, loaded):
        super().__init__()
        self.nodes = nodes          # merged nodes from every loaded chart
        self.loaded = loaded        # set of chart_ids available

    def ask(self, options):
        for i, o in enumerate(options, 1):
            print(f"   {i}) {o['answer']}")
        while True:
            r = input("   > ").strip()
            if r.isdigit() and 1 <= int(r) <= len(options):
                return options[int(r) - 1]["next"]
            print("   (enter one of the listed numbers)")

    @Rule(AS.cur << Current(nid=MATCH.nid))
    def walk(self, cur, nid):
        node = self.nodes[nid]
        print(f"\n[{nid}] {node['text']}  (p.{node['page']})")
        self.retract(cur)                               # leave the old position
        t = node["type"]
        if t == "action":                               # leaf — stop
            print("=== END (action / leaf) ===")
        elif t == "instruction":
            input("   [enter] to continue ")
            self.declare(Current(nid=node["next"]))
        elif t == "question":
            self.declare(Current(nid=self.ask(node["options"])))
        elif t == "jump":                               # one-way cross-tree transfer
            tc, tn = node["target_chart"], node.get("target_node", "entry")
            if tc in self.loaded:
                print(f"   >> JUMP to chart '{tc}' (node '{tn}') <<")
                self.declare(Current(nid=tn))
            else:
                print(f"   >> would transfer to chart '{tc}' (node '{tn}') — not loaded <<")
                print("=== END (jump stub) ===")


def load_all(data_dir="data"):
    nodes, loaded = {}, set()
    for f in glob.glob(os.path.join(data_dir, "*.json")):
        c = json.load(open(f))
        loaded.add(c["meta"]["chart_id"])
        nodes.update(c["nodes"])                         # prefixed ids => no collisions
    return nodes, loaded


def main(path):
    chart = json.load(open(path))
    nodes, loaded = load_all(os.path.dirname(path) or "data")
    print(f"=== {chart['meta']['title']}  ({chart['meta']['chart_id']}) ===")
    print(f"(loaded charts: {', '.join(sorted(loaded))})")
    e = ResQRules(nodes, loaded)
    e.reset()
    e.declare(Current(nid=chart["entry"]))
    try:
        e.run()
    except (EOFError, KeyboardInterrupt):
        print("\n=== aborted (no more input) ===")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/choking.json")
