

#Flask imports
from flask import Flask, request

#  General imports
import json
import os
from dotenv import load_dotenv

load_dotenv()

from app.api.routes_handler import run_route
from app.cron.cron_handler import run_jobs


app = Flask(__name__)

@app.route( '/api/<sub_api>/<sub_path>' )
def get_sub_api( sub_api = "", sub_path = "" ):
    res = run_route( request )
    return json.dumps(res[0]), res[1]

@app.route( '/cron/<sub_path>' )
def trigger_cron( sub_path = "" ):
    run_jobs( request )
    return "Ok", 200

if __name__ == '__main__' and os.getenv("ENV") == 'dev':
    app.run(
        port = os.getenv('PORT', '8080'),
        debug = True,
        threaded = True,
        host = "0.0.0.0"
    )