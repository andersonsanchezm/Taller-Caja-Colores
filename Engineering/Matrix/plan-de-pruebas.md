# Plan de pruebas QA

## Objetivo

Demostrar que FastExpress cumple el contrato de cotización en backend, frontend y comunicación entre ambos.

## Niveles

- **Unit tests:** reglas aisladas de cotización y validadores.
- **Integración:** endpoints, serialización, errores y CORS.
- **Caja negra:** límites, equivalencias, combinaciones y errores observables.
- **Caja blanca:** ramas, decisiones, excepciones y cobertura.
- **E2E:** frontend → API → frontend.
- **Manual:** interfaz, accesibilidad básica y ausencia de datos ficticios.

## Cobertura objetivo

- Backend mínimo 85% de líneas y ramas, según `pyproject.toml`.
- 100% de combinaciones de cliente y envío.
- 100% de valores límite del peso.
- Todos los errores definidos de API y frontend.

## Técnicas

- Valores límite: `0.00`, `0.01`, `5.00`, `5.01`, `20.00`, `20.01`.
- Clases de equivalencia: válido, vacío, texto, booleano, precisión y rango.
- Tabla de decisión: 3 clientes × 2 envíos.
- Pruebas negativas: faltantes, adicionales, tipos inválidos y backend detenido.

## Comandos

```bash
cd backend
pytest -v
pytest --cov=app --cov-branch --cov-report=term-missing
```

```bash
cd frontend
npm run build
npm run dev
```

## Criterio de salida

Requisitos críticos cubiertos, valores límite ejecutados, cobertura mínima alcanzada, un E2E exitoso y uno de error ejecutados, y resultados registrados en la matriz.
