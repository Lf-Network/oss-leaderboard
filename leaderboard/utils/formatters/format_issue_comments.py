import pandas as pd
from typing import List, Dict, Any

from leaderboard.constants.contribTypes import scores


def format_issue_comments(
    issue_comment_list: List[Dict[str, Any]],
    user_id: str,
    user_name: str,
    time_delta: str,
    df: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Formats a list of issue comments and appends them to a pandas DataFrame.

    Args:
        issue_comment_list (List[Dict[str, Any]]): A list of issue comments.
        user_id (str): The ID of the user who made the comments.
        user_name (str): The name of the user who made the comments.
        time_delta (str): A string representing the time delta for filtering comments.
        df (pd.DataFrame): A pandas DataFrame to which the formatted comments will be appended.

    Returns:
        Dict[str, Any]: A dictionary containing the updated DataFrame and a boolean indicating whether there are older comments.
    """
    new_df = pd.DataFrame(
        [
            {
                "github_id": comment["node"]["id"],
                "user_id": user_id,
                "user_name": user_name,
                "type": scores["T4"]["description"],
                "repo_id": comment["node"]["issue"]["repository"]["id"],
                "repo_owner_id": comment["node"]["issue"]["repository"]["owner"]["id"],
                "reactions": comment["node"]["issue"]["reactions"]["totalCount"],
                "created_at": comment["node"]["createdAt"],
                "last_updated_at": comment["node"]["updatedAt"],
            }
            for comment in issue_comment_list
            if comment["node"]["createdAt"] >= time_delta
        ]
    )

    return {
        "df": pd.concat([df, new_df], ignore_index=True),
        "hasOldData": any(
            comment["node"]["createdAt"] < time_delta for comment in issue_comment_list
        ),
    }
