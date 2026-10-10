"""Endpoints HTTP relacionados con las cotizaciones."""

from dataclasses import asdict

from fastapi import APIRouter, HTTPException, status

from app.schemas.quote import ErrorResponse, QuoteRequest, QuoteResponse
from app.services.quotation import QuotationValidationError, calculate_quote


router = APIRouter(prefix="/api/v1/quotes", tags=["quotes"])


@router.post(
    "/calculate",
    response_model=QuoteResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponse}},
)
def calculate_quote_endpoint(payload: QuoteRequest) -> QuoteResponse:
    """Recibe los datos del envio y devuelve la cotizacion calculada."""

    try:
        result = calculate_quote(
            weight_kg=payload.weight_kg,
            customer_type=payload.customer_type,
            shipping_type=payload.shipping_type,
        )
    except QuotationValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                "code": error.code,
                "message": error.message,
                "field": error.field,
            },
        ) from error

    return QuoteResponse.model_validate(asdict(result))

