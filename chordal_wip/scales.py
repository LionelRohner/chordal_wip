from typing import ValuesView
import pandas as pd
import numpy as np
import random


def rotate_list(arr, n, dir="left"):
    """
    Rotate array elements left or right by n positions.

    Args:
        arr: Input array
        n: Number of positions to rotate (wraps around if n > len (arr))
        dir: Rotation direction ('left' or 'right')

    Returns:
        Rotated array
    """
    if len(arr) == 0:
        return arr

    arr = np.array(arr)
    n = n % len(arr)

    if dir == "left":
        return np.concatenate((arr[n:], arr[:n]))
    elif dir == "right":
        return np.concatenate((arr[-n:], arr[:-n]))
    else:
        raise ValueError("Direction must be 'left' or 'right'!")


class Scale:
    """A class to represent musical scales, specifically church modes derived from the major scale."""

    ALL_NOTES = np.array(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])

    # Distance between intervalls in diatonic sclae, i.e. 2 (whole-step) or 1 (half-step)
    DIATONIC_INTERVALS = np.array([2, 2, 1, 2, 2, 2, 1])

    scales_dict = {
        "ionian": DIATONIC_INTERVALS,
        "dorian": rotate_list(DIATONIC_INTERVALS, 1),
        "phyrgian": rotate_list(DIATONIC_INTERVALS, 2),
        "lydian": rotate_list(DIATONIC_INTERVALS, 3),
        "mixolydian": rotate_list(DIATONIC_INTERVALS, 4),
        "aeolian": rotate_list(DIATONIC_INTERVALS, 5),
        "locrian": rotate_list(DIATONIC_INTERVALS, 6),
    }

    def __init__(self, root_note, scale_type):
        if root_note not in self.ALL_NOTES:
            raise ValueError(f"Invalid root note: {root_note}. Must be one of {self.ALL_NOTES}.")
        if scale_type not in self.scales_dict:
            raise ValueError(
                f"Invalid scale type: {scale_type}. Must be one of {list(self.scales_dict.keys())}."
            )
        self.root_note = root_note
        self.scale_type = scale_type
        self.rotated_notes = self._rotate_notes()

    def _rotate_notes(self):
        """Return all notes rotated to start at the root note."""
        n_rot = np.where(Scale.ALL_NOTES == self.root_note)[0][0]
        all_notes_rot = rotate_list(Scale.ALL_NOTES, n_rot)
        return all_notes_rot

    @property
    def notes(self):
        """Return the notes of the scale."""
        scale_dist = Scale.scales_dict[self.scale_type]
        scale_indices = np.cumsum(scale_dist)[:-1]
        scale_indices_with_root = np.concatenate(([0], scale_indices))
        scale_chars = self.rotated_notes[scale_indices_with_root]
        return scale_chars


class Chord:
    # Define chord formulas as distances from the root (in semitones)
    CHORD_FORMULAS = {
        "maj": [0, 4, 7],  # Root, major 3rd, perfect 5th
        "min": [0, 3, 7],  # Root, minor 3rd, perfect 5th
        "maj7": [0, 4, 7, 11],  # Root, major 3rd, perfect 5th, major 7th
        "min7": [0, 3, 7, 10],  # Root, minor 3rd, perfect 5th, minor 7th
        "7": [0, 4, 7, 10],  # Root, major 3rd, perfect 5th, minor 7th
        # Add more chord types as needed
    }

    # We need ionian triads and 7th chord to generate all chords for the modes using rotations
    IONIAN_BASE_CHORDS = ["maj", "min", "min", "maj", "maj", "min", "dim"]
    IONIAN_7_CHORDS = ["maj7", "min7", "min7", "maj7", "7", "min7", "min7♭5"]

    # TODO: scale_type is just needed for filtering, maybe there is a better solution
    MODE_CHORDS = pd.concat(
        [
            pd.DataFrame(
                {
                    "position": list(range(1, 8)),
                    "scale_type": ["ionian"] * 7,
                    "triads": IONIAN_BASE_CHORDS,
                    "7ths": IONIAN_7_CHORDS,
                    "roman": ["I", "ii", "iii", "IV", "V", "vi", "vii°"],
                }
            ),
            pd.DataFrame(
                {
                    "position": list(range(1, 8)),
                    "scale_type": ["dorian"] * 7,
                    "triads": rotate_list(IONIAN_BASE_CHORDS, 1),
                    "7ths": rotate_list(IONIAN_7_CHORDS, 1),
                    "roman": ["i", "ii", "♭III", "IV", "v", "vi°", "♭VII"],
                }
            ),
            pd.DataFrame(
                {
                    "position": list(range(1, 8)),
                    "scale_type": ["phrygian"] * 7,
                    "triads": rotate_list(IONIAN_BASE_CHORDS, 2),
                    "7ths": rotate_list(IONIAN_7_CHORDS, 2),
                    "roman": ["i", "♭II", "♭III", "iv", "v°", " ♭VI", "♭vii"],
                }
            ),
            pd.DataFrame(
                {
                    "position": list(range(1, 8)),
                    "scale_type": ["lydian"] * 7,
                    "triads": rotate_list(IONIAN_BASE_CHORDS, 3),
                    "7ths": rotate_list(IONIAN_7_CHORDS, 3),
                    "roman": ["I", "II", "iii", "♯iv°", "V", "vi", "vii"],
                }
            ),
            pd.DataFrame(
                {
                    "position": list(range(1, 8)),
                    "scale_type": ["mixolydian"] * 7,
                    "triads": rotate_list(IONIAN_BASE_CHORDS, 4),
                    "7ths": rotate_list(IONIAN_7_CHORDS, 4),
                    "roman": ["I", "ii", "iii°", "IV", "v", "vi", "♭VII"],
                }
            ),
            pd.DataFrame(
                {
                    "position": list(range(1, 8)),
                    "scale_type": ["aolian"] * 7,
                    "triads": rotate_list(IONIAN_BASE_CHORDS, 5),
                    "7ths": rotate_list(IONIAN_7_CHORDS, 5),
                    "roman": ["i", "ii°", "♭III", "iv", "v", "♭VI", "♭VII"],
                }
            ),
            pd.DataFrame(
                {
                    "scale_type": ["locrian"] * 7,
                    "triads": rotate_list(IONIAN_BASE_CHORDS, 6),
                    "7ths": rotate_list(IONIAN_7_CHORDS, 6),
                    "roman": ["i°", "♭II", "♭iii", "iv", "♭V", "♭VI", "♭vii"],
                    "position": list(range(1, 8)),
                }
            ),
        ]
    )

    CHORD_DEGREES = pd.DataFrame(
        [
            {"position": 1, "name": "tonic", "type": "tonic", "tension": -100},
            {"position": 2, "name": "supertonic", "type": "subdominant", "tension": 30},
            {"position": 3, "name": "mediant", "type": "tonic", "tension": -80},
            {
                "position": 4,
                "name": "subdominant",
                "type": "subdominant",
                "tension": 20,
            },
            {"position": 5, "name": "dominant", "type": "dominant", "tension": 80},
            {"position": 6, "name": "submediant", "type": "tonic", "tension": -70},
            {"position": 7, "name": "leading", "type": "dominant", "tension": 80},
        ]
    )

    def __init__(self, scale):
        # TODO: what is actually needed here?
        self.scale = scale
        self.root_note = scale.root_note
        self.scale_type = scale.scale_type
        self.notes = scale.notes
        self.data = self.merge_data()

    def merge_data(self):
        # filter df for scale_type
        mode_chords = self.MODE_CHORDS[self.MODE_CHORDS["scale_type"] == self.scale_type].copy()

        # mutate chord cols
        mode_chords["triads"] = self.notes + mode_chords["triads"]
        mode_chords["7ths"] = self.notes + mode_chords["7ths"]

        # add chord degree information
        merged_data = pd.merge(mode_chords, self.CHORD_DEGREES, on="position", how="left")
        return merged_data

    # def get_chord(self, degree, chord_type=None):
    #     """
    #     Get the notes of a chord for a given scale degree.
    #     Args:
    #         degree: Scale degree (1-7, where 1 is the root).
    #         chord_type: Optional. If None, uses the diatonic chord quality for the mode.
    #     Returns:
    #         List of notes in the chord.
    #     """
    #     if chord_type is None:
    #         chord_type = self.chord_qualities[degree - 1]
    #
    #     # Get the root note of the chord (e.g., degree=1 -> self.notes[0])
    #     chord_root = self.notes[degree - 1]
    #
    #     # Find the index of the chord root in the full list of notes (ALL_NOTES)
    #     root_index_in_all_notes = np.where(self.scale.ALL_NOTES == chord_root)[0][0]
    #
    #     # Calculate the indices of the chord notes in ALL_NOTES
    #     chord_note_indices = [(root_index_in_all_notes + interval) % 12 for interval in self.CHORD_FORMULAS[chord_type]]
    #
    #     # Get the chord notes from ALL_NOTESq
    #     chord_notes = self.scale.ALL_NOTES[chord_note_indices]
    #
    #     return chord_notes
    #
    # def get_chord_progression(self, progression):
    #     """
    #     Get the notes for a chord progression (e.g., [1, 4, 5]).
    #     Args:
    #         progression: List of scale degrees (e.g., [1, 4, 5]).
    #     Returns:
    #         List of chords (each chord is a list of notes).
    #     """
    #     return [self.get_chord(degree) for degree in progression]


class ChordProgression(Chord):
    def __init__(self, n_chords, chord: Chord):
        super().__init__(chord)  # Initialize the Chord class
        self.n_chords = n_chords
        self.progression = self.generate_chord_progression(n_chords)

    def generate_chord_progression(self, n_chords):
        # start with tonic, then subdominant, then dominant and resolve with other tonic
        tonic_chords = self.data[self.data["type"] == "tonic"]
        subdominant_chords = self.data[self.data["type"] == "subdominant"]
        dominant_chords = self.data[self.data["type"] == "dominant"]
        all_dominant_chords = self.data[self.data["type"].isin(["subdominant", "dominant"])]

        progression = pd.DataFrame(columns=self.data.columns)
        for i in range(n_chords):
            if i == 0:
                next_chord = tonic_chords.sample(n=1)
            elif i == n_chords - 1 and not progression["name"].eq("tonic").any():
                next_chord = tonic_chords[tonic_chords["name"] == "tonic"]
            elif progression["tension"].sum() <= 0:
                next_chord = all_dominant_chords.sample(n=1)
            else:
                next_chord = tonic_chords.sample(n=1)

            progression = pd.concat([progression, next_chord], ignore_index=True)

        return progression


class MarkovChordProgression(Chord):
    def __init__(self, n_chords, chord: Chord):
        super().__init__(chord)  # init from  parent
        self.n_chords = n_chords
        self.chord_names = self.data["roman"].values
        self.intial_state = self._init_state_vec()
        self.transition_matrix = self._build_transition_matrix()
        self.progression = self.generate_progression(n_chords)

    def _init_state_vec(self):
        """
        Set initial state probaility vector
        """
        tension = self.data["tension"].values * -1
        tension_min_max = (tension - min(tension)) / (max(tension) - min(tension))
        tension_norm = tension_min_max / sum(tension_min_max)
        return tension_norm

    def _build_transition_matrix(self):
        """
        Explain logic later
        """

        # hardcoded transition matrix: THIS SUCKS
        transition_matrix = np.array(
            [
                # From (Row) / To (Col)
                # t  # st  # m  # sd # d # sm #ln
                [0.1, 0.2, 0.05, 0.3, 0.25, 0.1, 0.0],  #  tonic
                [0.3, 0.0, 0.1, 0.3, 0.2, 0.0, 0.1],  #  subtonic
                [0.2, 0.1, 0.0, 0.2, 0.3, 0.1, 0.1],  #  mediant
                [0.3, 0.1, 0.1, 0.1, 0.3, 0.0, 0.1],  #  Isubdominant
                [0.6, 0.0, 0.0, 0.1, 0.0, 0.2, 0.1],  #  dominant
                [0.4, 0.1, 0.1, 0.2, 0.1, 0.0, 0.1],  #  subdemiant
                [0.6, 0.0, 0.2, 0.1, 0.1, 0.0, 0.0],  #  leadning note
            ]
        )

        # Add fuzzyness depending on genre or whatevs
        return transition_matrix

    def generate_progression(self, n_chords):
        """
        Generate a chord progression by walking through the transition matrix
        """
        chord_position = self.data["position"].values.astype(int)
        first_chord = np.random.choice(chord_position, size=1, p=self.intial_state)
        progression = np.array(first_chord, dtype=int)

        for _ in range(n_chords - 1):
            last_chord_idx = progression[-1]
            print("idx", last_chord_idx)
            print("A", self.transition_matrix[last_chord_idx])
            print("chord_position", chord_position)
            print("length row vec:", len(self.transition_matrix[last_chord_idx]))
            next_chord = np.random.choice(chord_position, size=1, p=self.transition_matrix[last_chord_idx])
            progression = np.append(progression, next_chord)

        out = self.data.head(0)
        for c in progression:
            out = pd.concat([out, self.data[self.data["position"] == c]])
        out = out.reset_index(drop=True)
        print(out)
        return out
