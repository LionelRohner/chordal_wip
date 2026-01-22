import numpy as np
from chordal_wip.scales import Scale


def test_C_ionian_scale_generation():
    root_note = "C"
    scale_type = "ionian"
    scale = Scale(root_note, scale_type)
    expected_notes = np.array(["C", "D", "E", "F", "G", "A", "B"])
    assert np.array_equal(scale.notes, expected_notes), (
        f"Expected {expected_notes}, got {scale.notes}"
    )


def test_D_dorian_scale_generation():
    root_note = "D"
    scale_type = "dorian"
    scale = Scale(root_note, scale_type)
    expected_notes = np.array(["D", "E", "F", "G", "A", "B", "C"])
    assert np.array_equal(scale.notes, expected_notes), (
        f"Expected {expected_notes}, got {scale.notes}"
    )


def test_F_myxolydian_scale_generation():
    root_note = "F#"
    scale_type = "mixolydian"
    scale = Scale(root_note, scale_type)
    print(scale)
    expected_notes = np.array(["F#", "G#", "A#", "B", "C#", "D#", "E"])
    assert np.array_equal(scale.notes, expected_notes), (
        f"Expected {expected_notes}, got {scale.notes}"
    )
