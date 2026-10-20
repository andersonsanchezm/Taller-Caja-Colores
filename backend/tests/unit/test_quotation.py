"""Pruebas unitarias y de caja blanca para las reglas de cotización."""

from decimal import Decimal

import pytest

from app.services.quotation import (
    CustomerType,
    QuotationValidationError,
    ShippingType,
    calculate_quote,
)


@pytest.mark.parametrize(
    ("weight", "rate"),
    [
        ("0.01", "2.00"),
        ("5.00", "2.00"),
        ("5.01", "4.00"),
        ("20.00", "4.00"),
    ],
)
def test_aplica_tarifa_en_limites_de_peso(weight: str, rate: str) -> None:
    # Valida: QUOTE-REQ-002, QUOTE-REQ-004, QUOTE-AC-002, QUOTE-AC-003
    result = calculate_quote(
        Decimal(weight), CustomerType.NEW, ShippingType.STANDARD
    )

    assert result.rate_per_kg == Decimal(rate)


@pytest.mark.parametrize(
    "weight",
    ["-0.01", "0.00", "20.01"],
)
def test_rechaza_peso_fuera_de_rango(weight: str) -> None:
    # Valida: QUOTE-REQ-002, QUOTE-REQ-009
    with pytest.raises(QuotationValidationError) as error:
        calculate_quote(Decimal(weight), CustomerType.NEW, ShippingType.STANDARD)

    assert error.value.code == "WEIGHT_OUT_OF_RANGE"
    assert error.value.field == "weight_kg"


def test_rechaza_peso_con_mas_de_dos_decimales() -> None:
    # Valida: QUOTE-REQ-003, QUOTE-AC-005
    with pytest.raises(QuotationValidationError) as error:
        calculate_quote(
            Decimal("1.234"), CustomerType.NEW, ShippingType.STANDARD
        )

    assert error.value.code == "WEIGHT_PRECISION_INVALID"


@pytest.mark.parametrize(
    ("customer", "discount"),
    [
        (CustomerType.NEW, "0.00"),
        (CustomerType.FREQUENT, "0.70"),
        (CustomerType.VIP, "1.40"),
    ],
)
def test_aplica_descuento_por_cliente(
    customer: CustomerType, discount: str, one_kg: Decimal
) -> None:
    # Valida: QUOTE-REQ-005, QUOTE-AC-004
    result = calculate_quote(one_kg, customer, ShippingType.STANDARD)

    assert result.discount == Decimal(discount)


@pytest.mark.parametrize(
    ("shipping", "surcharge"),
    [
        (ShippingType.STANDARD, "0.00"),
        (ShippingType.EXPRESS, "1.75"),
    ],
)
def test_aplica_recargo_por_envio(
    shipping: ShippingType, surcharge: str, one_kg: Decimal
) -> None:
    # Valida: QUOTE-REQ-006, QUOTE-AC-004
    result = calculate_quote(one_kg, CustomerType.NEW, shipping)

    assert result.surcharge == Decimal(surcharge)


def test_calcula_cotizacion_vip_express() -> None:
    # Valida: QUOTE-REQ-001, QUOTE-REQ-007, QUOTE-REQ-008, QUOTE-AC-001
    result = calculate_quote(
        Decimal("5.01"), CustomerType.VIP, ShippingType.EXPRESS
    )

    assert result.base_rate == Decimal("5.00")
    assert result.weight_charge == Decimal("20.04")
    assert result.subtotal == Decimal("25.04")
    assert result.discount == Decimal("5.01")
    assert result.surcharge == Decimal("6.26")
    assert result.total == Decimal("26.29")
    assert result.currency == "USD"


@pytest.mark.parametrize("weight", [Decimal("NaN"), Decimal("Infinity")])
def test_rechaza_peso_no_finito(weight: Decimal) -> None:
    # Valida: QUOTE-REQ-009
    with pytest.raises(QuotationValidationError) as error:
        calculate_quote(weight, CustomerType.NEW, ShippingType.STANDARD)

    assert error.value.code == "REQUEST_VALIDATION_ERROR"

