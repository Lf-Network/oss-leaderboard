import pandas as pd
from typing import List

from leaderboard.constants.contribTypes import scores


def format_pr_contributions(
    pr_contribution_list: List, user_id: str, user_name: str, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Formats pull request contributions and appends them to a pandas DataFrame.

    Args:
        pr_contribution_list (List): A list of pull request contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the contributions will be appended.

    Returns:
        pd.DataFrame: The updated pandas DataFrame with the new contributions.
    """
    for pr in pr_contribution_list:
        github_id = pr["node"]["pullRequest"]["id"]

        pr_node = pr["node"]["pullRequest"]

        # Do not count contribution in archived repo
        if pr_node["repository"]["isArchived"]:
            continue

        repo_id = pr_node["repository"]["id"]
        repo_owner_id = pr_node["repository"]["owner"]["id"]
        pr_status = pr_node["state"]

        # Do not count contibution for closed PRs
        if pr_status == "CLOSED":
            continue
        author_id = user_id
        commits = pr_node["commits"]["totalCount"]

        merged_by_id = ""
        if pr_node["merged"] and pr_node["mergedBy"]:
            mb = pr_node["mergedBy"]
            if "id" in mb:
                merged_by_id = pr_node["mergedBy"]["id"]
        labels = []
        do_not_continue = False
        for edge in pr_node["labels"]["edges"]:
            # if invalid or spam label, do not continue
            if edge["node"]["name"] == "invalid" or edge["node"]["name"] == "spam":
                do_not_continue = True
            labels.append(edge["node"]["name"])
        label = ", ".join(labels)

        if do_not_continue:
            continue

        created_at = pr_node["createdAt"]
        last_updated_at = pr_node["updatedAt"]
        # forks, stars, comments

        new_row = pd.DataFrame(
            {
                "github_id": [github_id],
                "user_id": [user_id],
                "user_name": [user_name],
                "type": [scores["T1"]["description"]],
                "repo_id": [repo_id],
                "repo_owner_id": [repo_owner_id],
                "pr_status": [pr_status],
                "author_id": [author_id],
                "label": [label],
                "commits": [commits],
                "merged_by_id": [merged_by_id],
                "created_at": [created_at],
                "last_updated_at": [last_updated_at],
            }
        )

        # Concatenating the new row to the existing DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

    return df
