# 수정 22-08-10
def longest_match(dic, string):        
    maxlen = max([len(k) for k in dic.keys()])
    st = "0" * len(string)

    for j in range(maxlen, 0, -1):
        if j > len(string):
            continue
        offset = 0
        for i in range(0, len(string)-j+1):
            start, end = i+offset, i+j+offset
            cand = string[start:end]
            if "1" in st[start:end]:
                continue
            if cand in dic.keys():
                string = string[:start] + dic[cand] + string[end:]
                st = st[:start] + "1" * len(dic[cand]) + st[end:]
                offset += len(dic[cand]) - len(cand)
                
    return string

pl = { "ab": "xxx", "cde": "yyy", "rr": "QQ", "cdefgh": "zzz", "z" : "X"}
src = "qqq abcde rrr abcdefghz"
print(longest_match(pl, src))
