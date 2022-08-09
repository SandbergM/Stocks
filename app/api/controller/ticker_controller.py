
from app.utils.gcp_secrets import get_secret

from google.cloud import bigquery

client = bigquery.Client()

import json

def get_all_tickers():
    project_id = get_secret( "PROJECT_ID" )
    query_result = client.query( query = f" SELECT ticker, company_name FROM `{ project_id }.stocks.tickers` ORDER BY ticker ASC " ).result()
    return json.dumps( [ dict( row ) for row in query_result ] )