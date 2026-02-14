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


def test_filter_chords_no_valid_chords():
    assert cc._filter_chords("This is not a chord") == ""


# Apply all the above to Series
def test_clean_1():
    # negative selection runs on a threshold of 3, which is inconvenient for manually written tests.
    cc = ChordCleaner(threshold=1)
    test = pd.Series(
        [
            "Intro: F#m7 D2 F#m7 D2 F#m7 D2 E F#m7 A/C# E D2 E F#m7 Bm A/C# D2 E G",
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
            "F#m7 D2 F#m7 D2 F#m7 D2 E F#m7 A/C# E D2 E F#m7 Bm A/C# D2 E G",
            "Em D C C D Em Em D C C D Em Em D C Am D Em G C Am D Bm",
            "Em Bm Am C Em Bm Am C Em Bm Am C Bm Em Bm Am C Em Bm Em Am Em Bm Am C Em Bm Am C",
            "Gm Dm C C Gm Dm C C Gm Dm C C Gm A# C Gm A# C Gm A# C Gm A# C",
        ]
    )
    assert actual.equals(expected), f"Expected {expected}, got {actual}"


def test_clean_2():
    # Bypass negative selection
    cc = ChordCleaner(threshold=None)

    test = pd.Series(
        [
            # Make sure these are not intrepreted as chords!
            "B|--5/7---5-5-5---7--| G|-------------------| D|-------------------|",
            # Use Amin instead of Am and Fmaj instead of F
            "Am Am7/G Am/F# Am7/G Am Am7/G Am/F# Am7/G (Am - G) F G F F G AbÂº Am",
            # Parenthesis and dash handling
            "(Am - G - F - E) F G F G (Am - G) F G E7 Am G F E7 Am G F E7 Am G F ",
            # C7M should be Cmaj7
            "Inro C7M G Am Em C7M G D4 D C7M G Am Em C7M G D4 D C7M G Am Em C7M",
        ]
    )

    actual = cc.clean(test)

    expected = pd.Series(
        [
            "",
            # Use Amin instead of Am and Fmaj instead of F. But Amin7/G should not be Amin7/Gmaj
            "Amin Amin7/G Am/F# Am7/G Am Am7/G Am/F# Am7/G (Am - G) F G F F G AbÂº Am",
            # Parenthesis and dash handling
            "(Am - G - F - E) F G F G (Am - G) F G E7 Am G F E7 Am G F E7 Am G F ",
            # C7M should be Cmaj7
            "Inro C7M G Am Em C7M G D4 D C7M G Am Em C7M G D4 D C7M G Am Em C7M",
        ]
    )

    assert actual.equals(expected), f"Expected {expected}, got {actual}"


def test_clean_3():
    cc = ChordCleaner(threshold=None)

    test = pd.Series(
        [
            " B|---4-4-4----3-3-?-3s4--------------| G|----------------3?--??-------------|	 ",
            "E|-----------------------------------| E|----------------------------------|		 ",
            "B|---4-4-4----3-3-?-3---------------| G|----------------3?--??------------|	 ",
            "D|-----------------3----------------| A|-3-3-3-3--1-1-1-----3-------------| ",
            "E|----------------------------------| D# A# Cm Ab Cm Dm D# A# Cm Dm D# Dm D# ",
            "	 		Intro: A# E A F hide this tab E B|-------------------5-5-5-5-5-5---------------|",
            "A|---5-4-3-------------------------------------| E|------------5-4-3------------------4-3-0-----| D"
            "D4 D B|--12-10v-| G B|------12--| C G/B D D4 D E|--10-10--| B|--10-10--| G C G/B E|--------10----10|"
            "B|--10-10----10---| D D4 D B|-10-10-10----------13----13---12---11p10---------------------------------|",
            "G|---------------------------------------------------13p12p10-12-----------| ",
            "A# C D SOLO: B|--9s10-10-10-10-10--13b15--13b15--15r13---11---13---11-13b15-------| "
            "E|-------------5--4--3------| E E E E E E A E|------5-3--2--0----| D D4 D G C G/B D D4",
        ]
    )

    actual = cc.clean(test)

    expected = pd.Series(
        [
            "",
            "",
            "",
            "",
            "D#maj A#maj Abmaj Cmin Dmin D#maj A#maj Cmin Dmin D#maj Dmin D#maj",
            "A#maj Emaj Amaj Fmaj E",
            "Dmaj",
            "D4 Dmaj Gmaj Cmaj G/B Dmaj D4 Dmaj Gmaj Cmaj G/B",
            "",
            "",
            "",
            "A#maj Cmaj Dmaj",
            "Emaj Emaj Emaj Emaj Emaj Emaj Amaj Dmaj D4 Dmaj Gmaj Cmaj G/B Dmaj D4",
        ]
    )

    assert actual.equals(expected), f"Expected {expected}, got {actual}"
