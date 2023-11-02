import requests
import pandas as pd
import json
import os
import datetime
import time
import warnings


def api(date: str, retry: int = 10, cold_down: int = 10) -> pd.DataFrame | None:
    """
    Download institutional investors data from TWSE.
    Args:
        date: the date of the data
        retry: the number of retry times
        cold_down: the time to wait between each retry
    Returns:
        None if the data is not exist (usually on holiday), otherwise the institutional investors data
    """
    url = f'https://www.twse.com.tw/rwd/zh/fund/T86?date={date}&selectType=ALL&response=json'
    r = requests.get(url)
    r.encoding = 'utf-8'

    if r.status_code != requests.codes.ok:
        # retry
        for i in range(retry):
            time.sleep(cold_down)
            print(f'retry {i+1}/{retry} times...')
            r = requests.get(url)
            r.encoding = 'utf-8'
            if r.status_code == requests.codes.ok:
                break

        raise Exception(f'Cannot get data from {url}. \
            It is because data crawling is too frequent generally, please try again later.') \
            if r.status_code != requests.codes.ok else None
    
    data = json.loads(r.text)

    if data['stat'] != 'OK':
        return None
    else:
        return pd.DataFrame(data['data'], columns=data['fields'])


def institutional_investors(start: str = '2018-02-21', end: str = '2023-01-18', output: str = None, cold_down: int = 10) -> None:
    """
    Download institutional investors data from TWSE.
    Args:
        start: start date of the data
        end: end date of the data (d-1 is the last day of the data)
        output: the path to save the data (do not contain the file name like 'data/train/法人買賣超日報', the file names are the date)
        cold_down: the time to wait between each download
    Returns:
        None
    """
    if output is None:
        raise ValueError('The output path is not specified!')
    
    if not os.path.exists(output):
        warnings.warn(f'The destination folder is not exist!', UserWarning)
        warnings.warn(f'Create one.', UserWarning)
        os.makedirs(output, exist_ok=True)

    print(f'start to download institutional investors data from {start} to {end}...')
    print(f'cold down time is set to {cold_down} seconds')
    
    offset = datetime.datetime.strptime(start, "%Y-%m-%d")
    while offset < datetime.datetime.strptime(end, "%Y-%m-%d"):
        data = api(offset.strftime("%Y%m%d"))
        if data is not None:
            data.to_csv(os.path.join(output, offset.strftime("%Y%m%d")+'.csv'))
            print(f'{offset.strftime("%Y%m%d")} is done')
        else:
            print(f'{offset.strftime("%Y%m%d")} is holiday')
        offset += datetime.timedelta(days=1)
        time.sleep(cold_down)

    print(f'all institutional investors data has been saved to {output}')


if __name__ == '__main__':
    # institutional_investors(output='data/train/法人買賣超日報')  # train
    # institutional_investors(output='data/test/法人買賣超日報', start='2023-01-30', end='2023-07-25')  # test
    institutional_investors(output='data/a/', start='2023-07-26', end='2023-10-28')
