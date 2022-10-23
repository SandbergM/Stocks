import logging
import os

from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def get_secret( secret ):

    try:
        secrets_project_id = '669434566480'
        request = {"name": f'projects/{ secrets_project_id }/secrets/{ secret }/versions/latest'}
        response = client.access_secret_version(request)
        return response.payload.data.decode("UTF-8")

    except:
        logging.warning(f'Secret "{secret}" could not be loaded')
        return None
