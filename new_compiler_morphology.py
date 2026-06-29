#!/usr/bin/env python3

import hunspell



class Morphology:

    IRREGULAR = {

        "is": "be",
        "are": "be",
        "am": "be",
        "was": "be",
        "were": "be",
        "been": "be",
        "being": "be",

        "has": "have",
        "had": "have",

        "does": "do",
        "did": "do",

    }


    def __init__(self):

        self.h = hunspell.HunSpell(
            "/usr/share/hunspell/en_US.dic",
            "/usr/share/hunspell/en_US.aff"
        )

    def lemma(self, token):

        word = token.lower()

        if word in self.IRREGULAR:

            return self.IRREGULAR[word]

        stems = self.h.stem(word)

        if stems:

            return stems[0].decode("utf-8")

        return word


if __name__ == "__main__":

    morph = Morphology()

    for word in (
        "possesses",
        "looking",
        "books",
        "children",
    ):

        print(word, "->", morph.lemma(word))
