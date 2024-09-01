import json
import logging
import pandas as pd
from typing import Dict

from leaderboard.queries.query import query
from leaderboard.fetch_data import execute_query
from leaderboard.utils.formatter import convert_to_intermediate_table

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("fetch_data")


def fetch_contributions_for_user(user_name: str, query_variables: Dict) -> pd.DataFrame:
    """
    Fetches contribution data for a single GitHub user and returns an intermediate table dataframe.

    Args:
        user_name (str): GitHub username whose contribution data is to be fetched.
        query_variables (Dict): Arguments required for the OSS graphql query.

    Returns:
        pd.DataFrame: Intermediate table dataframe for the user.
    """
    query_variables["username"] = user_name
    page_info = initialize_page_info()

    intermediate_dataframes = []
    while True:
        query_variables = update_query_variables(query_variables, page_info)
        result = execute_query(query, query_variables)

        if not result.get("data", {}).get("user"):
            logger.info("Invalid GitHub user detected %s\n", user_name)
            break

        flat_data = convert_to_intermediate_table(
            json.dumps(result, indent=4), query_variables["timedelta"]
        )

        intermediate_dataframes.append(flat_data["intermediate_table"])

        page_info = update_page_info(page_info, flat_data["page_info"])

        if not should_continue_fetching(page_info):
            break

    return pd.concat(intermediate_dataframes)


def initialize_page_info() -> Dict:
    """
    Initializes the page info dictionary with default values.

    Returns:
        Dict: Page info dictionary with default values.
    """
    return {
        "page_info_T1": {"hasNextPage": True, "endCursor": None},
        "page_info_T2": {"hasNextPage": True, "endCursor": None},
        "page_info_T3": {"hasNextPage": True, "endCursor": None},
        "page_info_T4": {"hasPreviousPage": True, "startCursor": None},
        "page_info_T5": {"hasNextPage": True, "endCursor": None},
    }


def update_query_variables(query_variables: Dict, page_info: Dict) -> Dict:
    """
    Updates the query variables with pagination info.

    Args:
        query_variables (Dict): Query variables dictionary.
        page_info (Dict): Page info dictionary.

    Returns:
        Dict: Updated query variables dictionary.
    """
    query_variables.update(
        {
            "pullReqCursor": page_info["page_info_T1"]["endCursor"],
            "pullreqreviewcursor": page_info["page_info_T2"]["endCursor"],
            "issueCursor": page_info["page_info_T3"]["endCursor"],
            "issueCommentsCursor": page_info["page_info_T4"]["startCursor"],
            "repoCursor": page_info["page_info_T5"]["endCursor"],
        }
    )

    if page_info["page_info_T4"]["hasPreviousPage"]:
        query_variables["issueCommentDataCount"] = query_variables["dataCount"]
    else:
        query_variables["issueCommentDataCount"] = 0

    return query_variables


def update_page_info(page_info: Dict, new_page_info: Dict) -> Dict:
    """
    Updates the page info dictionary with new values.

    Args:
        page_info (Dict): Page info dictionary.
        new_page_info (Dict): New page info dictionary.

    Returns:
        Dict: Updated page info dictionary.
    """
    for key in page_info:
        if page_info[key].get("hasNextPage") or page_info[key].get("hasPreviousPage"):
            page_info[key] = new_page_info[key]

    return page_info


def should_continue_fetching(page_info: Dict) -> bool:
    """
    Checks if fetching should continue based on page info.

    Args:
        page_info (Dict): Page info dictionary.

    Returns:
        bool: True if fetching should continue, False otherwise.
    """
    return any(
        page_info[key].get("hasNextPage", False)
        or page_info[key].get("hasPreviousPage", False)
        for key in page_info
    )


def fetch_contributions_for_multi_users(
    user_list: list, query_variables: Dict
) -> pd.DataFrame:
    """
    Fetches contribution data for multiple GitHub users and returns a combined intermediate table dataframe.

    Args:
        user_list (list): List of GitHub usernames whose contribution data is to be fetched.
        query_variables (Dict): Arguments required for the OSS graphql query.

    Returns:
        pd.DataFrame: Combined intermediate table dataframe for all users.
    """
    intermediate_dataframes = (
        fetch_contributions_for_user(user_name, query_variables.copy())
        for user_name in user_list
    )

    return pd.concat(intermediate_dataframes)
