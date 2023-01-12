import re
from flask import Blueprint, request

api_routes = Blueprint( 'api_routes', __name__ )

from app.api.controllers.ticker_controller import ticker_search
from app.api.controllers.ticker_controller import add_ticker_to_db
from app.api.controllers.ticker_controller import ticker_history

@api_routes.route('/ticker/ticker_search', methods=["GET"])
def ticker_search_route():
    return ticker_search( **request.args )

@api_routes.route('/ticker/ticker_add', methods=["POST"])
def add_ticker_to_db_route():
    ticker = request.args.get("ticker")
    company_name = request.args.get("company_name")
    country = request.args.get("country")
    return add_ticker_to_db(ticker, company_name, country)


@api_routes.route('/ticker/historical_data', methods=["GET"])
def get_ticker_historical_data_route():

    ticker = request.args.get('ticker')
    
    b_rate = int(request.args.get('b_rate', 10))
    b_diviation = float(request.args.get('b_diviation', 2))
    interval_type = request.args.get('interval_type', 'year')
    interval_length = request.args.get('interval_length', 1)

    wmas = [ re.sub('[^0-9]+', '', v) for k, v in dict(request.args.items()).items() if k[:3] == "wma"]
    rsis = [ re.sub('[^0-9]+', '', v) for k, v in dict(request.args.items()).items() if k[:3] == "rsi"]

    return [dict( el ) for el in ticker_history(ticker, b_rate, b_diviation, wmas, rsis, interval_type, interval_length)]