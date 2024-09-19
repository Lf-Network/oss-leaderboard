from typing import Dict
import pandas as pd
from leaderboard.constants.contribTypes import scores


def get_intermediate_score_table(intermediate_table_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns contribution counts of all sub types for all users.

    Args:
        intermediate_table_df: Intermediate Table containing flattened data of the github contributions for a group of users.

    Returns:
        A pandas DataFrame containing the contribution counts of all subtypes for all users.
    """
    columns = [
        "user_name",
        "user_id",
        "t1s1",
        "t1s2",
        "t2s1",
        "t2s2",
        "t2s3",
        "t2s4",
        "t3s1",
        "t3s2",
        "t4s1",
        "t4s2",
        "t4s3",
        "t4s4",
        "t5s1",
    ]

    result_df = pd.DataFrame(columns=columns)
    user_groups = intermediate_table_df.groupby(["user_id", "user_name"])

    for (user_id, user_name), frame in user_groups:
        counts = get_contribution_counts(frame, user_id)
        result_df = pd.concat(
            [
                result_df,
                pd.DataFrame([{"user_name": user_name, "user_id": user_id, **counts}]),
            ],
            ignore_index=True,
        )

    return result_df


def get_contribution_counts(frame: pd.DataFrame, user_id: str) -> Dict:
    """
    Calculate contribution counts for a given user.

    Args:
        frame: DataFrame containing contributions for a user.
        user_id: ID of the user.

    Returns:
        A dictionary containing the counts for each contribution subtype.
    """
    counts = {
        "t1s1": 0,
        "t1s2": 0,
        "t2s1": 0,
        "t2s2": 0,
        "t2s3": 0,
        "t2s4": 0,
        "t3s1": 0,
        "t3s2": 0,
        "t4s1": 0,
        "t4s2": 0,
        "t4s3": 0,
        "t4s4": 0,
        "t5s1": 0,
    }

    contrib_groups = frame.groupby("type")
    for contrib_type, frame2 in contrib_groups:
        if contrib_type == scores["T1"]["description"]:
            counts["t1s1"] = len(frame2[frame2.repo_owner_id != user_id])
            counts["t1s2"] = len(frame2[frame2.repo_owner_id == user_id])
        elif contrib_type == scores["T2"]["description"]:
            counts.update(get_pr_reviewed_counts(frame2, user_id))
        elif contrib_type == scores["T3"]["description"]:
            counts.update(get_issue_created_counts(frame2, user_id))
        elif contrib_type == scores["T4"]["description"]:
            counts.update(get_commented_on_issue_counts(frame2, user_id))
        elif contrib_type == scores["T5"]["description"]:
            counts["t5s1"] = len(frame2)

    return counts


def get_pr_reviewed_counts(df: pd.DataFrame, user_id: str) -> Dict:
    """
    Returns individual counts for all subtypes under the 'PR Reviewed' type.

    Args:
        df: DataFrame containing contributions for 'PR Reviewed' type by a particular contributor.
        user_id: ID of the contributor.

    Returns:
        A dictionary containing the counts for each subtype under the 'PR Reviewed' type.
    """
    mask1 = (df.author_id == user_id) & (df.repo_owner_id == user_id)
    mask2 = (df.author_id != user_id) & (df.repo_owner_id == user_id)
    mask3 = (df.author_id == user_id) & (df.repo_owner_id != user_id)
    mask4 = (df.author_id != user_id) & (df.repo_owner_id != user_id)

    return {
        "t2s1": len(df[mask1]),
        "t2s2": len(df[mask2]),
        "t2s3": len(df[mask3]),
        "t2s4": len(df[mask4]),
    }


def get_issue_created_counts(df: pd.DataFrame, user_id: str) -> Dict:
    """
    Returns individual counts for all subtypes under the 'Issue Created' type.

    Args:
        df: DataFrame containing contributions for 'Issue Created' type by a particular contributor.
        user_id: ID of the contributor.

    Returns:
        A dictionary containing the counts for each subtype under the 'Issue Created' type.
    """
    return {
        "t3s1": len(df[df.repo_owner_id == user_id]),
        "t3s2": len(df[df.repo_owner_id != user_id]),
    }


def get_commented_on_issue_counts(df: pd.DataFrame, user_id: str) -> Dict:
    """
    Returns individual counts for all subtypes under the 'Commented On Issue' type.

    Args:
        df: DataFrame containing contributions for 'Commented On Issue' type by a particular contributor.
        user_id: ID of the contributor.

    Returns:
        A dictionary containing the counts for each subtype under the 'Commented On Issue' type.
    """
    mask1 = (df.author_id == user_id) & (df.repo_owner_id == user_id)
    mask2 = (df.author_id != user_id) & (df.repo_owner_id == user_id)
    mask3 = (df.author_id == user_id) & (df.repo_owner_id != user_id)
    mask4 = (df.author_id != user_id) & (df.repo_owner_id != user_id)

    return {
        "t4s1": len(df[mask1]),
        "t4s2": len(df[mask2]),
        "t4s3": len(df[mask3]),
        "t4s4": len(df[mask4]),
    }
