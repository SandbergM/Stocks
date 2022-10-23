from app.utils import SecretHandler

from google.cloud import bigquery

client = bigquery.Client()


def query( query, query_parameters = None ):

    params = []

    dtypes = {
        "str" : "STRING",
        "int" : "INTEGER"
    }

    if query_parameters is None:
        query_parameters = []

    for query_parameter in query_parameters:
            bigquery.ScalarQueryParameter(
                query_parameter.get("name"), 
                dtypes.get(f"{query_parameter.get('dtype')}"), 
                query_parameter.get("value")
            )

    job_config = bigquery.QueryJobConfig(query_parameters=params)

    return client.query( query = query, job_config = job_config ).to_dataframe()

def save( df ):

    try:
        df.to_gbq(
            destination_table   = "stocks.fi_insider_trades", 
            project_id          = SecretHandler.get_secret( 'PROJECT_ID' ),
            if_exists           = 'append',
            reauth              = False,
            chunksize           = 10000,
            progress_bar        = False
        )
        return True

    except Exception as e:
        print(e)
        return False