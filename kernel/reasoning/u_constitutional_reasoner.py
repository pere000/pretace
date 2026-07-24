"""
u_constitutional_reasoner.py

Constitutional Reasoner

Derives constitutional conclusions from a
Constitutional Model using the Constitutional Code.
"""

class ConstitutionalReasoner:

    def __init__(self, constitution):

        self.constitution = constitution

    ##################################################

    def reason(self, model):

        proof = []

        changed = True

        while changed:

            changed = False

            for article in self.constitution.articles():

                result = article.evaluate(model)

                if result.applied:

                    proof.append(result)

                    changed = True

        return proof
