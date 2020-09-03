""" Main module for the OSS Leaderboard. """
import logging
import json

from leaderboard.queries.query import query
from leaderboard.utils.data import get_date
from leaderboard.fetch_data import execute_query

from leaderboard.utils.formatter import convert_to_intermediate_table
from leaderboard.utils.intermediate_score_table import get_intermediate_score_table
from leaderboard.utils.final_score_table import get_final_score_table
from leaderboard.utils.data import convert_df_to_markdown

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")

variables = {
    "timedelta": get_date(100),
    "username": "sindresorhus",
    "dataCount": 5,
}


def main():
    """ Script entrypoint. """

    result = execute_query(query, variables)

    intermediate_table = convert_to_intermediate_table(
        json.dumps(result.json(), indent=4)
    )

    intermediate_score_table = get_intermediate_score_table(intermediate_table)
    final_score_table = get_final_score_table(intermediate_score_table)
    markdown_table = convert_df_to_markdown(final_score_table)

    print(markdown_table)


main()
