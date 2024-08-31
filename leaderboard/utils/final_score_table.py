import pandas as pd

from leaderboard.constants.contribTypes import scores

def get_final_score_table(
    intermediate_score_df: pd.DataFrame, user_list: list
) -> pd.DataFrame:
    """
    Returns a final score table dataframe based on the intermediate score table containing contribution counts of all sub types for given users.

    Args:
        intermediate_score_df (pandas DataFrame): Intermediate Score Table containing contribution counts of all sub types for given users.
        user_list (list): List of user names for which the final score table is to be generated.

    Returns:
        pandas DataFrame: Final score table dataframe containing the total score of each user based on their contributions across all sub types.
    """

    intermediate_score_df.set_index("user_name", inplace=True)

    final_score_table = pd.DataFrame(
        {
            "User Name": pd.Series(dtype="string"),
            scores["T1"]["description"]: pd.Series(dtype="float"),
            scores["T2"]["description"]: pd.Series(dtype="float"),
            scores["T3"]["description"]: pd.Series(dtype="float"),
            scores["T4"]["description"]: pd.Series(dtype="float"),
            "Total Score": pd.Series(dtype="float"),
        }
    )

    rows = []

    for user_name in user_list:
        t1_score, t2_score, t3_score, t4_score, total_score = (
            0,
            0,
            0,
            0,
            0,
        )

        try:
            user_row = intermediate_score_df.loc[user_name]

            t1_score = (
                user_row.t1s1 * scores["T1"]["subtypes"]["T1S1"]["weight"]
                + user_row.t1s2 * scores["T1"]["subtypes"]["T1S2"]["weight"]
            )

            t2_score = (
                user_row.t2s1 * scores["T2"]["subtypes"]["T2S1"]["weight"]
                + user_row.t2s2 * scores["T2"]["subtypes"]["T2S2"]["weight"]
                + user_row.t2s3 * scores["T2"]["subtypes"]["T2S3"]["weight"]
                + user_row.t2s4 * scores["T2"]["subtypes"]["T2S4"]["weight"]
            )

            t3_score = (
                user_row.t3s1 * scores["T3"]["subtypes"]["T3S1"]["weight"]
                + user_row.t3s2 * scores["T3"]["subtypes"]["T3S2"]["weight"]
            )

            t4_score = (
                user_row.t4s1 * scores["T4"]["subtypes"]["T4S1"]["weight"]
                + user_row.t4s2 * scores["T4"]["subtypes"]["T4S2"]["weight"]
                + user_row.t4s3 * scores["T4"]["subtypes"]["T4S3"]["weight"]
                + user_row.t4s4 * scores["T4"]["subtypes"]["T4S4"]["weight"]
            )

            total_score = t1_score + t2_score + t3_score + t4_score

            if total_score <= 0.0:
                continue

            new_row_data = {
                "User Name": user_name,
                scores["T1"]["description"]: t1_score,
                scores["T2"]["description"]: t2_score,
                scores["T3"]["description"]: t3_score,
                scores["T4"]["description"]: t4_score,
                "Total Score": total_score,
            }
            rows.append(new_row_data)

        except KeyError:
            # If the user is not in the intermediate_score_df, skip them
            if total_score <= 0.0:
                continue

            new_row_data = {
                "User Name": user_name,
                scores["T1"]["description"]: t1_score,
                scores["T2"]["description"]: t2_score,
                scores["T3"]["description"]: t3_score,
                scores["T4"]["description"]: t4_score,
                "Total Score": total_score,
            }
            rows.append(new_row_data)

    rows_df = pd.DataFrame(rows)
    final_score_table = pd.concat(
        [final_score_table, rows_df], ignore_index=True, join="outer"
    )

    return final_score_table.sort_values(
        by=["Total Score", "User Name"], ascending=[False, True]
    )
