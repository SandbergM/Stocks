

# Jobs
from app.cron.jobs.yahoo_finance_tickers.main import get_yahoo_finance_tickers
from app.cron.jobs.fi_insider_trading.main import get_insider_trades
from app.cron.jobs.fi_blanking_history.main import get_blankings

# Helpers
from app.cron.utils.cron_helpers import ready_to_run
from app.cron.utils.cron_helpers import set_as_completed
from app.utils.common import log

def run_jobs( request ):

    trigger = request.path.replace( '/cron/', '' )

    if trigger == 'get_yahoo_finance_tickers':
        run_cron([
            get_yahoo_finance_tickers
        ])
    
    if trigger == "get_insider_trades":
        run_cron([
            get_insider_trades
        ])

    if trigger == "get_blankings":
        run_cron([
            get_blankings
        ])


def run_cron( funcs ):

    for func in funcs:
        try:
            if ready_to_run( func.__name__  ):
                log( f"Running cron { func.__name__  }" )
                func()
                set_as_completed( func.__name__ )
        except Exception as e:
            set_as_completed( func.__name__ )
            print( e )