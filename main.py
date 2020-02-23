""" Main module for the OSS Leaderboard. """
import logging
from leaderboard.query.query import test_query
from leaderboard.fetch_data import execute_query


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")


def main():
    """ Script entrypoint. """
    execute_query(test_query, "yankeexe")


main()
