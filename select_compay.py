import pandas as pd
import os
from datetime import datetime

cwd_location = os.getcwd()
file_list = os.listdir()

def get_stock_latest_file_name(file_list):
    file_name_list = []
    buffer_list = [s for s in file_list if 'stock' and 'csv' in s]

    if not buffer_list:
        return None
    elif len(buffer_list) == 1:
        return buffer_list
    else:
        for file_name in buffer_list:
            file_name_list.append(list(file_name.split('_')))

        latest_idx = 0
        for count in range(1, len(file_name_list)):
            buffer_bn = datetime.strptime(file_name_list[latest_idx][-2] + ' ' + file_name_list[latest_idx][-1].split('.')[0], '%Y-%m-%d %H-%M-%S')
            buffer_n = datetime.strptime(file_name_list[count][-2] + ' ' + file_name_list[count][-1].split('.')[0], '%Y-%m-%d %H-%M-%S')

            # print(buffer_bn, buffer_n)
            if buffer_n > buffer_bn:
                latest_idx = count
            else:
                pass

    return buffer_list[latest_idx]


if __name__ == '__main__':
    latest_file = get_stock_latest_file_name(file_list)
    df_stock_top_100_volume = pd.read_csv(f'{cwd_location}\{latest_file}', encoding='cp949').set_index('N')

    df_low_per_company = df_stock_top_100_volume.sort_values(by=['PER'])
    print(df_low_per_company.loc[df_low_per_company['PER'] > 0].head())



