# Métricas QA

## Métricas obligatorias

| Métrica | Fórmula o fuente |
|---|---|
| Cobertura de requisitos | Requisitos validados / requisitos totales × 100 |
| Cobertura de código | Reporte pytest-cov |
| Tasa de aprobación | Tests Passed / tests ejecutados × 100 |
| Tasa de bloqueo | Tests Blocked / tests planificados × 100 |
| Defectos por severidad | Conteo del registro de defectos |
| Defectos reabiertos | Defectos reabiertos / defectos cerrados |
| Automatización | Tests automatizados / tests totales × 100 |
| Tiempo de ejecución | Duración de CI y suites locales |

## Reglas

- No contar `Not Run` como aprobado.
- Un snapshot actualizado sin revisión no cuenta como evidencia.
- Un defecto reproducible es `Failed`, no `Blocked`.
- Las métricas deben indicar commit y fecha.
