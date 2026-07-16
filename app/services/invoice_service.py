from pathlib import Path
from datetime import datetime, UTC
import json

INVOICE_DIR = Path("storage/invoices")

def generate_invoice_file(
    order_id: int,
    user_id: int,
    email: str,
    total_price: float,
    status: str,
    items: list[dict],
):
    INVOICE_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "invoice_number": f"INV-{order_id}",
        "generated_at": datetime.now(UTC).isoformat(),
        "order_id": order_id,
        "user_id": user_id,
        "email": email,
        "status": status,
        "total_price": total_price,
        "items": items,
    }

    output_file = INVOICE_DIR / f"order_{order_id}_invoice.json"
    output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")