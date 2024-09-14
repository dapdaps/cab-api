from datetime import datetime, timezone, time


def get_today_timestamp(hour: int = 0, minute: int = 0, second: int = 0):
    today_utc = datetime.now(timezone.utc).date()
    midnight_utc = datetime.combine(today_utc, time(hour, minute, second), timezone.utc)
    timestamp_utc = int(midnight_utc.timestamp())
    return timestamp_utc


def is_same_day(timestamp1, timestamp2):
    dt1 = datetime.fromtimestamp(timestamp1, tz=timezone.utc)
    dt2 = datetime.fromtimestamp(timestamp2, tz=timezone.utc)
    return dt1.date() == dt2.date()


def is_same_hour(timestamp1, timestamp2):
    dt1 = datetime.fromtimestamp(timestamp1, tz=timezone.utc)
    dt2 = datetime.fromtimestamp(timestamp2, tz=timezone.utc)
    return (dt1.year == dt2.year and
            dt1.month == dt2.month and
            dt1.day == dt2.day and
            dt1.hour == dt2.hour)


def is_midnight(timestamp):
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    midnight = datetime.combine(dt.date(), time(0, 0, 0), timezone.utc)
    return dt == midnight
