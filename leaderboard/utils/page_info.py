import pandas as pd
from typing import Dict


def extract_page_info(df: pd.DataFrame) -> Dict:
    """
    Returns page info for each of the contribution types

    Args:
        df: graphql query api response converted to dataframe

    Returns:
        A dictionary containing page info for each of the contribution types
    """
    page_info_keys = {
        "T1": "pullRequestContributions",
        "T2": "pullRequestReviewContributions",
        "T3": "issueContributions",
        "T4": "issueComments",  # Note: This uses 'hasPreviousPage' and 'startCursor'
        "T5": "repositoryContributions",
    }

    page_info = {}
    for key, contribution_type in page_info_keys.items():
        if key == "T4":
            page_info[f"page_info_{key}"] = {
                "hasPreviousPage": df[
                    f"data.user.{contribution_type}.pageInfo.hasPreviousPage"
                ].iloc[0],
                "startCursor": df[
                    f"data.user.{contribution_type}.pageInfo.startCursor"
                ].iloc[0],
            }
        else:
            page_info[f"page_info_{key}"] = {
                "hasNextPage": df[
                    f"data.user.contributionsCollection.{contribution_type}.pageInfo.hasNextPage"
                ].iloc[0],
                "endCursor": df[
                    f"data.user.contributionsCollection.{contribution_type}.pageInfo.endCursor"
                ].iloc[0],
            }

    return page_info
