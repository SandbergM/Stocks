#  General imports
import os

#  Load env variables
from dotenv import load_dotenv
load_dotenv()

#  Routes
from app.api.routes.api_routes import api_routes
from app.cron_jobs.cron_routes import cron_routes

#Flask imports
from flask import Flask
from config import config_by_name

# Init app and load routes
app = Flask(__name__)
app.register_blueprint(cron_routes)
app.register_blueprint(api_routes)

#  Load config based on ENV variable
app.config.from_object(config_by_name[os.getenv( "ENV", 'DEV' )])

if __name__ == '__main__':
    app.run()