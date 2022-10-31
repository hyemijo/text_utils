# Q. Extract bijective phrases 
# 1. Statistics 

# NUM_LINES 
# NUM_SRC_TOKENS
# NUM_TGT_TOKENS
# MULTIPLE_TRANSLATIONS_IN_SRC_TO_TGT
# MULTIPLE_TRANSLATIONS_IN_TGT_TO_SRC
# NUM_TOKENS_EQUAL_IN_LINE
# NUM_TOKENS_INEQUAL_IN_LINE

# 2. Details

# MULTIPLE_TRANSLATIONS_IN_SRC_TO_TGT Valentine
# MULTIPLE_TRANSLATIONS_IN_SRC_TO_TGT ('밸런타인', 3, 확률, (4797, 'Bobby Valentine', '바비 밸런타인'))
# MULTIPLE_TRANSLATIONS_IN_SRC_TO_TGT ('발렌타인', 1, 확률, (9662, 'Dori Valentine', '도리 발렌타인'))
# MULTIPLE_TRANSLATIONS_IN_SRC_TO_TGT ('발렌틴', 1, 확률, (22104, 'Karen Valentine', '카렌 발렌틴'))
# MULTIPLE_TRANSLATIONS_IN_TGT_TO_SRC 솔
# MULTIPLE_TRANSLATIONS_IN_TGT_TO_SRC ('Soul', 1, 확률, (8810, 'David Soul', '데이비드 솔'))
# MULTIPLE_TRANSLATIONS_IN_TGT_TO_SRC ('Sol', 2, 확률, (40956, 'Sol Bamba', '솔 밤바'))
# MULTIPLE_TRANSLATIONS_IN_TGT_TO_SRC ('Saul', 2, 확률 (39096, 'Saul Perlmutter', '솔 펄머터'))

import random

def print_dict(results, result_ex, stats, src2tgt, file=None):
    stats_keys = ("MULTIPLE_TRANSLATIONS_IN_SRC_TO_TGT", "MULTIPLE_TRANSLATIONS_IN_TGT_TO_SRC")
    idx = 0 if src2tgt else 1
    
    # 결과 출력
    for (token, token_dict) in sorted(results[idx].items()): # 정렬: 알파벳순
        if len(token_dict) < 2: # print multiple translations only
            continue            
        print(stats_keys[idx], token, file=file)
        
        sum_freq = sum(token_dict.values())
        for (tl, freq) in sorted(token_dict.items(), key=lambda x: (-x[1], x[0])): # 정렬: 빈도 역순, 알파벳순
            prob = round(freq / sum_freq, 2) if sum_freq else 0
            print(stats_keys[idx], (tl, freq, prob, result_ex[token][tl]), file=file)
            stats[stats_keys[idx]] += freq
    
    # 집계
    for (token, token_dict) in results[1-idx].items():
        if len(token_dict) < 2: # print multiple translations only
            continue
        for (tl, freq) in token_dict.items():
            stats[stats_keys[1-idx]] += freq

    # 통계량 출력
    for k, v in stats.items():
        print(k, v, file=file)


def update_freq(token, tl, result_dict):
    if token not in result_dict:
        result_dict[token] = dict()
    if tl not in result_dict[token]:
        result_dict[token][tl] = 0
    result_dict[token][tl] += 1

        
def update_ex(token, tl, update_val, result_dict):
    if token not in result_dict:
        result_dict[token] = dict()
    if tl not in result_dict[token]:  # 예시 저장
        result_dict[token][tl] = update_val
        return
    if random.choice((0,1)): # 예시 교체
        result_dict[token][tl] = update_val

        
def get_bijectives(fname, src2tgt, file=None):
    stats = {'NUM_LINES':0,
             'NUM_SRC_TOKENS':0,
             'NUM_TGT_TOKENS':0,
             'MULTIPLE_TRANSLATIONS_IN_SRC_TO_TGT':0,
             'MULTIPLE_TRANSLATIONS_IN_TGT_TO_SRC':0,
             'NUM_TOKENS_EQUAL_IN_LINE':0,
             'NUM_TOKENS_INEQUAL_IN_LINE':0}
    
    result_src, result_tgt = dict(), dict()
    result_ex_src, result_ex_tgt = dict(), dict()
    results = (result_src, result_tgt)

    with open(fname, encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            # update stats
            stats["NUM_LINES"] += 1
            
            src, tgt = line[:-1].split("\t")
            num_src_tokens = len(src.split(" "))
            num_tgt_tokens = len(tgt.split(" "))
            stats["NUM_SRC_TOKENS"] += num_src_tokens
            stats["NUM_TGT_TOKENS"] += num_tgt_tokens
            
            if num_src_tokens != num_tgt_tokens:
                stats["NUM_TOKENS_INEQUAL_IN_LINE"] += 1
                continue
            stats["NUM_TOKENS_EQUAL_IN_LINE"] += 1
            
            # src, tgt이 well aligned 되었다고 가정
            src_tgt_mapping = zip(src.lower().split(" "), tgt.lower().split(" ")) # 정규화
            for (s, t) in src_tgt_mapping:
                # 빈도 업데이트
                update_freq(s, t, result_src)
                update_freq(t, s, result_tgt)
                
                # 예시 업데이트
                update_ex(s, t, (i, src, tgt), result_ex_src) # 예시: 원본 보존
                update_ex(t, s, (i, src, tgt), result_ex_tgt)

    
    # 결과 출력
    if src2tgt:
        print_dict(results, result_ex_src, stats, src2tgt, file)
    else:
        print_dict(results, result_ex_tgt, stats, src2tgt, file)





import time

start = time.process_time()

fname = "06.enko.dict.person"
with open(fname+".mul_tl.stt", "w") as f:
    get_bijectives(fname, src2tgt = True, file=f)
with open(fname+".mul_tl.tts", "w") as f:
    get_bijectives(fname, src2tgt = False, file=f)
    
end = time.process_time()
print(f"time elapsed: {end - start}")


# 통계량
# NUM_LINES 48391
# NUM_SRC_TOKENS 98255
# NUM_TGT_TOKENS 91921
# MULTIPLE_TRANSLATIONS_IN_SRC_TO_TGT 32447
# MULTIPLE_TRANSLATIONS_IN_TGT_TO_SRC 35750
# NUM_TOKENS_EQUAL_IN_LINE 42058
# NUM_TOKENS_INEQUAL_IN_LINE 6333
