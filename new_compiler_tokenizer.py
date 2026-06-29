#!/usr/bin/env python3

import re


class Tokenizer:

    TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)

    def tokenize(self, sentence: str):

        return self.TOKEN_PATTERN.findall(sentence)


if __name__ == "__main__":

    tokenizer = Tokenizer()

    sentence = "John possesses a book."

    print(tokenizer.tokenize(sentence))
