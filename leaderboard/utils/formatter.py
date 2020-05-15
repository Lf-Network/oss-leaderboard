""" Util to convert the json to dataframe
"""

import json
import pandas as pd
from pandas.io.json import json_normalize


def convert_to_intermediate_table(data):
    df = pd.DataFrame.from_dict(
        json_normalize(json.loads(data.encode())), orient="columns"
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

    new_df = format_issue_comments(
        issue_comment_list, user_github_id, user_name, new_df
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

    return new_df


def format_issue_comments(issue_comment_list, user_id, user_name, df):
    for issue_comment in issue_comment_list:
        github_id = issue_comment["node"]["id"]
        user = issue_comment["node"]["issue"]["author"]["id"]
        repo_id = issue_comment["node"]["issue"]["repository"]["id"]
        repo_owner_id = issue_comment["node"]["issue"]["repository"]["owner"]["id"]
        reactions = issue_comment["node"]["issue"]["reactions"]["totalCount"]
        created_at = issue_comment["node"]["createdAt"]
        last_updated_at = issue_comment["node"]["updatedAt"]
        df = df.append(
            {
                "github_id": github_id,
                "user_id": user_id,
                "user_name": user_name,
                "type": "Issue Comments",
                "repo_id": repo_id,
                "repo_owner_id": repo_owner_id,
                "reactions": reactions,
                "created_at": created_at,
                "last_updated_at": last_updated_at,
            },
            ignore_index=True,
        )
    return df


def format_pr_review_contributions(review_contribution_list, user_id, user_name, df):
    for pr_review in review_contribution_list:
        github_id = pr_review["node"]["pullRequestReview"]["id"]
        pr_review_node = pr_review["node"]["pullRequestReview"]
        repo_id = pr_review["node"]["repository"]["id"]
        repo_owner_id = pr_review["node"]["repository"]["owner"]["id"]

        review_type = pr_review_node["ReviewState"]
        pr_status = pr_review_node["pullRequest"]["state"]
        author_id = pr_review_node["pullRequest"]["author"]["id"]
        reactions = pr_review_node["reactions"]["totalCount"]
        merged_by_id = ""
        if pr_review_node["pullRequest"]["merged"]:
            merged_by_id = pr_review_node["pullRequest"]["mergedBy"]["login"]

        created_at = pr_review_node["createdAt"]
        last_updated_at = pr_review_node["updatedAt"]
        # label, commits, forks, stars, comments

        df = df.append(
            {
                "github_id": github_id,
                "user_id": user_id,
                "user_name": user_name,
                "type": "PR Reviewed",
                "repo_id": repo_id,
                "repo_owner_id": repo_owner_id,
                "review_type": review_type,
                "pr_status": pr_status,
                "author_id": author_id,
                "merged_by_id": merged_by_id,
                "reactions": reactions,
                "created_at": created_at,
                "last_updated_at": last_updated_at,
            },
            ignore_index=True,
        )
    return df


def format_pr_contributions(pr_contribution_list, user_id, user_name, df):
    for pr in pr_contribution_list:
        github_id = pr["node"]["pullRequest"]["id"]

        pr_node = pr["node"]["pullRequest"]

        repo_id = pr_node["repository"]["id"]
        repo_owner_id = pr_node["repository"]["owner"]["id"]
        pr_status = pr_node["state"]
        author_id = user_id
        commits = pr_node["commits"]["totalCount"]

        merged_by_id = ""
        if pr_node["merged"]:
            merged_by_id = pr_node["mergedBy"]["id"]

        labels = []
        for edge in pr_node["labels"]["edges"]:
            labels.append(edge["node"]["name"])
        label = ", ".join(labels)

        created_at = pr_node["createdAt"]
        last_updated_at = pr_node["updatedAt"]
        # forks, stars, comments

        df = df.append(
            {
                "github_id": github_id,
                "user_id": user_id,
                "user_name": user_name,
                "type": "PR Opened",
                "repo_id": repo_id,
                "repo_owner_id": repo_owner_id,
                "pr_status": pr_status,
                "author_id": author_id,
                "label": label,
                "commits": commits,
                "merged_by_id": merged_by_id,
                "created_at": created_at,
                "last_updated_at": last_updated_at,
            },
            ignore_index=True,
        )

    return df


def format_issue_contributions(issue_contribution_list, user_id, user_name, df):
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
        # type = 'Issue'
        df.append(
            {
                "github_id": github_id,
                "user_id": user_id,
                "user_name": user_name,
                "type": "Issue",
                "repo_id": repo_id,
                "repo_owner_id": repo_owner_id,
                "reactions": reactions,
                "label": label,
                "comments": comments,
                "created_at": created_at,
                "last_updated_at": last_updated_at,
            },
            ignore_index=True,
        )
    return df


def format_repo_contributions(repo_contribution_list, user_id, user_name, df):
    for repo in repo_contribution_list:
        github_id = repo["node"]["repository"]["id"]
        repo_node = repo["node"]["repository"]
        repo_id = repo_node["id"]
        forks = repo_node["forkCount"]
        stars = repo_node["stargazers"]["totalCount"]
        created_at = repo_node["createdAt"]
        last_updated_at = repo_node["updatedAt"]
        is_fork = repo_node["isFork"]
        df.append(
            {
                "github_id": github_id,
                "user_id": user_id,
                "user_name": user_name,
                "type": "Repo Created",
                "repo_id": repo_id,
                "repo_owner_id": user_id,
                "forks": forks,
                "stars": stars,
                "is_fork": is_fork,
                "created_at": created_at,
                "last_updated_at": last_updated_at,
            },
            ignore_index=True,
        )
    return df
