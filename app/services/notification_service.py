from pathlib import Path
from datetime import datetime, UTC
import json

NOTIFICATION_DIR = Path("storage/notifications")

def write_order_notification(
    order_id: int,
    user_id: int,
    email: str,
    event_type: str,
    message: str,
):
    NOTIFICATION_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "event_type": event_type,
        "created_at": datetime.now(UTC).isoformat(),
        "order_id": order_id,
        "user_id": user_id,
        "email": email,
        "message": message,
    }

    output_file = NOTIFICATION_DIR / f"order_{order_id}_{event_type.lower()}_{int(datetime.now(UTC).timestamp())}.json"
    output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")