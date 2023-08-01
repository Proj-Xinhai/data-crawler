import yfinance as yf
import pandas as pd
import os
import warnings
import tqdm


def stock(ind: list, start: str = '2018-02-21', end: str = '2023-01-18', output: str = None) -> None:
    """
    Download stock data from list.
    Args:
        ind: list of stock index
        start: start date of the data
        end: end date of the data (d-1 is the last day of the data)
        output: the path to save the data (do not contain the file name like 'data/train/個股', the file names are the stock index)
    Returns:
        None
    """
    if output is None:
        raise ValueError('The output path is not specified!')

    if not os.path.exists(output):
        warnings.warn(f'The destination folder is not exist!', UserWarning)
        warnings.warn(f'Create one.', UserWarning)
        os.makedirs(output, exist_ok=True)

    print(f'start to download stock data from {start} to {end}...')
    print(f'{len(ind)} stocks are going to download')

    for item in tqdm.tqdm(ind):
        api = yf.Ticker(str(item)+'.TW')
        hist = api.history(start=start, end=end)
        hist.to_csv(os.path.join(output, str(item)+'.csv'))
    
    print(f'all stock data has been saved to {output}')


if __name__ == '__main__':
    ind_list = pd.read_csv('data/ind.csv')['代號'].to_list()
    stock(ind=ind_list, output='data/train/個股')  # train
    stock(ind=ind_list, output='data/test/個股', start='2023-01-30', end='2023-07-25')  # test
