import yfinance as yf
import pandas as pd
import os
import warnings

def twii(start: str = '2018-02-21', end: str = '2023-01-18', output: str = None) -> pd.DataFrame:
    if output is not None and not os.path.exists(output):
        warnings.warn(f'The destination folder is not exist!', UserWarning)
        warnings.warn(f'Create one.', UserWarning)
        os.makedirs(os.path.dirname(output), exist_ok=True)

    print(f'start to download twii data from {start} to {end}...')

    data = yf.Ticker('^TWII').history(start=start, end=end)

    if output is not None:
        data.to_csv(output)
        print(f'twii data has been saved to {output}')

    return data

if __name__ == '__main__':
    print(twii(output='data/train/twii.csv'))