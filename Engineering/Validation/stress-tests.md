# Stress tests

## Objetivo

Comprobar estabilidad ante ejecuciones repetidas, sin cambios inesperados ni excepciones.

## Backend

Archivo: `backend/tests/stress/test_quotation_stress.py`.

Prueba mil ejecuciones de una cotización y 250 repeticiones de una matriz de pesos, clientes y envíos.

### Ambiente y comando

```bash
cd backend
source .venv/bin/activate
pytest tests/stress -m stress -q
```

### Resultado de referencia

`1001 passed`.

## Frontend

Archivo: `frontend/tests/stress/quotationService.stress.test.js`.

Prueba 5.000 validaciones válidas e inválidas repetidas.

### Ambiente y comando

```bash
cd frontend
npm install
npm run test:stress
```

## Criterio

No debe haber excepciones y una misma entrada debe producir siempre el mismo resultado.
