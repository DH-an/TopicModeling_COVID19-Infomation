import csv
import re
import MeCab
from konlpy.tag import Mecab
from sklearn.feature_extraction.text import CountVectorizer
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.matutils import sparse2full
import pandas as pd
import multiprocessing
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis


# 데이터 불러오기
with open('new_data_2020.01.csv', 'r', encoding='utf-8') as f:
    rdr = csv.reader(f)
    text = [row[4] for row in rdr]


# 한글 형태소 분석기 사용
mecab = Mecab()

# 불용어 제거
stopwords = ['을', '를', '이', '가', '은', '는']

# 특수 문자 제거
def clean_text(text):
    text = re.sub('[^가-힣\s]', '', text)
    text = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', '', text)
    return text

# 토큰화 및 어근 추출
def tokenize(text):
    tokens = mecab.pos(text)
    result = []
    for token in tokens:
        if token[1] in ['NNG', 'NNP', 'VV', 'VA', 'XR'] and token[0] not in stopwords:
            result.append(token[0])
    return result

# CountVectorizer를 사용하여 문서를 단어-문서 행렬로 변환
vectorizer = CountVectorizer(tokenizer=tokenize)
X = vectorizer.fit_transform(text)

# 단어 목록 추출
words = vectorizer.get_feature_names_out()

# # LDA 모델 생성
# corpus = []
# for i in range(len(text)):
#     doc = tokenize(text[i])
#     corpus.append(doc)
    
# dictionary = corpora.Dictionary(corpus)
# corpus_bow = [dictionary.doc2bow(doc) for doc in corpus]

# lda = LdaModel(corpus=corpus_bow, id2word=dictionary, num_topics=10, passes=10)

# # 결과 시각화
# vis_data = gensimvis.prepare(lda, corpus, dictionary)
# pyLDAvis.save_html(vis_data, 'lda1.html')

# LDA 모델 생성
corpus = []
for i in range(len(text)):
    doc = tokenize(text[i])
    corpus.append(doc)
    
dictionary = corpora.Dictionary(corpus)
corpus_bow = [dictionary.doc2bow(doc) for doc in corpus]

doc_indices = []
doc_data = []

for doc in corpus_bow:
    indices, freqs = zip(*doc)
    doc_indices.append(list(indices))
    doc_data.append(list(freqs))

lda = LdaModel(corpus=corpus_bow, id2word=dictionary, num_topics=10, passes=10)

# 결과 시각화
vis_data = gensimvis.prepare(lda, corpus_bow, dictionary)
pyLDAvis.save_html(vis_data, 'lda1.html')
