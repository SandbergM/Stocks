

from app.api.controllers.ticker_controller import get_ticker_historical_data
from app.utils.CommonUtils import log
from app.__data import DbHandler
import time 
from datetime import datetime


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