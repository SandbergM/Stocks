import numpy as np
import pandas as pd
from datetime import datetime

from app.utils.CommonUtils import log

from app.data import DbHandler

import time 


def get_tickers_data():
    log( "Getting tickers" )
    return DbHandler.select_query(f"SELECT * FROM tickers")

def save_data( df ):

    data = []

    for row in df.iterrows():

        _ticker         = row[1].get('ticker')
        _company_name   = row[1].get('company_name')
        _date           = row[1].get('date').to_pydatetime().date()
        _open           = row[1].get('open')
        _high           = row[1].get('high')
        _low            = row[1].get('low')
        _close          = row[1].get('close')
        _adj_close      = row[1].get('adj_close')
        _volume         = row[1].get('volume')

        data.append(( _ticker, _company_name, _date, _open, _high, _low, _close, _adj_close, _volume ))

    return DbHandler.multiple_insert( "INSERT INTO yahoo_finance_1d_historical_data values (?,?,?,?,?,?,?,?,?)", data )

def update_tickers_table( ticker, unix ):
    return DbHandler.update_query("UPDATE tickers SET unix = ? WHERE ticker = ?", ( unix, ticker ))

def get_yahoo_finance_tickers():

    tickers = get_tickers_data()

    for ticker in tickers:
        
        log( f"Getting data for { ticker.get( 'company_name' ) }" )

        res = get_ticker_historical_data(
            ticker = ticker.get( 'ticker' ),
            company_name = ticker.get( 'company_name' ),
            interval = '1d',
            start = ticker.get( 'unix' ),
            end = int(time.time())
        )

        if len( res ):
            if save_data( res ):
                update_tickers_table( ticker.get( 'ticker' ), res['date'].max().timestamp() )

def get_ticker_historical_data( ticker, company_name, start, end, interval = '1d' ):

    try:    

        # Full url
        url = f''\
        f'https://query1.finance.yahoo.com/v7/finance/download/{ ticker }'\
        f'?period1={ int(start) }'\
        f'&period2={ int(end) }'\
        f'&interval={ interval }'\
        f'&events=history'\
        f'&includeAdjustedClose=true'
        input(url)
        # Get CSV
        res                 = pd.read_csv( url )

        # Fix col names
        res.columns         = [ col.replace(' ', '_').replace( '*', '' ).lower().strip() for col in res.columns ]
        
        # Add ticker and company_name as columns
        res                 = res.reindex([ 'ticker', 'company_name', *res.columns.tolist() ], axis = 1)
        res['ticker']       = ticker
        res['company_name'] = company_name

        # Remove prev saved days ( If found )
        start_dt            = datetime.fromtimestamp(int( start ))
        res['date']         = pd.to_datetime(res['date'], format="%Y-%m-%d")
        res.drop(res[(res['date'] <= start_dt )].index, inplace=True)
        
        # Some 'volume's come as float for some reason
        res.dropna( inplace=True )
        res['volume']       = res['volume'].astype(np.int64)
        
        return res

    except Exception as e :
        print(e)
        return pd.DataFrame()