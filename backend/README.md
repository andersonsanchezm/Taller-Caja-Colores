# Backend FastExpress

API REST escrita en Python con FastAPI para calcular cotizaciones de envios.

## Estado actual

La estructura inicial esta creada y la aplicacion contiene unicamente un endpoint de salud. El algoritmo de cotizacion todavia no esta implementado.

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

## Preparar el entorno local en macOS o Linux

Desde la carpeta `backend`:

```bash
python3.12 --version
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
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
python -m pip install -e ".[dev]"
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

Si el frontend utiliza otro origen, se puede crear un archivo `.env` a partir de `.env.example`:

```bash
cp .env.example .env
```

Luego se ajusta la variable:

```text
FASTEXPRESS_CORS_ORIGINS=http://localhost:5173
```

Para cargar ese archivo al iniciar el servidor:

```bash
uvicorn app.main:app --reload --env-file .env
```

Los distintos origenes se separan mediante comas. Un origen incluye el protocolo, el dominio y el puerto; por ejemplo, `http://localhost:5173`.
