#!/usr/bin/env python3

try:
    from new_reasoning_rule import Rule
    from new_reasoning_matcher import Matcher
except ModuleNotFoundError:
    from new_reasoning_rule import Rule
    from new_reasoning_matcher import Matcher

RULES = [

    Rule(

        name="IS_A_TRANSITIVITY",

        antecedents=[

            ("?x","IS_A","?y"),

            ("?y","IS_A","?z"),

        ],

        consequent=(

            "?x",

            "IS_A",

            "?z",

        ),

    ),

]

class ReasoningEngine:

    def __init__(self):

        self.matcher = Matcher()

    def derive(self, relations):

        derived = set()

        for rule in RULES:

            matches = self.matcher.match(
                relations,
                rule,
            )

            for m in matches:

                s,o,t = rule.consequent

                derived.add((
                    m[s],
                    o,
                    m[t],
                ))

        return derived


if __name__ == "__main__":

    engine = ReasoningEngine()

    facts = {

        ("John","IS_A","Human"),

        ("Human","IS_A","Animal"),

    }

    print(engine.derive(facts))
