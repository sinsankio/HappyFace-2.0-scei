from datetime import datetime


def get_iso_datetime(current_datetime: datetime) -> str:
    return current_datetime.isoformat()


def get_current_iso_datetime() -> str:
    current_datetime = datetime.now()
    return get_iso_datetime(current_datetime)
