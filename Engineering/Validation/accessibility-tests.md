# Pruebas de accesibilidad

## Objetivo

Verificar que el formulario y el recibo sean utilizables mediante teclado y tecnologías de asistencia.

## Casos

- Todos los controles son alcanzables con `Tab`.
- El foco es visible.
- El campo de peso tiene `label` asociado.
- Los errores usan `role="alert"`.
- El campo inválido expone `aria-invalid`.
- `aria-describedby` apunta al texto de ayuda y error.
- No existen elementos sin nombre accesible.
- El contraste de texto permite lectura.
- El contenido funciona en móvil y escritorio.

## Ejecución manual

```bash
cd frontend
npm run dev
```

Abrir `http://localhost:5173` y ejecutar los casos con teclado y lector de pantalla.

## Automatización futura

Agregar `@axe-core/playwright` y ejecutar una auditoría axe en cada página E2E.
