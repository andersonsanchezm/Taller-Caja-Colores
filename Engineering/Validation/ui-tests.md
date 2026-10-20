# UI tests de componentes

## Objetivo

Validar componentes Vue aislados usando DOM simulado. Estos tests no abren Chrome.

## Ambiente

```bash
cd frontend
npm install
```

Herramientas: Vitest, Vue Test Utils y JSDOM.

## Archivo

`frontend/tests/ui/QuoteForm.ui.test.js`

## Cobertura

- Entrada del peso.
- Eventos emitidos.
- Selección de cliente.
- Selección de envío.
- Submit del formulario.
- Mensajes de error.
- Estado de carga.

## Comando

```bash
npm run test:ui
```

## Resultado de referencia

`4 passed`.
