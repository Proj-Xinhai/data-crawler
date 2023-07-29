# Data Crawler

## Description
Tool set for crawling data from various sources to be used for preparing data.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
 - `twii.py` is used to crawl twii data from yahoo finance.
 - `stock.py` is used to crawl stock data from yahoo finance.
 > Note: You need to download the ind.csv from release page and put it in `data/` before running stock.py.
 - `institutional_investors.py` is used to crawl institutional investors data from twse.
    - `data_transformer.py` is used to transform the data crawled by `institutional_investors.py` to the format that separated by stock code.
 - `industry.py` is used to crawl weighted index data of each industry from FinMind.