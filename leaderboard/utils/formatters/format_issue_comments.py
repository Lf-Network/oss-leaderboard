import pandas as pd
from typing import Dict

from leaderboard.constants.contribTypes import scores


def format_issue_comments(
    issue_comment_list: str,
    user_id: str,
    user_name: str,
    timeDelta: str,
    df: pd.DataFrame,
) -> Dict:
    """
    Formats a list of issue comments and appends them to a pandas DataFrame.

    Args:
        issue_comment_list (str): A list of issue comments.
        user_id (str): The ID of the user who made the comments.
        user_name (str): The name of the user who made the comments.
        timeDelta (str): A string representing the time delta for filtering comments.
        df (pd.DataFrame): A pandas DataFrame to which the formatted comments will be appended.

    Returns:
        dict: A dictionary containing the updated DataFrame and a boolean indicating whether there are older comments.
    """
    olderDataCount = 0

    for issue_comment in issue_comment_list:
        github_id = issue_comment["node"]["id"]
        repo_id = issue_comment["node"]["issue"]["repository"]["id"]
        repo_owner_id = issue_comment["node"]["issue"]["repository"]["owner"]["id"]
        reactions = issue_comment["node"]["issue"]["reactions"]["totalCount"]
        created_at = issue_comment["node"]["createdAt"]
        last_updated_at = issue_comment["node"]["updatedAt"]

        if created_at >= timeDelta:
            new_row = pd.DataFrame(
                {
                    "github_id": [github_id],
                    "user_id": [user_id],
                    "user_name": [user_name],
                    "type": [scores["T4"]["description"]],
                    "repo_id": [repo_id],
                    "repo_owner_id": [repo_owner_id],
                    "reactions": [reactions],
                    "created_at": [created_at],
                    "last_updated_at": [last_updated_at],
                }
            )

            # Concatenating the new row to the existing DataFrame
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            olderDataCount += 1

    return {"df": df, "hasOldData": olderDataCount > 0}
