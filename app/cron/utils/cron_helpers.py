
from google.cloud import bigquery
import time

client = bigquery.Client()

from app.utils.gcp_secrets import get_secret

def ready_to_run( job_name ):

    sql_query = f""" 

        SELECT 
            * 
        FROM 
            `{ get_secret( 'PROJECT_ID' ) }.meta_data.cron_jobs` 
        WHERE 
            LOWER( name ) = LOWER( @name )   
    """

    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('name', 'STRING', job_name),
        ]
    )

    res = client.query( sql_query, query_config ).to_dataframe()



    if len( res ) == 0:
        __insert_job_name( job_name )
        return True

    last_inititated = dict( res.iloc[0] )['initiated']

    if last_inititated == 0:
        __set_as_active( job_name )
        return True
    
    return False

def __insert_job_name( job_name ):

    sql_query = f"""
    INSERT INTO `{ get_secret( 'PROJECT_ID' ) }.meta_data.cron_jobs` VALUES( @name, @initiated )
    """

    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('name', 'STRING', job_name),
            bigquery.ScalarQueryParameter('initiated', 'INT64', int( time.time() )),
        ]
    )

    return client.query( sql_query, query_config ).result()

def __set_as_active( job_name ):

    sql_query = f"""
        UPDATE 
            `{ get_secret( 'PROJECT_ID' ) }.meta_data.cron_jobs` 
        SET 
            initiated = @initiated
        WHERE 
            LOWER( name ) = LOWER( @name )
    """

    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('name', 'STRING', job_name),
            bigquery.ScalarQueryParameter('initiated', 'INT64', int( time.time() )),
        ]
    )

    return client.query( sql_query, query_config ).result()


def set_as_completed( job_name ):

    sql_query = f"""
        UPDATE 
            `{ get_secret( 'PROJECT_ID' ) }.meta_data.cron_jobs` 
        SET 
            initiated = 0 
        WHERE 
            LOWER( name ) = LOWER( @name )
    """

    query_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('name', 'STRING', job_name),
        ]
    )

    return client.query( sql_query, query_config ).result()