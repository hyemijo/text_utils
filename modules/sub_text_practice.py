# non-greedy match
import re
txt = "떵훈떵훈떵훈떵훈 ㅋㅋㅋㅋㅋ큐ㅠㅠㅠㅠㅜㅜㅜㅠ넘넘넘넘넘 사랑해애애애애ㅐㅐㅐㅐㅐㅐ!!!!!!!!!!ㅎㅎㅎㅎ"
k = 0
tag = "[REPEAT]"
for m in re.finditer("([^ㅠㅜ!]+?)\\1{2,}", txt):
    i, j  = m.start(), m.end()
    txt = txt[:i-k] + m.group(1) + tag + txt[j-k:]
    k +=  len(m.group()) - len(m.group(1) + tag)
txt



dict_koen = {"엔씨": "NC", "나노":"nano", "장터":"market", "판매":"sell", "도구리": "Doguri", 
      "흰":"white", "색":"color", "티셔츠" : "t-shirt", "원" : "$", "모르겄는디":"I don't get it"}
txt = "<나노장터> <판매> 엔씨 도구리 모르겄는디 흰색티셔츠 15000원"

dict_koen_len = sorted(set([len(k) for k in dict_koen.keys()]), reverse=True)
print("every key is unigram: ", any(" " not in k for k in dict_koen.keys()))
print("key len:", sorted(set([len(k) for k in dict_koen]), key = lambda x : -x))
print(txt)

k = 0
idx_start = 0


for w in txt.split(" "): # 각 어절 대상으로 dict_koen의 key 탐색 (every key is unigram)
    multiple_sub = False # 한 어절에서 치환 여러 번 발생하는 경우 대응
    for i, char in enumerate(w): # i: 어절 내부에서의 시작 인덱스
        for j in dict_koen_len: # j: 스팬
            if i+j > len(w): continue # 어절에서 추출한 ngram의 끝 인덱스는 어절 길이보다 작아야 함
            ngram = w[i : i+j]
            if ngram in dict_koen:
                v = " " + dict_koen[ngram] if multiple_sub else dict_koen[ngram] # 치환되는 문자열 앞 공백 추가
                txt = txt[:idx_start + i + k] + v + txt[idx_start + i + j + k:]
                k += len(v) - len(ngram)
                multiple_sub = True
    else: 
        idx_start += len(w) + 1 # 공백 1개 길이 반영

    
# 15000$ -> $11.7
num = ""
i = 0
print("before:\t", txt)
while i < len(txt):
    if txt[i] == "$":
        for j in range(i-1, -1, -1):
         # 금액 찾기
            if not txt[j]:
                break
            if txt[j].isdigit():
                num = txt[j] + num
        else: v = "$" + str(int(num) * 0.00078)
        txt = txt[:i-len(v)] + v + txt[i+1:]
        break
    i += 1
print("after:\t", txt)
