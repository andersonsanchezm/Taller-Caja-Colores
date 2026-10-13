# UC-08 — Cobertura de caja blanca del backend

## Valida

- QUOTE-REQ-002
- QUOTE-REQ-003
- QUOTE-REQ-004
- QUOTE-REQ-005
- QUOTE-REQ-006
- QUOTE-REQ-007
- API-REQ-001
- API-REQ-004
- API-REQ-006

## Tipo

Caja blanca y unit test.

## Rutas mínimas

- Validación finita, precisión, mínimo y máximo.
- Tramo ligero y pesado.
- Tres descuentos y dos recargos.
- Redondeo `ROUND_HALF_UP`.
- Excepciones y handlers `422`.
- Handler `/health`.

## Comando

```bash
cd backend
pytest --cov=app --cov-branch --cov-report=term-missing
```

## Criterio

Cobertura objetivo mínima: `85%`. Resultado: `Not Run`.
