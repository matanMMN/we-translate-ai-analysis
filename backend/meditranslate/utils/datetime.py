from datetime import datetime
from zoneinfo import ZoneInfo

def datetime_to_str(dt: datetime,timezone:str,format:str="%Y-%m-%d %H:%M:%S %Z") -> str:
    """
    Convert a datetime object to a string in the format YYYY-MM-DD HH:MM:SS,
    always set to Jerusalem timezone and include time.

    :param dt: The datetime object to convert.
    :param timezone: timezone string
    :param format: optional overide string format
    :return: A string representation of the datetime in a readable format.
    """
    if dt is None:
        raise ValueError("The datetime argument cannot be None.")
    tz = ZoneInfo(timezone)
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=tz)
    else:
        dt = dt.astimezone(tz)
    return dt.strftime(format)
