import csv
import pandas as pd
from gensim.models.ldamodel import LdaModel


year = 20
num = 1
file_name = f"topics_{year}_{num}.csv"
model_name = f"lda_model_{year}_{num}"


# CSV 파일 불러오기
topics = pd.read_csv(file_name, header=None, encoding='cp949')

# 저장된 모델 불러오기
loaded_model = LdaModel.load(f"{model_name}")

# 출력 결과를 CSV 파일로 저장
output_file = f"Atopics_{year}_{num}.csv"
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['topic_num', 'word_text', 'word_num', 'percentage'])
    for i in range(len(topics)):
        row = topics.iloc[i]
        topic_num = row[0]
        topic_words = row[1].split('+')
        percentage = float(row[2].split('%')[0])/100 # Percentage 값 추출
        for word in topic_words:
            word = word.strip()
            word_num = float(word.split('*')[0])
            word_text = word.split('*')[1].replace('"','').strip()
            writer.writerow([topic_num, word_text, word_num, percentage])
