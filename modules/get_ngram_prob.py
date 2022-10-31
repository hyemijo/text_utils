# 수정: class 이용하여 코드 작성

import math
import re


class Ngram:
    def __init__(self, fname, N, unit, preprocess):
        self.fname = fname
        self.N = N
        self.unit = unit
        self.preprocess = preprocess # input lang == ko
        self.ngrams_list = self.get_data()
    
    
    def get_data(self):
        ngrams_list = [dict() for i in range(self.N)] # [ dict for unigram, dict for bigram, ... ]

        with open(self.fname, encoding="utf-8") as f:
            for i, line in enumerate(f):
                self.update_ngrams(line[:-1], ngrams_list)
        return ngrams_list
    

    def decompose_syll(self, syll):
        # reference: https://blex.me/@baealex/%ED%95%9C%EA%B8%80-%EB%B6%84%EB%A6%AC-%EB%B3%91%ED%95%A9
        chosung = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
        jungsung = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
        jongsung = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
        u = ord(syll)

        if u < 0xAC00 or u > 0xD7A3: # if not Hangeul syllable
            return tuple(("", "", ""))
        u -= 0xAC00
        f = u % 28 # final consonant
        m = u // 28 % 21 # medial vowel
        i = u // 28 // 21 # initial consonant

        return tuple((chosung[i], jungsung[m], jongsung[f]))


    def decompose_str(self, string):
        result = ""
        for char in string:
            result += "".join(self.decompose_syll(char)).strip()
        return result
    

    def romanize(self, s):
        ### tbd
        return o

    
    def update_ngrams(self, seq, ngrams_list):   
        seq = seq.lower()
        
        if self.preprocess == "romanize":
            seq = re.sub("[^가-힣]", "", seq)
            seq = self.romanize(seq)
        elif self.preprocess == "jaso":
            seq = self.decompose_str(seq)
        elif self.preprocess == "none":
            pass
        else:
            print("Invalid preprocessing")
            return
    
        if self.unit == "word":
            seq = seq.split(" ") # pass if self.unit == "char" OR else
        
        for n in range(1, self.N+1): # n 설정
            ngrams_n = ngrams_list[n-1]
            for i in range(len(seq) - (n-1)): # starting idx 설정
                key = tuple(seq[i:i+n])    
                if key not in ngrams_n:
                    ngrams_n[key] = 0
                ngrams_n[key] += 1
                
                
    def get_prob_dict(self, query):
        probdict = dict()
        sums = [sum(ngrams_n.values()) for ngrams_n in self.ngrams_list]

        for i, ngrams_n in enumerate(self.ngrams_list):
            for (ngram, freq) in ngrams_n.items():
                if ngram[0] != query: # ngram이 query로 시작하는 경우만 체크
                    continue
                if ngram not in probdict: # 확률 업데이트
                    probdict[ngram] = freq / sums[i] # ngram 빈도 / ngram 토큰 수 총합
        return probdict

    
    def print_data(self, query):
        # 1. 확률값 계산
        probdict = self.get_prob_dict(query)
        sums = [sum(ngrams_n.values()) for ngrams_n in self.ngrams_list]

        # 2. 정렬 & 출력
        probdict = sorted(probdict.items(), key=lambda x: (-x[1], x[0])) # 확률 내림차순, ngram 오름차순 정렬
        for (ngram, prob) in probdict:
            print(math.log(prob), ngram, sep="\t")



ngram_corpus = Ngram("05.corpus.txt", N=3, unit="word", preprocess="none")
ngram_corpus.print_data("학교에")
