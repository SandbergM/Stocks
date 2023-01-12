
import time

# Jobs
from app.cron_jobs.jobs.yahoo_finance_tickers.main import get_yahoo_finance_tickers
from app.cron_jobs.jobs.fi_insider_trading.main import get_insider_trades
from app.cron_jobs.jobs.fi_blanking_history.main import get_blankings

from app.utils import CommonUtils
from app.data import DbHandler

from flask import Blueprint

import os

cron_routes = Blueprint('cron_routes', __name__ )

@cron_routes.route('/cron/yahoo_finance')
def yahoo_finance_1d():
    run_cron( get_yahoo_finance_tickers )
    return "Ok", 200

@cron_routes.route('/cron/fi_insider_trades')
def fi_insider_trades():
    run_cron( get_insider_trades )
    return "Ok", 200

@cron_routes.route('/cron/fi_blanking_history')
def fi_blanking_history_route():
    run_cron( get_blankings )
    return "Ok", 200

def run_cron( func ):

    running_cron = DbHandler.select_query("SELECT * FROM cron_jobs WHERE job_name = ? and inititated > ?",(func.__name__, int( time.time() - 3_600)))

    if len(running_cron) == 0 or os.getenv( 'ENV' ) == 'dev':
        DbHandler.multiple_insert( "INSERT INTO cron_jobs VALUES(?,?)", [( func.__name__, int(time.time()) )] )
        CommonUtils.log( f"Running { func.__name__ }" )
        func()