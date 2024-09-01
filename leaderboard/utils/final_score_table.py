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

    # Set index for efficient lookup
    intermediate_score_df.set_index("user_name", inplace=True)

    def calculate_type_score(user_row, type_description, subtypes):
        return sum(
            user_row[f"{type_description.lower()}s{i}"] * subtypes[f"{type_description.upper()}S{i}"]["weight"]
            for i in range(1, len(subtypes) + 1)
        )

    rows = []

    for user_name in user_list:
        try:
            user_row = intermediate_score_df.loc[user_name]
        except KeyError:
            continue

        t1_score = calculate_type_score(user_row, "T1", scores["T1"]["subtypes"])
        t2_score = calculate_type_score(user_row, "T2", scores["T2"]["subtypes"])
        t3_score = calculate_type_score(user_row, "T3", scores["T3"]["subtypes"])
        t4_score = calculate_type_score(user_row, "T4", scores["T4"]["subtypes"])

        total_score = t1_score + t2_score + t3_score + t4_score

        # Skip users with zero total score
        if total_score <= 0.0:
            continue

        # Create a new row for the final score table
        new_row_data = {
            "User Name": user_name,
            scores["T1"]["description"]: t1_score,
            scores["T2"]["description"]: t2_score,
            scores["T3"]["description"]: t3_score,
            scores["T4"]["description"]: t4_score,
            "Total Score": total_score,
        }
        rows.append(new_row_data)

    # Create the final score table DataFrame
    final_score_table = pd.DataFrame(rows)

    # Sort the final score table
    return final_score_table.sort_values(by=["Total Score", "User Name"], ascending=[False, True])