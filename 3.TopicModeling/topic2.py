import csv
import pandas as pd

year = 23
num = 1
file_name = f"topics_{year}_{num}.csv"

# CSV 파일 불러오기
topics = pd.read_csv(file_name, header=None, encoding='cp949')
print(topics)

for i in range(len(topics)):
    row = topics.iloc[i]
    topic_num = row[0]
    topic_words = row[1].split('+')
    print(f"Topic {topic_num}:")
    for word in topic_words:
        word = word.strip()
        word_num = float(word.split('*')[0])
        word_text = word.split('*')[1].replace('"','').strip()
        print(f"{word_text}: {word_num}")
    print("\n")
