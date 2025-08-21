from chordal_wip.scales import Scale, Chord


scale_ref = Scale("C", "ionian")
# print("C ionian:", scale_ref.notes)

chord = Chord(scale_ref)
print(vars(chord))


# scale = Scale("F#", "mixolydian")
# print("F mixolydian:", scale.notes)
