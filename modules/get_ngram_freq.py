# get 1 ~ N gram (word, char)
import re

def get_ngrams(seq, N, word = True):   
    ngrams = []
    seq = seq.lower()
    
    if word:
        seq = re.sub("(?=[.,’])", " ", seq)
        seq = re.sub("(?<=[’])", " ", seq) # if apastrophe is considered a token (alliance`s -> alliance ` s) 
        seq = seq.split(" ")
    
    for n in range(1, N+1):
        ngram = dict()
        for i in range(len(seq) - (n-1)):
            key = seq[i:i+n]
            if word:
                key = " ".join(key)            
            if not key in ngram:
                ngram[key] = 0
            ngram[key] += 1
        ngrams.append(sorted(ngram.items(), key = lambda x : -x[1]))
        
    return ngrams


##################################################
n = 3
#txt = "Biden, who met with Andersson and Finnish President Sauli Niinisto in the Oval Office before making public remarks, did not reference any specific security measures the United States would provide the two countries before their membership is finalized. The application period is seen as a particularly vulnerable one, because the two countries are defying years of Russian threats against joining NATO but don’t yet fall under the alliance’s security umbrella."
txt = "Regular expressions called REs, or regexes, or regex patterns are essentially a tiny, highly specialized programming language embedded inside Python and made available through the re module."

# 어절 단위 N-gram 출력
for i, ngram in enumerate(get_ngrams(txt, n, word = True), start = 1):
    print(str(i)+"-GRAM_WORD")
    for k, v in ngram:
        print(v, k, sep="\t")
    print()    

# 음절 단위 N-gram 출력
for i, ngram in enumerate(get_ngrams(txt, n, word = False), start = 1):
    print(str(i)+"-GRAM_CHAR")
    for k, v in ngram:
        print(v, k, sep="\t")
    print()    
