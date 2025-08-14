import numpy as np


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
    # Start at 0 (equals root), then move by 2 (whole-step) or 1 (half-step)
    church_modes_dist = [2, 2, 1, 2, 2, 2, 1]

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
    # tiling needed? if yes use np.tile(arr, number of repeats)
    # use bs instead of # for minor modes?
    all_notes = np.array(
        ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    )

    def __init__(self, root_note, scale_type):
        self.root_note = root_note
        self.all_notes_rot = self.set_root()
        self.scale_type = scale_type
        self.notes = self.generate_scale()

    def set_root(self):
        n_rot = np.where(Scale.all_notes == self.root_note)[0][0]
        all_notes_rot = rotate_list(Scale.all_notes, n_rot)
        return all_notes_rot

    def generate_scale(self):
        scale_dist = Scale.scales_dict[self.scale_type]
        # print("scale_dist:", scale_dist)
        scale_ind = np.cumsum(scale_dist)[:-1]
        scale_ind_w_root = np.concatenate(([0], scale_ind))
        # print("scale_ind:", scale_ind_w_root)
        scale_chars = self.all_notes_rot[scale_ind_w_root]
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
