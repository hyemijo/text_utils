import re
k = 0
txt = "sdskjld aaadskkkk fdfdmmmmmkkf qqqbbbwqmfff"
out = "sdskjld AdsK fdfdMkkf QBwqmF"

for m in re.finditer("(.)\\1{2,}", txt):
    i, j = m.start(), m.end()
    cap = m.group()[0].upper()
    txt = txt[:i-k] + cap + txt[j-k:]
    k += len(m.group()) - len(cap)
txt == out
