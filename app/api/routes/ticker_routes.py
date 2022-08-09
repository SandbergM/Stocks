
from app.api.controller.ticker_controller import get_all_tickers

def ticker_routes_handler( request ):
    return get_all_tickers(), 200