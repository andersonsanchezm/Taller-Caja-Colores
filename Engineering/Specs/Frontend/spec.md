# Especificación: Frontend

## Metadatos

Estado: Provisional  
Responsable: QA / Frontend

## Requisitos

### UI-REQ-001 — Formulario

Permite ingresar peso, cliente y modalidad.

### UI-REQ-002 — Validación local

Valida vacío, formato, precisión y rango antes de llamar a la API.

### UI-REQ-003 — Solicitud

Envía los datos válidos como `POST` al endpoint oficial.

### UI-REQ-004 — Resultado

Una respuesta `200` se muestra como recibo con su desglose.

### UI-REQ-005 — Errores

Diferencia errores `422`, `400`, HTTP y conexión.

### UI-REQ-006 — Sin datos ficticios

Una respuesta fallida nunca se presenta como cotización válida.

## Criterios de aceptación

### UI-AC-001 — Validación

Dado un dato inválido, cuando se calcula, entonces se muestra el mensaje y no se llama a la API.

### UI-AC-002 — Éxito

Dado un formulario válido y backend disponible, entonces se muestra el recibo correcto.

### UI-AC-003 — Conexión

Dado un backend detenido, entonces se muestra error sin resultado ficticio.
