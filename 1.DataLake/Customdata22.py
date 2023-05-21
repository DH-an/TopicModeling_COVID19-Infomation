import pandas as pd
import re
from konlpy.tag import Mecab
from sklearn.feature_extraction.text import CountVectorizer

# 데이터 불러오기
data = pd.read_csv('new_data_2020.02.csv')
text = data['New_Contents'].tolist()

# 한글 형태소 분석기 사용
mecab = Mecab()

# 불용어 제거
stopwords = ['을', '를', '이', '가', '은', '는']

# 특수 문자 제거
def clean_text(text):
    text = re.sub('[^가-힣\s]', '', text)
    text = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', '', text)
    return text

# processed_data = data['Contents'].apply(clean_text)
# processed_data.to_csv('processed_data3.csv', index=False, encoding='utf-8-sig')


# 토큰화 및 어근 추출
def tokenize(text):
    tokens = mecab.pos(text)
    result = []
    for token in tokens:
        if token[1] in ['NNG', 'NNP', 'VV', 'VA', 'XR'] and token[0] not in stopwords:
            result.append(token[0])
    return result

# processed_data = data['Contents'].apply(tokenize)
# processed_data.to_csv('processed_data4.csv', index=False, encoding='utf-8-sig')


# 데이터 전처리
def preprocess_data(data):
    clean_data = data.apply(clean_text)
    tokenized_data = clean_data.apply(tokenize)
    return tokenized_data

# 데이터 벡터화
def vectorize_data(data):
    cv = CountVectorizer(tokenizer=lambda x: x, preprocessor=None, max_features=1000)
    vectorized_data = cv.fit_transform(data)
    return vectorized_data

# 데이터 전처리
def preprocess_data(data):
    clean_data = data.apply(lambda x: clean_text(str(x)))
    tokenized_data = clean_data.apply(tokenize)
    return tokenized_data

# 데이터 전처리
processed_data = preprocess_data(data['New_Contents'])

# 전처리된 데이터 저장-
processed_data.to_csv('processed20_2.csv', index=False, encoding='utf-8-sig')
