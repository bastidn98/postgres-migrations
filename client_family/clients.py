import requests, json, boto3, os
from dotenv import load_dotenv
from .logger import logging

logger = logging.getLogger(__package__)

remote_user = "nbastida@treasuryspring.com"

clients_query = '''
query{
  entities{
    code
    name
    domains
    status
  }
}
'''

# graphql_url = 'internal-core-unprotected-1806904533.eu-west-2.elb.amazonaws.com:80'
graphql_url = 'ip-172-31-5-83.eu-west-2.compute.internal:8000'


def get_clients(retries=3):
    url = f"http://{graphql_url}/graphql"
    headers = {
        "Remote-User": remote_user,
    }
    # retried = 0
    # while retried < retries:      
    try:
        logger.debug('Trying to get clients')
        response = requests.post(url=url, json={"query":clients_query}, headers=headers)
        # break
    except json.JSONDecodeError as e:
            # retried += 1
            # if retries == retries:
            logger.critical("Not getting expected Client data from Core Server Graphql query")
            raise e
            logger.warning('Retrying request to core server')
    client_data = json.loads(response.content)["data"]['entities']
    return client_data

def make_client_choices(retries=3, filter_status=True):
    client_data = get_clients(retries)
    if filter_status:
        return [(f"{client['code']}:{client['name']}", f'{client["name"]} ({client["code"]})') for client in client_data if client['status'] == 'Active']
    return [(f"{client['code']}:{client['name']}", f'{client["name"]} ({client["code"]})') for client in client_data]

def client_code_name_dict(retries=3, filter_status=True):
    client_data = get_clients(retries)
    if filter_status:
        return {client['code']: client['name'] for client in client_data if client['status'] == 'Active'}
    return {client['code']: client['name'] for client in client_data}

def client_code_domain_dict(retries=3, filter_status=True):
    client_data = get_clients(retries)
    if filter_status:
        return {client['code']: client['domains'] for client in client_data if client['status'] == 'Active'}
    return {client['code']: client['domains'] for client in client_data}

def client_code_data_dict(retries=3, filter_status=True):
    client_data = get_clients(retries)
    if filter_status:
        return {client['code']: client for client in client_data if client['status'] == 'Active'}
    return {client['code']: client for client in client_data}
    

if __name__ == "__main__":
    a = client_code_domain_dict()
    b = client_code_data_dict()
    x=10