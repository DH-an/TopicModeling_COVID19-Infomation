import os

folder_path = 'C:\\Users\\User\\Desktop\\dat'

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        new_file_name = file_name[:22] + '.csv'
        os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))
