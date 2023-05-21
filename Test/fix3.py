import csv

for year in range(2020, 2024):
    for month in range(1, 13):
        input_file = f"data_{year:04}.{month:02}.csv"
        output_file = f"new_data_{year:04}.{month:02}.csv"
        
        try:
            with open(input_file, "r", encoding="utf-8-sig", newline="") as f_input, \
                 open(output_file, "w", encoding="utf-8-sig", newline="") as f_output:
                
                reader = csv.DictReader(f_input)
                writer = csv.DictWriter(f_output, fieldnames=reader.fieldnames+["New_Contents"])
                
                writer.writeheader()
                
                for row in reader:
                    new_contents = row["Title"] + " " + row["Contents"]
                    row["New_Contents"] = new_contents
                    writer.writerow(row)
                
                print(f"{input_file} -> {output_file} 변환 완료")
                
        except FileNotFoundError:
            continue
