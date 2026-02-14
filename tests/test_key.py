from chordal_wip.scales import get_ref_scales
from chordal_wip.key import KeyPredictor


def test_C_ionian_key_prediction():
    progression = "Cmaj Gmaj Am Fmaj Cmaj Fmaj Cmaj Fmaj Cmaj Gmaj Am Fmaj"

    reference = get_ref_scales()

    kp = KeyPredictor(progression, reference).top_scale

    actual_key = f"{kp['key']} {kp['mode']}"
    expected_key = "C ionian"
    assert actual_key == expected_key, (
        f"Expected {expected_key}, got {actual_key}"
    )


def test_come_together_beatles_key_prediction():
    # TODO: Fix use of non standard chord notation, e.g. Dm instead of Dmin and A instead of Amaj
    progression = "Dm Dm A7 G7 Dm Dm A7 G7 Bm A G A Dm Dm A7 G7 Bm A G A Dm Dm A7 G7 Bm A G A Dm"

    reference = get_ref_scales()

    kp = KeyPredictor(progression, reference).top_scale

    actual_key = f"{kp['key']} {kp['mode']}"
    expected_key = "D aeolian"
    assert actual_key == expected_key, (
        f"Expected {expected_key}, got {actual_key}"
    )
