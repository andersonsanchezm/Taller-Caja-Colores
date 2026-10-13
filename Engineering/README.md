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
