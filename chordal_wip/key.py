import pandas as pd
import numpy as np
from collections import Counter
import re


class KeyPredictor:
    """
    A class for predicting key from a chord progression.
    """

    def __init__(self, chord_txt: str):
        self.chord_txt = chord_txt
        self.chord_progression = self._chord_progression()
        self.n_chords = len(self.chord_progression)
        self.chord_counts = self._count_chords()
        self.chord_proportions = self._chord_proportions()

        self.test = self._standardize()

    def _chord_progression(self) -> list:
        chord_lst = self.chord_txt.split(" ")
        return [
            chord for chord in chord_lst if "/" not in chord
        ]  # Question: Is this fine?

    def _count_chords(self) -> dict:
        return dict(Counter(self.chord_progression))

    def _chord_proportions(self) -> dict:
        return {
            chord: cnt / self.n_chords
            for chord, cnt in self.chord_counts.items()
        }

    def _standardize(self):
        sort = sorted(self.chord_progression)
        print(sort)

    def __str__(self):
        return (
            f"KeyPredictor:\n"
            f"  Chord Progression: {self.chord_progression}\n"
            f"  Chord Counts: {self.chord_counts}\n"
            f"  Chord Proportions: {self.chord_proportions}"
        )


test = "G G/B C Cm G Bm C/E D G Bm C/E D C C D G Em C D B G B G Cm G Em C D"

kp = KeyPredictor(test)

print(kp)
