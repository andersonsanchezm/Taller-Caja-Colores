# Especificacion del backend FastExpress

## Objetivo

El backend debe recibir los datos de una solicitud de cotizacion, validar que sean correctos, aplicar las reglas de negocio BR-01 a BR-04 y devolver el desglose del precio del envio.

Esta especificacion traduce el enunciado del proyecto a decisiones tecnicas verificables. Las decisiones que no aparecen expresamente en el documento original se identifican como supuestos del equipo.

## Entradas de la cotizacion

| Campo | Tipo conceptual | Valores permitidos | Motivo |
|---|---|---|---|
| `weight_kg` | Numero decimal | De `0.01` a `20.00` | Determina el cargo por peso |
| `customer_type` | Categoria | `NUEVO`, `FRECUENTE`, `VIP` | Determina el descuento |
| `shipping_type` | Categoria | `ESTANDAR`, `EXPRESS` | Determina el recargo |

Los nombres tecnicos estan escritos en ingles para mantener una convencion comun en el codigo. La documentacion visible para el usuario puede permanecer en espanol.

## Salidas de la cotizacion

| Campo | Significado |
|---|---|
| `base_rate` | Tarifa fija de toda orden |
| `weight_charge` | Resultado de multiplicar el peso por la tarifa aplicable |
| `subtotal` | Suma de la tarifa base y el cargo por peso |
| `discount` | Valor monetario descontado segun el tipo de cliente |
| `surcharge` | Valor monetario agregado segun el tipo de envio |
| `total` | Precio final de la cotizacion |

## Contrato JSON de la API

El frontend enviara una solicitud HTTP `POST` al endpoint:

```text
/api/v1/quotes/calculate
```

`POST` significa que el cliente envia datos al backend para que este los procese. Un endpoint es una direccion concreta de la API que realiza una operacion.

### JSON de entrada

```json
{
  "weight_kg": 5.01,
  "customer_type": "VIP",
  "shipping_type": "EXPRESS"
}
```

Significado de cada propiedad:

- `weight_kg`: peso del envio expresado en kilogramos.
- `customer_type`: categoria utilizada para elegir el descuento.
- `shipping_type`: categoria utilizada para elegir el recargo.

Los nombres y valores de las categorias deben coincidir con el contrato. En una primera version, `VIP` sera valido y `vip` sera rechazado. Esto evita aceptar variantes de forma silenciosa.

### JSON de respuesta correcta

Para la solicitud anterior, el backend respondera con el codigo HTTP `200 OK` y el siguiente cuerpo:

```json
{
  "weight_kg": "5.01",
  "customer_type": "VIP",
  "shipping_type": "EXPRESS",
  "base_rate": "5.00",
  "rate_per_kg": "4.00",
  "weight_charge": "20.04",
  "subtotal": "25.04",
  "discount_rate": "0.20",
  "discount": "5.01",
  "surcharge_rate": "0.25",
  "surcharge": "6.26",
  "total": "26.29",
  "currency": "USD"
}
```

Los valores decimales de la respuesta se enviaran como cadenas de texto. Por ejemplo, se utilizara `"5.00"` en lugar de `5.0`. Esto conserva de forma explicita los dos decimales y evita que una conversion binaria altere un valor monetario.

El frontend podra mostrar estos valores directamente o convertirlos de forma controlada si necesita realizar otra operacion.

### JSON de error de negocio

Si el peso es `20.01`, el backend respondera con el codigo HTTP `422 Unprocessable Entity`:

```json
{
  "detail": {
    "code": "WEIGHT_OUT_OF_RANGE",
    "message": "El peso debe estar entre 0.01 y 20.00 kg.",
    "field": "weight_kg"
  }
}
```

El codigo HTTP `422` indica que la solicitud tiene una estructura reconocible, pero alguno de sus datos no satisface las reglas del sistema.

El objeto de error contiene:

- `code`: identificador estable que el frontend puede reconocer.
- `message`: explicacion legible para una persona.
- `field`: propiedad de la solicitud que produjo el error.

### Errores que debe contemplar el contrato

| Codigo interno | Situacion |
|---|---|
| `WEIGHT_OUT_OF_RANGE` | Peso menor que 0.01 o mayor que 20.00 |
| `WEIGHT_PRECISION_INVALID` | Peso con mas de dos cifras decimales |
| `CUSTOMER_TYPE_INVALID` | Tipo de cliente desconocido |
| `SHIPPING_TYPE_INVALID` | Tipo de envio desconocido |
| `REQUEST_VALIDATION_ERROR` | Campo ausente o con un tipo de dato incorrecto |

Los errores conservaran una estructura uniforme para que el frontend no necesite interpretar formatos diferentes.

## Reglas de calculo

### Tarifa base

```text
base_rate = 5.00 USD
```

Toda cotizacion valida comienza con una tarifa fija de 5.00 USD.

### Cargo por peso

```text
Si 0.01 <= peso <= 5.00:
    tarifa_por_kg = 2.00

Si 5.01 <= peso <= 20.00:
    tarifa_por_kg = 4.00

Si peso > 20.00:
    rechazar la cotizacion
```

El cargo se obtiene con esta formula:

```text
weight_charge = weight_kg * rate_per_kg
```

### Subtotal

```text
subtotal = base_rate + weight_charge
```

El subtotal es el valor de la cotizacion antes de aplicar descuentos y recargos.

### Descuento

| Tipo de cliente | Porcentaje |
|---|---:|
| `NUEVO` | 0 % |
| `FRECUENTE` | 10 % |
| `VIP` | 20 % |

```text
discount = subtotal * discount_rate
```

### Recargo

| Tipo de envio | Porcentaje |
|---|---:|
| `ESTANDAR` | 0 % |
| `EXPRESS` | 25 % |

```text
surcharge = subtotal * surcharge_rate
```

### Total

```text
total = subtotal - discount + surcharge
```

El descuento y el recargo se calculan sobre el mismo subtotal. Esta es una interpretacion del equipo porque el enunciado no especifica completamente el orden de las operaciones.

## Validaciones del backend

El backend debe rechazar una solicitud cuando ocurra cualquiera de estas situaciones:

- El peso es menor que `0.01` kg.
- El peso es mayor que `20.00` kg.
- El peso contiene mas de dos cifras decimales.
- El peso no es un numero decimal valido.
- El tipo de cliente no pertenece a las categorias permitidas.
- El tipo de envio no pertenece a las categorias permitidas.
- Falta uno de los campos obligatorios.

Validar significa comprobar los datos antes de ejecutar el calculo. Esto evita resultados incorrectos y permite devolver un error comprensible al frontend.

## Precision numerica

Los pesos, tarifas y resultados monetarios se representaran con `Decimal` en Python.

`Decimal` se utilizara porque los numeros binarios de punto flotante, representados normalmente mediante `float`, pueden introducir pequenas diferencias en operaciones monetarias. Los importes se redondearan a dos decimales mediante una regla explicita.

## Limites relevantes

| Peso | Resultado esperado |
|---:|---|
| `0.00` | Invalido |
| `0.01` | Valido a 2.00 USD por kg |
| `5.00` | Valido a 2.00 USD por kg |
| `5.01` | Valido a 4.00 USD por kg |
| `20.00` | Valido a 4.00 USD por kg |
| `20.01` | Rechazado por exceder el limite |

Estos valores son importantes porque se encuentran justo en los puntos donde cambia el comportamiento del algoritmo.

## Decision sobre la base de datos

La primera version del backend no utilizara base de datos. El calculo de una cotizacion es una operacion que recibe datos y devuelve un resultado, sin que el enunciado exija guardar historiales.

Esta decision mantiene el algoritmo independiente y facilita su revision. Si el equipo decide almacenar cotizaciones posteriormente, la persistencia se agregara como una capa separada sin modificar las reglas de calculo.

## Decision sobre el campo Monto

El enunciado solicita pruebas para un campo llamado `Monto`, pero no lo define como dato de entrada. En esta especificacion se interpreta provisionalmente como el total calculado de la cotizacion y no como una entrada de la API.

Esta interpretacion debe confirmarse con el profesor. Si `Monto` representa otra cosa, la especificacion y las pruebas tendran que actualizarse.

## Separacion de responsabilidades del codigo

El backend se dividira conceptualmente en dos partes:

1. Logica de negocio: contiene exclusivamente las reglas y formulas de la cotizacion.
2. API REST: recibe solicitudes HTTP, valida su estructura, llama a la logica de negocio y devuelve una respuesta JSON.

Esta separacion permite entender y comprobar el algoritmo sin depender del servidor web.

## Criterios de aceptacion del backend

- Implementa las reglas BR-01, BR-02, BR-03 y BR-04.
- Rechaza datos fuera del dominio permitido.
- Devuelve un desglose comprensible del calculo.
- Mantiene la logica de negocio separada de FastAPI.
- Utiliza aritmetica decimal para los valores monetarios.
- Expone posteriormente un endpoint REST documentado.
- Puede ser probado por QA sin requerir una interfaz grafica ni una base de datos remota.
