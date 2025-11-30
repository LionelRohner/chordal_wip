import re


class ChordCleaner:
    """
    A class for data cleanup for lluccardoner/melodyGPT-song-chords-text-1
    """

    def __init__(self, threshold=3):
        self.threshold = threshold

    def _clean_spaces(self, txt):
        """Replace multiple whitespaces with a single space."""
        # replace n whitespaces with a single clean_spaces
        txt = re.sub(r"\s+", " ", txt)
        return txt.strip()

    # TODO: What to do with normal parenthesis?
    def _rm_symbols(self, txt):
        """Remove symbols, such as parentheses, asterisk and pipes."""
        # Remove parentheses and their contents
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

    def _negative_selection(self, txt):
        counts = txt.str.split(" ").explode().value_counts()

        counts_filtered = counts[counts <= self.threshold].index
        # re.sub acts sequentially, hence this sorting avoids filtering substrings
        counts_filtered = sorted(counts_filtered, key=len, reverse=True)
        counts_filtered = [re.escape(pattern) for pattern in counts_filtered]

        neg_selection_patterns = f"({('|').join(counts_filtered)})"
        txt = txt.apply(lambda x: re.sub(neg_selection_patterns, "", x).strip())
        return txt

    def _clean_double_extensions(self, txt):
        """ """
        # Convert slash notation to parenthesis notation
        slash_pattern = r"([A-G]{1}[#b]?[Majmdinsu]{0,3}\d{1,2})/(\d{1,2})"
        txt = re.sub(slash_pattern, r"\1(\2)", txt)
        # Convert add notation to parenthesis notation
        add_pattern = r"([A-G]{1}[#b]?[Majmdinsu]{0,3}\d{1,2})add(\d{1,2})"
        txt = re.sub(add_pattern, r"\1(\2)", txt)
        return txt

    def _filter_chords(self, txt):
        """Filter chords using a regex pattern."""
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
        chord_series = chord_series.apply(self._rm_symbols)
        chord_series = chord_series.apply(self._standardize_chords)
        chord_series = chord_series.apply(self._clean_spaces)
        chord_series = chord_series.str.strip()
        chord_series = chord_series[chord_series != ""]

        return chord_series
