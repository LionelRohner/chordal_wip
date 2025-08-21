import numpy as np

# import pytest
from chordal_wip.scales import Scale, Chord


def test_C_ionian_chord_generation():
    root_note = "C"
    scale_type = "ionian"
    scale = Scale(root_note, scale_type)
    chord = Chord(scale)

    # Expected triads
    expected_progression = np.array(["Cmaj", "Dmin", "Emin", "Fmaj", "Gmaj", "Amin", "Bdim"])
    assert np.array_equal(chord.chord_base_progression, expected_progression), (
        f"Expected {expected_progression}, got {chord.chord_base_progression}"
    )

    # Expected 7th chords
    expected_progression = np.array(["Cmaj7", "Dmin7", "Emin7", "Fmaj7", "G7", "Amin7", "Bmin7♭5"])
    assert np.array_equal(chord.chord_7th_progression, expected_progression), (
        f"Expected {expected_progression}, got {chord.chord_7th_progression}"
    )

def test_D_dorian_chord_generation():
    root_note = "D"
    scale_type = "dorian"
    scale = Scale(root_note, scale_type)
    chord = Chord(scale)

    # Expected triads
    expected_progression = np.array(["Dmin", "Emin", "Fmaj", "Gmaj", "Amin", "Bdim", "Cmaj"])
    assert np.array_equal(chord.chord_base_progression, expected_progression), (
        f"Expected {expected_progression}, got {chord.chord_base_progression}"
    )

    # Expected 7th chords
    expected_progression = np.array(["Dmin7", "Emin7", "Fmaj7", "G7", "Amin7", "Bmin7♭5", "Cmaj7"])
    assert np.array_equal(chord.chord_7th_progression, expected_progression), (
        f"Expected {expected_progression}, got {chord.chord_7th_progression}"
    )


def test_F_myxolydian_chord_generation():
    root_note = "F#"
    scale_type = "mixolydian"
    scale = Scale(root_note, scale_type)
    chord = Chord(scale)

    # Expected triads
    expected_progression = np.array(["F#maj", "G#min", "A#dim", "Bmaj", "C#min", "D#min", "Emaj"])
    assert np.array_equal(chord.chord_base_progression, expected_progression), (
        f"Expected {expected_progression}, got {chord.chord_base_progression}"
    )

    # Expected 7th chords
    expected_progression = np.array(["F#7", "G#min7", "A#min7♭5", "Bmaj7", "C#min7", "D#min7", "Emaj7"])
    assert np.array_equal(chord.chord_7th_progression, expected_progression), (
        f"Expected {expected_progression}, got {chord.chord_7th_progression}"
    )
