''' Main module for the OSS Leaderboard. '''
from queries import test_query
from fetch_data import execute_query


def main(): 
    ''' Script entrypoint. '''
    execute_query(test_query, 'yankeexe')

main()
