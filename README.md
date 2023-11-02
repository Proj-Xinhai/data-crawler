# Data Crawler

## Description
Tool set for crawling data from various sources to be used for preparing data.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
 - `stock.py` is used to crawl stock data from FinMind.
 > Note: You need to download the `ind.csv` from release page and put it in `data/` before running stock.py.
 - `institutional_investors.py` is used to crawl institutional investors data from FinMind.
 - `margin_purchase_short_sale.py` is used to crawl margin purchase short sale data from FinMind.
### (Deprecated)
 - `twii.py` is used to crawl twii data from yahoo finance.
 - `industry.py` is used to crawl weighted index data of each industry from FinMind.
 - `institutional_investors_twse.py` is used to crawl institutional investors data from TWSE.
    - `data_transformer.py` is used to transform the data crawled by `institutional_investors_twse.py` to the format that separated by stock code.

 > Please note that the data crawler may return error message "the limit of FinMind API". 
 > If it happens too many times, please check if the stock have no data in the period you crawled.
 > The `ind.csv` we provided is the list of stock id that we already checked in the period of 2018-02-21 to 2020-10-27