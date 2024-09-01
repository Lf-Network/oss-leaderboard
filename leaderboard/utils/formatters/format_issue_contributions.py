import pandas as pd
from typing import List

from leaderboard.constants.contribTypes import scores


def format_issue_contributions(
    issue_contribution_list: List, user_id: str, user_name: str, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Formats a list of issue contributions and appends them to a pandas DataFrame.

    Args:
        issue_contribution_list (List): A list of issue contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the formatted contributions will be appended.

    Returns:
        pd.DataFrame: The pandas DataFrame with the formatted contributions appended.
    """
    for issue in issue_contribution_list:
        github_id = issue["node"]["issue"]["id"]
        issue_node = issue["node"]["issue"]
        repo_id = issue_node["repository"]["id"]
        repo_owner_id = issue_node["repository"]["owner"]["id"]
        reactions = issue_node["reactions"]["totalCount"]
        labels = []

        for edge in issue_node["labels"]["edges"]:
            labels.append(edge["node"]["name"])
        label = ", ".join(labels)

        comments = issue_node["comments"]["totalCount"]
        created_at = issue_node["createdAt"]
        last_updated_at = issue_node["updatedAt"]

        new_row = pd.DataFrame(
            {
                "github_id": [github_id],
                "user_id": [user_id],
                "user_name": [user_name],
                "type": [scores["T3"]["description"]],
                "repo_id": [repo_id],
                "repo_owner_id": [repo_owner_id],
                "reactions": [reactions],
                "label": [label],
                "comments": [comments],
                "created_at": [created_at],
                "last_updated_at": [last_updated_at],
            }
        )

        # Concatenating the new row to the existing DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

    return df
