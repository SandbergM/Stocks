
from app.utils.gcp_secrets import get_secret

import pandas as pd
import datetime
import json
from google.cloud import bigquery

client = bigquery.Client()


def get_all_tickers():
    project_id = get_secret( "PROJECT_ID" )
    query_result = client.query( query = f" SELECT ticker, company_name FROM `{ project_id }.stocks.tickers` ORDER BY ticker ASC " ).result()
    return json.dumps( [ dict( row ) for row in query_result ] )
    
def get_ticker_historical_data( **args ):

    try:    

        ticker = args.get( 'ticker' )
        start_timestamp = args.get( 'start_timestamp' )
        end_timestamp = args.get( 'end_timestamp' )
        interval = args.get( 'interval' )
        company_name = args.get( 'company_name' )

        # Full url
        url = f''\
        f'https://query1.finance.yahoo.com/v7/finance/download/{ ticker }'\
        f'?period1={ int(start_timestamp) }'\
        f'&period2={ int(end_timestamp) }'\
        f'&interval={ interval }'\
        f'&events=history'\
        f'&includeAdjustedClose=true'

        # Get CSV
        res                 = pd.read_csv( url )

        # Fix col names
        res.columns         = [ col.replace(' ', '_').replace( '*', '' ).lower().strip() for col in res.columns ]
        
        # Add ticker and company_name as columns
        res                 = res.reindex([ 'ticker', 'company_name', *res.columns.tolist() ], axis = 1)
        res['ticker']       = ticker
        res['company_name'] = company_name

        # Remove prev saved days ( If found )
        start_dt            = datetime.datetime.fromtimestamp(int( start_timestamp ))
        res['date']         = pd.to_datetime(res['date'], format="%Y-%m-%d")
        res.drop(res[(res['date'] <= start_dt )].index, inplace=True)
        
        # Some 'volume's come as float for some reason
        res.dropna( inplace=True )
        res['volume']       = res['volume'].astype(np.int64)
        
        return res

    except Exception as e :
        return pd.DataFrame()