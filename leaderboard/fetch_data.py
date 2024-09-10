import os
import json
import logging
from typing import Dict

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
API_ENDPOINT = "https://api.github.com/graphql"

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("fetch_data")

# Headers
headers = {"Authorization": f"token {GITHUB_TOKEN}"}
logger.info(f"Headers: {headers}")


def execute_query(query: str, variables: Dict) -> Dict:
    """
    Executes query to fetch data from GraphQL API.

    Args:
        query (str): GraphQL query for fetching data.
        variables (Dict): Variables to be used in the GraphQL query.

    Returns:
        Dict: JSON response containing the fetched data.

    Raises:
        requests.RequestException: If the request fails.
    """

    # Session with retries
    s = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["POST"],
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        # Execute the query
        response = s.post(
            url=API_ENDPOINT,
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        result = response.json()
        logger.info(json.dumps(result, indent=4))
        return result
    except requests.RequestException as e:
        raise requests.RequestException(f"Request failed: {e}")
