from dotenv import load_dotenv
load_dotenv()


#Flask imports
from flask import Flask, request
from flask import jsonify
import os

from app.api.routes_handler import run_route
from app.cron.cron_handler import run_jobs

app = Flask(__name__)

@app.route( '/api/<sub_api>/<sub_path>' )
def get_sub_api( sub_api = "", sub_path = "" ):
    res, status = run_route( request )
    return jsonify(res), status

@app.route( '/cron/<sub_path>' )
def trigger_cron( sub_path = "" ):
    run_jobs( request )
    return "Ok", 200

if __name__ == '__main__':

    from config import config_by_name
    app.config.from_object(config_by_name[os.getenv( "ENV" )])

    app.run()