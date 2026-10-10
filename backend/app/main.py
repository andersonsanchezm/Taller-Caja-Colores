"""Punto de entrada de la API FastExpress."""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.quotes import router as quotes_router
from app.core.config import get_cors_origins


app = FastAPI(
    title="FastExpress API",
    description="API para calcular cotizaciones de envios y descuentos.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request,
    error: RequestValidationError,
) -> JSONResponse:
    """Convierte los errores de Pydantic al contrato uniforme de la API."""

    first_error: dict[str, Any] = error.errors()[0]
    location = first_error.get("loc", ())
    field = location[-1] if location and isinstance(location[-1], str) else None

    code = "REQUEST_VALIDATION_ERROR"
    message = "La solicitud contiene datos invalidos."

    if field == "customer_type":
        code = "CUSTOMER_TYPE_INVALID"
        message = "El tipo de cliente debe ser NUEVO, FRECUENTE o VIP."
    elif field == "shipping_type":
        code = "SHIPPING_TYPE_INVALID"
        message = "El tipo de envio debe ser ESTANDAR o EXPRESS."
    elif field == "weight_kg":
        message = "El peso debe enviarse como un numero JSON."

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": {
                "code": code,
                "message": message,
                "field": field,
            }
        },
    )


app.include_router(quotes_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Confirma que la aplicacion esta disponible."""

    return {"status": "ok"}
