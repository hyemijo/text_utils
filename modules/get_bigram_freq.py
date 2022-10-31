import re

pattern_punc = re.compile("(?<=\w)\W(?=\s|$)") # nonwords that follow words & are followed by whitespaces or are at the end of the string
txt = "Biden, who met with Andersson and Finnish President Sauli Niinisto in the Oval Office before making public remarks, did not reference any specific security measures the United States would provide the two countries before their membership is finalized. The application period is seen as a particularly vulnerable one, because the two countries are defying years of Russian threats against joining NATO but don’t yet fall under the alliance’s security umbrella." 
punc = re.findall(pattern_punc, txt)
#txt_no_punc = re.sub(pattern_punc, "", txt)

def get_bigram(seq):   
    bigram = dict()
    for i in range(len(seq) - 1):
        if not (seq[i], seq[i+1]) in bigram:
            bigram[(seq[i], seq[i+1])] = 0
        bigram[(seq[i], seq[i+1])] += 1
    return sorted(bigram.items(), key = lambda x : -x[1])    

punc_dict = dict()
for char in punc:
    if char not in punc_dict:
        punc_dict[char] = 0
    punc_dict[char] += 1    
    
##########################################################
# (0) 구두점 빈도수 역순 정렬
print("PUNCTUATION")    
for (k, v) in sorted(punc_dict.items(), key = lambda x : -x[1]):  
    print(f"{v}\t{k}")
print()

# (1) 어절단위의 bi-gram 빈도수 역순 정렬   
print("BIGRAM_WORD")    
for (k, v) in get_bigram(txt.split(" ")):
    #print(f"{v}\t{k[0]}\t{k[1]}")
    #print(v, k[0], k[1], sep="\t")
    bigram = " ".join((k[0],k[1]))
    print(v, bigram)
print()

# (2) 음절단위의 bi-gram 빈도수 역순 정렬    
print("BIGRAM_CHAR")    
for (k, v) in get_bigram(txt):
    print(f"{v}\t{k[0]}{k[1]}")
