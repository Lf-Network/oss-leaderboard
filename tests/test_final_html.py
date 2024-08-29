import os
import pytest
import difflib
import pandas as pd

from final_html_output import final_html_output
from multi_users_fetch import fetch_contributions_for_multi_users
from leaderboard.utils.final_score_table import get_final_score_table
from leaderboard.utils.intermediate_score_table import get_intermediate_score_table


@pytest.fixture
def final_score_table() -> pd.DataFrame:
    """
    Fixture to fetch and construct the final score table for users.

    This function retrieves a list of users and relevant parameters from environment variables,
    fetches contributions for these users, and constructs the final score table.

    Returns:
        pd.DataFrame: The final score table containing user scores.
    """
    user_list = [
        user.strip()
        for user in os.environ.get("USER_LIST", "").split(",")
        if user.strip()
    ]
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


def test_final_html(final_score_table: pd.DataFrame) -> None:
    """
    Test the final HTML against expected results.

    This function reads expected results from a HTML file and
    compares the HTML file with the actual HTML file.

    Args:
        final_score_table (pd.DataFrame): The final score table to be tested.

    Raises:
        AssertionError: If the final HTML does not match the expected HTML.
    """

    final_html_output(final_score_table)

    # Compare the generated HTML
    with open("test_output/index.html", "r") as f:
        expected_html = f.read()

    with open("build/index.html", "r") as f:
        actual_html = f.read()

    # Close the file handles
    f.close()

    # Compare the HTML content
    diff = difflib.unified_diff(
        expected_html.splitlines(),
        actual_html.splitlines(),
        fromfile='expected',
        tofile='actual',
        lineterm=''
    )

    diff_lines = '\n'.join(diff)
    assert diff_lines == '', f"HTML content differs:\n{diff_lines}"
