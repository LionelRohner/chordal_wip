from chordal_wip.chordcleaner import ChordCleaner
import pandas as pd

cc = ChordCleaner()


def test_clean_spaces():
    test = "Cmaj7 Gmaj7   Am9                   F13"

    actual = cc._clean_spaces(test)
    expected = "Cmaj7 Gmaj7 Am9 F13"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_rm_symbols():
    test = "Cmaj7(13) {Gmaj7} [Am9[]] F7(13) A* B |Em"

    actual = cc._rm_symbols(test)
    expected = "Cmaj7(13) Gmaj7 Am9 F7(13) A B Em"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_standardize_chords():
    test = "Am5- A° A+ A#+ A7(13+) A7(11-) A#- A5- Ano3 Ano5 A(no3) A(no5"

    actual = cc._standardize_chords(test)
    expected = "Adim Adim Aaug A#aug A7(13#) A7(11b) A#dim Adim A A A A"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_standardize_chords_empty():
    assert cc._standardize_chords("") == ""


def test_clean_double_extensions():
    test = "A7/13 D7add9 E9/11 Cmaj7add6"

    actual = cc._clean_double_extensions(test)
    expected = "A7(13) D7(9) E9(11) Cmaj7(6)"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_negative_selection():
    test = pd.Series(
        [
            "Am Am Am",
            "Am Am outro",
            "intro: E|--------6-- remove_this",
            "k k k k k k k",
        ]
    )

    actual = cc._negative_selection(test)
    expected = pd.Series(["Am Am Am", "Am Am", "", "k k k k k k k"])
    assert actual.equals(expected), f"Expected {expected}, got {actual}"


def test_filter_chords():
    test = "A#M7 A#maj7 A#maj A#maj7(b13) A Amaj6(9) C7sus4 Fb7sus4(b5, b13) A7(11,13) Xm7 PM7"

    actual = cc._filter_chords(test)
    expected = "A#M7 A#maj7 A#maj A#maj7(b13) A Amaj6(9) C7sus4 Fb7sus4(b5, b13) A7(11,13)"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_filter_chords_no_valid_chords():
    assert cc._filter_chords("This is not a chord") == ""
    assert cc._filter_chords("Chorus and Bridge or chorus And bridge!") == ""


def test_clean_wo_threshold():
    # Bypass negative selection
    cc = ChordCleaner(threshold=None)

    test = pd.Series(
        [
            # TODO: Test for Amin?
            "Am7/G Am/F# Am (Am - G) AbÂº",
            # Parenthesis and dash handling
            "(Am - G - F - E) F G (Am - G) E7 Am ",
            # C7M should be Cmaj7
            "Inro C7M G Am Em C7M G D4 D",
            # Complex Chords and random words
            "Intro: F#m7 D2 F#m7 D4",
            # TODO: D4/7 and other fancy chords
            # TODO: Fix Bridge >> B issue
            # "Em Dmaj7(9) Bridge C C D Em",
            "Intro: Em Bm ( C ) Am C (2x) Em ",
            "Intro: Gm - Dm - C - C x2 C* Gm A# C* Gm",
        ]
    )

    actual = cc.clean(test)

    expected = pd.Series(
        [
            # Use Am instead of Am and Fmaj instead of F. But Am7/G should not be Am7/Gmaj
            "Am7/G Am/F# Am Am G Ab",
            # Parenthesis and dash handling
            "Am G F E F G Am G E7 Am",
            # C7M should be Cmaj7
            "Cmaj7 G Am Em Cmaj7 G D4 D",
            # Complex chords
            "F#m7 D2 F#m7 D4",
            # "Em Dmaj7(9) C C D Em",
            "Em Bm C Am C Em",
            "Gm Dm C C C Gm A# C Gm",
        ]
    )

    assert actual.equals(expected), f"Expected {expected}, got {actual}"


def test_clean_tabs():
    cc = ChordCleaner(threshold=None)

    test = pd.Series(
        [
            " B|---4-4-4----3-3-?-3s4-------| G|-------------3?--??--------|	",
            "E|---------------------------| E|---------------|		 ",
            "E|-----------------------------| D# A# Cm Ab Cm Dm ",
            "B|--5/7---5-5-5---7--| G|-------------------|",
            "	 		Intro: A# E A F hide this tab E B|----------------5-5-5-5--------|",
            "A|---5-4-3-------------------------------------| E|------------5-4-3------------------4-3-0-----| D Fmaj7(9)",
            "D4 D B|--12-10v-| G B|------12--| C G/B D D4 E|--10-10--| B|--10-10--| G C G/B E|--------10----10|",
            "B|--10-10----10---| D D4 D B|-10-10-10----------13----13---12---11p10---------------------------------|",
            "G|---------------------------------------------------13p12p10-12-----------| ",
            "A# C D SOLO: B|--9s10-10-10-10-10--13b15--13b15--15r13---11---13---11-13b15-------| ",
            "E|-------------5--4--3------| E E A E|------5-3--2--0----| D4 D G C G/B",
        ]
    )

    actual = cc.clean(test)

    expected = pd.Series(
        [
            "",
            "",
            "D# A# Cm Ab Cm Dm",
            "",
            "A# E A F E",
            "D Fmaj7(9)",
            "D4 D G C G/B D D4 G C G/B",
            "D D4 D",
            "",
            "A# C D",
            "E E A D4 D G C G/B",
        ]
    )

    assert actual.equals(expected), f"Expected {expected}, got {actual}"
