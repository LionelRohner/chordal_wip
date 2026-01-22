from datasets import load_dataset
import pandas as pd
import re
from chordal_wip.chordcleaner import ChordCleaner

cc = ChordCleaner(threshold=3)
# a = "dim|sus|add|aug|no"
# # a = "M|Maj|maj|m|min"
# b = re.sub(r"\|", "", a)
# c = set(b)
# d = set(b.upper())
# print(list(c) + list(d))
# e = "".join(sorted(list(c) + list(d)))
# print(e)

# test = pd.Series(
#     [
#         "Intro: F#m7 D2 F#m7 D2 F#m7 D2 E F#m7 A/C# E D2 E F#m7 Bm A/C# D2 E G",
#         "Em - D C C D Em Em D C C D Em Em D C Am D Em G C Am D Bm",
#         "Intro: Em Bm Am C (2x) Em Bm Am C Em Bm Am C Bm Em Bm Am C Em Bm Em Am Em Bm Am ( C ) Em Bm Am ( C )",
#         "Intro: Am7 Gm - Dm - C - C x2 Gm Dm C C Gm Dm C C Gm A# C* Gm A# C* Gm A# C* Gm A# C*",
#         "B|-----------11----11--------------6---6-------------8---8--------8--------8------| ",
#         "G|--------12----------12---------7-------7---------9-------9--------9--------9----| ",
#     ]
# )

# Somethings fishy here
# TODO: Check for progression that have many very simple chord changes to not overblow the prob of certain changes

# actual = cc.clean(test)
# print(f"\n\n ----- \n\n")
# print(actual)
# print(
#     pd.Series(
#         [
#             "F#m7 D2 F#m7 D2 F#m7 D2 E F#m7 A/C# E D2 E F#m7 Bm A/C# D2 E G",
#             "Em D C C D Em Em D C C D Em Em D C Am D Em G C Am D Bm",
#             "Em Bm Am C Em Bm Am C Em Bm Am C Bm Em Bm Am C Em Bm Em Am Em Bm Am C Em Bm Am C",
#             "Gm Dm C C Gm Dm C C Gm Dm C C Gm A# C Gm A# C Gm A# C Gm A# C",
#         ]
#     )
# )

# exit()
ds = load_dataset("lluccardoner/melodyGPT-song-chords-text-1")

ds = ds["train"].to_pandas()

ds = ds[ds["chords_str"].notna()]

# Filter by pop
ds_pop = ds[ds["genres"].str.contains("pop", case=False)]


series = ds_pop["chords_str"]
print(f"nrow: {series.shape[0]}")

ds_pop["chords_str"] = cc.clean(series)
print(f"nrow: {series.shape[0]}")

ds_pop.iloc[0:1000].to_csv("test.csv")
