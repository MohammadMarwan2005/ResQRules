#!/usr/bin/env python3
"""ResQRules engine — a generic, data-driven Experta walker for SARC SOP charts.

A SMALL set of generic rules walks ANY chart JSON (see SCHEMA.md). There are NO
per-node rules: the single `walk` rule matches the `Current` fact, prints the node,
and asserts the next `Current` — forward chaining through the tree. Cross-tree
`jump` nodes degrade gracefully (Phase 2 adds a real return-stack).
"""
import json
import sys
from experta import KnowledgeEngine, Rule, Fact, Field, MATCH, AS


class Current(Fact):
    """The single 'where we are' fact the generic rule chains on."""
    nid = Field(str, mandatory=True)


class ResQRules(KnowledgeEngine):
    def __init__(self, chart, loaded=None):
        super().__init__()
        self.nodes = chart["nodes"]
        self.loaded = loaded or {chart["meta"]["chart_id"]}  # charts available this run

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
            tgt = node["target_chart"]
            if tgt in self.loaded:                       # Phase 2 wires the real hand-off
                self.declare(Current(nid=node.get("target_node", "entry")))
            else:
                print(f"   >> would transfer to chart '{tgt}' "
                      f"(node '{node.get('target_node', 'entry')}') — not loaded this run <<")
                print("=== END (jump stub) ===")


def main(path):
    chart = json.load(open(path))
    print(f"=== {chart['meta']['title']}  ({chart['meta']['chart_id']}) ===")
    e = ResQRules(chart)
    e.reset()
    e.declare(Current(nid=chart["entry"]))
    e.run()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/choking.json")
