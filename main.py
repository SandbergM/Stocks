from dotenv import load_dotenv
load_dotenv()


#Flask imports
from flask import Flask, request
from flask import jsonify
import os

from app.api.routes.ticker_routes import ticker_routes_handler

app = Flask(__name__)

@app.route( '/api/<sub_path>' )
def get_api( sub_path = "" ):
    res, status = ticker_routes_handler( request )
    return res, status

if __name__ == '__main__':

    from config import config_by_name
    app.config.from_object(config_by_name[os.getenv( "ENV" )])

    app.run()