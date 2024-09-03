""" Main module for the OSS Leaderboard. """
import os
import logging

from leaderboard.utils.intermediate_score_table import get_intermediate_score_table
from leaderboard.utils.final_score_table import get_final_score_table
from multi_users_fetch import fetch_contributions_for_multi_users
from final_html_output import final_html_output

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")

user_list = [x.strip() for x in os.environ.get("USER_LIST", "").split(",")]
data_count = int(os.environ.get("PAGE_DATA_COUNT", 5))
start_date = os.environ.get("START_DATE", "2023-10-01T00:00:00")


variables = {
    "timedelta": start_date,
    "dataCount": data_count,
}


def generate_html(user_list, variables):
    """Generate HTML output for a leaderboard based on user contributions.

    This function fetches contributions for multiple users, calculates their scores, 
    and generates an HTML representation of the final leaderboard.

    Args:
        user_list (list): A list of user identifiers for whom contributions are to be fetched.
        variables (dict): A dictionary of variables that may affect the contribution fetching process.

    Returns:
        str: An HTML string representing the final leaderboard based on the calculated scores.
    """

    result = fetch_contributions_for_multi_users(user_list, variables)

    intermediate_score_table = get_intermediate_score_table(result)
    final_score_table = get_final_score_table(intermediate_score_table, user_list)

    return final_html_output(final_score_table)


if __name__ == "__main__":
    html_string = generate_html(user_list, variables)

    if not os.path.exists("build"):
        os.mkdir("build")
    
    with open("build/index.html", "w") as f:
        f.write(html_string)
