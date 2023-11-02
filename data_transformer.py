import pandas as pd
import os 
import tqdm
import warnings
import datetime
import numpy as np


def transformer(ind: list, source: str = 'data/train/法人買賣超日報', output: str = 'data/train/法人買賣超日報_個股'):
    """
    Transform institutional investors data crawled by institutional_investors.py to the format that separated by stock code.
    Args:
        ind: list of stock index to transform
        source: the path of the institutional investors data (do not contain the file name like 'data/train/法人買賣超日報', the file names are the date)
        output: the path to save the data (do not contain the file name like 'data/train/法人買賣超日報_個股', the file names are the stock index)
    Returns:
        None
    """
    if not os.path.exists(source):
        raise ValueError('The input path is not exist!')
    
    if not os.path.exists(output):
        warnings.warn(f'The destination folder is not exist!', UserWarning)
        warnings.warn(f'Create one.', UserWarning)
        os.makedirs(output, exist_ok=True)

    print(f'start to transform institutional investors data from {source} to {output}...')
    print(f'{len(ind)} stocks are going to transform')

    for f in tqdm.tqdm(os.listdir(source)):
        temp = pd.read_csv(os.path.join(source, f), index_col=0)
        col = temp.drop(columns=['證券代號', '證券名稱']).columns.to_list()
        col.insert(0, 'Date')
        
        d = datetime.datetime.strptime(f.split('.')[0], '%Y%m%d')

        for item in ind:
            if not os.path.isfile(os.path.join(output, str(item)+'.csv')):
                out = pd.DataFrame(columns=col)
            else:
                out = pd.read_csv(os.path.join(output, str(item)+'.csv'), index_col=0)

            if item in temp['證券代號'].unique():
                new_line = np.insert(temp[temp['證券代號'] == item]
                                     .drop(columns=['證券代號', '證券名稱'])
                                     .values[0], 0, d.strftime("%Y-%m-%d %H:%M:%S+08:00"), axis=0)
                new_line = pd.DataFrame(new_line.reshape(1, -1), columns=col)
                out = pd.concat([out, new_line], ignore_index=True)
            else:
                new_line = np.insert(np.zeros(len(col)-1).astype(str), 0, d.strftime("%Y-%m-%d %H:%M:%S+08:00"), axis=0)
                new_line = pd.DataFrame(new_line.reshape(1, -1), columns=col)
                out = pd.concat([out, new_line], ignore_index=True)

            out.to_csv(os.path.join(output, str(item)+'.csv'))

    print(f'all institutional investors data has been transformed to {output}')


if __name__ == '__main__':
    ind_list = pd.read_csv('data/ind.csv')['代號'].to_list()
    # transformer(ind=ind_list)  # train
    # transformer(ind=ind_list, source='data/test/法人買賣超日報', output='data/test/法人買賣超日報_個股')  # test
    transformer(ind=ind_list, source='data/法人買賣超日報', output='data/法人買賣超日報_個股')  # all
