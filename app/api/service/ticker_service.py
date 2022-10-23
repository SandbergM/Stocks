from app.utils import SecretHandler
from app.utils import BigQueryUtils
from datetime import datetime



def get_ticker_data( ticker, start = None, end = None ):

    start = start if start else '2000-01-01'
    end = end if end else str(datetime.today().strftime('%Y-%m-%d'))

    sql_query = f"""
        SELECT 
            * 
        FROM 
            `{ SecretHandler.get_secret( "PROJECT_ID" ) }.stocks.1d_historical_data` 
        WHERE 
            ticker = @ticker
        AND
            date BETWEEN @start AND @end
    """

    query_parameters = [
        { "name" : "ticker", "dtype" : str, "value" : ticker },
        { "name" : "start", "dtype" : str, "value" : start },
        { "name" : "end", "dtype" : str, "value" : end },
    ]

    return BigQueryUtils.query(sql_query, query_parameters)
