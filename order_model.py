"""Datamodell och valideringsregler för en orderrad."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Order(BaseModel):
    """Beskriver vilka värden en orderrad får innehålla."""

    model_config = ConfigDict(extra="forbid")

    order_id: str
    product: str
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0, decimal_places=2, allow_inf_nan=False)
    order_date: date

    @field_validator("order_id", "product", mode="after")
    @classmethod
    def clean_required_text(cls, value: str) -> str:
        """Tar bort omgivande blanksteg och avvisar tom text."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "Fältet får inte vara tomt eller bara innehålla blanksteg."
            )
        return cleaned
