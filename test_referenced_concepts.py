#!/usr/bin/env python3

import unittest

from new_knowledge_realizer import KnowledgeRealizer


class ReferencedConceptExtractionTest(unittest.TestCase):

    def setUp(self):
        self.realizer = KnowledgeRealizer()

    def test_prime_potency_longest_match_suppresses_potency_fragment(self):
        text = (
            "Matrix: The repository of Prime Potency possibilities "
            "that admit actualization and isomorphic representation."
        )
        referenced = self.realizer._find_concepts_in_text(text)

        self.assertIn("Matrix", referenced)
        self.assertIn("Prime_Potency", referenced)
        self.assertNotIn("Potency", referenced)

    def test_potency_is_included_when_independently_referenced(self):
        text = (
            "Matrix arises from Prime Potency. "
            "Potency remains a distinct metaphysical concept."
        )
        referenced = self.realizer._find_concepts_in_text(text)

        self.assertIn("Prime_Potency", referenced)
        self.assertIn("Potency", referenced)


if __name__ == "__main__":
    unittest.main()
