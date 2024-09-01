""" Util to convert the json to dataframe. """

import json
import pandas as pd
from typing import Dict
from leaderboard.utils.page_info import extract_page_info
from leaderboard.utils.formatters.format_pr_review_contributions import format_pr_review_contributions
from leaderboard.utils.formatters.format_pr_contributions import format_pr_contributions
from leaderboard.utils.formatters.format_issue_contributions import format_issue_contributions
from leaderboard.utils.formatters.format_repo_contributions import format_repo_contributions
from leaderboard.utils.formatters.format_issue_comments import format_issue_comments


def convert_to_intermediate_table(data: str, timeDelta: str) -> Dict:
    """
    Converts a JSON string containing data about a user's contributions on GitHub
    into an intermediate table format that can be used to generate a leaderboard.

    Args:
        data (str): A JSON string containing data about a user's contributions on GitHub.
        timeDelta (str): A string representing a time delta in the format "X days/hours/minutes".

    Returns:
        dict: A dictionary containing two keys:
            - "intermediate_table": A pandas DataFrame containing the intermediate table.
            - "page_info": A dictionary containing pagination information for the API query.
    """
    df = pd.DataFrame.from_dict(
        pd.json_normalize(json.loads(data.encode())), orient="columns"
    )

    user_github_id = df["data.user.id"][0]
    user_name = df["data.user.username"][0]
    issue_comment_list = df["data.user.issueComments.edges"][0]
    review_contribution_list = df[
        "data.user.contributionsCollection.pullRequestReviewContributions.edges"
    ][0]
    pr_contribution_list = df[
        "data.user.contributionsCollection.pullRequestContributions.edges"
    ][0]
    issue_contribution_list = df[
        "data.user.contributionsCollection.issueContributions.edges"
    ][0]
    repo_contribution_list = df[
        "data.user.contributionsCollection.repositoryContributions.edges"
    ][0]

    new_df = pd.DataFrame(
        columns=[
            "github_id",
            "user_id",
            "user_name",
            "type",
            "repo_id",
            "repo_owner_id",
            "pr_status",
            "label",
            "commits",
            "review_type",
            "forks",
            "stars",
            "comments",
            "reactions",
            "merged_by_id",
            "author_id",
            "is_fork",
            "created_at",
            "last_updated_at",
        ]
    )

    new_df = format_pr_review_contributions(
        review_contribution_list, user_github_id, user_name, new_df
    )
    new_df = format_pr_contributions(
        pr_contribution_list, user_github_id, user_name, new_df
    )
    new_df = format_issue_contributions(
        issue_contribution_list, user_github_id, user_name, new_df
    )
    new_df = format_repo_contributions(
        repo_contribution_list, user_github_id, user_name, new_df
    )
    new_df_info = format_issue_comments(
        issue_comment_list, user_github_id, user_name, timeDelta, new_df
    )

    page_info = extract_page_info(df)

    # in case of issue comment(T4), we calculate the value for hasPreviousPage
    # based on whether the latest api response has any issue comment contribution data that was created before the specified time
    page_info["page_info_T4"]["hasPreviousPage"] = (
        not new_df_info["hasOldData"] and page_info["page_info_T4"]["hasPreviousPage"]
    )

    return {"intermediate_table": new_df_info["df"], "page_info": page_info}
