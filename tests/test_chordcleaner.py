import numpy as np
from chordal_wip.chordcleaner import ChordCleaner
import pandas as pd

cc = ChordCleaner()


def test_clean_spaces():
    test = "CMaj7 GMaj7   Am9                   F13"

    actual = cc._clean_spaces(test)
    expected = "CMaj7 GMaj7 Am9 F13"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_rm_symbols():
    test = "CMaj7(13) {GMaj7} [Am9[]] F7(13) A* B |Em"

    actual = cc._rm_symbols(test)
    expected = "CMaj7(13) GMaj7 Am9 F7(13) A B Em"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_standardize_chords():
    test = "Am5- A° A+ A#+ A7(13+) A7(11-) A#- A5- Ano3 Ano5 A(no3) A(no5"

    actual = cc._standardize_chords(test)
    expected = "Adim Adim Aaug A#aug A7(13#) A7(11b) A#dim Adim A A A A"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_clean_double_extensions():
    test = "A7/13 D7add9 E9/11 Cmaj7add6"

    actual = cc._clean_double_extensions(test)
    expected = "A7(13) D7(9) E9(11) Cmaj7(6)"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_negative_selection():
    test = pd.Series(
        [
            "Amin Amin Amin",
            "Amin Amin outro",
            "intro: E|--------6-- remove_this",
            "k k k k k k k",
        ]
    )

    actual = cc._negative_selection(test)
    expected = pd.Series(["Amin Amin Amin", "Amin Amin", "", "k k k k k k k"])
    assert actual.equals(expected), f"Expected {expected}, got {actual}"
