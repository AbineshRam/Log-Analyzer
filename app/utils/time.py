from datetime import datetime, timezone


def utc_now() -> datetime:
    """
    Returns current UTC time.
    """
    return datetime.now(timezone.utc)


def utc_iso() -> str:
    """
    Returns UTC time in ISO format.
    """
    return utc_now().isoformat()
