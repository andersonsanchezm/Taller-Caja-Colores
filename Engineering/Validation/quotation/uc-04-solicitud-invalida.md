# UC-04 — Solicitud inválida

## Valida

- QUOTE-REQ-002
- QUOTE-REQ-003
- QUOTE-REQ-009
- API-REQ-003
- API-REQ-004
- API-REQ-006

## Tipo

Caja negra e integración.

| ID | Entrada | Esperado |
|---|---|---|
| INV-01 | Falta `weight_kg` | `422` |
| INV-02 | Peso texto | `422` |
| INV-03 | Peso booleano | `422` |
| INV-04 | Cliente `vip` | `422` |
| INV-05 | Envío `express` | `422` |
| INV-06 | Campo adicional | `422` |
| INV-07 | Peso `1.234` | `422` |
| INV-08 | Peso `20.01` | `422` |

## Resultado esperado

No debe existir respuesta `200`; `detail` contiene `code`, `message` y `field` cuando corresponda.

## Resultado

`Not Run`.
