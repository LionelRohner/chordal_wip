from datasets import load_dataset
import pandas as pd
import re
from chordal_wip.chordcleaner import ChordCleaner

cc = ChordCleaner(freq_threshold=3)

ds = load_dataset("lluccardoner/melodyGPT-song-chords-text-1")

ds = ds["train"].to_pandas()

ds = ds[ds["chords_str"].notna()]

# Filter by pop
# ds_pop = ds[ds["genres"].str.contains("jazz", case=False)]

series = ds["chords_str"]

ds["chords_str_clean"] = cc.clean(series)

# ds.iloc[8888:9888].to_csv("test.csv")
# exit()

# TODO: Move into ChordCleaner
unique_words = ds["chords_str_clean"].str.split().explode().drop_duplicates()
word_length_df = unique_words.reset_index(drop=True).to_frame()
word_length_df["length"] = word_length_df["chords_str_clean"].str.len()
word_length_df.to_csv("test_cnt_len.csv")
exit()
cnts = ds["chords_str_clean"].str.split().explode().value_counts()
print(len(ds["chords_str_clean"].str.split().explode()))

# cnts.to_csv("test_cnts.csv", header=True)

#
# ds_pop["chords_str_clean"] = cc.clean(series)
# print(f"nrow: {series.shape[0]}")
#
#
# ds_pop.iloc[0:1000].to_csv("test.csv")
