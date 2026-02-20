from chordal_wip.chordcleaner import ChordCleanerToken

cc = ChordCleanerToken(char_threshold=10)


def test_tokenize():
    test = " X1 X2  X3^X4 X5%X6  (X7,X8)    X9 "

    actual = cc._tokenize(test)
    expected = ["X1", "X2", "X3", "X4", "X5", "X6", "(X7", "X8)", "X9"]

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_erode_pos():
    test = "(((((Cmaj"

    actual = cc._erode(test)
    expected = "Cmaj"

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_erode_neg():
    test = "this-is-not-a-chord"

    actual = cc._erode(test)
    expected = ""

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_select_long():
    test = "this-is-longer-than-limit"

    actual = cc._select(test)
    expected = False

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_select_tab():
    test = "A|-3-2-0---x------|"

    actual = cc._select(test)
    expected = False

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_select_pos():
    test = "Amin7(9)"

    actual = cc._select(test)
    expected = True

    assert actual == expected, f"Expected {expected}, got {actual}"


def test_():
    test = "XX Amin7(9) E:---- ((Cmaj"

    actual = cc.clean(test)
    expected = "Amin7(9) Cmaj"

    assert actual == expected, f"Expected {expected}, got {actual}"
