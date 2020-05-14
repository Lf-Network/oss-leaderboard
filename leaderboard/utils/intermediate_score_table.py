import pandas as pd


def get_intermediate_score_table(intermediate_table_df):
    """ Returns a dataframe - contribution counts of all sub types for all users
    Args: 
        df: pandas DataFrame - Intermediate Table containing flattened data of the github contributions for a group of users
    
    Returns: 
        pandas DataFrame object
    """

    # Intermediate score table that stores the counts for each of the contribution subtypes
    result_df = pd.DataFrame(
        columns=[
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
    )

    user_groups = intermediate_table_df.groupby(["user_id", "user_name"])

    for user_tuple, frame in user_groups:
        # reset count for each user
        t1s1, t1s2, t2s1, t2s2, t2s3, t2s4, t3s1, t3s2, t4s1, t4s2, t4s3, t4s4, t5s1 = (
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )

        user_contrib_group_by_type = frame.groupby(["type"])
        for contrib_type, frame2 in user_contrib_group_by_type:
            if contrib_type == 1:
                t1s1, t1s2 = get_pr_opened_counts(frame2, user_tuple[0])
            elif contrib_type == 2:
                t2s1, t2s2, t2s3, t2s4 = get_pr_reviewed_counts(frame2, user_tuple[0])
            elif contrib_type == 3:
                t3s1, t3s2 = get_issue_created_counts(frame2, user_tuple[0])
            elif contrib_type == 4:
                t4s1, t4s2, t4s3, t4s4 = get_commented_on_issue_counts(
                    frame2, user_tuple[0]
                )
            elif contrib_type == 5:
                t5s1 = get_repo_created_counts(frame2)

        # set total contribution counts of a user
        result_df = result_df.append(
            {
                "user_name": user_tuple[1],
                "user_id": user_tuple[0],
                "t1s1": t1s1,
                "t1s2": t1s2,
                "t2s1": t2s1,
                "t2s2": t2s2,
                "t2s3": t2s3,
                "t2s4": t2s4,
                "t3s1": t3s1,
                "t3s2": t3s2,
                "t4s1": t4s1,
                "t4s2": t4s2,
                "t4s3": t4s3,
                "t4s4": t4s4,
                "t5s1": t5s1,
            },
            ignore_index=True,
        )

    return result_df


def get_pr_opened_counts(df, user_id):
    """ Returns a individual counts for all subtypes under the 'PR Opened' type
    Args: 
        df: pandas DataFrame - sub-table of contributions for 'PR Opened' type by a particular contributor
        user_id: usedID of contributor
    Returns: 
        int, int
    """

    t1s1, t1s2 = 0, 0

    for index, contribution in df.iterrows():
        if user_id != contribution.repo_owner_id:
            t1s1 += 1
        elif user_id == contribution.repo_owner_id:
            t1s2 += 1

    return t1s1, t1s2


def get_pr_reviewed_counts(df, user_id):
    """ Returns a individual counts for all subtypes under the 'PR Reviewed' type
    Args: 
        df: pandas DataFrame - sub-table of contributions for 'PR Reviewed' type by a particular contributor
        user_id: usedID of contributor
    Returns: 
        int, int, int, int
    """

    t2s1, t2s2, t2s3, t2s4 = 0, 0, 0, 0

    for index, contribution in df.iterrows():
        if user_id == contribution.author_id and user_id == contribution.repo_owner_id:
            t2s1 += 1
        elif (
            user_id != contribution.author_id and user_id == contribution.repo_owner_id
        ):
            t2s2 += 1
        elif (
            user_id == contribution.author_id and user_id != contribution.repo_owner_id
        ):
            t2s3 += 1
        elif (
            user_id != contribution.author_id and user_id != contribution.repo_owner_id
        ):
            t2s4 += 1

    return t2s1, t2s2, t2s3, t2s4


def get_issue_created_counts(df, user_id):
    """ Returns a individual counts for all subtypes under the 'Issue Created' type
    Args: 
        df: pandas DataFrame - sub-table of contributions for 'Issue Created' type by a particular contributor
        user_id: usedID of contributor
    Returns: 
        int, int
    """

    t3s1, t3s2 = 0, 0

    for index, contribution in df.iterrows():
        if user_id == contribution.repo_owner_id:
            t3s1 += 1
        elif user_id != contribution.repo_owner_id:
            t3s2 += 1

    return t3s1, t3s2


def get_commented_on_issue_counts(df, user_id):
    """ Returns a individual counts for all subtypes under the 'Commented On Issue' type
    Args: 
        df: pandas DataFrame - sub-table of contributions for 'Commented On Issue' type by a particular contributor
        user_id: usedID of contributor
    Returns: 
        int, int, int, int
    """

    t4s1, t4s2, t4s3, t4s4 = 0, 0, 0, 0

    for index, contribution in df.iterrows():
        if user_id == contribution.author_id and user_id == contribution.repo_owner_id:
            t4s1 += 1
        elif (
            user_id != contribution.author_id and user_id == contribution.repo_owner_id
        ):
            t4s2 += 1
        elif (
            user_id == contribution.author_id and user_id != contribution.repo_owner_id
        ):
            t4s3 += 1
        elif (
            user_id != contribution.author_id and user_id != contribution.repo_owner_id
        ):
            t4s4 += 1

    return t4s1, t4s2, t4s3, t4s4


def get_repo_created_counts(df):
    """ Returns a individual counts for all subtypes under the 'Repo Created' type
    Args: 
        df: pandas DataFrame - sub-table of contributions for 'Repo Created' type by a particular contributor
    Returns: 
        int
    """

    t5s1 = 0

    for index, contribution in df.iterrows():
        t5s1 += 1

    return t5s1
