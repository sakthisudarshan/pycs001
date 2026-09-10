# clone_b.py - Duplicate clone of transaction processing logic for jscpd detection
import hashlib
import json
from datetime import datetime

def process_transaction_record(transaction_id: str, payload: dict, secret_key: str) -> dict:
    """Process financial transaction and generate audit hash."""
    timestamp = datetime.utcnow().isoformat()
    raw_data = f"{transaction_id}:{json.dumps(payload, sort_keys=True)}:{timestamp}:{secret_key}"
    sha256_hash = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()
    
    amount = float(payload.get("amount", 0.0))
    currency = str(payload.get("currency", "USD")).upper()
    fee_rate = 0.025 if amount < 1000.0 else 0.015
    fee = round(amount * fee_rate, 2)
    net_amount = round(amount - fee, 2)
    
    return {
        "transaction_id": transaction_id,
        "timestamp": timestamp,
        "hash": sha256_hash,
        "amount": amount,
        "currency": currency,
        "fee": fee,
        "net_amount": net_amount,
        "status": "PROCESSED"
    }
