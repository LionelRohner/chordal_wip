import numpy as np
import pytest
from chordal_wip.scales import Scale  # Adjust import path as needed

def test_ionian_scale_generation():
    # Test C Ionian (C Major)
    root_note = "C"
    scale_type = "ionian"
    scale = Scale(root_note, scale_type)
    expected_notes = np.array(["C", "D", "E", "F", "G", "A", "B"])
    assert np.array_equal(scale.notes, expected_notes), \
        f"Expected {expected_notes}, got {scale.notes}"

