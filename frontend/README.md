# FastExpress - Módulo Frontend de Cotización de Envíos

Interfaz web moderna, limpia, accesible y responsive para el cálculo y cotización de envíos de paquetes de **FastExpress**, diseñada con rigor metodológico de **Calidad de Software**, validación de datos y **Análisis de Valores Límite (Boundary Value Analysis - BVA)**.

La aplicación se comunica de forma exclusiva con el endpoint REST oficial del backend para el cálculo de cotizaciones.

---

## 1. Stack Tecnológico

- **Vue 3:** Composition API (`<script setup>`) para gestión clara y reactiva del estado.
- **Vite 6:** Entorno de construcción ultrarrápido y servidor de desarrollo.
- **Tailwind CSS 3:** Estilos utilitarios, diseño responsive y paleta de colores corporativa.
- **PrimeVue 4 (Tema Aura):** Componentes visuales y tokens de diseño accesibles.

---

## 2. Estructura del Proyecto

```text
frontend/
├── dist/                          # Compilación optimizada para producción
├── src/
│   ├── assets/
│   │   └── main.css               # Estilos globales y directivas Tailwind
│   ├── constants/
│   │   └── pricingRules.js        # Parámetros y definiciones de clientes y envíos
│   ├── services/
│   │   ├── quotationService.js    # Funciones de validación de entradas en frontend (BVA)
│   │   └── apiService.js          # Cliente HTTP asíncrono hacia el endpoint oficial
│   ├── components/
│   │   ├── Header.vue             # Identidad y logotipo de FastExpress
│   │   ├── QuoteForm.vue          # Formulario accesible con validación visual y alertas
│   │   └── QuoteReceipt.vue       # Panel de resultados estilo recibo comercial y estado vacío
│   ├── App.vue                    # Vista principal tipo dashboard de 2 columnas
│   └── main.js                    # Punto de entrada y configuración de Vue/PrimeVue
├── index.html                     # Plantilla HTML base
├── package.json                   # Dependencias y scripts
├── postcss.config.js              # Configuración de PostCSS
├── tailwind.config.js             # Configuración de temas Tailwind
└── vite.config.js                 # Configuración de Vite
```

---

## 3. Integración con el Backend REST

Todas las cotizaciones se solicitan exclusivamente al endpoint oficial:

```http
POST http://127.0.0.1:8000/api/v1/quotes/calculate
Content-Type: application/json
Accept: application/json
```

### Contrato de Solicitud (JSON):
```json
{
  "weight_kg": 5.01,
  "customer_type": "VIP",
  "shipping_type": "EXPRESS"
}
```

### Comportamiento ante Respuestas:
- **200 OK:** Procesa y muestra el desglose comercial devuelto por el servidor (tarifa base, costo por peso con tramo, subtotal, descuento, recargo y total a pagar en USD).
- **422 Unprocessable Entity:** Extrae el mensaje de validación o rechazo de negocio devuelto por el backend. Si el peso supera 20.00 kg, despliega la alerta visual de rechazo.
- **400 Bad Request:** Muestra el error de solicitud devuelto por el servidor.
- **Error de conexión / Servidor no disponible:** Informa con claridad que no fue posible comunicarse con el servidor en `http://127.0.0.1:8000` sin generar cotizaciones ficticias ni alternar a modos simulados.

---

## 4. Validaciones del Formulario y Análisis de Valores Límite (BVA)

El formulario implementa comprobaciones inmediatas para asegurar una experiencia de usuario óptima:
- **Campo obligatorio y formato numérico:** Rechaza campos vacíos, texto o valores con más de dos cifras decimales.
- **Peso menor o igual a 0.00 kg:** Muestra el mensaje:
  > `"El peso debe ser mayor a 0.00 kg"`
- **Peso superior a 20.00 kg:** Muestra una alerta destacada con el mensaje exacto:
  > `"Envío Rechazado: El peso excede el límite máximo permitido de 20.00 kg"`
- **Límites operativos válidos:** Acepta valores en el intervalo `(0.00, 20.00] kg`, incluyendo los valores frontera `0.01 kg` y `20.00 kg`.

---

## 5. Comandos de Ejecución

Desde la carpeta `frontend/`:

### A. Iniciar en modo desarrollo
```bash
npm run dev
```
*(En Windows PowerShell, usar `npm.cmd run dev` o `cmd /c npm run dev`).*  
La aplicación estará disponible en [http://localhost:5173](http://localhost:5173).

### B. Construir para producción
```bash
npm run build
```
Genera los archivos estáticos en `dist/`.
