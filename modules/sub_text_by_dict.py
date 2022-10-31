import re

pl = {"aaa": "AA", "bbb": "BBBBB"}
txt = "sdskjld aaadskkkk fdfdf qqqbbbwqmf" #"sdskjld AAdskkkk fdfdf qqqBBBBBwqmf"
txt2 = "aaaaaaa bbb b" # AAAAa BBBBB b

for k,v in pl.items():
    val = 0
    for m in re.finditer(k, txt):
        i, j = m.start(), m.end()
        txt = txt[:i-val] + v + txt[j-val:]
        val += len(k) - len(v)
txt
