
from datetime import datetime
from app.api.controllers.ticker_controller import ticker_history

def get_ticker_data( ticker, b_rate, b_diviation, start = None, end = None ):
    start = start if start else '2000-01-01'
    end = end if end else str(datetime.today().strftime('%Y-%m-%d'))
    return ticker_history(ticker, b_rate, b_diviation, start, end)
