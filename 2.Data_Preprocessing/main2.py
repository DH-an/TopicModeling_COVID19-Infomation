import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import pandas as pd
import multiprocessing
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import csv

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


# #토픽모델링 일관성 점수 보기
coherence_score=[]

if __name__ == '__main__':
    multiprocessing.freeze_support()
    for i in range(5,11):
        model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=i, passes= 5)
        coherence_model = CoherenceModel(model, texts=tokens, dictionary=dictionary, coherence='c_v')
        coherence_lda = coherence_model.get_coherence()
        print('k=',i,'\nCoherence Score: ', coherence_lda)
        coherence_score.append(coherence_lda)

# CSV 파일로 저장
with open(f"{coh_name}", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['num_topics', 'coherence_score'])
    for i, score in enumerate(coherence_score, start=5):
        writer.writerow([i, round(score, 4)])


# # LDA 모델 생성
# model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, passes=5)

# # 모델 저장
# model.save(f"{model_name}")

# # 모델 불러오기
# loaded_model = LdaModel.load(f"{model_name}")

# # 저장한 LDA 모델 로드
# lda_model = gensim.models.ldamodel.LdaModel.load(f"{model_name}")

# # 시각화 데이터 생성
# vis_data = gensimvis.prepare(lda_model, corpus, dictionary)

# # HTML 파일로 저장
# pyLDAvis.save_html(vis_data, f"{vis_name}")


#####