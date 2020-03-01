""" Main module for the OSS Leaderboard. """
import logging

from leaderboard.queries.query import query
from leaderboard.utils.data import get_date
from leaderboard.fetch_data import execute_query


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")

variables = {
    "timedelta": get_date(100),
    "username": "sindresorhus",
    "dataCount": 5,
}


def main():
    """ Script entrypoint. """
    execute_query(query, variables)


main()
