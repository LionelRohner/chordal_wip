from chordal_wip.scales import ChordProgression, Scale, Chord


scale_ref = Scale("C", "ionian")
# print("C ionian:", scale_ref.notes)

chord = Chord(scale_ref)
# print(vars(chord))

chord_progression = ChordProgression(n_chords=4, chord=chord)

print(vars(chord_progression))

# scale = Scale("F#", "mixolydian")
# print("F mixolydian:", scale.notes)
