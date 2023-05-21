import os
import pandas as pd

folder_path = "20-1"

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        data_count = len(df)
        print(f"{filename}: {data_count} rows")

