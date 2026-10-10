# Backend FastExpress

API REST escrita en Python con FastAPI para calcular cotizaciones de envios.

## Estado actual

El backend ya permite calcular cotizaciones mediante una API REST. Incluye:

- Reglas de tarifa base y cargo por peso.
- Descuentos para clientes `NUEVO`, `FRECUENTE` y `VIP`.
- Recargos para envios `ESTANDAR` y `EXPRESS`.
- Validacion de solicitudes y respuestas de error uniformes.
- Documentacion interactiva mediante Swagger.
- Configuracion CORS para conectar un frontend local.
- Endpoint de salud para comprobar la disponibilidad del servidor.

La primera version no utiliza base de datos porque el enunciado no exige almacenar las cotizaciones.

## Estructura

```text
backend/
|-- app/
|   |-- api/          Endpoints HTTP
|   |-- schemas/      Estructuras de entrada y salida
|   |-- services/     Reglas y calculos del negocio
|   `-- main.py       Punto de entrada de FastAPI
|-- tests/
|   |-- api/          Comprobaciones de endpoints
|   `-- unit/         Comprobaciones de funciones aisladas
|-- pyproject.toml    Dependencias y configuracion del proyecto
`-- README.md         Instrucciones y descripcion del backend
```

## Descargar el proyecto

En macOS, Linux o Windows, copia la URL HTTPS desde el boton `Code` del repositorio de GitHub y ejecuta:

```bash
git clone https://github.com/andersonsanchezm/Taller-Caja-Colores.git
cd Taller-Caja-Colores/backend
```

Si el repositorio ya se encuentra descargado, solo es necesario entrar en la carpeta `backend` antes de continuar.

## Preparar el entorno local en macOS o Linux

Desde la carpeta `backend`:

```bash
python3.12 --version
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Un entorno virtual aisla las dependencias de este proyecto para no mezclarlas con otros programas instalados en el equipo.

El proyecto requiere Python 3.11 o posterior. En el equipo donde se preparo inicialmente, el comando generico `python3` corresponde a Python 3.9, por lo que se debe seleccionar expresamente una instalacion mas reciente.

## Preparar el entorno local en Windows PowerShell

Desde la carpeta `backend`:

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si PowerShell bloquea temporalmente la activacion del entorno virtual, se puede habilitar solo para la terminal actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

En el simbolo del sistema tradicional de Windows, la activacion se realiza con:

```bat
.venv\Scripts\activate.bat
```

## Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

El mismo comando de Uvicorn se utiliza en macOS, Linux y Windows despues de activar el entorno virtual.

La aplicacion quedara disponible en:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Salud: `http://127.0.0.1:8000/health`

La opcion `--reload` reinicia el servidor automaticamente cuando cambia un archivo. Debe utilizarse durante el desarrollo, no en produccion.

## Probar una cotizacion

La forma mas sencilla es abrir `http://127.0.0.1:8000/docs`, seleccionar `POST /api/v1/quotes/calculate`, pulsar `Try it out`, escribir el JSON y pulsar `Execute`.

Tambien se puede utilizar otra terminal:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/quotes/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "weight_kg": 5.01,
    "customer_type": "VIP",
    "shipping_type": "EXPRESS"
  }'
```

El servidor se detiene con `Ctrl+C` en la terminal donde se esta ejecutando Uvicorn.

## Conectar un frontend local

El backend permite por defecto solicitudes provenientes de los puertos locales `3000` y `5173`, utilizados comunmente por herramientas de desarrollo frontend.

### Crear el archivo `.env` en macOS o Linux

Desde la carpeta `backend`:

```bash
cp .env.example .env
```

### Crear el archivo `.env` en Windows PowerShell

Desde la carpeta `backend`:

```powershell
Copy-Item .env.example .env
```

El archivo `.env.example` es una plantilla que si se comparte mediante Git. Cada integrante crea su propio `.env`, que permanece local y esta excluido por `.gitignore`.

Si el frontend utiliza otro puerto u origen, se modifica la variable dentro de `.env`:

```text
FASTEXPRESS_CORS_ORIGINS=http://localhost:5173
```

Para cargar ese archivo al iniciar el servidor:

```bash
uvicorn app.main:app --reload --env-file .env
```

Los distintos origenes se separan mediante comas. Un origen incluye el protocolo, el dominio y el puerto; por ejemplo, `http://localhost:5173`.

No se deben escribir contrasenas, tokens ni otros secretos en `.env.example`. Si en el futuro se agregan secretos al `.env`, solo se documentara el nombre de cada variable en la plantilla, dejando su valor vacio.

## Alternativa de instalacion editable

El archivo `pyproject.toml` tambien permite instalar el proyecto y sus dependencias de desarrollo en modo editable:

```bash
python -m pip install -e ".[dev]"
```

El modo editable resulta util durante el desarrollo porque los cambios del codigo se reflejan sin reinstalar el paquete. Para ejecutar la tarea, `requirements.txt` es la opcion mas directa.
