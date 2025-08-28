from chordal_wip.scales import ChordProgression, Scale, Chord


scale_ref = Scale("C", "ionian")
# print("C ionian:", scale_ref.notes)

chord = Chord(scale_ref)
# print(vars(chord))

chord_progression = ChordProgression(n_chords=4, chord=chord)

# print(vars(chord_progression))
dd = chord_progression.progression
# print([chord for chord in dd if chord["name"] == "tonic"])
# print(vars(chord_progression))
# [d["name"].values() for d in dd.values()]
# lst = [{"a": "str1", "b": 1}, {"a": "str2", "b": 2}, {"a": "str3", "b": 3}]

# print(sum(d["b"] for d in lst))
# print([sum(v for v in d["b"]) for d in lst])

# print(vars(chord_progression))

# scale = Scale("F#", "mixolydian")
# print("F mixolydian:", scale.notes)
