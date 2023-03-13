import pytz


def datetimefilter(value, dt_format="%H:%M %d-%b-%Y"):
    """Set date timezone and convert to string according to the format specified."""
    tz = pytz.timezone('Asia/Tbilisi')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(dt_format)
