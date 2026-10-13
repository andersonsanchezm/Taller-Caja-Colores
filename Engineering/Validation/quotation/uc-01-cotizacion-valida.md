# UC-01 — Cotización válida

## Valida

- QUOTE-REQ-001
- QUOTE-REQ-004
- QUOTE-REQ-005
- QUOTE-REQ-006
- QUOTE-REQ-007
- QUOTE-REQ-008
- QUOTE-AC-001
- API-REQ-005

## Objetivo

Comprobar una cotización válida desde la API.

## Tipo

Caja negra, integración y unit test.

## Precondiciones

Backend activo en `http://127.0.0.1:8000`.

## Datos

```json
{"weight_kg": 5.01, "customer_type": "VIP", "shipping_type": "EXPRESS"}
```

## Procedimiento

1. Enviar `POST /api/v1/quotes/calculate`.
2. Revisar código, estructura y valores.

## Resultado esperado

HTTP `200`; tarifa `4.00`; cargo `20.04`; subtotal `25.04`; descuento `5.01`; recargo `6.26`; total `26.29`; moneda `USD`.

## Evidencia y resultado

Registrar comando, JSON y test automatizado. Resultado: `Not Run`.
