from chordal_wip.scales import Scale, Chord

s = Scale("D", "aeolian")
print(s)
c = Chord(s)
print(c)

modes = ["ionian"]  # , "aeolian"]
keys = Scale.ALL_NOTES

all_scales_dict = {}

for mode in modes:
    for key in keys:
        print(f"{key}:{mode}")
        scale = Chord(Scale(key, mode))
        k = f"{key}_{mode}"

        all_scales_dict.update({k: scale.data["triads"].tolist()})

print(all_scales_dict)
