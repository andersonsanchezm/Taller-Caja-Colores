# UC-09 — Detección de mutaciones

## Valida

- QUOTE-REQ-002
- QUOTE-REQ-004
- QUOTE-REQ-005
- QUOTE-REQ-006
- QUOTE-REQ-007

## Objetivo

Comprobar que la suite falla cuando se altera intencionalmente una regla crítica.

## Mutaciones sugeridas

1. Cambiar `5.00` por `5.01` en el límite de tarifa.
2. Cambiar `4.00` por `2.00` en el tramo pesado.
3. Cambiar el descuento VIP de `0.20` a `0.10`.
4. Cambiar el recargo EXPRESS de `0.25` a `0.00`.
5. Cambiar `total = subtotal - discount + surcharge` por suma del descuento.
6. Eliminar el rechazo de pesos mayores a `20.00`.

## Resultado esperado

Cada mutación debe ser detectada por al menos un test. Una mutación que sobreviva indica una brecha en la cobertura.

## Procedimiento

Ejecutar las pruebas después de cada cambio temporal y restaurar el código antes de confirmar cambios. La mutación no es un cambio funcional permanente.
