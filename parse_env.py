from pathlib import Path
from dotenv import load_dotenv
from os import getenv

def load_from_env_file(env_file_path:str=None):
    if env_file_path:
        if not Path.exists(env_file_path):
            raise FileNotFoundError(f'Environment file not found: {env_file_path}')
        load_dotenv(env_file_path)
    else:
        default_env_files = ['.env', 'secrets.env', 'qualtrics.env']
        for default_env_file in default_env_files:
            if Path.exists(default_env_file):
                load_dotenv(default_env_file)
                print(f'load from default file {default_env_file}')
                break
    api_token = getenv('QUALTRICS_API_TOKEN')
    client_id = getenv('QUALTRICS_CLIENT_ID') 
    client_secret = getenv('QUALTRICS_CLIENT_SECRET')
    scope = getenv('QUALTRICS_SCOPE', 'manage:all')
    datacenter = getenv('QUALTRICS_DATACENTER')
    
    return {
        'api_token': api_token,
        'client_id': client_id, 
        'client_secret': client_secret,
        'scope': scope,
        'datacenter': datacenter
    }
