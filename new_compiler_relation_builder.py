#!/usr/bin/env python3

from new_compiler_tokenizer import Tokenizer
from new_compiler_phrase_detector import PhraseDetector
from new_compiler_morphology import Morphology
from new_compiler_resolver import Resolver

from new_compiler_linguistic import (
    LinguisticEntity,
    LinguisticRelation,
)


class RelationBuilder:

    DETERMINERS = {
        "a",
        "an",
        "the",
        "this",
        "that",
        "these",
        "those",
    }

    def __init__(self):

        self.tokenizer = Tokenizer()
        self.detector = PhraseDetector()
        self.morphology = Morphology()
        self.resolver = Resolver()

    def build(self, sentence):

        tokens = self.tokenizer.tokenize(sentence)
        tokens = self.detector.detect(tokens)

        if len(tokens) < 3:
            return None

        subject = tokens[0]

        verb = self.morphology.lemma(tokens[1])

        reduction = self.resolver.resolve(verb)

        operator = (
            reduction.canonical_operator
            if reduction is not None
            else verb.upper()
        )

        obj = None

        for token in tokens[2:]:

            if token.lower() in self.DETERMINERS:
                continue

            obj = token.rstrip(".,!?")
            break

        if obj is None:
            return None

        return LinguisticRelation(

            subject=LinguisticEntity(
                lexical=subject,
            ),

            operator=operator,

            object=LinguisticEntity(
                lexical=obj,
            ),

        )


if __name__ == "__main__":

    builder = RelationBuilder()

    print(
        builder.build(
            "John possesses the book."
        )
    )
