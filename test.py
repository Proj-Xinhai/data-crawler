import pandas as pd
import os


if __name__ == '__main__':
    ind_list = pd.read_csv('data/ind.csv')
    for item in ind_list['代號'].to_list():
        data = pd.read_csv(f'data/個股/{item}.csv')
        if data[data['date'] == '2018-02-21'].empty:
            print(f'{item} seems don\'t have data start from 2018-02-21, skip it...')
            ind_list = ind_list.mask(ind_list['代號'] == item)
        else:
            # move file path
            os.rename(f'data/個股/{item}.csv', f'data/個股_new/{item}.csv')

    ind_list.dropna().to_csv('data/ind_new.csv', index=False)

