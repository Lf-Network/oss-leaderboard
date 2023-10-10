""" Main module for the OSS Leaderboard. """
import os
import logging

from leaderboard.utils.intermediate_score_table import get_intermediate_score_table
from leaderboard.utils.final_score_table import get_final_score_table, set_users_info
from multi_users_fetch import fetch_contributions_for_multi_users, fetch_users_info
from final_html_output import final_html_output

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")

user_list = [x.strip() for x in os.environ.get("USER_LIST", "").split(",")]
duration = int(os.environ.get("DURATION_IN_DAYS", 5))
data_count = int(os.environ.get("PAGE_DATA_COUNT", 5))
start_date = os.environ.get("START_DATE", "2023-10-01T00:00:00")


variables = {
    "timedelta": start_date,
    "dataCount": data_count,
}


def main():
    """Script entrypoint."""

    result = fetch_contributions_for_multi_users(user_list, variables)
    users_info = fetch_users_info(user_list)

    intermediate_score_table = get_intermediate_score_table(result)
    final_score_table = get_final_score_table(intermediate_score_table, user_list)
    final_score_table = set_users_info(final_score_table, users_info)

    final_html_output(final_score_table)


main()
