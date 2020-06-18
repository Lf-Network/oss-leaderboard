import pandas as pd

from leaderboard.constants import scores


def get_final_score_table(intermediate_score_df: pd.DataFrame) -> pd.DataFrame:
    """ Returns final score table dataframe
    Args: 
        df: pandas DataFrame - Intermediate Score Table containing contribution counts of all sub types for given users
    
    Returns: 
        pandas DataFrame object
    """

    final_score_table = pd.DataFrame(
        columns=[
            "User Name",
            "PR Opened",
            "PR Reviewed",
            "Issue",
            "Issue Comments",
            "Repo Created",
            "Total Score",
        ]
    )

    for _, user_row in intermediate_score_df.iterrows():
        t1_score, t2_score, t3_score, t4_score, t5_score = (0, 0, 0, 0, 0)

        t1_score = user_row.t1s1 * scores.T1S1 + user_row.t1s2 * scores.T1S2

        t2_score = (
            user_row.t2s1 * scores.T2S1
            + user_row.t2s2 * scores.T2S2
            + user_row.t2s3 * scores.T2S3
            + user_row.t2s4 * scores.T2S4
        )

        t3_score = user_row.t3s1 * scores.T3S1 + user_row.t3s2 * scores.T3S2

        t4_score = (
            user_row.t4s1 * scores.T4S1
            + user_row.t4s2 * scores.T4S2
            + user_row.t4s3 * scores.T4S3
            + user_row.t4s4 * scores.T4S4
        )

        t5_score = user_row.t5s1 * scores.T5S1

        total_score = t1_score + t2_score + t3_score + t4_score + t5_score

        final_score_table = final_score_table.append(
            {
                "User Name": user_row.user_name,
                "PR Opened": t1_score,
                "PR Reviewed": t2_score,
                "Issue": t3_score,
                "Issue Comments": t4_score,
                "Repo Created": t5_score,
                "Total Score": total_score,
            },
            ignore_index=True,
        )

    final_score_table = final_score_table.append(
        {
            "User Name": "patrick",
            "PR Opened": 0,
            "PR Reviewed": 0,
            "Issue": 0,
            "Issue Comments": 0,
            "Repo Created": 0,
            "Total Score": 0,
        },
        ignore_index=True,
    )

    return final_score_table
