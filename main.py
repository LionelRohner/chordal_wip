from chordal_wip.scales import ChordProgression, Scale, Chord


scale_ref = Scale("C", "ionian")
# print("C ionian:", scale_ref.notes)

chord = Chord(scale_ref)
print(vars(chord))

chord_progression = ChordProgression(scale_ref)
# scale = Scale("F#", "mixolydian")
# print("F mixolydian:", scale.notes)
