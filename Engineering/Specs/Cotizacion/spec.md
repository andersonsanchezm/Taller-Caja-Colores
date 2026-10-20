# Especificación: Cotización de envíos

## Metadatos

Estado: Provisional  
Responsable: QA / Backend

## Propósito

Definir el cálculo observable de una cotización FastExpress.

## Alcance

Incluye peso, tarifas, descuentos, recargos, redondeo y desglose. No incluye autenticación, pagos ni persistencia.

## Requisitos

### QUOTE-REQ-001 — Tarifa base

Toda cotización válida incluye `5.00 USD` de tarifa base.

### QUOTE-REQ-002 — Rango de peso

Se aceptan pesos entre `0.01` y `20.00` kg inclusive.

### QUOTE-REQ-003 — Precisión del peso

El peso admite máximo dos cifras decimales.

### QUOTE-REQ-004 — Tarifa por peso

De `0.01` a `5.00` kg se aplica `2.00 USD/kg`; de `5.01` a `20.00` kg, `4.00 USD/kg`.

### QUOTE-REQ-005 — Descuento por cliente

`NUEVO` aplica 0%, `FRECUENTE` 10% y `VIP` 20% sobre el subtotal.

### QUOTE-REQ-006 — Recargo por envío

`ESTANDAR` aplica 0% y `EXPRESS` 25% sobre el subtotal.

### QUOTE-REQ-007 — Total

`subtotal = base + cargo`; `total = subtotal - descuento + recargo`.

### QUOTE-REQ-008 — Precisión monetaria

Los importes se redondean a dos decimales y se devuelven con dos cifras.

### QUOTE-REQ-009 — Rechazo seguro

Una entrada inválida no produce una cotización exitosa ni valores ficticios.

## Criterios de aceptación

### QUOTE-AC-001 — VIP EXPRESS

Dado `5.01 kg`, cliente `VIP` y envío `EXPRESS`, cuando se calcula, entonces el total es `26.29 USD`, con cargo `20.04`, descuento `5.01` y recargo `6.26`.

### QUOTE-AC-002 — Límites

`0.01` y `20.00` son válidos; `0.00` y `20.01` son inválidos.

### QUOTE-AC-003 — Cambio de tramo

`5.00` usa `2.00 USD/kg` y `5.01` usa `4.00 USD/kg`.

### QUOTE-AC-004 — Combinaciones

Las seis combinaciones de cliente y envío aplican sus porcentajes correspondientes.

## Preguntas abiertas

- Confirmar el significado del campo “Monto” del enunciado; no existe como entrada en la API actual.
