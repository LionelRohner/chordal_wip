from collections import Counter
from pytest import approx
from chordal_wip.helpers import rotate_list
import chordal_wip.scales as scales
import pandas as pd


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
        self._integrity_proportions()
        self._sort_chords()

    def _chord_progression(self) -> list:
        chord_lst = self.chord_txt.split(" ")
        return [chord for chord in chord_lst if "/" not in chord]

    def _count_chords(self) -> dict:
        return dict(Counter(self.chord_progression))

    def _chord_proportions(self) -> dict:
        return {
            chord: cnt / self.n_chords
            for chord, cnt in self.chord_counts.items()
        }

    def _integrity_proportions(self):
        sum_to_one = sum(self.chord_proportions.values())

        if sum_to_one != approx(1.0):
            raise ValueError(f"Proportions do not sum to 1, got {sum_to_one}")

    def _sort_chords(self):
        print(max())

    def __str__(self):
        return (
            f"KeyPredictor:\n"
            f"  Chord Progression: {self.chord_progression}\n"
            f"  Chord Counts: {self.chord_counts}\n"
            f"  Chord Proportions: {self.chord_proportions}"
        )


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
        self._integrity_proportions()

    def _chord_progression(self) -> list:
        chord_lst = self.chord_txt.split(" ")
        return [chord for chord in chord_lst if "/" not in chord]

    def _count_chords(self) -> pd.Series:
        counts_unsorted = pd.Series(Counter(self.chord_progression))
        return self._sort_chords(counts_unsorted)

    def _chord_proportions(self) -> pd.Series:
        return self.chord_counts / self.n_chords

    def _integrity_proportions(self):
        sum_to_one = self.chord_proportions.sum()

        if sum_to_one != approx(1.0):
            raise ValueError(f"Proportions do not sum to 1, got {sum_to_one}")

    def _sort_chords(self, counts_unsorted: pd.Series) -> pd.Series:
        # Find key with highest value
        max_key = counts_unsorted.idxmax()
        # print(f"max_key : {max_key}")

        # Get sorted index as a list
        sorted_index = counts_unsorted.sort_index().index.tolist()
        # print(f"sorted_index : {sorted_index}")

        # Find position of max_key
        max_key_idx = sorted_index.index(max_key)
        # print(f"max_key_idx : {max_key_idx}")

        # Rotate the index list
        rotated_index = rotate_list(sorted_index, max_key_idx, dir="left")
        # print(f"rotated_index : {rotated_index}")

        return counts_unsorted[rotated_index]

    def __str__(self):
        df_summary = pd.DataFrame(
            {
                "Chord": self.chord_proportions.index,
                "Count": self.chord_counts.values,
                "Proportion": self.chord_proportions.values,
            }
        )

        df_summary.loc["Total"] = df_summary.sum(numeric_only=True)

        return f"KeyPredictor:\n{df_summary}"


test = "Gmaj G/B Cmaj Cmin Gmaj Bmin C/E Dmin Gmaj Bmin C/E Dmaj Cmaj Cmaj Dmaj Gmaj Emin Cmaj Dmaj Bmaj Gmaj Bmaj Gmaj Cmin Gmaj Emin Cmaj Dmaj"

kp = KeyPredictor(test)

# print(kp)

ref_scales = scales.get_ref_scales()

reference = ref_scales
print(reference)

progression = pd.Series(["Gmaj", "Cmaj", "Bmin", ...])
# matches = progression.map(reference)

# print(ref_scales)
