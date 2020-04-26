import pandas as pd

def get_intermediate_score_table (intermediate_table_df):
    """ Returns a dataframe - contribution counts of all sub types for all users
    Args: 
        df: pandas DataFrame - Intermediate Table containing flattened data of the github contributions for a group of users
    
    Returns: 
        pandas DataFrame object
    """

    # Intermediate score table that stores the counts for each of the contribution subtypes  
    result_df = pd.DataFrame(columns=['user_name', 'user_id', 'T1S1', 'T1S2', 'T2S1', 'T2S2', 'T2S3', 'T2S4', 'T3S1', 'T3S2', 'T4S1', 'T4S2', 'T4S3', 'T4S4', 'T5S1'])
    
    user_groups = intermediate_table_df.groupby(['user_id', 'user_name'])

    for user_tuple, frame in user_groups:
        # reset count for each user
        T1S1, T1S2, T2S1, T2S2, T2S3, T2S4, T3S1, T3S2, T4S1, T4S2, T4S3, T4S4, T5S1 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        user_contrib_group_by_type = frame.groupby(['type'])
        for contrib_type, frame2 in user_contrib_group_by_type:
            if contrib_type == 1 :
                T1S1, T1S2 = get_pr_opened_counts(frame2, user_tuple[0])
            elif contrib_type == 2 :
                T2S1, T2S2, T2S3, T2S4 = get_pr_reviewed_counts(frame2, user_tuple[0])
            elif contrib_type == 3 :
                T3S1, T3S2 = get_issue_created_counts(frame2, user_tuple[0])
            elif contrib_type == 4 :
                T4S1, T4S2, T4S3, T4S4 = get_commented_on_issue_counts(frame2, user_tuple[0])
            elif contrib_type == 5 :
                T5S1 = get_repo_created_counts(frame2) 
        
        # set total contribution counts of a user
        result_df = result_df.append({
            'user_name': user_tuple[1],
            'user_id':user_tuple[0], 
            'T1S1': T1S1, 
            'T1S2': T1S2,

            'T2S1': T2S1,
            'T2S2': T2S2,
            'T2S3': T2S3,
            'T2S4': T2S4,

            'T3S1': T3S1,
            'T3S2': T3S2,

            'T4S1': T4S1,
            'T4S2': T4S2,
            'T4S3': T4S3,
            'T4S4': T4S4,

            'T5S1': T5S1  
        }, ignore_index=True)
    

    print("Intermediate Score Table: ", result_df, sep='\n')

    return result_df


def get_pr_opened_counts (df, user_id) :
    """ Returns a individual counts for all subtypes under the 'PR Opened' type
    Args: 
        df: pandas DataFrame - sub-table of contributions for 'PR Opened' type by a particular contributor
        user_id: usedID of contributor
    Returns: 
        int, int
    """

    T1S1, T1S2 = 0, 0
    
    for index, contribution in df.iterrows():
        if user_id != contribution.repo_owner_id :
            T1S1 += 1
        elif user_id == contribution.repo_owner_id :
            T1S2 += 1

    return T1S1, T1S2


def get_pr_reviewed_counts (df, user_id) :
    """ Returns a individual counts for all subtypes under the 'PR Reviewed' type
    Args: 
        df: pandas DataFrame - sub-table of contributions for 'PR Reviewed' type by a particular contributor
        user_id: usedID of contributor
    Returns: 
        int, int, int, int
    """

    T2S1, T2S2, T2S3, T2S4 = 0, 0, 0, 0
    
    for index, contribution in df.iterrows():
        if user_id == contribution.author_id and user_id == contribution.repo_owner_id :
            T2S1 += 1
        elif user_id != contribution.author_id and user_id == contribution.repo_owner_id :
            T2S2 += 1
        elif user_id == contribution.author_id and user_id != contribution.repo_owner_id :
            T2S3 += 1
        elif user_id != contribution.author_id and user_id != contribution.repo_owner_id :
            T2S4 += 1

    return T2S1, T2S2, T2S3, T2S4


def get_issue_created_counts (df, user_id) :
    """ Returns a individual counts for all subtypes under the 'Issue Created' type
    Args: 
        df: pandas DataFrame - sub-table of contributions for 'Issue Created' type by a particular contributor
        user_id: usedID of contributor
    Returns: 
        int, int
    """

    T3S1, T3S2 = 0, 0
    
    for index, contribution in df.iterrows():
        if user_id == contribution.repo_owner_id :
            T3S1 += 1
        elif user_id != contribution.repo_owner_id :
            T3S2 += 1

    return T3S1, T3S2


def get_commented_on_issue_counts (df, user_id) :
    """ Returns a individual counts for all subtypes under the 'Commented On Issue' type
    Args: 
        df: pandas DataFrame - sub-table of contributions for 'Commented On Issue' type by a particular contributor
        user_id: usedID of contributor
    Returns: 
        int, int, int, int
    """

    T4S1, T4S2, T4S3, T4S4 = 0, 0, 0, 0
    
    for index, contribution in df.iterrows():
        if user_id == contribution.author_id and user_id == contribution.repo_owner_id :
            T4S1 += 1
        elif user_id != contribution.author_id and user_id == contribution.repo_owner_id :
            T4S2 += 1
        elif user_id == contribution.author_id and user_id != contribution.repo_owner_id :
            T4S3 += 1
        elif user_id != contribution.author_id and user_id != contribution.repo_owner_id :
            T4S4 += 1

    return T4S1, T4S2, T4S3, T4S4


def get_repo_created_counts (df) :
    """ Returns a individual counts for all subtypes under the 'Repo Created' type
    Args: 
        df: pandas DataFrame - sub-table of contributions for 'Repo Created' type by a particular contributor
    Returns: 
        int
    """

    T5S1 = 0
    
    for index, contribution in df.iterrows():
        T5S1 += 1

    return T5S1
