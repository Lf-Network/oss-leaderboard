""" Utilities for data processing. """
from datetime import datetime, timedelta


def get_date(days: int) -> datetime:
    """ Get date before x days.
    Args: 
        days: number of days before from which data is fetched.
    
    Returns: 
        DateTime object in isoformat.
    """

    return (datetime.today() - timedelta(days=days)).isoformat()
