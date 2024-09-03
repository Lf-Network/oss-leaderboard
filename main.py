""" Main module for the OSS Leaderboard. """

import os
import logging

from typing import List, Dict, Any

from leaderboard.final_html_output import final_html_output
from leaderboard.utils.final_score_table import get_final_score_table
from leaderboard.multi_users_fetch import fetch_contributions_for_multi_users
from leaderboard.utils.intermediate_score_table import get_intermediate_score_table

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")


def get_environment_variables() -> dict:
    """
    Get environment variables.

    Returns:
        dict: A dictionary containing the environment variables.
    """
    return {
        "USER_LIST": os.environ.get("USER_LIST", ""),
        "DURATION_IN_DAYS": int(os.environ.get("DURATION_IN_DAYS", 5)),
        "PAGE_DATA_COUNT": int(os.environ.get("PAGE_DATA_COUNT", 5)),
        "START_DATE": os.environ.get("START_DATE", "2023-10-01T00:00:00"),
    }


def get_user_list(environment_variables: dict) -> list:
    """
    Get user list.

    Args:
        environment_variables (dict): A dictionary containing the environment variables.

    Returns:
        list: A list of users.
    """
    return [x.strip() for x in environment_variables["USER_LIST"].split(",")]


def get_variables(environment_variables: dict) -> dict:
    """
    Get variables.

    Args:
        environment_variables (dict): A dictionary containing the environment variables.

    Returns:
        dict: A dictionary containing the variables.
    """
    return {
        "timedelta": environment_variables["START_DATE"],
        "dataCount": environment_variables["PAGE_DATA_COUNT"],
    }


def generate_html(user_list: List[str], variables: Dict[str, Any]) -> str:
    """
    Generates an HTML representation of the final leaderboard based on user contributions.

    This function fetches contributions for multiple users, calculates their scores, 
    and generates an HTML string representing the final leaderboard.

    Args:
        user_list (List[str]): A list of user identifiers for whom contributions are to be fetched.
        variables (Dict[str, Any]): A dictionary of variables that may affect the contribution fetching process.

    Returns:
        str: An HTML string representing the final leaderboard based on the calculated scores.
    """

    result = fetch_contributions_for_multi_users(user_list, variables)

    intermediate_score_table = get_intermediate_score_table(result)
    final_score_table = get_final_score_table(intermediate_score_table, user_list)

    return final_html_output(final_score_table)


def write_html(html_string: str) -> None:
    """
    Writes an HTML string to a file named 'index.html' in the 'build' directory.

    If the 'build' directory does not exist, it will be created.

    Args:
        html_string (str): The HTML string to be written to the file.

    Returns:
        None
    """
    if not os.path.exists("build"):
        os.mkdir("build")
    
    with open("build/index.html", "w") as f:
        f.write(html_string)


if __name__ == "__main__":
    environment_variables = get_environment_variables()

    user_list = get_user_list(environment_variables)
    variables = get_variables(environment_variables)

    html_string = generate_html(user_list, variables)

    write_html(html_string)
