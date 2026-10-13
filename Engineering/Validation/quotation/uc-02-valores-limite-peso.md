# UC-02 — Valores límite del peso

## Valida

- QUOTE-REQ-002
- QUOTE-REQ-003
- QUOTE-REQ-004
- QUOTE-AC-002
- QUOTE-AC-003

## Tipo

Caja negra y caja blanca.

| ID | Peso | Resultado esperado |
|---|---:|---|
| WL-01 | `-0.01` | Rechazado |
| WL-02 | `0.00` | Rechazado |
| WL-03 | `0.01` | Válido, tarifa 2.00 |
| WL-04 | `5.00` | Válido, tarifa 2.00 |
| WL-05 | `5.01` | Válido, tarifa 4.00 |
| WL-06 | `20.00` | Válido |
| WL-07 | `20.01` | Rechazado |
| WL-08 | `1.234` | Rechazado por precisión |

## Procedimiento

Ejecutar cada dato contra la API y repetirlo contra `calculate_quote()`.

## Resultado

`Not Run`.
