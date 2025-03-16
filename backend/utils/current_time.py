from datetime import datetime, timezone

def current_time() -> datetime:
    return datetime.now(tz=timezone.utc)