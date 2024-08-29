import os
import pytest
import pandas as pd
from leaderboard.utils.intermediate_score_table import get_intermediate_score_table
from leaderboard.utils.final_score_table import get_final_score_table
from multi_users_fetch import fetch_contributions_for_multi_users


@pytest.fixture
def final_score_table() -> pd.DataFrame:
    """
    Fixture to fetch and construct the final score table for users.

    This function retrieves a list of users and relevant parameters from environment variables,
    fetches contributions for these users, and constructs the final score table.

    Returns:
        pd.DataFrame: The final score table containing user scores.
    """
    user_list = [user.strip() for user in os.environ.get("USER_LIST", "").split(",") if user.strip()]
    data_count: int = int(os.environ.get("PAGE_DATA_COUNT", 5))
    start_date: str = os.environ.get("START_DATE", "2023-10-01T00:00:00")

    # Prepare variables for fetching contributions
    variables = {
        "timedelta": start_date,
        "dataCount": data_count,
    }

    # Fetch contributions and construct score tables
    result = fetch_contributions_for_multi_users(user_list, variables)
    intermediate_score_table = get_intermediate_score_table(result)
    final_score_table = get_final_score_table(intermediate_score_table, user_list)

    return final_score_table


def test_final_score_table(final_score_table: pd.DataFrame) -> None:
    """
    Test the final score table against expected results.

    This function reads expected results from a CSV file, sets the index for comparison,
    and asserts that the final score table matches the expected DataFrame.

    Args:
        final_score_table (pd.DataFrame): The final score table to be tested.

    Raises:
        AssertionError: If the final score table does not match the expected DataFrame.
    """
    # Read the expected results from the CSV file
    expected_df = pd.read_csv('test_output/final_scores.csv')

    # Set the index of both DataFrames to 'User Name'
    final_score_table.set_index("User Name", inplace=True)
    expected_df.set_index("User Name", inplace=True)

    # Compare the DataFrames
    pd.testing.assert_frame_equal(final_score_table, expected_df)