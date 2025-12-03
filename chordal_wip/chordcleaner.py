import re


class ChordCleaner:
    """
    A class for cleaning and standardizing chord notations in text data.
    """

    def __init__(self, threshold=3):
        self.threshold = threshold

    def _clean_spaces(self, txt):
        """Remove specific symbols such as parentheses, asterisks, and pipes."""
        txt = re.sub(r"\s+", " ", txt)
        return txt.strip()

    def _rm_symbols(self, txt):
        """Replace multiple whitespace characters with a single space."""
        return re.sub(r"(\[|\]|\{|\}|\*|\|)", "", txt)

    def _standardize_chords(self, txt):
        """Apply standardization rules to chord notations."""
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
        return txt

    def _negative_selection(self, chord_series):
        """
        Filters the input text by removing words that appear a number of times
        less than or equal to a predefined threshold.

        This method counts the occurrences of each word in the input text,
        filters out the words that meet the filtering criteria, and then
        removes those words from the text. The removal of words is done in
        such a way to avoid matching substrings.

        Args:
            chord_series (pd.Series): A pandas Series containing text data where
                             each entry is a string to be processed.

        Returns:
            pd.Series: A new Series with filtered text entries where words
                        that appeared equal to or below the threshold have
                        been removed.
        """
        counts = chord_series.str.split(" ").explode().value_counts()

        counts_filtered = counts[counts <= self.threshold].index
        # re.sub acts sequentially, hence this sorting avoids filtering substrings
        counts_filtered = sorted(counts_filtered, key=len, reverse=True)
        counts_filtered = [re.escape(pattern) for pattern in counts_filtered]

        neg_selection_patterns = f"({('|').join(counts_filtered)})"
        chord_series = chord_series.apply(
            lambda x: re.sub(neg_selection_patterns, "", x).strip()
        )
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
        extension = r"(?:2|4|5|6|7|9|10|11|13)?"
        modifier = r"(?:[ADGIMNOSUadgimnosu]{0,3}[24]?)?"
        extension_2 = rf"(?:\((?:{accidental}{extension},?\s*){{1,2}}\))?"
        slash = rf"(?:\/{root}{accidental})?"
        chord_anatomy = rf"{root}{accidental}{quality}{extension}{modifier}{extension_2}{slash}"

        chords = re.findall(chord_anatomy, txt)
        return " ".join(chords)

    # Tab filter >> maybe use "-*"
    # Max length filter?

    def clean(self, chord_series):
        """Process and clean the provided Series of chord notations."""

        # Negative selection
        chord_series = self._negative_selection(chord_series)

        # General clean-up
        chord_series = chord_series.apply(self._rm_symbols)
        chord_series = chord_series.apply(self._standardize_chords)
        chord_series = chord_series.apply(self._clean_spaces)
        chord_series = chord_series.str.strip()
        chord_series = chord_series[chord_series != ""]

        # Positive selection
        chord_series = chord_series.apply(self._filter_chords)

        return chord_series
