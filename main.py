class Scale:
    scales_dict = {
        "major": [0, 1, 1, 0.5, 1, 1, 1, 0.5],
        # basically minor is a rotation of major, like all other modes
        # therefor make generic
        "minor": [0, 1, 1, 0.5, 1, 1, 0.5, 1],
    }
    scales_dict = {key: [x * 2 for x in value] for key, value in scales_dict.items()}

    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"] * 3

    def __init__(self, root_note, scale_type):
        self.root_note = root_note
        self.scale_type = scale_type
        self.notes = self.generate_scale()

    def generate_scale(self):
        print(self.notes)
        # scale = Scale.scales_dict[self.scale_type]
        # continue here


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
        print(self.scale)


# Example usage
scale = Scale("C", "major")
# print(scale.scales_dict)


chord_progression_generator = ChordProgressionGenerator(scale)
chords = chord_progression_generator.get_chord_progression()
