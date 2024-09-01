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

    has_next_page_T1 = df[
        "data.user.contributionsCollection.pullRequestContributions.pageInfo.hasNextPage"
    ][0]
    end_cursor_T1 = df[
        "data.user.contributionsCollection.pullRequestContributions.pageInfo.endCursor"
    ][0]

    has_next_page_T2 = df[
        "data.user.contributionsCollection.pullRequestReviewContributions.pageInfo.hasNextPage"
    ][0]
    end_cursor_T2 = df[
        "data.user.contributionsCollection.pullRequestReviewContributions.pageInfo.endCursor"
    ][0]

    has_next_page_T3 = df[
        "data.user.contributionsCollection.issueContributions.pageInfo.hasNextPage"
    ][0]
    end_cursor_T3 = df[
        "data.user.contributionsCollection.issueContributions.pageInfo.endCursor"
    ][0]

    has_next_page_T4 = df["data.user.issueComments.pageInfo.hasPreviousPage"][0]
    end_cursor_T4 = df["data.user.issueComments.pageInfo.startCursor"][0]

    has_next_page_T5 = df[
        "data.user.contributionsCollection.repositoryContributions.pageInfo.hasNextPage"
    ][0]
    end_cursor_T5 = df[
        "data.user.contributionsCollection.repositoryContributions.pageInfo.endCursor"
    ][0]

    return {
        "page_info_T1": {
            "hasNextPage": has_next_page_T1,
            "endCursor": end_cursor_T1,
        },
        "page_info_T2": {
            "hasNextPage": has_next_page_T2,
            "endCursor": end_cursor_T2,
        },
        "page_info_T3": {
            "hasNextPage": has_next_page_T3,
            "endCursor": end_cursor_T3,
        },
        "page_info_T4": {
            "hasPreviousPage": has_next_page_T4,
            "startCursor": end_cursor_T4,
        },
        "page_info_T5": {
            "hasNextPage": has_next_page_T5,
            "endCursor": end_cursor_T5,
        },
    }
