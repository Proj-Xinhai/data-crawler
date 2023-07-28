import pandas as pd
from FinMind.data import DataLoader
import os
import tqdm
import warnings


def industry_index(start: str = '2018-02-21', end: str = '2023-01-18', output: str = None) -> None:
    '''
    Download industry_index data from FinMind.
    Args:
        start: start date of the data
        end: end date of the data (d-1 is the last day of the data)
        output: the path to save the data (do not contain the file name like 'data/train/類股指', the file names are the stock index)
    Returns:
        None
    '''
    if output is None:
        raise ValueError('The output path is not specified!')
    
    if not os.path.exists(output):
        warnings.warn(f'The destination folder is not exist!', UserWarning)
        warnings.warn(f'Create one.', UserWarning)
        os.makedirs(output, exist_ok=True)

    print(f'start to download industry_index data from {start} to {end}...')

    api = DataLoader()

    cat_ind = api.taiwan_stock_info()
    cat_ind = cat_ind[cat_ind['industry_category'] == 'Index'][['stock_id', 'stock_name']].reset_index(drop=True)
    cat_ind.columns = ['FinMind_id', 'FinMind_name']

    for cat in tqdm.tqdm(cat_ind['FinMind_id'].values):
        stock_data = api.taiwan_stock_daily(stock_id=cat, start_date=start, end_date=end)[['date', 'open', 'max', 'min', 'close', 'Trading_Volume']]
        stock_data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        stock_data.to_csv(os.path.join(output, cat+'.csv'), index=False)

    print(f'all industry_index data has been saved to {output}')

if __name__ == '__main__':
    industry_index(output='data/train/類股指') # train
    industry_index(output='data/test/類股指', start='2023-01-30', end='2023-07-25') # test