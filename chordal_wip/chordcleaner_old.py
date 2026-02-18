import re
from time import perf_counter


class ChordCleaner:
    """
    A class for cleaning and standardizing chord notations in text data.
    """

    def __init__(self, threshold=3):
        self.threshold = threshold

    def _remove_tab_notation(self, txt):
        """Remove tablature notation from the text."""
        # This pattern looks for sequences with many dashes and numbers
        tab_pattern = r"\b[A-G]#?b?\|[-0-9hpsbrv?\/]+[\| ]+"
        return re.sub(tab_pattern, "", txt)

    def _clean_spaces(self, txt):
        """Remove specific symbols such as parentheses, asterisks, and pipes."""
        txt = re.sub(r"\s+", " ", txt)
        return txt.strip()

    def _rm_symbols(self, txt):
        """Replace multiple whitespace characters with a single space."""
        return re.sub(r"(\[|\]|\{|\}|\*|\|)", "", txt)

    def _standardize_chords(self, txt):
        """Apply standardization rules to chord notations."""
        # Convert major 7th chords from "C7M" to "Cmaj7"
        txt = re.sub(r"([A-G][#b]?)7M", r"\1maj7", txt)
        # Convert "m5-" to "dim"
        txt = re.sub(r"m5-", "dim", txt)
        # Convert "°" to "dim"
        txt = re.sub(r"°", "dim", txt)
        # Convert "-" to "dim" after a 5 or an uppercase letter
        txt = re.sub(r"([A-G][#b]?)-", r"\1dim", txt)
        txt = re.sub(r"5-", "dim", txt)
        # Convert "+" to "aug" if it comes after an uppercase letter
        txt = re.sub(r"([A-G][#b]?)\+", r"\1aug", txt)
        # Convert "+" to "#" if it comes after a number
        txt = re.sub(r"([0-9])(\+)", r"\1#", txt)
        # Convert "-" to "b" after any number that is not 5
        txt = re.sub(r"([0-9])(-)(?![0-9])", r"\1b", txt)
        # Remove no3 and no5 qaulities
        txt = re.sub(r"\(?no[357]{1}\)?", "", txt)

        # TODO: RM, obsolete, right?
        # Convert minor chords from "Cm" to "Cmin"
        # txt = re.sub(r"([A-G][#b]?)m\b", r"\1min", txt)
        # Convert major chords from "C" to "Cmaj" when not followed by other chord symbols
        # txt = re.sub(r"\b([A-G][#b]?)(?![0-9a-zA-Z])", r"\1maj", txt)

        return txt

    def _negative_selection(self, chord_series):
        """
        Filters the input text by removing words that appear a number of times
        less than or equal to a predefined threshold.

        This method counts the occurrences of each word in the input text,
        filters out the words that are below a threshold (default = 3), and then
        removes those words from the text.

        Args:
            chord_series (pd.Series): A pandas Series containing text data where
                             each entry is a string to be processed.

        Returns:
            pd.Series: A new Series with filtered text entries where words
                        that appeared equal to or below the threshold have
                        been removed.
        """
        if self.threshold is None:
            return chord_series

        word_count = chord_series.str.split(" ").explode().value_counts()
        # Sets have O(1) lookup time
        rare_words = set(word_count[word_count <= self.threshold].index)

        def filter_rare_words(txt):
            words = txt.split()
            filtered_words = [word for word in words if word not in rare_words]
            return " ".join(filtered_words)

        chord_series = chord_series.apply(filter_rare_words)
        return chord_series

    def _clean_double_extensions(self, txt):
        """
        Standardize chord notation with double extensions by placing all of them in parentheses.
        Some example:
            - A7add13 is converted to A7(13)
            - C7/13 is converted to C7(13)
            - C6/9 is converted to C6(9), which is not common but avoids issues with identification of slash chords
        """
        # Convert slash notation to parenthesis notation
        slash_pattern = r"([A-G]{1}[#b]?[Majmdinsu]{0,3}\d{1,2})/(\d{1,2})"
        txt = re.sub(slash_pattern, r"\1(\2)", txt)
        # Convert add notation to parenthesis notation
        add_pattern = r"([A-G]{1}[#b]?[Majmdinsu]{0,3}\d{1,2})add(\d{1,2})"
        txt = re.sub(add_pattern, r"\1(\2)", txt)
        return txt

    def _filter_chords(self, txt):
        """Extract and filter valid chord notations from the given text."""
        # Anatomy of a chord
        root = "[A-G]{1}"
        accidental = "[#b]?"
        quality = "[AIJMMNaijmn]{0,3}"
        # quality = r"(?:maj|min|dim|aug|sus|add|m|M)?"
        extension = r"(?:2|4|5|6|7|9|10|11|13)?"
        modifier = r"(?:[ADGIMNOSUadgimnosu]{0,3}[24]?)?"
        extension_2 = rf"(?:\((?:{accidental}{extension},?\s*){{1,2}}\))?"
        slash = rf"(?:\/{root}{accidental})?"
        chord_anatomy = rf"{root}{accidental}{quality}{extension}{modifier}{extension_2}{slash}"

        # chord_anatomy = rf"(?<![A-Za-z])({chord_anatomy})(?![A-Za-z])"

        chords = re.findall(chord_anatomy, txt)
        return " ".join(chords)

    # Tab filter >> maybe use "-*"
    # Max length filter?

    def clean(self, chord_series):
        """Process and clean the provided Series of chord notations."""

        # Tab Removal
        start = perf_counter()
        chord_series = chord_series.apply(self._remove_tab_notation)
        print(f"_remove_tab_notation chord_series :\n {chord_series}")
        stop = perf_counter()
        # print(f"[_remove_tab_notation] Elapsed: {(stop - start):.5f}")

        # Negative selection
        start = perf_counter()
        chord_series = self._negative_selection(chord_series)
        print(f"_negative_selection chord_series :\n {chord_series}")
        stop = perf_counter()
        # print(f"[_negative_selection] Elapsed: {(stop - start):.5f}")

        # General clean-up
        start = perf_counter()
        chord_series = chord_series.apply(self._rm_symbols)
        print(f"_rm_symbols chord_series :\n {chord_series}")
        stop = perf_counter()
        # print(f"[_rm_symbols] Elapsed: {(stop - start):.5f}")

        start = perf_counter()
        chord_series = chord_series.apply(self._standardize_chords)
        print(f"_standardize_chords chord_series :\n {chord_series}")
        stop = perf_counter()
        # print(f"[_standardize_chords] Elapsed: {(stop - start):.5f}")

        start = perf_counter()
        chord_series = chord_series.apply(self._clean_spaces)
        print(f"_clean_spaces chord_series :\n {chord_series}")
        stop = perf_counter()
        # print(f"[_clean_spaces] Elapsed: {(stop - start):.5f}")

        start = perf_counter()
        chord_series = chord_series.str.strip()
        print(f"strip chord_series :\n {len(chord_series)}")
        stop = perf_counter()
        # print(f"[strip] Elapsed: {(stop - start):.5f}")

        # TODO: move somewhere else - the dimensions of the input should remain
        # start = perf_counter()
        # chord_series = chord_series[chord_series != ""]
        # print(f"chord_series :\n {len(chord_series)}")
        # stop = perf_counter()
        # print(f"[rm empty strings] Elapsed: {(stop - start):.5f}")

        # Positive selection
        no_pos_selection = False
        if no_pos_selection:
            start = perf_counter()
            chord_series = chord_series.apply(self._filter_chords)
            print(f"_filter_chords chord_series :\n {chord_series}")
            stop = perf_counter()
            print(f"[_filter_chords] Elapsed: {(stop - start):.6f}")

        return chord_series


# Issues to fix ----
# Before: B|--5/7---5-5-5---7--| G|-------------------| D|-------------------| A|-------------------| E|-------------------| Am Am7/G Am/F# Am7/G Am Am7/G Am/F# Am7/G (Am - G) F G F G (Am - G) F G AbÂº Am G F E7 Am G F E7 Am Am7/G Am/F# Am7/G Am Am7/G Am/F# Am7/G (Am - G) F G F G (Am - G) F G AbÂº Am G F E7 Am G F E7 Am G F E7 Am G F E7 F G F G AbÂº (Am - G - F - E) F G F G (Am - G) F G E7 Am G F E7 Am G F E7 Am G F E7 Am G F E7 Am G F E7
# After: Gdim Ddim Adim Edim Am Am7/G Am/F# Am7/G Am Am7/G Am/F# Am7/G Am G F G F G Am G F G Ab Am G F E7 Am G F E7 Am Am7/G Am/F# Am7/G Am Am7/G Am/F# Am7/G Am G F G F G Am G F G Ab Am G F E7 Am G F E7 Am G F E7 Am G F E7 F G F G Ab Am G F E F G F G Am G F G E7 Am G F E7 Am G F E7 Am G F E7 Am G F E7 Am G F E7i
#
# Somehow G|----- and D|----- become Gdim and Ddim....

import pandas as pd

cc = ChordCleaner(threshold=None)


test = pd.Series(["C Bridge E", "Chorus and Bridge or chorus And bridge!"])

print(cc.clean(test))
