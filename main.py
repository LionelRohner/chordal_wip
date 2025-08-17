from chordal_wip.scales import Scale, Chord


scale_ref = Scale("C", "ionian")
print("C ionian:", scale_ref.notes)

chord_generator = Chord(scale_ref)
# print(chord_generator)


scale = Scale("F#", "mixolydian")
print("F mixolydian:", scale.notes)
