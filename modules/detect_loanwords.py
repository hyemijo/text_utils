# 활용: 차용어 탐지
    # 가정: 철자 배열은 음소배열제약을 반영
    # 데이터: 표준국어대사전 표제어 총 99,341건
        # 외래어 23,820건
        # 고유어 75,521건
    # 방법: char 단위 ngram마다 확률 계산
    # input: 한국어 단어
    # output: 해당 단어의 분류 결과
        # 해당 단어가 외래어일 확률과 해당 단어가 고유어일 확률의 차이 이용
    # 단어 분류
        # 차용어
            # loanwords: 컴퓨터, 노트북
            # loanblends: 기초과학연구센터, 테니스장, 버스터미널
            # loanshifts: 벼룩시장
        # 고유어, 한자어: 책, 잔디밭, 완두콩


class LoanwordDetector:
    def __init__(self, fname_loan, fname_native, N, preprocess, threshold):
        self.N = N
        self.preprocess = preprocess
        self.threshold = threshold
        self.ngrams_loan = Ngram(fname_loan, N, unit="char", preprocess=preprocess)
        self.ngrams_native = Ngram(fname_native, N, unit="char", preprocess=preprocess)
        self.prob_dict_loan = self.get_prob_dict(self.ngrams_loan.ngrams_list)
        self.prob_dict_native = self.get_prob_dict(self.ngrams_native.ngrams_list)

        
    def get_prob_dict(self, ngrams_list):
        probdict = dict()
        sums = [sum(ngrams_n.values()) for ngrams_n in ngrams_list]

        for i, ngrams_n in enumerate(ngrams_list):
            for (ngram, freq) in ngrams_n.items():
                if ngram not in probdict: # 확률 업데이트
                    probdict[ngram] = freq / sums[i] # ngram 빈도 / ngram 토큰 수 총합
                    
        return probdict
        
        
    def get_ngram_prob(self, seq, Ngram, probdict, verbose):
        # get ngram probability
        prob = 1
        prob_min = min(probdict.values())
        sums = [sum(ngrams_n.values()) for ngrams_n in Ngram.ngrams_list]
        
        num_start_tag = self.N - 1
        seq = "_" * num_start_tag + seq # starting tag
        
        for i in range(len(seq) - (self.N-1)): # input seq에서 ngram 추출
            ngram = tuple(seq[i:i+self.N])
            ngram_str = "".join(ngram)
            try:
                if ngram_str.startswith("_" * num_start_tag): # 0th char -> unigram prob # (_, _, a)
                    ngram_prob_num = Ngram.ngrams_list[0][(ngram[-1], )] # (a)
                    ngram_prob_denom = sums[0] # total unigram freq
                elif ngram_str.startswith("_" * (num_start_tag - 1)): # 1th char # bigram prob (_, a, b)
                    ngram_prob_num = Ngram.ngrams_list[1][ngram[1:]] # (a, b)
                    ngram_prob_denom = Ngram.ngrams_list[0][(ngram[1], )] # (a)
                else: # 2th char or char after 2th # (a, b, c)
                    ngram_prob_num = Ngram.ngrams_list[2][ngram] # (a, b, c)
                    ngram_prob_denom = Ngram.ngrams_list[1][ngram[:-1]] # (a, b)
                if ngram_prob_num == 0 or ngram_prob_denom == 0:
                    ngram_prob = prob_min
                else:
                    ngram_prob = ngram_prob_num / ngram_prob_denom
                    
            except KeyError: # ngram not in ngrams_list
                ngram_prob = prob_min
            
            prob *= ngram_prob
            if verbose:
                print(ngram, ngram_prob, prob)
        return math.log(prob)
        
        
    def classify(self, query, verbose):
        # classify query word based on char n-gram
        classify_result = ""

        if self.preprocess == "romanize":
            query = re.sub("[^가-힣]", "", query)
            query = self.ngrams_loan.romanize(query)
        elif self.preprocess == "jaso":
            query = self.ngrams_loan.decompose_str(query)
        else:
            pass
    
        prob_loan = self.get_ngram_prob(query, self.ngrams_loan, self.prob_dict_loan, verbose)
        prob_native = self.get_ngram_prob(query, self.ngrams_native, self.prob_dict_native, verbose)
        val = prob_loan - prob_native
        
        if val > self.threshold:
            classify_result = "LOAN"
        elif val < - self.threshold:
            classify_result = "NATIVE"
        else:
            classify_result = "AMBIGUOUS"
            
        if verbose:
            print("==============================")
            print("MODEL:", self.preprocess)
            print("QUERY:", query)
            print("PROB_LOAN: ", prob_loan)
            print("PROB_NATIVE: ", prob_native)
            print("RESULT: ", classify_result)
            print("==============================")
            
        return val, classify_result



import time

N = 3
threshold = 3

start = time.time()
ld1 = LoanwordDetector("stdict.loan", "stdict.native_sino", N=N, threshold=threshold, preprocess="none")
end = time.time()
print(f"Model1 (none) / time elapsed: {end-start}")

start = time.time()
ld2 = LoanwordDetector("stdict.loan", "stdict.native_sino", N=N, threshold=threshold, preprocess="romanize")
end = time.time()
print(f"Model2 (romanize) / time elapsed: {end-start}")

start = time.time()
ld3 = LoanwordDetector("stdict.loan", "stdict.native_sino", N=N, threshold=threshold, preprocess="jaso")
end = time.time()
print(f"Model3 (jaso) / time elapsed: {end-start}")




loanwords = "컬러링북 컴퓨터 노트북 파이썬 제트로켓 소나타 프로그래밍 버스터미널 인터내셔널 온라인"
loanblends = "고속버스 택시승강장 평창올림픽"
loanshifts = "벼룩시장"
natives = "책 잔디밭 완두콩 물병 건전지 말투 부채 괭이부리말 부엉이 황새"

wordlist = " ".join((loanwords, loanblends, loanshifts, natives)).split(" ")

detectors = (ld1, ld2, ld3)
preprocess_type = "none romanize jaso".split(" ")
for word in wordlist:
    print("===================")
    print(word)
    for i, d in enumerate(detectors):
        result = d.classify(word, verbose=False)
        print(f"d{i+1} ({preprocess_type[i]}): ", result)
