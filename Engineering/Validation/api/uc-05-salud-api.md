# UC-05 — Salud de la API

## Valida

- API-REQ-001
- API-AC-001

## Tipo

Smoke test y caja negra.

## Procedimiento

1. Iniciar el backend.
2. Ejecutar `GET http://127.0.0.1:8000/health`.

## Resultado esperado

HTTP `200` y `{ "status": "ok" }`.

## Resultado

`Not Run`.
