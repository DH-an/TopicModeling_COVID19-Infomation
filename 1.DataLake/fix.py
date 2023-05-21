import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('processed_data.csv', header=None)

# 1글자 이상의 단어만 추출하기
df = df[0].str.findall(r'\b\w{2,}\b').str.join(' ')

# 전처리된 데이터 저장하기
df.to_csv('processed_data_new2.csv', index=False, header=False)
