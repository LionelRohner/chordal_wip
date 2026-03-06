from chordal_wip.chordcleaner import ChordCanonizer

cc = ChordCanonizer()


def test_parse_1():
    test = "Ebmaj7add9/G"

    actual = cc._parse(test)
    expected = {
        "root": "Eb",
        "quality": "maj7",
        "extensions": [],
        "adds": ["add9"],
        "sus": None,
        "alterations": [],
        "slash": "G",
    }
    assert actual == expected, f"Expected {expected}, got {actual}"


def test_parse_2():
    test = "E13-"

    actual = cc._parse(test)
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
