import pandas as pd
from typing import List, Dict, Any

from leaderboard.constants.contribTypes import scores


def format_pr_review_contributions(
    review_contribution_list: List[Dict[str, Any]],
    user_id: str,
    user_name: str,
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Formats pull request review contributions and appends them to a pandas DataFrame.

    Args:
        review_contribution_list (List[Dict[str, Any]]): A list of pull request review contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the formatted contributions will be appended.

    Returns:
        pd.DataFrame: The pandas DataFrame with the formatted contributions appended.
    """

    new_df = pd.DataFrame(
        [
            {
                "github_id": pr_review["node"]["pullRequestReview"]["id"],
                "user_id": user_id,
                "user_name": user_name,
                "type": scores["T2"]["description"],
                "repo_id": pr_review["node"]["repository"]["id"],
                "repo_owner_id": pr_review["node"]["repository"]["owner"]["id"],
                "review_type": pr_review["node"]["pullRequestReview"]["ReviewState"],
                "pr_status": pr_review["node"]["pullRequestReview"]["pullRequest"][
                    "state"
                ],
                "author_id": (
                    pr_review["node"]["pullRequestReview"]["pullRequest"].get("author")
                    or {}
                ).get("id", ""),
                "merged_by_id": (
                    pr_review["node"]["pullRequestReview"]["pullRequest"]
                    .get("mergedBy", {})
                    .get("login", "")
                    if pr_review["node"]["pullRequestReview"]["pullRequest"].get(
                        "merged"
                    )
                    else ""
                ),
                "reactions": pr_review["node"]["pullRequestReview"]["reactions"][
                    "totalCount"
                ],
                "created_at": pr_review["node"]["pullRequestReview"]["createdAt"],
                "last_updated_at": pr_review["node"]["pullRequestReview"]["updatedAt"],
            }
            for pr_review in review_contribution_list
        ]
    )

    return pd.concat([df, new_df], ignore_index=True)
