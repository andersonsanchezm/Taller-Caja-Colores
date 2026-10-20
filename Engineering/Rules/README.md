# Reglas de Engineering y QA

1. Todo comportamiento verificable debe pertenecer a una especificación.
2. Todo requisito y criterio debe tener un ID estable.
3. `Specs` define qué debe hacer el sistema; `Validation` define cómo demostrarlo.
4. Las pruebas aportan evidencia; no redefinen el contrato.
5. Cada validación debe indicar los requisitos que comprueba.
6. Caja negra, caja blanca, unitarias, integración y E2E deben distinguirse.
7. `Blocked` significa que una precondición externa impidió ejecutar la prueba; un defecto reproducible es `Failed`.
