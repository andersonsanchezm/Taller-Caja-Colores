# Unit tests

## Objetivo

Validar unidades aisladas sin depender de servidores, navegador ni servicios externos.

## Ambiente

```bash
cd backend
source .venv/bin/activate
```

Requisitos: Python 3.11+, pytest y pytest-cov.

## Backend

Archivos:

- `backend/tests/unit/test_quotation.py`
- `backend/tests/unit/test_quotation_properties.py`
- `backend/tests/unit/test_error_paths.py`
- `Testing/backend/mocks.py`

Se validan tarifas, límites, descuentos, recargos, redondeo, invariantes y excepciones.

## Frontend

Archivos:

- `frontend/tests/unit/quotationService.test.js`
- `frontend/tests/unit/apiService.test.js`
- `Testing/frontend/apiMocks.js`

El cliente HTTP usa `fetch` mockeado; no se requiere backend activo.

## Comandos

```bash
cd backend
pytest tests/unit -q
```

```bash
cd frontend
npm run test:unit
```

## Resultado de referencia

- Backend: `58 passed`.
- Frontend: incluido en la suite de Vitest.
