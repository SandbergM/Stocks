import pandas as pd
import numpy as np
from datetime import datetime 
import time

from app.data import DbHandler
from app.utils import CommonUtils
from app.cron_jobs.jobs.yahoo_finance_tickers.main import get_ticker_historical_data, update_tickers_table, save_data

def ticker_search( company_name_search = None ):
    if company_name_search is not None:
        custom_query = f"""SELECT ticker, unix, company_name, country FROM tickers WHERE company_name LIKE ? OR ticker LIKE ? ORDER BY ticker ASC LIMIT 25"""
        return DbHandler.select_query(custom_query, (f"%{company_name_search}%", f"%{company_name_search}%",) )
    else:
        return DbHandler.select_query( f"""SELECT ticker, unix, company_name, country FROM tickers ORDER BY ticker ASC LIMIT 25""" )

def ticker_history(ticker, b_rate, b_diviation, start, end):

    data = DbHandler.select_query(f""" SELECT * FROM yahoo_finance_1d_historical_data WHERE ticker = ? """,(ticker,))

    def get_sma(prices, rate):
        return prices.rolling(rate).mean()

    def get_bollinger_bands(prices, rate, diviation):
        sma = get_sma(prices, rate)
        std = prices.rolling(rate).std()
        bollinger_up = sma + std * diviation
        bollinger_down = sma - std * diviation

        bollinger_up = bollinger_up.replace(np.nan, None)
        bollinger_down = bollinger_down.replace(np.nan, None)

        return bollinger_up.values.tolist(), bollinger_down.values.tolist()

    closing_prices = pd.DataFrame(data=[ el.get('close') for el in data])
    bollinger_up, bollinger_down = get_bollinger_bands(closing_prices, b_rate, b_diviation)

    wma_10 = [CommonUtils.get_weighted_moving_average([el.get('close') for el in data[idx-10:idx]]) for idx in range(len(data))]
    wma_20 = [CommonUtils.get_weighted_moving_average([el.get('close') for el in data[idx-20:idx]]) for idx in range(len(data))]
    wma_50 = [CommonUtils.get_weighted_moving_average([el.get('close') for el in data[idx-50:idx]]) for idx in range(len(data))]
    wma_100 = [CommonUtils.get_weighted_moving_average([el.get('close') for el in data[idx-100:idx]]) for idx in range(len(data))]

    norm_lists = {
        'open_norm' : [],
        'high_norm' : [],
        'low_norm' : [],
        'close_norm' : [],
        'adj_close_norm' : [],
        'volume_norm' : [],
    }

    if type(start) == str:
        start = datetime.strptime(start, '%Y-%m-%d')

    for key in norm_lists:
        norm_max = max([el.get(key.replace('_norm', '')) for el in data if datetime.strptime(el.get('date'), '%Y-%m-%d') >= start])
        norm_lists[key] = [int((el.get(key.replace('_norm', '')) / norm_max) * 100) for el in data]

    return [{
        **el, 
        'b_up' : bollinger_up[idx][0], 
        'b_down' : bollinger_down[idx][0], 
        'open_norm' : norm_lists.get('open_norm')[idx],
        'high_norm' : norm_lists.get('high_norm')[idx],
        'low_norm' : norm_lists.get('low_norm')[idx],
        'close_norm' : norm_lists.get('close_norm')[idx],
        'adj_close_norm' : norm_lists.get('adj_close_norm')[idx],
        'volume_norm' : norm_lists.get('volume_norm')[idx],
        "wma_10" : wma_10[idx],
        "wma_20" : wma_20[idx],
        "wma_50" : wma_50[idx],
        "wma_100" : wma_100[idx],
    } for idx, el in enumerate(data)]

def add_ticker_to_db( ticker, company_name, country ):

    if len(DbHandler.select_query(""" SELECT * FROM tickers WHERE  ticker = ? """, ( ticker, ))) == 0:

        DbHandler.multiple_insert(""" INSERT INTO tickers VALUES(?, ?, ?, ?)""", [(ticker, 0, company_name, country, )])

        res = get_ticker_historical_data(
            ticker = ticker,
            company_name = company_name,
            interval = '1d',
            start = 0,
            end = int(time.time())
        )
        
        if len( res ):
            if save_data( res ):
                update_tickers_table( ticker, res['date'].max().timestamp() )

        return "Ok1"
    else:
        return "Ok2"