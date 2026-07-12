#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass(slots=True)
class Rule:

    name: str

    antecedents: list

    consequent: tuple
