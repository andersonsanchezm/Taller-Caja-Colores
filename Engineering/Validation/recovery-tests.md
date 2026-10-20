# Pruebas de recuperación

## Casos

1. Detener el backend y enviar una cotización válida.
2. Confirmar mensaje de conexión y ausencia de recibo ficticio.
3. Reiniciar el backend.
4. Repetir la cotización.
5. Confirmar que el flujo vuelve a funcionar.
6. Simular respuesta `500`, respuesta no JSON y timeout.
7. Confirmar que el formulario puede reiniciarse después del error.

## Resultado esperado

El frontend informa el error, limpia el resultado inválido y permite una nueva operación cuando el servicio se recupera.

## Ejecución E2E

```bash
cd frontend
npm run test:e2e
```
