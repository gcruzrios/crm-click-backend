from datetime import datetime, timezone


def utcnow() -> datetime:
    """Returns naive UTC datetime (compatible with asyncpg DateTime columns)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
