"""Jämför normal och strikt validering av antalet i vår ordermodell."""

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from pydantic import ValidationError

from order_model import Order


def validate_quantity(value: object, strict: bool) -> str:
    """Validerar ett testvärde medan övriga fält har rätt Python-typer."""
    data = {
        "order_id": "ORD-TEST",
        "product": "Anteckningsbok",
        "quantity": value,
        "unit_price": Decimal("49.90"),
        "order_date": date(2026, 9, 1),
    }

    try:
        order = Order.model_validate(data, strict=strict)
    except ValidationError as exc:
        error_types = ", ".join(error["type"] for error in exc.errors())
        return f"Underkänd ({error_types})"

    return f"Godkänd (antal={order.quantity})"


def main() -> None:
    """Kör sex jämförelser och sparar resultaten i JSON-format."""
    test_values = ["3", 3, 3.0, 3.5, True, 0]
    results = []

    for value in test_values:
        result = {
            "input": repr(value),
            "input_type": type(value).__name__,
            "normal": validate_quantity(value, strict=False),
            "strict": validate_quantity(value, strict=True),
        }
        results.append(result)
        print(
            f"{result['input']} ({result['input_type']}): "
            f"normal={result['normal']}; strikt={result['strict']}"
        )

    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "strictness_comparison.json"
    output_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("\nSparat i outputs/strictness_comparison.json")


if __name__ == "__main__":
    main()
