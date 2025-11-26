import numpy as np
from chordal_wip.chordcleaner import ChordCleaner


cc = ChordCleaner()


def test_clean_spaces():
    test = "CMaj7 GMaj7   Am9                   F13"

    actual = cc.clean_spaces(test)
    expected = "CMaj7 GMaj7 Am9 F13"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_clean_spaces():
    test = "CMaj7(13) {GMaj7} [Am9[]] F7(13)"

    actual = cc.rm_parentheses(test)
    expected = "CMaj7(13) GMaj7 Am9 F7(13)"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_standardize_chords():
    test = "Am5- A° A* A+ A#+ A7(13+) A7(11-) A#- A5-"

    actual = cc.standardize_chords(test)
    expected = "Adim Adim A Aaug A#aug A7(13#) A7(11b) A#dim Adim"

    assert actual == expected, f"Expected {expected}, got {actual}"
