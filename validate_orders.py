"""Validerar orderdata från CSV och sparar godkända rader och en felrapport."""

import csv
import json
from decimal import Decimal
from pathlib import Path

from pydantic import ValidationError

from order_model import Order

CSV_COLUMNS = list(Order.model_fields)


def validate_csv(input_path: Path) -> tuple[list[Order], list[dict]]:
    """Läser CSV-data och skiljer godkända orderrader från underkända."""
    valid_orders = []
    rejected_rows = []

    with input_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, restkey="__extra_columns__", strict=True)
        headers = reader.fieldnames

        if headers is None:
            raise ValueError("CSV-filen saknar en rubrikrad.")

        if len(headers) != len(CSV_COLUMNS) or set(headers) != set(CSV_COLUMNS):
            raise ValueError(
                "CSV-filen måste innehålla exakt dessa kolumner: "
                + ", ".join(CSV_COLUMNS)
            )

        for row in reader:
            try:
                order = Order.model_validate(row)
            except ValidationError as exc:
                row_errors = [
                    {
                        "field": ".".join(str(part) for part in error["loc"]),
                        "message": error["msg"],
                        "type": error["type"],
                    }
                    for error in exc.errors()
                ]
                rejected_rows.append(
                    {
                        "csv_line": reader.line_num,
                        "order_id": row.get("order_id"),
                        "errors": row_errors,
                    }
                )
            else:
                valid_orders.append(order)

    return valid_orders, rejected_rows


def save_results(
    valid_orders: list[Order],
    rejected_rows: list[dict],
    input_path: Path,
    output_dir: Path,
) -> dict:
    """Sparar validerade orderrader och en rapport med sammanfattning och fel."""
    total_amount = sum(
        (order.quantity * order.unit_price for order in valid_orders),
        Decimal("0.00"),
    )

    report = {
        "source_file": input_path.name,
        "total_rows": len(valid_orders) + len(rejected_rows),
        "valid_rows": len(valid_orders),
        "invalid_rows": len(rejected_rows),
        "error_count": sum(len(row["errors"]) for row in rejected_rows),
        "valid_total_amount": format(total_amount, ".2f"),
        "currency": "SEK",
        "rejected_rows": rejected_rows,
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "valid_orders.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for order in valid_orders:
            writer.writerow(order.model_dump(mode="json"))

    (output_dir / "validation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return report


def main() -> None:
    """Kör valideringen med projektets exempeldata."""
    project_dir = Path(__file__).resolve().parent
    input_path = project_dir / "data" / "orders.csv"
    output_dir = project_dir / "outputs"

    try:
        valid_orders, rejected_rows = validate_csv(input_path)
        report = save_results(valid_orders, rejected_rows, input_path, output_dir)
    except (OSError, ValueError, csv.Error) as exc:
        raise SystemExit(f"Kunde inte slutföra körningen: {exc}")

    print("Validering klar.")
    print(f"Behandlade rader: {report['total_rows']}")
    print(f"Godkända rader: {report['valid_rows']}")
    print(f"Underkända rader: {report['invalid_rows']}")
    print(f"Valideringsfel: {report['error_count']}")
    print(f"Summa för godkända orderrader: {report['valid_total_amount']} SEK")
    print("Sparat i outputs/valid_orders.csv och outputs/validation_report.json")


if __name__ == "__main__":
    main()
