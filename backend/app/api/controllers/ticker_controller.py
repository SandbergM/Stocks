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

def ticker_history(ticker, b_rate, b_diviation, wmas, rsis, interval_type, interval_length):

    end_date = CommonUtils.generate_date(interval_type, interval_length)
    table = '1d' if (datetime.now() - end_date).days <= (370 * 3) else '1wk'
    print("table : ", table, end_date)
    data = DbHandler.select_query(f"""SELECT * FROM yahoo_finance_{table}_historical_data WHERE ticker = ?""",(ticker,))

    closing_prices = pd.DataFrame(data=[ el.get('close') for el in data])
    bollinger_up, bollinger_down = CommonUtils.get_bollinger_bands(closing_prices, b_rate, b_diviation)

    # Weighted moving avg
    wma_lists = {
        f'WMA {el}' : [CommonUtils.get_weighted_moving_average([el.get('close') for el in data[idx-int(el):idx]]) for idx in range(len(data))]
        for el in wmas
    }

    # Relative Strength Index's
    rsi_lists = {
        f'RSI {el}' : [CommonUtils.get_rsi([el.get('close') for el in data[idx-int(el):idx]]) for idx in range(len(data))]
        for el in rsis
    }
    
    # Relative Strength Index's
    rsi_lists = {
        f'RSI {el}' : [CommonUtils.get_rsi([el.get('close') for el in data[idx-int(el):idx]]) for idx in range(len(data))]
        for el in rsis
    }
    
    return [{
        **{k.replace("_", " ").title() : v for k, v in el.items()}, 
        **{k : v[idx] for k, v in wma_lists.items()},
        **{k : v[idx] for k, v in rsi_lists.items()},
        'Bollinger Upper' : bollinger_up[idx][0], 
        'Bollinger Lower' : bollinger_down[idx][0], 
    } for idx, el in enumerate(data) if datetime.strptime(el.get('date'), '%Y-%m-%d') >= end_date]

def add_ticker_to_db( ticker, company_name, country ):

    if len(DbHandler.select_query(""" SELECT * FROM tickers WHERE  ticker = ? """, ( ticker, ))) == 0:

        DbHandler.multiple_insert(""" INSERT INTO tickers VALUES(?, ?, ?, ?)""", [(ticker, 0, company_name, country, )])

        for interval in ["1d", "1wk"]:
            res = get_ticker_historical_data(
                ticker = ticker,
                company_name = company_name,
                interval = interval,
                start = 0,
                end = int(time.time())
            )
            
            if len( res ):
                if save_data( res, interval_table=interval ):
                    update_tickers_table( ticker, res['date'].max().timestamp() )

        return "Ok"
    else:
        return "Ok"