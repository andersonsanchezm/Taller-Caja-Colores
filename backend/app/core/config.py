"""Configuracion del backend obtenida desde variables de entorno."""

import os


DEFAULT_CORS_ORIGINS = (
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
)


def get_cors_origins() -> list[str]:
    """Devuelve los origenes autorizados para llamar a la API."""

    configured_origins = os.getenv("FASTEXPRESS_CORS_ORIGINS")

    if configured_origins is None:
        return list(DEFAULT_CORS_ORIGINS)

    return [
        origin.strip()
        for origin in configured_origins.split(",")
        if origin.strip()
    ]

