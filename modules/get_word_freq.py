# 어절 단위 토크나이징
sent = """이슈!이슈 그.......간, 그간. 그간!!!!! 코로나19로 인~한 '인한' 장기간 여러 어려움에도 불구하고, 극복의 과정에 최선을 다 해주고 계신 사우님들께 다시 한번 깊은 감사의 인사 드립니다."""
freqdict = dict()
punct = '!"#$%&' + "'()*+,-./:;<=>?@[\]^_`{|}~." # cf. python string.punctuation
filename = "freq.txt"

for word in sent.split(" "):
    token = ""
    token_char = ""
    
    for char in word:
        if char in punct:
            token_char += char
        else:
            token += char
            
    # add punct
    for c in token_char:
        if c not in freqdict:
            freqdict[c] = 0
        freqdict[c] += 1
        
    # add word
    if token not in freqdict:
        freqdict[token] = 0
    freqdict[token] += 1
    
freqlist = sorted(freqdict.items(), key = lambda x : -x[1])
for k , v in freqlist:
    print(freqlist)


'''
# save the result as .txt
with open(filename, "w", encoding = "utf-8") as f:
    for (k, v) in freqlist:
        print(str(v) +"\t" + k, file  = f)
        
'''
