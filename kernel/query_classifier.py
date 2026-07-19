"""
QueryClassifier: identifies the domain of a user query.

Version 0.1
"""

class QueryClassifier:

    RULES = {
        "ontology": [
            "matrix",
            "q-form",
            "silver bridge",
            "consciousness",
            "form",
            "substance",
        ],
        "adr": [
            "adr",
            "inheritance",
            "architecture decision",
        ],
        "semantic_constitution": [
            "semantic",
            "meaning",
            "language",
            "definition",
        ],
        "software_constitution": [
            "software",
            "repository",
            "kernel",
            "module",
        ],
        "session_footprint": [
            "session",
            "footprint",
            "yesterday",
            "last conversation",
        ],
    }

    def classify(self, query: str) -> str:
        q = query.lower()

        for category, keywords in self.RULES.items():
            for keyword in keywords:
                if keyword in q:
                    return category.upper()

        return "UNKNOWN"
