from chordal_wip.chordcleaner import ChordCanonizer
import pytest

cc = ChordCanonizer()


def test_decompose_1():
    test = "Ebmaj7add9/G"

    actual = cc._decompose(test)
    expected = {
        "root": "Eb",
        "quality": "maj",
        "extensions": ["7"],
        "adds": ["add9"],
        "sus": None,
        "alterations": [],
        "slash": "G",
        "unclear": [],
    }
    assert actual == expected, f"Expected {expected}, got {actual}"


# TODO: Cave!!! E13- should be Em13 instead of E13b, but E13
@pytest.mark.skip(reason="Skipping this test for now")
def test_decompose_2():
    test = "E13-"

    actual = cc._decompose(test)
    expected = {
        "root": "E",
        "quality": "m",
        "extensions": ["13"],
        "adds": [],
        "sus": None,
        "alterations": [],
        "slash": None,
    }
    assert actual == expected, f"Expected {expected}, got {actual}"


def test_canonicalize_length_conservation():
    test = "not_chord exit progression lit effect"

    actual = cc.canonicalize(test)
    expected = ["X", "X", "X", "X", "X"]

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_canonicalize_triads():
    test = "Emin Em EMaj Emaj EM"

    actual = cc.canonicalize(test)
    expected = ["Em", "Em", "E", "E", "E"]

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_canonicalize_7th():
    test = "Emaj7 Emin7 Em7 E7M EM7 E7"

    actual = cc.canonicalize(test)
    expected = ["Emaj7", "Em7", "Em7", "Emaj7", "Emaj7", "E7"]

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_canonicalize_7th_2():
    test = "Gmaj9 Gmaj7 Gmaj7(9+)"

    actual = cc.canonicalize(test)
    expected = ["Gmaj9", "Gmaj7", "Gmaj7(9#)"]

    assert actual == expected, f"Expected {expected}, got {actual}"
