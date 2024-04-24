import pandas as pd
import os
import warnings
import tqdm
from time import sleep
from FinMind.data import DataLoader
from dotenv import dotenv_values


def stock(ind: list, start: str = '2018-02-21', end: str = '2023-10-27', output: str = None) -> None:
    """
    Download stock data in list.
    Args:
        ind: list of stock index
        start: start date of the data
        end: end date of the data
        output: the path to save the data (do not contain the file name like 'data/個股', the file names are the stock index)
    Returns:
        None
    """
    if output is None:
        raise ValueError('The output path is not specified!')

    if not os.path.exists(output):
        warnings.warn('The destination folder is not exist!', UserWarning)
        warnings.warn('Create one.', UserWarning)
        os.makedirs(output, exist_ok=True)

    print(f'start to download stock data from {start} to {end}...')
    print(f'{len(ind)} stocks are going to download')

    dl = DataLoader()

    config = dotenv_values('.env')
    try:
        token = config['FINMIND_TOKEN']
        dl.login_by_token(token)
    except KeyError:
        print('Token is not specified, download data without login...')
    except Exception:
        raise ValueError('Cannot login by token, please check your token in .env file.')

    for item in tqdm.tqdm(ind):
        while True:
            try:
                data = dl.taiwan_stock_daily(
                    stock_id=item,
                    start_date=start,
                    end_date=end
                )

                data.set_index('date').to_csv(os.path.join(output, str(item)+'.csv'))
                break
            except Exception:
                print(f'error occurs when downloading {item},'
                      ' is\'s usually because of the limit of FinMind API, retry after 10 mins...')
                sleep(10 * 60)  # sleep 10 mins
    
    print(f'all stock data has been saved to {output}')


if __name__ == '__main__':
    ind_list = pd.read_csv('data/ind.csv')['代號'].to_list()
    stock(ind=ind_list, output='data/個股_fix')
