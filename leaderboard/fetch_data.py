''' Fetch required data from the GitHub API. '''
import os 
import logging

import requests


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('fetch_data')

ACCESS_TOKEN = os.environ.get('GITHUB_TOKEN')
API_ENDPOINT = "https://api.github.com/graphql"

headers = {"Authorization": ACCESS_TOKEN}

logger.info(headers)


def execute_query(query: str, username: str): 
    ''' Executes query to fetch data from GraphQL API.

    Args: 
        query: GraphQL query for fetching data. 
        username: whose data will be fetched.
    '''
    request = requests.post(url = API_ENDPOINT, json = {"query": query.format(username = username)}, headers = headers)

    if request.status_code == 200: 
        logger.info(request.json())
    else: 
        raise Exception("Request failed with code of {} \n{}.".format(request.status_code, request.text))
