import os
import pandas as pd

for year in range(2020, 2024):
    for month in range(1, 13):
        if year == 2020 and month < 2:
            continue
        if year == 2023 and month > 3:
            continue
        filename = f'n_kin_crawling_{year:04d}.{month:02d}.csv'
        if not os.path.exists(filename):
            continue
        df = pd.read_csv(filename)
        df.drop_duplicates(subset='Contents', inplace=True)
        new_filename = f'data_{year:04d}.{month:02d}.csv'
        df.to_csv(new_filename, index=False, encoding='utf-8-sig')

##01월이 빠져서 추가하는 코드
# filename = 'n_kin_crawling_2020.01.csv'
# df = pd.read_csv(filename)
# df.drop_duplicates(subset='Contents', inplace=True)
# new_filename = 'data_2020.01.csv'
# df.to_csv(new_filename, index=False, encoding='utf-8-sig')
