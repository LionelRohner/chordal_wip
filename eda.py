from datasets import load_dataset
import pandas as pd
import re

# ds = load_dataset("lluccardoner/melodyGPT-song-chords-txt-1")
#
# ds = ds["train"].to_pandas()
#
# # Filter by pop
# ds_pop = ds[ds["genres"].str.contains("pop", case=False)]


def clean_spaces(txt):
    # replace n whitespaces with a single clean_spaces
    return re.sub(r"\s+", " ", txt)


a = "a    b    cc "
print(clean_spaces(a))


def rm_parenthesis(txt):
    # Remove parentheses and their contents
    return re.sub(r"(\(|\)|\[|\]|\{|\})", "", txt)


b = "G7(13) [A] {G}"
print(rm_parenthesis(b))


def standardize_chords(txt):
    # Convert "m5-" to "dim"
    txt = re.sub(r"m5-", "dim", txt)
    # Convert "°" to "dim"
    txt = re.sub(r"°", "dim", txt)
    # Remove "*"
    txt = re.sub(r"\*", "", txt)
    # Convert "+" to "aug" if it comes after an uppercase letter
    txt = re.sub(r"([A-G])\+", r"\1aug", txt)
    # Convert "+" to "#" if it comes after a number
    txt = re.sub(r"([0-9])(\+)", r"\1#", txt)
    # Convert "-" to "dim" after a 5 or an uppercase letter
    txt = re.sub(r"([A-G])-", r"\1dim", txt)
    txt = re.sub(r"5-", "dim", txt)
    # Convert "-" to "b" after any number that is not 5
    txt = re.sub(r"([0-9])(-)(?![0-9])", r"\1b", txt)
    return txt


c = "Am5- A° A* A+ A7(13+) A7(11-) A- A5-"
print(standardize_chords(c))
# pop_counts = ds_pop["chords_str"].str.split(" ").explode().value_counts()

# pop_counts.to_csv("chords_split_raw.csv")

# print(ds_pop)
