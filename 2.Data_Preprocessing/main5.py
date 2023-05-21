import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import pandas as pd
import multiprocessing
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import csv
import matplotlib.pyplot as plt

# 파일명에서 숫자 부분만 변경할 수 있도록 변수 생성
year = 20
num = 1
file_name = f"Aprocessed{year}_{num}.csv"
model_name = f"lda_model_{year}_{num}"
vis_name = f"lda_visualization_{year}_{num}.html"
coh_name = f"coherence_scores_{year}_{num}.csv"

# CSV 파일 불러오기
tokens = pd.read_csv(file_name, header=None)

# NaN값이 들어있는 행 삭제
tokens.dropna(inplace=True)

# 문자열 데이터를 리스트로 변환
tokens = [doc.split() for doc in tokens[0]]

dictionary = corpora.Dictionary(tokens) # 토큰 단어와 gensim 내부 아이디 매칭
dictionary.filter_extremes(no_below=2, no_above=0.5) # 빈도 2이상 포함, 전체 50% 이상 단어 제거
corpus = [dictionary.doc2bow(token) for token in tokens] 


# 저장된 모델 불러오기
loaded_model = LdaModel.load(f"{model_name}")

# 토픽 결과 출력
topics = loaded_model.print_topics(num_words=12)
for topic in topics:
    print(topic)
    
# 토픽 결과 CSV 파일 저장
with open(f"topics_{year}_{num}.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for topic in topics:
        writer.writerow(topic)

# 저장된 모델 불러오기
loaded_model = LdaModel.load(f"{model_name}")

# 출력 결과를 CSV 파일로 저장
output_file = f"Atopics_{year}_{num}.csv"
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['topic_num', 'word_text', 'word_num', 'percentage'])
    for topic in topics:
        topic_num = topic[0]
        topic_words = topic[1]
        sum_weight = sum(weight for word, weight in topic_words)
        for word, weight in topic_words:
            word_text = word
            word_num = weight
            percentage = round(weight/sum_weight, 4)
            writer.writerow([topic_num, word_text, word_num, percentage])

