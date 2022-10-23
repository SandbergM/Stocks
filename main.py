#Flask imports
from flask import Flask, request
from config import config_by_name

#  General imports
import json
import os
from dotenv import load_dotenv

load_dotenv()

from app.api.routes_handler import run_route
from app.cron.cron_handler import run_jobs

app = Flask(__name__)
app.config.from_object(config_by_name[os.getenv( "ENV" )])

@app.route( '/api/<sub_api>/<sub_path>' )
def get_sub_api( sub_api = "", sub_path = "" ):
    res = run_route( request )
    return json.dumps(res[0]), res[1]

@app.route( '/cron/<sub_path>' )
def trigger_cron( sub_path = "" ):
    run_jobs( request )
    return "Ok", 200

if __name__ == '__main__':
    app.run()