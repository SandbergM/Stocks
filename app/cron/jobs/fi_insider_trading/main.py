
from app.utils import SecretHandler
from datetime import date

from app.api.controller.fi_controller import get_insider_data
from app.utils.common import log
from app.utils import BigQueryUtils

import pandas as pd

def get_insider_trades():

    log("Running get_insider_trades")
    
    from_transactions_date = max_publiceringsdatum()
    to_transactions_date = date.today()
    data = get_insider_data( **{ "from_transactions_date" : from_transactions_date, "to_transactions_date" : to_transactions_date, "as_type" : 'dataframe' } )
    data = pd.DataFrame( data = data )
    data = data.rename(columns = { col : column_name_fix( col ) for col in data.columns })

    BigQueryUtils.save( data )

def column_name_fix( s ):

    s = s.replace( 'å', 'a' )
    s = s.replace( 'ä', 'a' )
    s = s.replace( 'ö', 'o' )
    s = s.replace( ' ', '_' )

    return s.lower()

def max_publiceringsdatum():

    sql_query = f""" SELECT MAX( publiceringsdatum ) AS publiceringsdatum FROM `{ SecretHandler.get_secret( 'PROJECT_ID' ) }.stocks.fi_insider_trades` """
    res = BigQueryUtils.query( sql_query )
    
    if len(res):
        max_publiceringsdatum = res['publiceringsdatum'].iloc[0]
        sql_query = f""" DELETE FROM `{ SecretHandler.get_secret( 'PROJECT_ID' ) }.stocks.fi_insider_trades` WHERE publiceringsdatum = '{ max_publiceringsdatum }' """
        BigQueryUtils.query( sql_query )
        return max_publiceringsdatum

    else:
        return "2000-01-01"

