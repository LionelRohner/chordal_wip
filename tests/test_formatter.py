import pandas as pd
from chordal_wip.chordformatter import ChordFormatter
from pandas.testing import assert_series_equal


frmtr = ChordFormatter()


def test_formatter():
    cf = ChordFormatter()
    chords = pd.DataFrame(
        {
            "chords": [
                "C#(q3:m)/A F#(q3:maj)/F G#(q3:m)",
                "F(q3:maj)(q5:aug)(q7:m)",
                "G#(q3:sus2) G#(q3:m) C#(q3:m)",
            ]
        }
    )

    actual_simplified = chords["chords"].apply(cf.format)
    expected_simplified = pd.Series(
        ["C#m F#maj G#m", "Fmaj", "G#maj G#m C#m"], name="chords"
    )

    (
        assert_series_equal(actual_simplified, expected_simplified),
        (f"Expected {expected_simplified}, got {actual_simplified}"),
    )
