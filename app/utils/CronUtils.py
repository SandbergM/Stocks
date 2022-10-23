

import time

from app.utils import SecretHandler
from app.utils import BigQueryUtils

def ready_to_run( job_name ):

    sql_query = f""" 

        SELECT 
            * 
        FROM 
            `{ SecretHandler.get_secret( 'PROJECT_ID' ) }.meta_data.cron_jobs` 
        WHERE 
            LOWER( name ) = LOWER( @name )   
    """

    query_parameters = [{ "name" : "name", "dtype" : str, "value" : job_name }]
    res = BigQueryUtils.query(sql_query, query_parameters)


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
    INSERT INTO `{ SecretHandler.get_secret( 'PROJECT_ID' ) }.meta_data.cron_jobs` VALUES( @name, @initiated )
    """

    query_parameters = [
        { "name" : "name", "dtype" : str, "value" : job_name },
        { "name" : "initiated", "dtype" : int, "value" : int(time.time()) }
    ]            

    return BigQueryUtils.query( sql_query, query_parameters )

def __set_as_active( job_name ):

    sql_query = f"""
        UPDATE 
            `{ SecretHandler.get_secret( 'PROJECT_ID' ) }.meta_data.cron_jobs` 
        SET 
            initiated = @initiated
        WHERE 
            LOWER( name ) = LOWER( @name )
    """

    query_parameters = [
        { "name" : "name", "dtype" : str, "value" : job_name },
        { "name" : "initiated", "dtype" : int, "value" : int(time.time()) }
    ]            

    return BigQueryUtils.query( sql_query, query_parameters )


def set_as_completed( job_name ):

    sql_query = f"""
        UPDATE 
            `{ SecretHandler.get_secret( 'PROJECT_ID' ) }.meta_data.cron_jobs` 
        SET 
            initiated = 0 
        WHERE 
            LOWER( name ) = LOWER( @name )
    """

    query_parameters = [{ "name" : "name", "dtype" : str, "value" : job_name }]            

    return BigQueryUtils.query( sql_query, query_parameters )