import pandas as pd
from typing import List, Dict

from leaderboard.constants.contribTypes import scores

def format_repo_contributions(
    repo_contribution_list: List[Dict], 
    user_id: str, 
    user_name: str, 
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Formats a list of repository contributions and appends them to a pandas DataFrame.

    Args:
        repo_contribution_list (List[Dict]): A list of repository contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the contributions will be appended.

    Returns:
        pd.DataFrame: The updated pandas DataFrame with the appended contributions.
    """
    new_df = pd.DataFrame(
        [
            {
                "github_id": repo["node"]["repository"]["id"],
                "user_id": user_id,
                "user_name": user_name,
                "type": scores["T5"]["description"],
                "repo_id": repo["node"]["repository"]["id"],
                "repo_owner_id": user_id,
                "forks": repo["node"]["repository"]["forkCount"],
                "stars": repo["node"]["repository"]["stargazers"]["totalCount"],
                "is_fork": repo["node"]["repository"]["isFork"],
                "created_at": repo["node"]["repository"]["createdAt"],
                "last_updated_at": repo["node"]["repository"]["updatedAt"],
            }
            for repo in repo_contribution_list
        ]
    )

    return pd.concat([df, new_df], ignore_index=True)