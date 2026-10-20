"""Configuración común de las pruebas del backend."""

import pytest
from decimal import Decimal
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Testing.backend.mocks import valid_quote_payload as make_valid_quote_payload


@pytest.fixture
def valid_quote_payload() -> dict[str, object]:
    return make_valid_quote_payload()


@pytest.fixture
def one_kg() -> Decimal:
    return Decimal("1.00")
