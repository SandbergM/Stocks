
from google.cloud import bigquery
import datetime

client = bigquery.Client()

from app.utils import SecretHandler
from app.api.controller.ticker_controller import get_ticker_historical_data
from app.utils.common import log

def get_tickers_data():
    """
    @return array
    """
    
    sql_query = f" SELECT * FROM `{ SecretHandler.get_secret( 'PROJECT_ID' ) }.stocks.tickers` WHERE country IN ( 'Sweden', 'Norway', 'Denmark', 'Finland' ) "
    
    log( "Getting tickers" )
    
    query_result = client.query( sql_query ).result()
    return [ dict( row ) for row in query_result ]

def save_ticker_data_to_bq( df ):
    try:
        df.to_gbq(
            destination_table   = "stocks.1d_historical_data", 
            project_id          = SecretHandler.get_secret( 'PROJECT_ID' ),
            if_exists           = 'append',
            reauth              = False,
            chunksize           = 10000,
            progress_bar        = False
        )
        return True
    except Exception as e:
        return False

def update_tickers_table( ticker, unix ):
    """
    @param String ticker
    @param Integer ticker
    """
    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('ticker', 'STRING', ticker),
            bigquery.ScalarQueryParameter('unix', 'INTEGER', int( unix ))
        ]
    )

    client.query( 
        query = f" UPDATE `{ SecretHandler.get_secret( 'PROJECT_ID' ) }.stocks.tickers` SET unix = @unix WHERE ticker = @ticker ", 
        job_config=query_config
    ).result()

def get_yahoo_finance_tickers():

    tickers = get_tickers_data()

    for ticker in tickers:
        log( f"Getting data for { ticker.get( 'company_name' ) }" )
        res = get_ticker_historical_data(
            ticker = ticker.get( 'ticker' ),
            company_name = ticker.get( 'company_name' ),
            interval = '1d',
            start_timestamp = ticker.get( 'unix' ),
            end_timestamp = datetime.datetime.now().timestamp()
        )

        if len( res ):
            if save_ticker_data_to_bq( res ):
                update_tickers_table( ticker.get( 'ticker' ), res['date'].max().timestamp() )