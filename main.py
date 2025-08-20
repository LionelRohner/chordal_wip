from chordal_wip.scales import Scale, Chord


scale_ref = Scale("C", "ionian")
# print("C ionian:", scale_ref.notes)

chord = Chord(scale_ref)
print(chord.chord_7th_progression)
print(chord.chord_base_progression)


# scale = Scale("F#", "mixolydian")
# print("F mixolydian:", scale.notes)
