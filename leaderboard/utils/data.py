""" Utilities for data processing. """
from datetime import datetime, timedelta
import pandas as pd


def get_date(days: int) -> str:
    """ Get date before x days.
    Args:
        days: number of days before from which data is fetched.

    Returns:
        DateTime string in isoformat.
    """

    return (datetime.today() - timedelta(days=days)).isoformat()


def convert_df_to_markdown(df: pd.DataFrame) -> str:
    print(df.to_markdown())
    return df.to_markdown()
