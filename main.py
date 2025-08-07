class Scale:
    def __init__(self, root_note, scale_type):
        self.root_note = root_note
        self.scale_type = scale_type
        self.notes = self.generate_scale()

    def generate_scale(self):
        pass

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
c_major_scale = Scale("C", "major")
chord_progression_generator = ChordProgressionGenerator(c_major_scale)
chords = chord_progression_generator.get_chord_progression()

print(c_major_scale)
print(chord_progression_generator)
print(chords)
