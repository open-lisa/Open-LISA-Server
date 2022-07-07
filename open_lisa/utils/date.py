from datetime import timezone, datetime


def get_UTC_timestamp():
    # UTC timestamp
    # Src: https://www.geeksforgeeks.org/get-utc-timestamp-in-python/#:~:text=Getting%20the%20UTC%20timestamp,convert%20our%20datetime%20to%20UTC.
    return datetime.now(
        timezone.utc).replace(tzinfo=timezone.utc).timestamp()
