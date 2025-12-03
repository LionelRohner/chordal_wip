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


def test_filter_chords():
    test = "A#M7 A#maj7 A#Maj A#Maj7(b13) A Amaj6(9) C7sus4 Fb7sus4(b5, b13) A7(11,13) Xmin7 PM7"

    actual = cc._filter_chords(test)
    expected = "A#M7 A#maj7 A#Maj A#Maj7(b13) A Amaj6(9) C7sus4 Fb7sus4(b5, b13) A7(11,13)"

    assert actual == expected, f"Expected {expected}, got {actual}"


# Apply all the above to Series
def test_clean():
    test = pd.Series(
        [
            "Intro: F#m7 D2 F#m7 D2 F#m7 D2 E F#m7 A/C# E D2 E F#m7 Bm A/C# D2 E",
            "Em D C C D Em Em D C C D Em Em D C Am D Em G C Am D Bm",
            "Intro: Em Bm Am C (2x) Em Bm Am C Em Bm Am C Bm Em Bm Am C Em Bm Em Am Em Bm Am ( C ) Em Bm Am ( C )",
            "Intro: Gm - Dm - C - C x2 Gm Dm C C Gm Dm C C Gm A# C* Gm A# C* Gm A# C* Gm A# C*",
            "B|-----------11----11--------------6---6-------------8---8--------8--------8------| ",
            "G|--------12----------12---------7-------7---------9-------9--------9--------9----| ",
        ]
    )

    actual = cc.clean(test)

    expected = pd.Series(
        [
            "Intro: F#m7 D2 F#m7 D2 F#m7 D2 E F#m7 A/C# E D2 E F#m7 Bm A/C# D2 E",
            "Em D C C D Em Em D C C D Em Em D C Am D Em G C Am D Bm",
            "Intro: Em Bm Am C (2x) Em Bm Am C Em Bm Am C Bm Em Bm Am C Em Bm Em Am Em Bm Am ( C ) Em Bm Am ( C )",
            "Intro: Gm - Dm - C - C x2 Gm Dm C C Gm Dm C C Gm A# C* Gm A# C* Gm A# C* Gm A# C*",
            "B|-----------11----11--------------6---6-------------8---8--------8--------8------| ",
            "G|--------12----------12---------7-------7---------9-------9--------9--------9----| ",
        ]
    )
    assert actual == expected, f"Expected {expected}, got {actual}"
