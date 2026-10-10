"""Modelos JSON de entrada y salida para las cotizaciones."""

from decimal import Decimal
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer, field_validator

from app.services.quotation import CustomerType, ShippingType


DecimalString = Annotated[
    Decimal,
    PlainSerializer(lambda value: format(value, "f"), return_type=str),
]


class QuoteRequest(BaseModel):
    """Datos que el frontend debe enviar para solicitar una cotizacion."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "weight_kg": 5.01,
                "customer_type": "VIP",
                "shipping_type": "EXPRESS",
            }
        },
    )

    weight_kg: Decimal = Field(description="Peso del envio en kilogramos")
    customer_type: CustomerType = Field(description="Categoria del cliente")
    shipping_type: ShippingType = Field(description="Modalidad de envio")

    @field_validator("weight_kg", mode="before")
    @classmethod
    def weight_must_be_a_json_number(cls, value: Any) -> Any:
        """Rechaza textos y booleanos antes de convertir el peso a Decimal."""

        if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
            raise ValueError("El peso debe enviarse como un numero JSON.")
        return value


class QuoteResponse(BaseModel):
    """Desglose que el backend devuelve para una cotizacion valida."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "weight_kg": "5.01",
                "customer_type": "VIP",
                "shipping_type": "EXPRESS",
                "base_rate": "5.00",
                "rate_per_kg": "4.00",
                "weight_charge": "20.04",
                "subtotal": "25.04",
                "discount_rate": "0.20",
                "discount": "5.01",
                "surcharge_rate": "0.25",
                "surcharge": "6.26",
                "total": "26.29",
                "currency": "USD",
            }
        }
    )

    weight_kg: DecimalString
    customer_type: CustomerType
    shipping_type: ShippingType
    base_rate: DecimalString
    rate_per_kg: DecimalString
    weight_charge: DecimalString
    subtotal: DecimalString
    discount_rate: DecimalString
    discount: DecimalString
    surcharge_rate: DecimalString
    surcharge: DecimalString
    total: DecimalString
    currency: Literal["USD"]


class ErrorDetail(BaseModel):
    """Informacion estable y legible acerca de un error de solicitud."""

    code: str
    message: str
    field: str | None = None


class ErrorResponse(BaseModel):
    """Estructura uniforme de los errores devueltos por la API."""

    detail: ErrorDetail
