from chordal_wip.scales import MarkovChordProgression, Scale, Chord

scale_ref = Scale("C", "dorian")
print(scale_ref.scales_dict.keys().tolist)
# print("C ionian:", scale_ref.notes)
chord = Chord(scale_ref)
# print(list(chord.data["triads"]))
chord_progression = MarkovChordProgression(n_chords=4, chord=chord)
# print(vars(chord_progression))
