import csv

with open('stopwords-ko.txt', 'r', encoding='utf-8') as f:
    data = [line.strip() for line in f.readlines()]

print(data)
