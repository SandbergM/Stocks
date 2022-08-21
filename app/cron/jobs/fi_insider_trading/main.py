
from app.utils.gcp_secrets import get_secret
from datetime import datetime

from app.api.controller.fi_controller import get_insider_data

def get_insider_trades():

    from_transactions_date = max_publiceringsdatum()
    to_transactions_date = datetime.date.today()
    data = get_insider_data( { "from_transactions_date" : from_transactions_date, "to_transactions_date" : to_transactions_date, "as_type" : 'dataframe' } )
    data.rename(columns = { col : column_name_fix( col ) for col in data.columns }, in_place = True)
    save_result( data )

def save_result( df ):
    try:
        df.to_gbq(
            destination_table   = "stocks.fi_insider_trades", 
            project_id          = get_secret( 'PROJECT_ID' ),
            if_exists           = 'append',
            reauth              = False,
            chunksize           = 10000,
            progress_bar        = False
        )
        return True
    except Exception as e:
        print(e)
        return False

def column_name_fix( s ):

    s = s.replace( 'å', 'a' )
    s = s.replace( 'ä', 'a' )
    s = s.replace( 'ö', 'o' )
    s = s.replace( ' ', '_' )

    return s.lower()

def max_publiceringsdatum():

    sql_query = f"""
            SELECT
                *
            FROM
                { get_secret( 'PROJECT_ID' ) }.stocks.fi_insider_trades`
            WHERE
                publiceringsdatum = (
                    SELECT
                        MAX( publiceringsdatum )
                    FROM
                        `{ get_secret( 'PROJECT_ID' ) }.stocks.fi_insider_trades` 
                )
    """
