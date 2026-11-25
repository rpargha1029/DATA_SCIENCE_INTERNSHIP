"""Week 2 Client Project: Pure-Python Data Cleaning (Deduplication & Filtering)."""

from typing import Any, Dict, List, Set


def clean_customer_records(
    raw_records: List[Dict[str, Any]], min_spend: float = 0.0
) -> List[Dict[str, Any]]:
    """
    Clean raw customer transaction records:
    - Strip whitespace and normalize email to lowercase.
    - Remove records with missing/invalid email or spend <= min_spend.
    - Deduplicate by (email, product) keeping the first valid record.
    """
    seen_keys: Set[tuple] = set()
    cleaned: List[Dict[str, Any]] = []

    for record in raw_records:
        email = str(record.get("email", "")).strip().lower()
        product = str(record.get("product", "")).strip()
        spend = record.get("spend")

        if not email or "@" not in email or not product:
            continue
        if not isinstance(spend, (int, float)) or spend <= min_spend:
            continue

        dedup_key = (email, product.lower())
        if dedup_key in seen_keys:
            continue

        seen_keys.add(dedup_key)
        cleaned.append(
            {
                "customer_id": record.get("customer_id"),
                "email": email,
                "product": product.title(),
                "spend": round(float(spend), 2),
            }
        )

    return cleaned


def main() -> None:
    """Run data cleaning pipeline on sample messy client records."""
    raw_data = [
        {"customer_id": 101, "email": " Alice@Example.com ", "product": "laptop", "spend": 1200.0},
        {"customer_id": 102, "email": "bob@example.com", "product": "mouse", "spend": 25.5},
        {"customer_id": 103, "email": "alice@example.com", "product": "Laptop", "spend": 1200.0},  # duplicate
        {"customer_id": 104, "email": "invalid-email", "product": "keyboard", "spend": 75.0},  # invalid email
        {"customer_id": 105, "email": "carol@example.com", "product": "monitor", "spend": -50.0},  # negative spend
        {"customer_id": 106, "email": "dave@example.com", "product": "webcam", "spend": 89.99},
    ]

    cleaned_data = clean_customer_records(raw_data, min_spend=0.0)
    print(f"Raw record count:     {len(raw_data)}")
    print(f"Cleaned record count: {len(cleaned_data)}")
    print("\n=== Cleaned Records ===")
    for row in cleaned_data:
        print(row)


if __name__ == "__main__":
    main()
