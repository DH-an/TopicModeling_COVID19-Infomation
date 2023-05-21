import csv

input_file = 'Nprocessed23_1.csv'
output_file = 'Aprocessed23_1.csv'
stopwords_file = 'stopwords-ko.txt'

with open(stopwords_file, 'r', encoding='utf-8') as f:
    stopwords = [line.strip() for line in f]

with open(input_file, 'r', encoding='utf-8-sig') as f_input, \
     open(output_file, 'w', encoding='utf-8-sig', newline='') as f_output:

    csv_reader = csv.reader(f_input)
    csv_writer = csv.writer(f_output)

    for row in csv_reader:
        new_row = []
        for column in row:
            column = column.replace("'", "")
            column = column.replace("[", "")
            column = column.replace("]", "")
            column = column.replace(",", "")
            if column not in stopwords:
                new_row.append(column)
        csv_writer.writerow(new_row)

