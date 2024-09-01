import pandas as pd
from typing import List

from leaderboard.constants.contribTypes import scores


def format_pr_review_contributions(
    review_contribution_list: List, user_id: str, user_name: str, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Formats pull request review contributions and appends them to a pandas DataFrame.

    Args:
        review_contribution_list (List): A list of pull request review contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the formatted contributions will be appended.

    Returns:
        pd.DataFrame: The pandas DataFrame with the formatted contributions appended.
    """
    for pr_review in review_contribution_list:
        github_id = pr_review["node"]["pullRequestReview"]["id"]
        pr_review_node = pr_review["node"]["pullRequestReview"]
        repo_id = pr_review["node"]["repository"]["id"]
        repo_owner_id = pr_review["node"]["repository"]["owner"]["id"]

        review_type = pr_review_node["ReviewState"]
        pr_status = pr_review_node["pullRequest"]["state"]

        author_id = ""
        if pr_review_node["pullRequest"]["author"]:  # handle deleted user
            author_id = pr_review_node["pullRequest"]["author"].get("id")

        reactions = pr_review_node["reactions"]["totalCount"]
        merged_by_id = ""

        if pr_review_node["pullRequest"]["merged"]:
            merged_by_id = pr_review_node["pullRequest"]["mergedBy"]["login"]

        created_at = pr_review_node["createdAt"]
        last_updated_at = pr_review_node["updatedAt"]
        # label, commits, forks, stars, comments

        new_row = pd.DataFrame(
            {
                "github_id": [github_id],
                "user_id": [user_id],
                "user_name": [user_name],
                "type": [scores["T2"]["description"]],
                "repo_id": [repo_id],
                "repo_owner_id": [repo_owner_id],
                "review_type": [review_type],
                "pr_status": [pr_status],
                "author_id": [author_id],
                "merged_by_id": [merged_by_id],
                "reactions": [reactions],
                "created_at": [created_at],
                "last_updated_at": [last_updated_at],
            }
        )

        # Concatenating the new row to the existing DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

    return df
