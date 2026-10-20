"""Mocks y factories de datos para pruebas del backend."""

from decimal import Decimal

from app.services.quotation import CustomerType, ShippingType


def valid_quote_payload() -> dict[str, object]:
    """Payload válido estándar para pruebas de integración."""
    return {
        "weight_kg": 5.01,
        "customer_type": CustomerType.VIP.value,
        "shipping_type": ShippingType.EXPRESS.value,
    }


def valid_quote_values() -> tuple[Decimal, CustomerType, ShippingType]:
    """Valores tipados para unit tests del dominio."""
    return Decimal("5.01"), CustomerType.VIP, ShippingType.EXPRESS


def invalid_payloads() -> list[dict[str, object]]:
    """Entradas inválidas reutilizables para pruebas de contrato."""
    return [
        {"customer_type": "VIP", "shipping_type": "EXPRESS"},
        {"weight_kg": "5.01", "customer_type": "VIP", "shipping_type": "EXPRESS"},
        {"weight_kg": True, "customer_type": "VIP", "shipping_type": "EXPRESS"},
        {"weight_kg": 1, "customer_type": "INVALID", "shipping_type": "EXPRESS"},
        {"weight_kg": 1, "customer_type": "VIP", "shipping_type": "INVALID"},
    ]
