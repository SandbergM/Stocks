
from datetime import datetime
from app.api.controllers.ticker_controller import ticker_history

def get_ticker_data(ticker, b_rate, b_diviation, wmas, rsis, interval_type, interval_length):
    return ticker_history(ticker, b_rate, b_diviation, wmas, rsis, interval_type, interval_length)
