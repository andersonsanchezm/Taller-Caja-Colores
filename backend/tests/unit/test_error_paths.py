"""Cobertura explícita de caminos de error y serialización."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.quote import QuoteRequest
from app.services.quotation import CustomerType, ShippingType, QuotationValidationError, calculate_quote


@pytest.mark.parametrize("value", ["1.00", True, None, [], {}])
def test_request_rechaza_tipos_no_numericos(value: object) -> None:
    with pytest.raises(ValidationError):
        QuoteRequest(weight_kg=value, customer_type="VIP", shipping_type="EXPRESS")


def test_error_de_dominio_expone_codigo_mensaje_y_campo() -> None:
    with pytest.raises(QuotationValidationError) as error:
        calculate_quote(Decimal("20.01"), CustomerType.NEW, ShippingType.STANDARD)

    assert error.value.code
    assert error.value.message
    assert error.value.field == "weight_kg"
