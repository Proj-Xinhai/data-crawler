import yfinance as yf
import pandas as pd
import os
import warnings


def twii(start: str = '2018-02-21', end: str = '2023-01-18', output: str = None) -> pd.DataFrame:
    """
    Download twii data from Yahoo Finance.
    Args:
        start: start date of the data
        end: end date of the data (d-1 is the last day of the data)
        output: the path to save the data (must contain the file name like 'data/train/twii.csv')
    Returns:
        data: the twii data
    """
    if output is not None and not os.path.exists(output):
        warnings.warn('The destination folder is not exist!', UserWarning)
        warnings.warn('Create one.', UserWarning)
        os.makedirs(os.path.dirname(output), exist_ok=True)

    print(f'start to download twii data from {start} to {end}...')

    data = yf.Ticker('^TWII').history(start=start, end=end)

    if output is not None:
        data.to_csv(output)
        print(f'twii data has been saved to {output}')

    return data


if __name__ == '__main__':
    print(twii(output='data/train/twii.csv'))  # train
    print(twii(output='data/test/twii.csv', start='2023-01-30', end='2023-07-25'))  # test
