"""Pruebas de estrés controladas para las reglas puras de cotización."""

from decimal import Decimal

import pytest

from app.services.quotation import CustomerType, ShippingType, calculate_quote


@pytest.mark.stress
@pytest.mark.parametrize("iteration", range(1000))
def test_calculo_repetido_es_estable(iteration: int) -> None:
    """Mil ejecuciones iguales no deben cambiar el resultado ni lanzar errores."""
    result = calculate_quote(
        Decimal("5.01"), CustomerType.VIP, ShippingType.EXPRESS
    )

    assert result.total == Decimal("26.29")


@pytest.mark.stress
def test_matriz_de_datos_repetida() -> None:
    """Procesa repetidamente todos los tramos y combinaciones comerciales."""
    inputs = [
        ("0.01", CustomerType.NEW, ShippingType.STANDARD),
        ("5.00", CustomerType.FREQUENT, ShippingType.EXPRESS),
        ("5.01", CustomerType.VIP, ShippingType.STANDARD),
        ("20.00", CustomerType.VIP, ShippingType.EXPRESS),
    ]

    for _ in range(250):
        for weight, customer, shipping in inputs:
            result = calculate_quote(Decimal(weight), customer, shipping)
            assert result.total.is_finite()
