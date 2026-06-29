#!/usr/bin/env python3

class Matcher:

    def match(self, relations, rule):

        results = []

        ants = rule.antecedents

        if len(ants) != 2:
            return results

        (_, op1, _) = ants[0]
        (_, op2, _) = ants[1]

        for a in relations:

            s1, o1, x1 = a

            if o1 != op1:
                continue

            for b in relations:

                s2, o2, x2 = b

                if o2 != op2:
                    continue

                if x1 != s2:
                    continue

                mapping = {
                    "?x": s1,
                    "?y": x1,
                    "?z": x2,
                }

                results.append(mapping)

        return results
