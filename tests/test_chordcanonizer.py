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


def test_num_sort():
    test = ["add9", "add2", "add13", "X"]

    actual = [cc._num_sort(i) for i in test]
    expected = [9, 2, 13, 999]

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


def test_canonicalize_aug():
    test = "C5+ C+5 C7+ Caug C+"

    actual = cc.canonicalize(test)
    expected = ["Caug5", "Caug5", "Caug7", "Caug", "Caug"]

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_canonicalize_7th():
    test = "Emaj7 Emin7 Em7 E7M EM7 E7"

    actual = cc.canonicalize(test)
    expected = ["Emaj7", "Em7", "Em7", "Emaj7", "Emaj7", "E7"]

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_canonicalize_7th_2():
    test = "Gmaj9 Gmaj7 Gmaj7(9+)"

    actual = cc.canonicalize(test)
    expected = ["Gmaj9", "Gmaj7", "Gmaj7(e:#9)"]

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_canonicalize_extensions():
    test = "C7/9- C9#11b13 C911+13-"

    actual = cc.canonicalize(test)
    expected = ["C7(e:b9)", "C9(e:#11,b13)", "C9(e:#11,b13)"]

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_canonicalize_extensions_edge_cases():
    """
    Leading accidentals "+" and "-" are not allowed.
    Trailing accidentals "#" and "b" are not allowed.
    Cave: Two trailing accidentals using "#" and "b" are wronly interpreted as valid cases, because of the above rules!
    """
    test = "C7/-9 C7/9b C7/9# C911#13b"

    actual = cc.canonicalize(test)
    expected = [
        "C7(u:-9)",  # Leading "-" is not expected in token splitting criteria
        "C7(e:b9)",  # TODO: find out why 9b is rotated
        "C7(e:#9)",  # TODO: find out why 9# is rotated
        "C9(e:11,#13)",  # Trailing # or b are not expected, hence it favors #13 instead of 11# and 13b.
    ]

    assert actual == expected, f"Expected {expected}, got {actual}"
