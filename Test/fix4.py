import glob
import pandas as pd

# 합치고자 하는 CSV 파일들이 있는 폴더 경로
folder_path = '23'

# 폴더 경로 내의 모든 CSV 파일 경로를 리스트로 가져오기
all_files = glob.glob(folder_path + "/*.csv")

# 모든 CSV 파일을 하나의 DataFrame으로 병합
combined_df = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)

# 결과를 하나의 CSV 파일로 저장
combined_df.to_csv('23-1.csv', index=False, encoding='utf-8-sig')
