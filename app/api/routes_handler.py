
from app.api.routes.fi_routes import insider_data_route, blanking_history_route
from app.api.routes.ticker_routes import get_ticker_prediction_route, get_all_tickers_route, get_ticker_historical_data_route

def run_route( request ):

    path = request.path.replace( '/api/', '' )

    if path == 'fi/insider_data':
        return insider_data_route( request ), 200

    if path == 'fi/blanking_history':
        return blanking_history_route( request ), 200

    if path == 'ticker/all_tickers':
        return get_all_tickers_route( request ), 200

    if path == 'ticker/predictions':
        return get_ticker_prediction_route( request ), 200

    if path == 'ticker/ticker_historical_data':
        return get_ticker_historical_data_route( request ), 200

    return 'Not found', 404