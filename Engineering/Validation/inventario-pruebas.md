# Inventario de pruebas QA

Este documento consolida todas las pruebas implementadas en FastExpress. Cada caso indica su categoría, archivo y comando de ejecución.

## Convenciones

- **Caja negra:** valida entradas, salidas y comportamiento observable.
- **Caja blanca:** valida rutas, condiciones, excepciones e invariantes internas.
- **Unit:** unidad aislada.
- **Integration:** contrato entre componentes o API.
- **UI:** componente Vue en DOM simulado.
- **Snapshot:** estructura renderizada.
- **Stress:** repetición y estabilidad.
- **E2E:** navegador real, frontend y backend.

## Caja negra — API e integración

Archivo principal: `backend/tests/integration/test_quotes_api.py`.

| ID | Caso | Tipo |
|---|---|---|
| BB-API-001 | `GET /health` responde `200` y `status=ok` | Integration |
| BB-API-002 | Cotización VIP EXPRESS válida | Integration |
| BB-API-003 | Peso fuera de rango | Integration |
| BB-API-004 | Peso con más de dos decimales | Integration |
| BB-API-005 | Cliente inválido | Integration |
| BB-API-006 | Envío inválido | Integration |
| BB-API-007 | Campo obligatorio faltante | Integration |
| BB-API-008 | Peso enviado como texto | Integration |
| BB-API-009 | Peso booleano | Integration |
| BB-API-010 | Campo adicional | Integration |
| BB-API-011 | Contrato uniforme de error | Integration |

Archivo adicional: `backend/tests/integration/test_contract_and_security.py`.

| ID | Caso | Tipo |
|---|---|---|
| BB-API-012 | Métodos HTTP no permitidos | Caja negra |
| BB-API-013 | Payload vacío o no objeto | Caja negra |
| BB-API-014 | Valores `null` | Caja negra |
| BB-API-015 | JSON mal formado | Caja negra |
| BB-API-016 | HTML o JavaScript en datos | Seguridad básica |
| BB-API-017 | Solicitudes concurrentes sin mezclar resultados | Concurrencia |
| BB-API-018 | Origen CORS no autorizado | Seguridad básica |

### Comando

```bash
cd backend
source .venv/bin/activate
pytest tests/integration -q
```

## Caja negra — frontend y navegador

### Unit orientadas a comportamiento

Archivo: `frontend/tests/unit/quotationService.test.js`.

| ID | Caso |
|---|---|
| BB-FE-001 | Peso vacío |
| BB-FE-002 | Texto no numérico |
| BB-FE-003 | Más de dos decimales |
| BB-FE-004 | Cero y negativos |
| BB-FE-005 | Peso superior a 20 kg |
| BB-FE-006 | Límites `0.01`, `5.00`, `5.01`, `20.00` |
| BB-FE-007 | Coma decimal |
| BB-FE-008 | Formateo monetario |

Archivo: `frontend/tests/unit/apiService.test.js`.

| ID | Caso |
|---|---|
| BB-FE-009 | Solicitud exitosa |
| BB-FE-010 | Error `422` |
| BB-FE-011 | Error `400` |
| BB-FE-012 | Error `500` |
| BB-FE-013 | JSON inválido |
| BB-FE-014 | Error de conexión |
| BB-FE-015 | No mostrar cotización ficticia |

### UI de componentes

Archivo: `frontend/tests/ui/QuoteForm.ui.test.js`.

| ID | Caso |
|---|---|
| BB-UI-001 | Emitir peso |
| BB-UI-002 | Seleccionar cliente |
| BB-UI-003 | Seleccionar envío |
| BB-UI-004 | Enviar formulario |
| BB-UI-005 | Mostrar error |
| BB-UI-006 | Bloquear acciones durante carga |

### Snapshots

Archivos: `frontend/tests/snapshot/`.

| ID | Estado |
|---|---|
| BB-SNAP-001 | Formulario inicial |
| BB-SNAP-002 | Formulario con error |
| BB-SNAP-003 | Formulario cargando |
| BB-SNAP-004 | Recibo vacío |
| BB-SNAP-005 | Recibo con error |
| BB-SNAP-006 | Recibo exitoso |

### E2E

Archivo: `frontend/tests/e2e/quotation.spec.js`.

| ID | Caso |
|---|---|
| BB-E2E-001 | Cotización VIP EXPRESS completa |
| BB-E2E-002 | Rechazo de peso superior al máximo |
| BB-E2E-003 | Backend no disponible |

### Comandos

```bash
cd frontend
npm run test:unit
npm run test:ui
npm run test:snapshot
npm run test:e2e
```

Para ver el navegador:

```bash
npm run test:e2e -- --headed
npx playwright test --ui
npx playwright test --debug
```

## Caja blanca — backend

### Lógica de negocio

Archivo: `backend/tests/unit/test_quotation.py`.

| ID | Camino interno |
|---|---|
| BW-QUOTE-001 | Tarifa ligera |
| BW-QUOTE-002 | Tarifa pesada |
| BW-QUOTE-003 | Mínimo válido |
| BW-QUOTE-004 | Máximo válido |
| BW-QUOTE-005 | Rechazo por rango |
| BW-QUOTE-006 | Rechazo por precisión |
| BW-QUOTE-007 | Descuento NUEVO |
| BW-QUOTE-008 | Descuento FRECUENTE |
| BW-QUOTE-009 | Descuento VIP |
| BW-QUOTE-010 | Recargo ESTANDAR |
| BW-QUOTE-011 | Recargo EXPRESS |
| BW-QUOTE-012 | Subtotal y total |
| BW-QUOTE-013 | Redondeo monetario |
| BW-QUOTE-014 | Peso `NaN` o infinito |

### Invariantes y errores

Archivos:

- `backend/tests/unit/test_quotation_properties.py`
- `backend/tests/unit/test_error_paths.py`

| ID | Camino interno |
|---|---|
| BW-DOM-001 | Total no negativo |
| BW-DOM-002 | Subtotal mayor o igual a base |
| BW-DOM-003 | Descuento no negativo |
| BW-DOM-004 | Recargo no negativo |
| BW-DOM-005 | Importes con dos decimales |
| BW-ERR-001 | Rechazo de string |
| BW-ERR-002 | Rechazo de booleano |
| BW-ERR-003 | Rechazo de `null` |
| BW-ERR-004 | Código, mensaje y campo de excepción |

### Stress interno

Archivo: `backend/tests/stress/test_quotation_stress.py`.

| ID | Camino interno |
|---|---|
| BW-STRESS-001 | 1.000 cálculos repetidos |
| BW-STRESS-002 | Matriz comercial repetida |
| BW-STRESS-003 | Resultados finitos y estables |

### Comandos

```bash
cd backend
source .venv/bin/activate
pytest tests/unit -q
pytest tests/stress -m stress -q
pytest --cov=app --cov-branch --cov-report=term-missing
```

## Caja blanca — frontend

Archivo: `frontend/tests/stress/quotationService.stress.test.js`.

| ID | Camino interno |
|---|---|
| BW-FE-001 | 5.000 validaciones válidas |
| BW-FE-002 | 5.000 validaciones inválidas |
| BW-FE-003 | Resultado consistente |
| BW-FE-004 | Sin excepciones |

## Pruebas complementarias

| Área | Documento |
|---|---|
| Accesibilidad | `Engineering/Validation/accessibility-tests.md` |
| Rendimiento | `Engineering/Validation/performance-tests.md` |
| Recuperación | `Engineering/Validation/recovery-tests.md` |
| Compatibilidad | `Engineering/Validation/compatibility-tests.md` |
| Mutación | `Engineering/Validation/white-box/uc-09-mutacion.md` |

## Resultados de referencia

| Suite | Resultado |
|---|---:|
| Backend unit | 58 passed |
| Backend integration | 25 passed |
| Backend stress | 1001 passed |
| Backend total | 1084 passed |
| Cobertura backend | 98.79% |
| Frontend Vitest | 29 passed |
| Frontend E2E | 3 passed |
