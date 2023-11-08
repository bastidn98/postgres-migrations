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
  }
}
'''


def get_url():
    load_dotenv()
    if os.environ["TESTING_URL"].lower() in ("t", "true", "yes"):
        dns = "ip-172-31-23-71.eu-west-2.compute.internal"
    else:
        ec2 = boto3.client("ec2")
        filters = [{"Name": "tag:Name", "Values": ["portal-prod"]}, {"Name": "instance-state-name", "Values": ["running"]}]
        reservations = ec2.describe_instances(Filters=filters)
        dns = reservations["Reservations"][0]["Instances"][0]["PrivateDnsName"]
    return dns

def get_clients(retries=3):
    url = f"http://{get_url()}:8000/graphql"
    headers = {
        "Remote-User": remote_user,
    }
    retried = 0
    while retried < retries:      
        try:
            logger.debug('Trying to get clients')
            response = requests.post(url=url, json={"query":clients_query}, headers=headers)
            break
        except json.JSONDecodeError as e:
                retried += 1
                if retries == retries:
                    logger.critical("Not getting expected Client data from Core Server Graphql query")
                    raise 
                logger.warning('Retrying request to core server')
    client_data = json.loads(response.content)["data"]['entities']
    return client_data

def make_client_choices(retries=3):
    client_data = get_clients(retries)
    return [(f"{client['code']}-{client['name']}", f'{client["name"]} ({client["code"]})') for client in client_data]
    
if __name__ == "__main__":
    a = make_client_choices()