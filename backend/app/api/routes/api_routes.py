from datetime import datetime
from dateutil.relativedelta import relativedelta

from flask import Blueprint, request

api_routes = Blueprint( 'api_routes', __name__ )

from app.api.controllers.ticker_controller import ticker_search
from app.api.controllers.ticker_controller import add_ticker_to_db
from app.api.services.ticker_service import get_ticker_data

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

    today_date = datetime.now()
    last_monday = today_date - relativedelta(days=-today_date.weekday(), weeks=1)

    dates = {
        '1w' : last_monday - relativedelta(weeks=1),
        '2w' : last_monday - relativedelta(weeks=2),
        '3w' : last_monday - relativedelta(weeks=3),
        '1m' : last_monday - relativedelta(months=1),
        '2m' : last_monday - relativedelta(months=2),
        '3m' : last_monday - relativedelta(months=3),
        '6m' : last_monday - relativedelta(months=6),
        '1y' : last_monday - relativedelta(years=1),
        '2y' : last_monday - relativedelta(years=2),
        '3y' : last_monday - relativedelta(years=3),
        '5y' : last_monday - relativedelta(years=5),
    }

    b_rate = int(request.args.get('b_rate', 10))
    b_diviation = float(request.args.get('b_diviation', 2))
    ticker = request.args.get('ticker')

    if request.args.get('timeframe') in dates:
        start = dates.get(request.args.get('timeframe'))
        return [dict( el ) for el in get_ticker_data(ticker, b_rate, b_diviation, start) if datetime.strptime(el.get('date'), '%Y-%m-%d') >= start]

    return [dict( el ) for el in get_ticker_data(ticker,b_rate, b_diviation)]