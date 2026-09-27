"""Visar typomvandling och valideringsfel med två orderexempel."""

from pydantic import ValidationError

from order_model import Order


def main() -> None:
    """Kör demonstrationen och skriver resultatet i terminalen."""
    valid_data = {
        "order_id": "ORD-1001",
        "product": "  Anteckningsbok  ",
        "quantity": "3",
        "unit_price": "49.90",
        "order_date": "2026-09-01",
    }

    order = Order.model_validate(valid_data)

    print("GODKÄND ORDER")
    for field, value in order.model_dump().items():
        print(f"{field}: {value} ({type(value).__name__})")

    invalid_data = {
        **valid_data,
        "product": "   ",
        "quantity": "0",
        "unit_price": "-10.00",
        "order_date": "2026-02-30",
    }

    print("\nFELAKTIG ORDER")
    try:
        Order.model_validate(invalid_data)
    except ValidationError as exc:
        print(f"Antal upptäckta fel: {exc.error_count()}")
        for error in exc.errors():
            print(f"- {error['loc'][0]}: {error['msg']}")


if __name__ == "__main__":
    main()
