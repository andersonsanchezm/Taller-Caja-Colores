# UC-07 — Errores del frontend

## Valida

- UI-REQ-002
- UI-REQ-005
- UI-REQ-006
- UI-AC-001
- UI-AC-003

## Tipo

Caja negra, integración y manual.

| ID | Acción | Esperado |
|---|---|---|
| FE-01 | Peso vacío | Mensaje obligatorio, sin API |
| FE-02 | Texto | Mensaje de formato, sin API |
| FE-03 | `1.234` | Mensaje de precisión |
| FE-04 | `0.00` | Mensaje de mínimo |
| FE-05 | `20.01` | Alerta de rechazo |
| FE-06 | Backend detenido | Error de conexión, sin recibo |
| FE-07 | Respuesta `422` | Mensaje de validación |
| FE-08 | Respuesta `400` | Mensaje de solicitud |
| FE-09 | Respuesta `500` | Error HTTP |

## Resultado

`Not Run`.
