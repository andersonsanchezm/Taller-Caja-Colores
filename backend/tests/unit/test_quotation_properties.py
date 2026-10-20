"""Propiedades e invariantes del dominio de cotizaciones."""

from decimal import Decimal

import pytest

from app.services.quotation import CustomerType, ShippingType, calculate_quote


@pytest.mark.parametrize("weight", ["0.01", "1.00", "5.00", "5.01", "10.00", "20.00"])
@pytest.mark.parametrize("customer", list(CustomerType))
@pytest.mark.parametrize("shipping", list(ShippingType))
def test_invariantes_de_cotizacion(
    weight: str, customer: CustomerType, shipping: ShippingType
) -> None:
    # Valida: QUOTE-REQ-007, QUOTE-REQ-008
    result = calculate_quote(Decimal(weight), customer, shipping)

    assert result.currency == "USD"
    assert result.total >= Decimal("0.00")
    assert result.subtotal >= result.base_rate
    assert result.discount >= Decimal("0.00")
    assert result.surcharge >= Decimal("0.00")
    for amount in (result.base_rate, result.weight_charge, result.subtotal, result.discount, result.surcharge, result.total):
        assert -amount.as_tuple().exponent <= 2
