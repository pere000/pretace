#!/usr/bin/env python3

"""
TACE Constructor

Constructs human-readable definitions
using only TACE knowledge.
"""

class Constructor:

    def construct(self, universe, subject):

        relations = []

        # Collect every relation where the subject appears
        for r in universe.relations:

            try:
                if r.subject.lexical.lower() == subject.lower():
                    relations.append(r)
            except AttributeError:
                continue

        if not relations:
            return None

        lines = []

        lines.append(subject.capitalize())
        lines.append("")
        lines.append("Constructed from TACE knowledge")
        lines.append("")

        isa = []
        props = []

        for r in relations:

            op = r.operator

            obj = r.object.lexical

            if op == "IS_A":
                isa.append(obj)

            elif op == "HAS":
                props.append(obj)

            else:
                lines.append(f"- {op} {obj}")

        if isa:
            lines.append(
                f"{subject.capitalize()} is " +
                ", ".join(isa) + "."
            )

        if props:
            lines.append("")
            lines.append("Properties:")

            for p in props:
                lines.append(f"• {p}")

        return "\n".join(lines)
