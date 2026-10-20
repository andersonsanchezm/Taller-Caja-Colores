# UI E2E en navegador real

## Objetivo

Validar el flujo completo con Chromium, frontend real y backend real.

## Ambiente

```bash
cd frontend
npm install
npx playwright install chromium
```

Playwright inicia automáticamente:

- Backend: `http://127.0.0.1:8000`.
- Frontend: `http://127.0.0.1:5173`.

La configuración está en `frontend/playwright.config.js`.

## Archivo

`frontend/tests/e2e/quotation.spec.js`

## Casos

1. Cotización VIP EXPRESS con total `26.29 USD`.
2. Rechazo de peso `20.01 kg`.
3. Backend no disponible.

## Comandos

Ejecución headless:

```bash
npm run test:e2e
```

Ejecución visible:

```bash
npm run test:e2e -- --headed
```

Modo interactivo:

```bash
npx playwright test --ui
```

Modo debug:

```bash
npx playwright test --debug
```

Reporte HTML:

```bash
npx playwright show-report
```

## Resultado de referencia

`3 passed`.
