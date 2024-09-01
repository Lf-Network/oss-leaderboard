import pandas as pd
from typing import List, Dict, Any

from leaderboard.constants.contribTypes import scores

def format_pr_contributions(
    pr_contribution_list: List[Dict[str, Any]],
    user_id: str,
    user_name: str,
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Formats pull request contributions and appends them to a pandas DataFrame.

    Args:
        pr_contribution_list (List[Dict[str, Any]]): A list of pull request contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the contributions will be appended.

    Returns:
        pd.DataFrame: The updated pandas DataFrame with the new contributions.
    """
    new_df = pd.DataFrame(
        [
            {
                "github_id": pr["node"]["pullRequest"]["id"],
                "user_id": user_id,
                "user_name": user_name,
                "type": scores["T1"]["description"],
                "repo_id": pr["node"]["pullRequest"]["repository"]["id"],
                "repo_owner_id": pr["node"]["pullRequest"]["repository"]["owner"]["id"],
                "pr_status": pr["node"]["pullRequest"]["state"],
                "author_id": user_id,
                "label": ", ".join(edge["node"]["name"] for edge in pr["node"]["pullRequest"]["labels"]["edges"]),
                "commits": pr["node"]["pullRequest"]["commits"]["totalCount"],
                "merged_by_id": pr["node"]["pullRequest"]["mergedBy"]["id"] if pr["node"]["pullRequest"]["merged"] and pr["node"]["pullRequest"]["mergedBy"] and "id" in pr["node"]["pullRequest"]["mergedBy"] else "",
                "created_at": pr["node"]["pullRequest"]["createdAt"],
                "last_updated_at": pr["node"]["pullRequest"]["updatedAt"],
            }
            for pr in pr_contribution_list
            if not (pr["node"]["pullRequest"]["repository"]["isArchived"] or pr["node"]["pullRequest"]["state"] == "CLOSED")
            if not ("invalid" in [edge["node"]["name"] for edge in pr["node"]["pullRequest"]["labels"]["edges"]] or "spam" in [edge["node"]["name"] for edge in pr["node"]["pullRequest"]["labels"]["edges"]])
        ]
    )
    
    return pd.concat([df, new_df], ignore_index=True)