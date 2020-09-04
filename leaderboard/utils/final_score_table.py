import pandas as pd

from leaderboard.constants import scoreWeights
from leaderboard.constants import contribTypes


def get_final_score_table(intermediate_score_df: pd.DataFrame) -> pd.DataFrame:
    """ Returns final score table dataframe
    Args: 
        df: pandas DataFrame - Intermediate Score Table containing contribution counts of all sub types for given users
    """

    final_score_table = pd.DataFrame(
        columns=[
            "User Name",
            contribTypes.T1,
            contribTypes.T2,
            contribTypes.T3,
            contribTypes.T4,
            contribTypes.T5,
            "Total Score",
        ]
    )

    for _, user_row in intermediate_score_df.iterrows():
        t1_score, t2_score, t3_score, t4_score, t5_score = (0, 0, 0, 0, 0)

        t1_score = user_row.t1s1 * scoreWeights.T1S1 + user_row.t1s2 * scoreWeights.T1S2

        t2_score = (
            user_row.t2s1 * scoreWeights.T2S1
            + user_row.t2s2 * scoreWeights.T2S2
            + user_row.t2s3 * scoreWeights.T2S3
            + user_row.t2s4 * scoreWeights.T2S4
        )

        t3_score = user_row.t3s1 * scoreWeights.T3S1 + user_row.t3s2 * scoreWeights.T3S2

        t4_score = (
            user_row.t4s1 * scoreWeights.T4S1
            + user_row.t4s2 * scoreWeights.T4S2
            + user_row.t4s3 * scoreWeights.T4S3
            + user_row.t4s4 * scoreWeights.T4S4
        )

        t5_score = user_row.t5s1 * scoreWeights.T5S1

        total_score = t1_score + t2_score + t3_score + t4_score + t5_score

        final_score_table = final_score_table.append(
            {
                "User Name": user_row.user_name,
                contribTypes.T1: t1_score,
                contribTypes.T2: t2_score,
                contribTypes.T3: t3_score,
                contribTypes.T4: t4_score,
                contribTypes.T5: t5_score,
                "Total Score": total_score,
            },
            ignore_index=True,
        )

    return final_score_table
