import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import pandas as pd
import multiprocessing
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

# CSV 파일 불러오기
tokens = pd.read_csv('processed21_1.csv', header=None)

# 문자열 데이터를 리스트로 변환
tokens = [doc.split() for doc in tokens[0]]


dictionary = corpora.Dictionary(tokens) # 토큰 단어와 gensim 내부 아이디 매칭
dictionary.filter_extremes(no_below=2, no_above=0.5) # 빈도 2이상 포함, 전체 50% 이상 단어 제거
corpus = [dictionary.doc2bow(token) for token in tokens] 


# #토픽모델링 일관성 점수 보기
# from gensim.models import CoherenceModel

# coherence_score=[]

# if __name__ == '__main__':
#     multiprocessing.freeze_support()
#     for i in range(7,12):
#         model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=i, passes= 5)
#         coherence_model = CoherenceModel(model, texts=tokens, dictionary=dictionary, coherence='c_v')
#         coherence_lda = coherence_model.get_coherence()
#         print('k=',i,'\nCoherence Score: ', coherence_lda)
#         coherence_score.append(coherence_lda)

# LDA 모델 생성
model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, passes=5)

# 모델 저장
model.save('lda_model_21-1')

# 모델 불러오기
loaded_model = LdaModel.load('lda_model_21-1')

# 저장한 LDA 모델 로드
lda_model = gensim.models.ldamodel.LdaModel.load('lda_model_21-1')

# 시각화 데이터 생성
vis_data = gensimvis.prepare(lda_model, corpus, dictionary)

# HTML 파일로 저장
pyLDAvis.save_html(vis_data, 'lda_visualization_21-1.html')

# #lad모델 설정
# lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary , num_topics= 7 , passes= 5)

# #lda_model.show_topics()
# #lda_model.print_topics()


# # prepared_data = gensimvis.prepare(lda_model, corpus, dictionary)
# # pyLDAvis.display(prepared_data)

# # 결과 시각화
# vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
# pyLDAvis.save_html(vis_data, 'lda1.html')
