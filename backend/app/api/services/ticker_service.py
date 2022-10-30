
from datetime import datetime
import pandas as pd


def get_ticker_data( ticker, start = None, end = None ):
    start = start if start else '2000-01-01'
    end = end if end else str(datetime.today().strftime('%Y-%m-%d'))
    return 
