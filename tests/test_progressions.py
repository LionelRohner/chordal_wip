import numpy as np
from chordal_wip.scales import Scale, Chord, ChordProgression


def test_progression_generation():
    root_note = "C"
    scale_type = "ionian"
    scale = Scale(root_note, scale_type)
    chord = Chord(scale)
    progression = ChordProgression(n_chords=4, chord=chord)

    # Expected triads
    expected_tonic = any(chord["name"] == "tonic" for chord in progression.progression)
    assert expected_tonic, (
        f"Expected the tonic chord in the progression, but it is absent"
    )
