""" Utilities for data processing. """
from datetime import datetime, timedelta
import pandas as pd
import markdown


def get_date(days: int) -> str:
    """ Get date before x days.
    Args:
        days: number of days before from which data is fetched.

    Returns:
        DateTime string in isoformat.
    """

    return (datetime.today() - timedelta(days=days)).isoformat()


def convert_df_to_markdown(df: pd.DataFrame) -> str:
    """ Convert dataframe to markdown 
    Args:
        df: dataframe object

    Returns:
        markdown string
    """

    return df.to_markdown()

def convert_df_to_html(df: pd.DataFrame) -> str:
    """ Convert dataframe to html 
    Args:
        df: dataframe object

    Returns:
        html string
    """

    return df.to_html()


def convert_mk_to_html(mk_data: str) -> str:
    """ Convert markdown to html 
    Args:
        mk_data: markdown string

    Returns:
        html string
    """

    return markdown.markdown(mk_data, extensions=["tables"])
