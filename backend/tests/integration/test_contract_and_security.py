"""Pruebas de caja negra del contrato HTTP y seguridad básica."""

from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
def test_endpoint_de_calculo_solo_acepta_post(client: TestClient, method: str) -> None:
    response = getattr(client, method)("/api/v1/quotes/calculate")

    assert response.status_code in {405, 422}


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        {},
        {"weight_kg": None, "customer_type": "VIP", "shipping_type": "EXPRESS"},
        {"weight_kg": 1, "customer_type": None, "shipping_type": "EXPRESS"},
        {"weight_kg": 1, "customer_type": "VIP", "shipping_type": None},
    ],
)
def test_rechaza_payloads_incompletos_o_no_objeto(
    client: TestClient, payload: object
) -> None:
    response = client.post("/api/v1/quotes/calculate", json=payload)

    assert response.status_code == 422


def test_rechaza_json_mal_formado(client: TestClient) -> None:
    response = client.post(
        "/api/v1/quotes/calculate",
        content='{"weight_kg": 1,',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422


def test_respuesta_de_error_tiene_contrato_uniforme(client: TestClient) -> None:
    response = client.post(
        "/api/v1/quotes/calculate",
        json={"weight_kg": 1, "customer_type": "INVALID", "shipping_type": "EXPRESS"},
    )

    detail = response.json()["detail"]
    assert set(detail) == {"code", "message", "field"}


def test_no_interpreta_html_en_los_datos(client: TestClient) -> None:
    response = client.post(
        "/api/v1/quotes/calculate",
        json={
            "weight_kg": 1,
            "customer_type": "<script>alert(1)</script>",
            "shipping_type": "EXPRESS",
        },
    )

    assert response.status_code == 422
    assert "<script>" not in response.text


def test_solicitud_concurrente_no_mezcla_resultados() -> None:
    payloads = [
        {"weight_kg": 1, "customer_type": "NUEVO", "shipping_type": "ESTANDAR"},
        {"weight_kg": 5.01, "customer_type": "VIP", "shipping_type": "EXPRESS"},
        {"weight_kg": 20, "customer_type": "FRECUENTE", "shipping_type": "EXPRESS"},
    ]

    def request(payload: dict[str, object]) -> tuple[int, str, float]:
        with TestClient(app) as client:
            response = client.post("/api/v1/quotes/calculate", json=payload)
            return response.status_code, response.json()["customer_type"], float(response.json()["weight_kg"])

    with ThreadPoolExecutor(max_workers=12) as executor:
        results = list(executor.map(request, payloads * 20))

    assert all(status == 200 for status, _, _ in results)
    assert {(customer, weight) for _, customer, weight in results} == {
        ("NUEVO", 1.0),
        ("VIP", 5.01),
        ("FRECUENTE", 20.0),
    }


def test_cors_rechaza_origen_no_configurado(client: TestClient) -> None:
    response = client.options(
        "/api/v1/quotes/calculate",
        headers={
            "Origin": "https://sitio-no-autorizado.example",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert "access-control-allow-origin" not in response.headers
