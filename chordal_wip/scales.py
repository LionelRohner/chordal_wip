from itertools import accumulate
import numpy as np


def rotate_list(a, n):
    return np.concatenate((a[-n:], a[:-n]))


class Scale:
    # Start at 0 (equals root), then move by 2 (whole-step) or 1 (half-step)
    church_modes_dist = [0, 2, 2, 1, 2, 2, 2, 1]

    # rotations of church_modes_dist yield all modes
    scales_dict = {
        "ionian": np.array(church_modes_dist),
        "dorian": rotate_list(church_modes_dist, 1),
        "phyrgian": rotate_list(church_modes_dist, 2),
        "lydian": rotate_list(church_modes_dist, 3),
        "mixolydian": rotate_list(church_modes_dist, 4),
        "aeolian": rotate_list(church_modes_dist, 5),
        "locrian": rotate_list(church_modes_dist, 6),
    }
    all_notes = np.tile(
        np.array(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]), 3
    )

    def __init__(self, root_note, scale_type):
        self.root_note = root_note
        self.scale_type = scale_type
        self.notes = self.generate_scale()

    def generate_scale(self):
        # print(Scale.scales_dict)
        scale_dist = Scale.scales_dict["ionian"]
        scale_ind = np.cumsum(scale_dist)[:-1]
        scale_chars = Scale.all_notes[scale_ind]
        return scale_chars


class Chord:
    def __init__(self, root_note, chord_type):
        self.root_note = root_note
        self.chord_type = chord_type

    def display_chord(self):
        pass


class Mode(Scale):
    pass


class ChordProgressionGenerator:
    def __init__(self, scale):
        self.scale = scale

    def get_chord_progression(self):
        pass
        # print(self.scale)
