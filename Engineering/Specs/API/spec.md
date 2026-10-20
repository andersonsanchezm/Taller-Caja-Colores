# Especificación: API

## Metadatos

Estado: Provisional  
Responsable: QA / Backend

## Requisitos

### API-REQ-001 — Salud

`GET /health` responde `200` con `{ "status": "ok" }`.

### API-REQ-002 — Cálculo

`POST /api/v1/quotes/calculate` recibe `weight_kg`, `customer_type` y `shipping_type`.

### API-REQ-003 — Valores permitidos

Los valores válidos son `NUEVO`, `FRECUENTE`, `VIP`, `ESTANDAR` y `EXPRESS`.

### API-REQ-004 — Contrato estricto

Se rechazan campos faltantes, tipos incorrectos y campos adicionales.

### API-REQ-005 — Respuesta exitosa

Una solicitud válida responde `200` con desglose completo y moneda `USD`; los decimales son strings.

### API-REQ-006 — Errores

Los errores responden `422` con `detail.code`, `detail.message` y `detail.field`.

### API-REQ-007 — CORS

Se permiten los orígenes locales configurados para el frontend.

## Criterios de aceptación

### API-AC-001 — Salud

Dado el backend activo, cuando se solicita `/health`, entonces responde `200` y `status=ok`.

### API-AC-002 — Solicitud válida

Dado un JSON válido, cuando se envía al endpoint, entonces responde `200` con todos los campos.

### API-AC-003 — Solicitud inválida

Dado un JSON inválido, cuando se envía, entonces responde `422` con el formato uniforme.
