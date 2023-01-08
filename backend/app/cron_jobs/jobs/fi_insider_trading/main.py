

from datetime import date

from app.api.controllers.fi_controller import get_insider_data
from app.utils.CommonUtils import log

from app.data import DbHandler

def get_insider_trades():
    log("Running get_insider_trades")
    from_transactions_date = max_publiceringsdatum()
    to_transactions_date = date.today()
    data = get_insider_data( from_transactions_date, to_transactions_date )
    DbHandler.multiple_insert("INSERT INTO fi_insider_trades VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [ tuple( r.values() ) for r in data])
    return True

def max_publiceringsdatum():

    res = DbHandler.select_query("SELECT MAX( publiceringsdatum ) AS publiceringsdatum FROM fi_insider_trades")

    if len(res) and res[0].get('publiceringsdatum'):
        max_publiceringsdatum = res[0].get('publiceringsdatum')
        print("max_publiceringsdatum : ", max_publiceringsdatum)
        DbHandler.delete_query( f""" DELETE FROM fi_insider_trades WHERE publiceringsdatum = ? """, (max_publiceringsdatum, ) )
        return max_publiceringsdatum

    else:
        return "2000-01-01"

