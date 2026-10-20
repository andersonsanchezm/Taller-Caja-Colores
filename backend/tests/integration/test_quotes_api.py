"""Pruebas de integración HTTP y contrato de la API."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_responde_ok(client: TestClient) -> None:
    # Valida: API-REQ-001, API-AC-001
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_calcula_cotizacion_valida(client: TestClient) -> None:
    # Valida: API-REQ-002, API-REQ-005, API-AC-002
    response = client.post(
        "/api/v1/quotes/calculate",
        json={
            "weight_kg": 5.01,
            "customer_type": "VIP",
            "shipping_type": "EXPRESS",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == "26.29"
    assert body["currency"] == "USD"
    assert body["weight_kg"] == "5.01"


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({"weight_kg": 20.01, "customer_type": "VIP", "shipping_type": "EXPRESS"}, "WEIGHT_OUT_OF_RANGE"),
        ({"weight_kg": 1.234, "customer_type": "VIP", "shipping_type": "EXPRESS"}, "WEIGHT_PRECISION_INVALID"),
        ({"weight_kg": 1, "customer_type": "vip", "shipping_type": "EXPRESS"}, "CUSTOMER_TYPE_INVALID"),
        ({"weight_kg": 1, "customer_type": "VIP", "shipping_type": "express"}, "SHIPPING_TYPE_INVALID"),
    ],
)
def test_rechaza_errores_de_negocio(
    client: TestClient, payload: dict[str, object], code: str
) -> None:
    # Valida: API-REQ-003, API-REQ-006, QUOTE-REQ-009
    response = client.post("/api/v1/quotes/calculate", json=payload)

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["code"] == code
    assert "message" in detail
    assert "field" in detail


@pytest.mark.parametrize(
    "payload",
    [
        {"customer_type": "VIP", "shipping_type": "EXPRESS"},
        {"weight_kg": "1.00", "customer_type": "VIP", "shipping_type": "EXPRESS"},
        {"weight_kg": True, "customer_type": "VIP", "shipping_type": "EXPRESS"},
        {"weight_kg": 1, "customer_type": "VIP", "shipping_type": "EXPRESS", "extra": 1},
    ],
)
def test_rechaza_contrato_estructural(
    client: TestClient, payload: dict[str, object]
) -> None:
    # Valida: API-REQ-004, API-AC-003
    response = client.post("/api/v1/quotes/calculate", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()

