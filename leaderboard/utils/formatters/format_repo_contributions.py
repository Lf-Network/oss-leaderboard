import pandas as pd
from typing import List

from leaderboard.constants.contribTypes import scores


def format_repo_contributions(
    repo_contribution_list: List, user_id: str, user_name: str, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Formats a list of repository contributions and appends them to a pandas DataFrame.

    Args:
        repo_contribution_list (List): A list of repository contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the contributions will be appended.

    Returns:
        pd.DataFrame: The updated pandas DataFrame with the appended contributions.
    """
    for repo in repo_contribution_list:
        github_id = repo["node"]["repository"]["id"]
        repo_node = repo["node"]["repository"]
        repo_id = repo_node["id"]
        forks = repo_node["forkCount"]
        stars = repo_node["stargazers"]["totalCount"]
        created_at = repo_node["createdAt"]
        last_updated_at = repo_node["updatedAt"]
        is_fork = repo_node["isFork"]
        
        new_row = pd.DataFrame(
            {
                "github_id": [github_id],
                "user_id": [user_id],
                "user_name": [user_name],
                "type": [scores["T5"]["description"]],
                "repo_id": [repo_id],
                "repo_owner_id": [user_id],
                "forks": [forks],
                "stars": [stars],
                "is_fork": [is_fork],
                "created_at": [created_at],
                "last_updated_at": [last_updated_at],
            }
        )

        # Concatenating the new row to the existing DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

    return df
