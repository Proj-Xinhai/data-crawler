from stock import stock
from institutional_investors import institutional_investors
from margin_purchase_short_sale import margin_purchase_short_sales
import pandas as pd


if __name__ == '__main__':
    ind_list = pd.read_csv('data/ind.csv')['代號'].to_list()
    stock(ind=ind_list, output='data/個股')
    institutional_investors(ind=ind_list, output='data/法人買賣超')
    margin_purchase_short_sales(ind=ind_list, output='data/融資融券')
