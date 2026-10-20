# Ingeniería y QA — FastExpress

Documentación del proyecto bajo **Specification-Driven Development (SDD)**. La especificación define el comportamiento esperado; las validaciones y pruebas aportan evidencia.

## Estructura

```text
Engineering/
├── Specs/          contratos funcionales
├── Validation/     procedimientos de QA
├── Rules/          reglas de trazabilidad
├── Templates/      plantillas
└── Matrix/         plan y matriz de pruebas
```

## Flujo SDD

```text
Especificación → Requisitos → Criterios de aceptación → Validación → Pruebas → Evidencia
```

Estados de especificación: `Borrador`, `Necesita decisión`, `Provisional`, `Aceptada`, `Rechazada`.

Resultados de validación: `Passed`, `Failed`, `Blocked`, `Not Run`.

## Documentos

- [Cotización](Specs/Cotizacion/spec.md)
- [API](Specs/API/spec.md)
- [Frontend](Specs/Frontend/spec.md)
- [Validaciones](Validation/README.md)
- [Matriz de trazabilidad](Matrix/matriz-trazabilidad.md)
- [Plan de pruebas](Matrix/plan-de-pruebas.md)

## QA complementario

- [Plan maestro de QA](QA/plan-qa.md)
- [Criterios de entrada y salida](QA/criterios-entrada-salida.md)
- [Métricas](QA/metricas.md)
- [Matriz de riesgos](Risks/matriz-riesgos.md)
- [Gestión de defectos](Defects/README.md)
- [Reportes](Reports/README.md)

## Ejecución centralizada

Los targets principales están en el [Makefile](../Makefile):

```bash
make setup
make test
make coverage
make frontend-e2e
```

## Pruebas UI

- UI de componentes: Vitest, Vue Test Utils y JSDOM.
- UI E2E: Playwright con navegador Chromium, frontend y backend reales.
