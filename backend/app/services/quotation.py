"""Reglas de negocio para calcular cotizaciones de FastExpress."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import StrEnum


BASE_RATE = Decimal("5.00")
MIN_WEIGHT = Decimal("0.01")
LIGHT_WEIGHT_LIMIT = Decimal("5.00")
MAX_WEIGHT = Decimal("20.00")
LIGHT_RATE_PER_KG = Decimal("2.00")
HEAVY_RATE_PER_KG = Decimal("4.00")
MONEY_PRECISION = Decimal("0.01")


class CustomerType(StrEnum):
    """Categorias de cliente admitidas por BR-03."""

    NEW = "NUEVO"
    FREQUENT = "FRECUENTE"
    VIP = "VIP"


class ShippingType(StrEnum):
    """Categorias de envio admitidas por BR-04."""

    STANDARD = "ESTANDAR"
    EXPRESS = "EXPRESS"


DISCOUNT_RATES = {
    CustomerType.NEW: Decimal("0.00"),
    CustomerType.FREQUENT: Decimal("0.10"),
    CustomerType.VIP: Decimal("0.20"),
}

SURCHARGE_RATES = {
    ShippingType.STANDARD: Decimal("0.00"),
    ShippingType.EXPRESS: Decimal("0.25"),
}


class QuotationValidationError(ValueError):
    """Representa una entrada que incumple las reglas de cotizacion."""

    def __init__(self, code: str, message: str, field: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.field = field


@dataclass(frozen=True)
class QuoteResult:
    """Contiene el desglose inmutable de una cotizacion calculada."""

    weight_kg: Decimal
    customer_type: CustomerType
    shipping_type: ShippingType
    base_rate: Decimal
    rate_per_kg: Decimal
    weight_charge: Decimal
    subtotal: Decimal
    discount_rate: Decimal
    discount: Decimal
    surcharge_rate: Decimal
    surcharge: Decimal
    total: Decimal
    currency: str = "USD"


def _money(value: Decimal) -> Decimal:
    """Redondea un importe monetario a dos decimales."""

    return value.quantize(MONEY_PRECISION, rounding=ROUND_HALF_UP)


def _validate_weight(weight_kg: Decimal) -> None:
    """Comprueba el dominio y la precision permitidos para el peso."""

    if not weight_kg.is_finite():
        raise QuotationValidationError(
            code="REQUEST_VALIDATION_ERROR",
            message="El peso debe ser un numero decimal finito.",
            field="weight_kg",
        )

    if weight_kg.as_tuple().exponent < -2:
        raise QuotationValidationError(
            code="WEIGHT_PRECISION_INVALID",
            message="El peso no puede tener mas de dos cifras decimales.",
            field="weight_kg",
        )

    if weight_kg < MIN_WEIGHT or weight_kg > MAX_WEIGHT:
        raise QuotationValidationError(
            code="WEIGHT_OUT_OF_RANGE",
            message="El peso debe estar entre 0.01 y 20.00 kg.",
            field="weight_kg",
        )


def calculate_quote(
    weight_kg: Decimal,
    customer_type: CustomerType,
    shipping_type: ShippingType,
) -> QuoteResult:
    """Calcula una cotizacion mediante las reglas BR-01 a BR-04."""

    _validate_weight(weight_kg)

    if weight_kg <= LIGHT_WEIGHT_LIMIT:
        rate_per_kg = LIGHT_RATE_PER_KG
    else:
        rate_per_kg = HEAVY_RATE_PER_KG

    discount_rate = DISCOUNT_RATES[customer_type]
    surcharge_rate = SURCHARGE_RATES[shipping_type]

    weight_charge = _money(weight_kg * rate_per_kg)
    subtotal = _money(BASE_RATE + weight_charge)
    discount = _money(subtotal * discount_rate)
    surcharge = _money(subtotal * surcharge_rate)
    total = _money(subtotal - discount + surcharge)

    return QuoteResult(
        weight_kg=weight_kg,
        customer_type=customer_type,
        shipping_type=shipping_type,
        base_rate=BASE_RATE,
        rate_per_kg=rate_per_kg,
        weight_charge=weight_charge,
        subtotal=subtotal,
        discount_rate=discount_rate,
        discount=discount,
        surcharge_rate=surcharge_rate,
        surcharge=surcharge,
        total=total,
    )
