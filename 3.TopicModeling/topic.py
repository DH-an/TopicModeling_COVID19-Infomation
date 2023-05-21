import csv
import pandas as pd

year = 23
num = 1
file_name = f"topics_{year}_{num}.csv"

# CSV 파일 불러오기
topics = pd.read_csv(file_name, header=None, encoding='cp949')

# 출력 결과를 CSV 파일로 저장
output_file = f"Ntopics_{year}_{num}.csv"
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['topic_num', 'word_text', 'word_num'])
    for i in range(len(topics)):
        row = topics.iloc[i]
        topic_num = row[0]
        topic_words = row[1].split('+')
        for word in topic_words:
            word = word.strip()
            word_num = float(word.split('*')[0])
            word_text = word.split('*')[1].replace('"','').strip()
            writer.writerow([topic_num, word_text, word_num])

# # 토픽 결과 출력
# topics = loaded_model.show_topics(num_topics=-1, num_words=12, formatted=False)
# with open(f"topics_{year}_{num}.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(["Topic", "Top Words", "Percentage"]) # 헤더 추가
#     for topic in topics:
#         topic_num = topic[0] # 토픽 번호
#         top_words = ", ".join([word[0] for word in topic[1]]) # 상위 단어
#         percentage = round(topic[1][0][1], 4) # 토픽 비율
#         writer.writerow([topic_num, top_words, percentage]) # 데이터 쓰기
