import re


class ChordCleaner:
    """
    A class for data cleanup for lluccardoner/melodyGPT-song-chords-text-1
    """

    def __init__(self, threshold=3):
        self.threshold = threshold

    def clean_spaces(self, txt):
        """Replace multiple whitespaces with a single space."""
        # replace n whitespaces with a single clean_spaces
        return re.sub(r"\s+", " ", txt)

    # TODO: What to do with normal parenthesis?
    def rm_parentheses(self, txt):
        """Remove parentheses."""
        # Remove parentheses and their contents
        return re.sub(r"(\[|\]|\{|\})", "", txt)

    def standardize_chords(self, txt):
        """Apply standardization rules to chord notations."""
        # Convert "m5-" to "dim"
        txt = re.sub(r"m5-", "dim", txt)
        # Convert "°" to "dim"
        txt = re.sub(r"°", "dim", txt)
        # Remove "*"
        txt = re.sub(r"\*", "", txt)
        # Convert "+" to "aug" if it comes after an uppercase letter
        txt = re.sub(r"([A-G][#b]?)\+", r"\1aug", txt)
        # Convert "+" to "#" if it comes after a number
        txt = re.sub(r"([0-9])(\+)", r"\1#", txt)
        # Convert "-" to "dim" after a 5 or an uppercase letter
        txt = re.sub(r"([A-G][#b]?)-", r"\1dim", txt)
        txt = re.sub(r"5-", "dim", txt)
        # Convert "-" to "b" after any number that is not 5
        txt = re.sub(r"([0-9])(-)(?![0-9])", r"\1b", txt)
        return txt

    # Max length filter!
