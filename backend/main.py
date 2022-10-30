#Flask imports
from flask import Flask
from config import config_by_name

#  General imports
import os
from dotenv import load_dotenv

load_dotenv()

from app.api.routes.api_routes import api_routes
from app.__cron_jobs.cron_routes import cron_routes

app = Flask(__name__)

app.register_blueprint(cron_routes)
app.register_blueprint(api_routes)
app.config.from_object(config_by_name[os.getenv( "ENV" )])

if __name__ == '__main__':
    app.run()