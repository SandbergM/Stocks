
from app.utils import SecretHandler
from app.api.controller.fi_controller import get_blanking_history

def get_blankings():
    save_result( get_blanking_history() )

def save_result( df ):

    try:
        df.to_gbq(
            destination_table   = "stocks.fi_insider_blankings", 
            project_id          = SecretHandler.get_secret( 'PROJECT_ID' ),
            if_exists           = 'replace',
            reauth              = False,
            chunksize           = 10000,
            progress_bar        = False
        )
        return True
    except Exception as e:
        print(e)
        return False