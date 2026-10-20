# Integration tests

## Objetivo

Validar la integración HTTP de FastAPI, el contrato JSON, serialización, errores y CORS.

## Ambiente

```bash
cd backend
source .venv/bin/activate
```

No es necesario iniciar Uvicorn: se utiliza `TestClient`.

## Archivos

- `backend/tests/integration/test_quotes_api.py`
- `backend/tests/integration/test_contract_and_security.py`
- `Testing/backend/mocks.py`

## Cobertura

- `GET /health`.
- `POST /api/v1/quotes/calculate`.
- Respuestas `200` y `422`.
- Campos faltantes, adicionales y tipos inválidos.
- JSON mal formado.
- Métodos HTTP no permitidos.
- Contrato uniforme de error.
- CORS.
- Solicitudes concurrentes.

## Comando

```bash
pytest tests/integration -q
```

## Resultado de referencia

`25 passed`.
