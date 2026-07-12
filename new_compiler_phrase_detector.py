#!/usr/bin/env python3

class PhraseDetector:

    def __init__(self):

        # Temporary dictionary.
        # Later this will come from the database.
        self.phrases = {
            ("looked", "after"),
            ("look", "after"),
            ("looking", "after"),
            ("looks", "after"),
        }

    def detect(self, tokens):

        result = []

        i = 0

        while i < len(tokens):

            if i + 1 < len(tokens):

                pair = (tokens[i], tokens[i + 1])

                if pair in self.phrases:
                    result.append(tokens[i] + " " + tokens[i + 1])
                    i += 2
                    continue

            result.append(tokens[i])
            i += 1

        return result


if __name__ == "__main__":

    detector = PhraseDetector()

    tokens = [
        "John",
        "looked",
        "after",
        "Mary",
        "."
    ]

    print(detector.detect(tokens))
