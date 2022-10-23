
from app.api.controller.ticker_controller import get_all_tickers
from app.api.controller.ticker_controller import get_ticker_prediction
from app.api.service.ticker_service import get_ticker_data

import json

def get_all_tickers_route( request ):
    return get_all_tickers()

def get_ticker_historical_data_route( request ):
    res = get_ticker_data( request.args.get('ticker'), request.args.get('start'), request.args.get('end') )
    return json.dumps([ dict( el ) for el in res.to_json() ])

def get_ticker_prediction_route( request ):
    return get_ticker_prediction( **request.args )