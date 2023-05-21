import pandas as pd
import re
from konlpy.tag import Mecab
from sklearn.feature_extraction.text import CountVectorizer

# 데이터 불러오기
data = pd.read_csv('naver_kin20_1_test.csv')

# 한글 형태소 분석기 사용
mecab = Mecab()

# print(data.head())
# print(data.info())


# 불용어 제거
stopwords = ['을', '를', '이', '가', '은', '는']

#특수 문자나 숫자 제거
def clean_text(text):
    text = re.sub('[^가-힣a-zA-Z\s]', '', text)
    return text

# 형태소를 원형으로 변환
def get_base_word(text):
    pos = mecab.pos(text)
    result = []
    for word, tag in pos:
        if tag in ['NNG', 'NNP', 'VV', 'VA', 'XR']:
            result.append(mecab.morphs(word)[0])
    return result

# 문장을 벡터화
def vectorize_text(data):
    cv = CountVectorizer(tokenizer=get_base_word, stop_words=stopwords, max_features=1000)
    vectorized_data = cv.fit_transform(data)
    return cv, vectorized_data

# 전처리된 데이터 저장
processed_data = data['Contents'].apply(clean_text)
processed_data.to_csv('processed_data2.csv', index=False, encoding='utf-8-sig')

cv, vectorized_data = vectorize_text(processed_data)

# 벡터화된 데이터 저장
vectorized_data = vectorize_text(processed_data)
pd.DataFrame(vectorized_data.toarray(), columns=cv.get_feature_names()).to_csv('vectorized_data.csv', index=False)

