import os
import json
from databricks.sdk import WorkspaceClient

# Define volume, folder, and file details.
# catalog = 'footballdb'
# schema = 'default'
# volume = 'jsonfiles'
# volume_folder = 'fixtures'

def get_databricks_credentials(env: str) -> dict:
    """
    Retrieves Databricks credentials from a JSON configuration file based on the specified environment.

    Args:
        env (str): The environment for which to retrieve credentials (e.g., 'dev', 'prod').
    """

    if env in ["prd"]:
        #config_path = '/opt/airflow/dags/soccer_analytics/config.json'
        config_path = '/Workspace/Users/spcoromulo@gmail.com/PaineldoFutebol/Databricks/configDatabricks.json'
    elif env in ["dev"]:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configDatabricks.json')

    file = open(config_path)
    args = json.load(file)
    file.close()

    return args

def init_databricks_credentials():
    """
    Initializes the Databricks WorkspaceClient using credentials from a JSON configuration file.
    """
    try:
        args = get_databricks_credentials('dev')  # or 'prd' depending on the environment

        w = WorkspaceClient(host=args['host'], token=args['token'])
        return w
    except Exception as e:
        print(f"Error initializing WorkspaceClient: {e}")
        return None
    
def upload_file_to_volume(local_file_path: str, catalog: str, volume: str, folder: str, filename: str):
    """
    Uploads a file to a Databricks volume.

    Args:
        local_file_path (str): The local path of the file to upload.
        volume_folder_path (str): The destination path in the Databricks volume.
    """

    volume_folder_path = f"/Volumes/{catalog}/default/{volume}/{folder}/{filename}" 
    try:        
        w = init_databricks_credentials()
        print(f"Sending file to {volume_folder_path}")
        with open(local_file_path, "rb") as f:
            w.files.upload_from(volume_folder_path, local_file_path, overwrite=True)
        print(f"File uploaded successfully to {volume_folder_path}")
        os.remove(local_file_path)  # Remove the local file after successful upload
    except Exception as e:
        #print(f"Error uploading file: {e}")
        raise Exception(f"Error uploading file: {e}")


def get_api_credentials(env: str) -> dict:
    """
    Retrieves API credentials from a JSON configuration file based on the specified environment.

    Args:
        env (str): The environment for which to retrieve credentials (e.g., 'dev', 'prod').
    """

    if env in ["prd"]:
        #config_path = '/opt/airflow/dags/soccer_analytics/config.json'
        config_path = '/Workspace/Users/spcoromulo@gmail.com/PaineldoFutebol/Databricks/config.json'
    elif env in ["dev"]:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

    file = open(config_path)
    args = json.load(file)
    file.close()

    return args