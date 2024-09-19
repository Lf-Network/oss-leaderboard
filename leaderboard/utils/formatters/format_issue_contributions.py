import pandas as pd
from typing import List, Dict, Any

from leaderboard.constants.contribTypes import scores


def format_issue_contributions(
    issue_contribution_list: List[Dict[str, Any]],
    user_id: str,
    user_name: str,
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Formats a list of issue contributions and appends them to a pandas DataFrame.

    Args:
        issue_contribution_list (List[Dict[str, Any]]): A list of issue contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the formatted contributions will be appended.

    Returns:
        pd.DataFrame: The pandas DataFrame with the formatted contributions appended.
    """
    new_df = pd.DataFrame(
        [
            {
                "github_id": issue["node"]["issue"]["id"],
                "user_id": user_id,
                "user_name": user_name,
                "type": scores["T3"]["description"],
                "repo_id": issue["node"]["issue"]["repository"]["id"],
                "repo_owner_id": issue["node"]["issue"]["repository"]["owner"]["id"],
                "reactions": issue["node"]["issue"]["reactions"]["totalCount"],
                "label": ", ".join(
                    edge["node"]["name"]
                    for edge in issue["node"]["issue"]["labels"]["edges"]
                ),
                "comments": issue["node"]["issue"]["comments"]["totalCount"],
                "created_at": issue["node"]["issue"]["createdAt"],
                "last_updated_at": issue["node"]["issue"]["updatedAt"],
            }
            for issue in issue_contribution_list
        ]
    )

    return pd.concat([df, new_df], ignore_index=True)
