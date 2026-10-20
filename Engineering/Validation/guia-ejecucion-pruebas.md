# Guía de ejecución de pruebas QA

## 1. Propósito

Este documento explica cómo ejecutar y entender las pruebas implementadas para FastExpress. La suite está organizada bajo SDD: los tests validan requisitos y criterios de aceptación documentados en `Engineering/Specs`.

## 2. Tipos de prueba implementados

| Tipo | Herramienta | Qué verifica |
|---|---|---|
| Unit test backend | pytest | Reglas de cálculo, validaciones, redondeo e invariantes. |
| Integration test | pytest + FastAPI TestClient | Contrato HTTP, endpoints, errores, serialización y CORS. |
| Unit test frontend | Vitest | Validadores y cliente HTTP con `fetch` mockeado. |
| UI test de componentes | Vitest + Vue Test Utils + JSDOM | Eventos, estados y comportamiento de componentes Vue aislados. |
| Snapshot test | Vitest | Cambios visuales estructurales inesperados en componentes. |
| Stress test | pytest/Vitest | Estabilidad ante ejecuciones repetidas. |
| UI E2E | Playwright + Chromium | Flujo completo en navegador: frontend real, API real y resultado visible. |

## 3. Ambiente requerido

### Backend

- Python `3.11` o superior.
- Entorno virtual en `backend/.venv`.
- FastAPI.
- Uvicorn.
- pytest.
- pytest-cov.
- httpx.

### Frontend

- Node.js.
- npm.
- Vue 3.
- Vite.
- Vitest.
- Vue Test Utils.
- JSDOM.
- Playwright.
- Chromium instalado mediante Playwright.

### Preparación inicial

Backend:

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Frontend:

```bash
cd frontend
npm install
npx playwright install chromium
```

## 4. Unit tests del backend

### Qué prueban

Los unit tests prueban la lógica de negocio sin iniciar un servidor HTTP:

- Límites `0.01`, `5.00`, `5.01` y `20.00`.
- Rechazo de pesos inválidos.
- Precisión máxima de dos decimales.
- Tarifas ligera y pesada.
- Descuentos NUEVO, FRECUENTE y VIP.
- Recargos ESTANDAR y EXPRESS.
- Fórmula del total.
- Redondeo monetario.
- Valores no finitos.
- Invariantes del dominio.
- Excepciones y sus códigos.

### Archivos

- `backend/tests/unit/test_quotation.py`
- `backend/tests/unit/test_quotation_properties.py`
- `backend/tests/unit/test_error_paths.py`
- `Testing/backend/mocks.py`

### Comando

```bash
cd backend
source .venv/bin/activate
pytest tests/unit -q
```

## 5. Integration tests del backend

### Qué prueban

Ejecutan la aplicación FastAPI mediante `TestClient` y verifican:

- `GET /health`.
- `POST /api/v1/quotes/calculate`.
- Respuestas `200`.
- Respuestas `422`.
- Campos faltantes y adicionales.
- Tipos inválidos.
- JSON mal formado.
- Métodos HTTP no permitidos.
- Contrato uniforme de errores.
- CORS.
- Solicitudes concurrentes.
- Payloads inseguros básicos.

### Archivos

- `backend/tests/integration/test_quotes_api.py`
- `backend/tests/integration/test_contract_and_security.py`
- `Testing/backend/mocks.py`

### Comando

```bash
cd backend
source .venv/bin/activate
pytest tests/integration -q
```

## 6. Stress tests del backend

### Qué prueban

- Mil ejecuciones repetidas del cálculo VIP EXPRESS.
- 250 repeticiones de una matriz de pesos, clientes y envíos.
- Estabilidad del resultado.
- Ausencia de resultados no finitos.

### Archivo

`backend/tests/stress/test_quotation_stress.py`

### Comando

```bash
cd backend
source .venv/bin/activate
pytest tests/stress -m stress -q
```

## 7. Cobertura del backend

### Comando

```bash
cd backend
source .venv/bin/activate
pytest --cov=app --cov-branch --cov-report=term-missing
```

### Resultado de referencia

```text
1084 passed
Cobertura total: 98.79%
Objetivo mínimo: 85%
```

La advertencia de Starlette/httpx no hizo fallar las pruebas. Es una advertencia de deprecación de una dependencia.

## 8. Unit tests del frontend

### Qué prueban

- Validación del peso.
- Valores vacíos, texto, cero y negativos.
- Precisión decimal.
- Límites operativos.
- Formateo de moneda.
- Cliente HTTP usando `fetch` mockeado.
- Respuestas exitosas, `400`, `422`, `500`, JSON inválido y error de red.

### Archivos

- `frontend/tests/unit/quotationService.test.js`
- `frontend/tests/unit/apiService.test.js`
- `Testing/frontend/apiMocks.js`

### Comando

```bash
cd frontend
npm run test:unit
```

## 9. UI tests de componentes

### Qué prueban

Estos tests montan componentes Vue en un DOM simulado. No abren un navegador real.

- Entrada del peso.
- Emisión de eventos.
- Selección de cliente.
- Selección de envío.
- Envío del formulario.
- Mensajes de validación.
- Estado de carga.

### Archivo

`frontend/tests/ui/QuoteForm.ui.test.js`

### Comando

```bash
cd frontend
npm run test:ui
```

## 10. Snapshot tests

### Qué prueban

Detectan cambios estructurales inesperados en el HTML renderizado de:

- Formulario inicial.
- Formulario con error.
- Formulario en carga.
- Recibo vacío.
- Recibo con error.
- Recibo exitoso.

### Archivos

- `frontend/tests/snapshot/QuoteForm.snapshot.test.js`
- `frontend/tests/snapshot/QuoteReceipt.snapshot.test.js`
- `frontend/tests/snapshot/__snapshots__/`

### Comando

```bash
cd frontend
npm run test:snapshot
```

Si el cambio visual es intencional, actualizar snapshots explícitamente:

```bash
npx vitest run -u
```

No se deben actualizar snapshots para ocultar un cambio inesperado.

## 11. Stress tests del frontend

### Qué prueban

- Cinco mil validaciones repetidas de pesos válidos.
- Cinco mil validaciones repetidas de pesos inválidos.
- Consistencia del resultado.
- Ausencia de excepciones.

### Archivo

`frontend/tests/stress/quotationService.stress.test.js`

### Comando

```bash
cd frontend
npm run test:stress
```

## 12. UI E2E en navegador real

### Qué prueban

Playwright abre Chromium y ejecuta el flujo real:

```text
Chromium → Frontend Vue → API FastAPI → Recibo visible
```

Casos:

1. Cotización VIP EXPRESS exitosa y total `26.29 USD`.
2. Rechazo de peso `20.01 kg` sin generar cotización.
3. Backend no disponible y mensaje de conexión.

### Archivo

`frontend/tests/e2e/quotation.spec.js`

### Ejecución headless

```bash
cd frontend
npm run test:e2e
```

### Ejecución visible

Abre una ventana de Chromium:

```bash
npm run test:e2e -- --headed
```

### Modo interactivo

```bash
npx playwright test --ui
```

### Modo depuración

```bash
npx playwright test --debug
```

### Reporte HTML

```bash
npx playwright show-report
```

Playwright inicia automáticamente el backend en `127.0.0.1:8000` y el frontend en `127.0.0.1:5173` mediante `frontend/playwright.config.js`.

## 13. Suite completa

Frontend:

```bash
cd frontend
npm run test:all
npm run test:e2e
```

Backend:

```bash
cd backend
source .venv/bin/activate
pytest -q
pytest --cov=app --cov-branch --cov-report=term-missing
```

## 14. Resultados de referencia

| Suite | Resultado |
|---|---:|
| Backend unit tests | 58 passed |
| Backend integration tests | 25 passed |
| Backend stress tests | 1001 passed |
| Backend suite completa | 1084 passed |
| Cobertura backend | 98.79% |
| Frontend unit/UI/snapshot/stress | 29 passed |
| Frontend E2E Chromium | 3 passed |

## 15. Evidencias y estados

Cada ejecución debe registrar:

- Fecha y hora.
- Commit o versión.
- Sistema operativo.
- Versiones de Python y Node.
- Comando utilizado.
- Resultado.
- Capturas o reporte HTML cuando aplique.

Estados permitidos: `Passed`, `Failed`, `Blocked`, `Not Run`.
