
from app.api.controllers.fi_controller import get_blanking_history

from ....__data import DbHandler

def get_blankings():

    from_date = DbHandler.select_query("SELECT IFNULL(MAX(position_date), '1900-01-01') AS position_date FROM fi_short_positions")[0].get('position_date')
    res = get_blanking_history() if from_date is None else get_blanking_history( from_date )

    if from_date is not None:
        DbHandler.delete_query( "DELETE FROM fi_short_positions WHERE position_date = ?", (from_date,))
    res = [tuple( el.values() ) for el in res] 
    DbHandler.multiple_insert( "INSERT INTO fi_short_positions VALUES(?,?,?,?,?,?)", res )