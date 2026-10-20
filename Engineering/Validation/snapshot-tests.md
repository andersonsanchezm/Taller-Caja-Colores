# Snapshot tests

## Objetivo

Detectar cambios estructurales inesperados en el HTML renderizado de los componentes.

## Ambiente

```bash
cd frontend
npm install
```

Los snapshots se ejecutan con Vitest, Vue Test Utils y JSDOM.

## Archivos

- `frontend/tests/snapshot/QuoteForm.snapshot.test.js`
- `frontend/tests/snapshot/QuoteReceipt.snapshot.test.js`
- `frontend/tests/snapshot/__snapshots__/`

## Estados cubiertos

- Formulario inicial.
- Formulario con error.
- Formulario en carga.
- Recibo vacío.
- Recibo con error.
- Recibo exitoso.

## Comando

```bash
npm run test:snapshot
```

Si el cambio visual es intencional:

```bash
npx vitest run -u
```

## Resultado de referencia

`6 passed`.
