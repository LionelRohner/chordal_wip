import re


class ChordCleaner:
    """
    A class for cleaning and standardizing chord notations in text data.
    """

    def __init__(self, freq_threshold=None, char_threshold=20):
        self.freq_threshold = freq_threshold
        self.char_threshold = char_threshold

    # Tokenize ----
    def _split_strings(self, txt):
        # Note: Do not include - since there are often tabs in the chord data
        split_comma_pattern = r"(?<=\S),(?=\S)"
        return re.sub(split_comma_pattern, " ", txt)

    # Clean up ----

    def _rm_long_words(self, txt):
        long_word_pattern = rf"\S{{{self.char_threshold},}}"
        return re.sub(long_word_pattern, "", txt)

    def _rm_tab_notation(self, txt):
        """Remove tablature notation from the text."""
        # This pattern looks for sequences with many dashes and numbers
        # tab_pattern = r"\b[A-G]#?b?\|{1,2}[-0-9hpsbrv?\/]+[\| ]+"
        tab_pattern = r"\b[A-G]#?b?\|{1,2}[-0-9hpsbrv?\/]+[\| ]+"
        return re.sub(tab_pattern, "", txt)

    def _rm_whitespace(self, txt):
        """Remove leading, trailing and excess whitespaces, i.e. n>1."""
        txt = re.sub(r"\s+", " ", txt)
        return txt.strip()

    def _rm_leading_parentheses(self, txt):
        """Remove leading parenthesis to break up enclosures like (C - G)"""
        leading_parenthesis_pattern = r"(?<!\S)\((?=[A-G])"
        return re.sub(leading_parenthesis_pattern, "", txt)

    def _rm_symbols(self, txt):
        """Replace multiple whitespace characters with a single space."""
        return re.sub(r"(\[|\]|\{|\}|\*|\||~)", "", txt)

    def _rm_non_chords(self, txt):
        non_chord_pattern = r"(?<!\S)(?![A-G])\S+"  # Use custom word boundary
        return re.sub(non_chord_pattern, "", txt)

    # Homogenization ----
    def _homogenize_qualities(self, txt):
        """Apply standardization rules to chord notations for chord qualities."""
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
        # Convert minor triads from "Cmin" to "Cm"
        txt = re.sub(r"([A-G][#b]?)min\b", r"\1m", txt)

        # TODO:
        # What about those? F#7(b9/b13)
        # Convert major chords from "C" to "Cmaj" when not followed by other chord symbols
        # txt = re.sub(r"\b([A-G][#b]?)(?![0-9a-zA-Z])", r"\1maj", txt)

        return txt

    def _homogenize_second_extensions(self, txt):
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

    # Selection ----
    def _negative_selection(self, chord_series):
        """
        Filters the input text by removing words that appear a number of times
        less than or equal to a predefined freq_threshold.

        This method counts the occurrences of each word in the input text,
        filters out the words that are below a freq_threshold (default = None), and then
        removes those words from the text.

        Args:
            chord_series (pd.Series): A pandas Series containing text data where
                             each entry is a string to be processed.

        Returns:
            pd.Series: A new Series with filtered text entries where words
                        that appeared equal to or below the freq_threshold have
                        been removed.
        """
        if self.freq_threshold is None:
            return chord_series

        word_count = chord_series.str.split(" ").explode().value_counts()
        # Sets have O(1) lookup time
        rare_words = set(word_count[word_count <= self.freq_threshold].index)

        def filter_rare_words(txt):
            words = txt.split()
            filtered_words = [word for word in words if word not in rare_words]
            return " ".join(filtered_words)

        chord_series = chord_series.apply(filter_rare_words)
        return chord_series

    def _positive_selection(self, txt):
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

        # Make sure chords appear as standalone tokens and not embedded inside words
        # Example: "Bridge" becomes "B"
        true_chords = rf"(?<![A-Za-z])({chord_anatomy})(?![A-Za-z])"

        chords = re.findall(true_chords, txt)
        return " ".join(chords)

    def clean(self, chord_series):
        chord_series = chord_series.apply(self._split_strings)
        chord_series = chord_series.apply(self._rm_leading_parentheses)
        chord_series = chord_series.apply(self._rm_long_words)
        chord_series = chord_series.apply(self._rm_tab_notation)
        chord_series = chord_series.apply(self._rm_non_chords)
        chord_series = chord_series.apply(self._rm_whitespace)
        # TODO: needed? chord_series = chord_series.apply(self._rm_symbols)
        return chord_series

    def homogenize(self, chord_series):
        chord_series = chord_series.apply(self._homogenize_qualities)
        chord_series = chord_series.apply(self._homogenize_second_extensions)
        return chord_series

    def select(self, chord_series):
        chord_series = self._negative_selection(chord_series)
        chord_series = chord_series.apply(self._positive_selection)
        return chord_series


class ChordCleanerToken:
    """
    A class for cleaning and standardizing chord notations in text data.
    """

    def __init__(self, char_threshold=20):
        self.char_threshold = char_threshold
        self._cached_tokens = {}

    # Tokenize ----
    def _tokenize(self, txt):
        """Split by coma and rm leading, trailing, and excess whitespaces, i.e. n > 1"""
        split_symbol_pattern = r"(?<=\S)[,^%]{1}(?=\S)"
        txt = re.sub(split_symbol_pattern, " ", txt)
        txt = re.sub(r"\s+", " ", txt)
        txt = txt.strip()
        return txt.split(" ")

    # Process list of tokens ----

    def _process_tokens(self, tokens):
        chords = []

        for token in tokens:
            token = self._erode(token)

            if not token:
                print("Empty token")
                continue

            token = self._homogenize(token)

            cached = self._cached_tokens.get(token)

            if cached is not None:
                print(f"{token} already in cache!")
                if cached:
                    chords.append(token)
                    continue
                else:
                    # Since token is junk, skip validation!
                    continue

            if self._reject(token):
                print(f"{token} rejected!")
                continue

            if self._validate(token):
                print(f"{token} validated and cached!")
                self._cached_tokens[token] = True
                chords.append(token)
            else:
                print(f"{token} added to cache as junk")
                self._cached_tokens[token] = False

        return chords

    # Cleaning functions ----
    def _erode(self, token):
        """
        Strips leading non-note characters from a token.
        Returns the substring starting with the first valid note (A-G) or an empty string if none is found.
        """
        # Or use regex? ^[^A-G]+

        for i, c in enumerate(token):
            if c in "ABCDEFG":
                return token[i:]
        return ""

    def _homogenize(self, token):
        # Convert Unicode to ASCII
        token = token.replace("♭", "b")
        token = token.replace("♯", "#")
        token = token.replace("°", "dim")
        token = token.replace("–", "-")

        # Strip trailing symbol leftovers
        token = token.rstrip("*~,/")

        return token

    def _reject(self, token):
        """Predicate that rejects tokens that are too long or resemble tabs"""
        if len(token) >= self.char_threshold:
            print(f"{token} too long")
            return True

        if re.match(r"^[A-G]{1}[#b]?[-|:\s]{1,2}", token):
            print(f"{token} is a tab!")

            return True

        return False

    def _validate(self, token):
        root = "[A-G]{1}"
        accidental = "[#b]?"
        quality = r"(?:maj|min|dim|aug|sus|add|m|M)?"
        extension = r"(?:2|4|5|6|7|9|10|11|13)?"
        modifier = r"(?:[ADGIMNOSUadgimnosu]{0,3}[24]?)?"
        extension_2 = rf"(?:\((?:{accidental}{extension},?\s*){{1,2}}\))?"
        slash = rf"(?:\/{root}{accidental})?"
        chord_anatomy = rf"^{root}{accidental}{quality}{extension}{modifier}{extension_2}{slash}$"
        # print(chord_anatomy)
        return re.match(chord_anatomy, token)

    def raw_chord_isolation(self, txt):
        """
        Stage 1 - Lenient chord detection
        Tokenization, minimal normalization and rough selection of tokens based on chord structure."""
        tokens = self._tokenize(txt)
        return self._process_tokens(tokens).join(" ")

    def chord_canonization(self, txt):
        """
        Stage 2 - Aggressive standardization and selection
        """
        pass


to_test = """
Amin
Amaj7(13)
Asus2dim


A(add9)/E
F7(9)(13)
F#7(4)(9)
F7(9)(5b)
Em7sus4/B
Fmaj7add2
Emmaj7/Eb
Fmaj7/11+
C7+/9/11+
G7/13(b9)
Eb°/(b13)
Eb7(9/5-)
D#m7(5b)
C#madd11
G#7M(5+)
D♭m
"""


cc = ChordCleanerToken()

test = "empty Bridge: C° C%& Amin7(9), C* E:---- ((Cmaj Cmaj C%&"

actual = cc.clean(test)
print(f"actual : {actual}")
