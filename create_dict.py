# from chordal_wip.scales import Scale, Chord
import chordal_wip.scales as s

print(s.get_ref_scales())
print("----")
print(s.get_ref_scales())

exit()


# s = Scale("C", "aeolian")
# print(s)
# c = Chord(s)
# print(c)
#
# modes = ["ionian", "aeolian"]
# keys = Scale.ALL_NOTES
#
# all_scales_dict = {}
#
# for mode in modes:
#     for key in keys:
#         print(f"{key}:{mode}")
#         scale = Chord(Scale(key, mode)).data
#         print(scale)
#         k = f"{key}_{mode}"
#
#         all_scales_dict.update({k: scale["triads"].tolist()})
#
# # print(all_scales_dict)
