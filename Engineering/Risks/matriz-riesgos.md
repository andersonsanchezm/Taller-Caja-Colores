# Matriz de riesgos QA

| Riesgo | Probabilidad | Impacto | Prioridad | Mitigación |
|---|---:|---:|---:|---|
| Total calculado incorrectamente | Media | Alta | Alta | Unit, integración y valores límite |
| Backend no disponible | Media | Alta | Alta | E2E y recuperación |
| Error de redondeo | Media | Alta | Alta | Decimal, invariantes y casos frontera |
| CORS bloquea frontend | Baja | Alta | Media | Tests de integración y E2E |
| Cambio visual no detectado | Media | Media | Media | Snapshots y UI tests |
| Problema de accesibilidad | Media | Media | Media | axe, teclado y revisión manual |
| Degradación bajo carga | Baja | Alta | Media | Stress, concurrencia y rendimiento |
| Dependencia vulnerable | Media | Alta | Alta | `npm audit`, revisión de dependencias |
