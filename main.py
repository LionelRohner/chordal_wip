from chordal_wip.scales import MarkovChordProgression, Scale, Chord

scale_ref = Scale("C", "dorian")
# print("C ionian:", scale_ref.notes)
chord = Chord(scale_ref)
# print(list(chord.data["triads"]))
chord_progression = MarkovChordProgression(n_chords=4, chord=chord)
# print(chord_progression.progression)
