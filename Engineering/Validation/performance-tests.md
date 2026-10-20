# Pruebas de rendimiento y carga

## Objetivo

Medir tiempos de respuesta, estabilidad y comportamiento concurrente.

## Indicadores

- Tiempo de respuesta de `/health`.
- Tiempo de respuesta del cálculo.
- Percentil 95.
- Solicitudes por segundo.
- Tasa de errores.
- Tiempo de carga del frontend.

## Criterios iniciales

- `/health`: p95 menor a 500 ms en ambiente local.
- Cálculo: p95 menor a 1 s en ambiente local.
- Sin errores en 100 solicitudes válidas concurrentes.
- El frontend debe construir correctamente con `npm run build`.

## Pruebas existentes relacionadas

```bash
cd backend
source .venv/bin/activate
pytest tests/stress -m stress -q
```

## Carga futura

Para una prueba de carga real se recomienda k6, Locust o JMeter; los resultados deben registrarse en `Engineering/Reports`.
