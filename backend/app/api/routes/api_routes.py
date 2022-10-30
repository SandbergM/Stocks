

from flask import Blueprint, request

api_routes = Blueprint( 'api_routes', __name__ )

from app.api.controllers.ticker_controller import ticker_search
from app.api.controllers.ticker_controller import get_ticker_prediction
from app.api.services.ticker_service import get_ticker_data

import json
@api_routes.route('/ticker/ticker_search', methods=["GET"])
def ticker_search_route():
    return ticker_search( **request.args )

@api_routes.route('/ticker/historical_data', methods=["GET"])
def get_ticker_historical_data_route():
    res = get_ticker_data( request.args.get('ticker'), request.args.get('start'), request.args.get('end') )
    return json.dumps([ dict( el ) for el in res.to_json() ])

@api_routes.route('/ticker/prediciton', methods=["GET"])
def get_ticker_prediction_route():
    return get_ticker_prediction( **request.args )