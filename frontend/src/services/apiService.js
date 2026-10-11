/**
 * Servicio de comunicación con la API REST de FastExpress.
 * 
 * Gestiona de forma exclusiva las solicitudes de cotización mediante el
 * endpoint oficial http://127.0.0.1:8000/api/v1/quotes/calculate.
 */

// Endpoint oficial y exclusivo de cotización
export const API_ENDPOINT = 'http://127.0.0.1:8000/api/v1/quotes/calculate';

/**
 * Envía una solicitud de cotización al backend mediante HTTP POST.
 * 
 * Contrato de la API FastExpress:
 * - weight_kg: número decimal JSON.
 * - customer_type: "NUEVO", "FRECUENTE" o "VIP".
 * - shipping_type: "ESTANDAR" o "EXPRESS".
 * 
 * @param {Object} params
 * @param {number|string} params.weight_kg Peso del paquete en kg
 * @param {string} params.customer_type Tipo de cliente
 * @param {string} params.shipping_type Tipo de envío
 * @returns {Promise<{ success: boolean, data?: Object, error?: string, isRejected?: boolean, status?: number }>}
 */
export async function fetchQuoteFromApi({ weight_kg, customer_type, shipping_type }) {
  const payload = {
    weight_kg: Number(weight_kg),
    customer_type: String(customer_type).trim().toUpperCase(),
    shipping_type: String(shipping_type).trim().toUpperCase()
  };

  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    // 200 OK: Respuesta exitosa del servidor
    if (response.ok) {
      try {
        const data = await response.json();
        return {
          success: true,
          status: response.status,
          isRejected: false,
          error: null,
          data
        };
      } catch (parseError) {
        return {
          success: false,
          status: response.status,
          isRejected: false,
          error: 'Respuesta inesperada: El servidor devolvió una respuesta que no es JSON válido.',
          data: null
        };
      }
    }

    // Intentar leer el cuerpo de error en formato JSON
    let errorBody = null;
    try {
      errorBody = await response.json();
    } catch {
      errorBody = null;
    }

    // 422 Unprocessable Entity: Error de validación o regla de negocio
    if (response.status === 422) {
      let errorMessage = 'Los datos enviados no son procesables por el servidor.';
      let isRejected = false;

      if (errorBody?.detail) {
        // Estructura uniforme de FastExpress { detail: { code, message, field } }
        if (typeof errorBody.detail === 'object' && !Array.isArray(errorBody.detail)) {
          const detail = errorBody.detail;
          errorMessage = detail.message || errorMessage;
          if (detail.code === 'WEIGHT_OUT_OF_RANGE' && payload.weight_kg > 20.00) {
            errorMessage = 'Envío Rechazado: El peso excede el límite máximo permitido de 20.00 kg';
            isRejected = true;
          }
        } else if (Array.isArray(errorBody.detail)) {
          // Estructura por defecto de FastAPI/Pydantic [ { msg, loc } ]
          const firstErr = errorBody.detail[0];
          errorMessage = firstErr?.msg || errorMessage;
        } else if (typeof errorBody.detail === 'string') {
          errorMessage = errorBody.detail;
        }
      }

      return {
        success: false,
        status: 422,
        isRejected,
        error: errorMessage,
        data: null
      };
    }

    // 400 Bad Request: Error de solicitud
    if (response.status === 400) {
      const errorMessage = errorBody?.detail?.message
        || (typeof errorBody?.detail === 'string' ? errorBody.detail : null)
        || errorBody?.message
        || 'Solicitud incorrecta (400 Bad Request).';

      return {
        success: false,
        status: 400,
        isRejected: false,
        error: errorMessage,
        data: null
      };
    }

    // Otros errores HTTP (500, 502, 503, etc.)
    return {
      success: false,
      status: response.status,
      isRejected: false,
      error: `Error del servidor HTTP ${response.status}: ${response.statusText || 'Error del servicio'}`,
      data: null
    };

  } catch (networkError) {
    // Error de conexión o servidor no disponible
    return {
      success: false,
      status: 0,
      isRejected: false,
      error: 'No fue posible comunicarse con el servicio de cotización (http://127.0.0.1:8000). Verifica que el servidor backend esté en ejecución.',
      data: null
    };
  }
}
