import { afterEach, describe, expect, it, vi } from 'vitest';

import { fetchQuoteFromApi } from '../../src/services/apiService';
import { validQuoteResponse } from '../../../Testing/frontend/apiMocks.js';

afterEach(() => {
  vi.restoreAllMocks();
});

describe('fetchQuoteFromApi', () => {
  it('envía una solicitud válida y devuelve la cotización', async () => {
    // Valida: UI-REQ-003, UI-REQ-004, UI-AC-002
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: vi.fn().mockResolvedValue(validQuoteResponse)
    }));

    const result = await fetchQuoteFromApi({
      weight_kg: '5.01',
      customer_type: 'vip',
      shipping_type: 'express'
    });

    expect(result).toMatchObject({
      success: true,
      status: 200,
      isRejected: false,
      data: { total: '26.29', currency: 'USD' }
    });
    expect(fetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          weight_kg: 5.01,
          customer_type: 'VIP',
          shipping_type: 'EXPRESS'
        })
      })
    );
  });

  it('transforma un rechazo 422 de peso en alerta de negocio', async () => {
    // Valida: UI-REQ-005, UI-AC-003
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      status: 422,
      json: vi.fn().mockResolvedValue({
        detail: {
          code: 'WEIGHT_OUT_OF_RANGE',
          message: 'Fuera de rango',
          field: 'weight_kg'
        }
      })
    }));

    const result = await fetchQuoteFromApi({
      weight_kg: 20.01,
      customer_type: 'VIP',
      shipping_type: 'EXPRESS'
    });

    expect(result.success).toBe(false);
    expect(result.isRejected).toBe(true);
    expect(result.error).toContain('Envío Rechazado');
  });

  it('maneja la caída del backend sin crear una cotización', async () => {
    // Valida: UI-REQ-006, UI-AC-003
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('offline')));

    const result = await fetchQuoteFromApi({
      weight_kg: 1,
      customer_type: 'VIP',
      shipping_type: 'EXPRESS'
    });

    expect(result).toMatchObject({
      success: false,
      status: 0,
      isRejected: false,
      data: null
    });
    expect(result.error).toContain('No fue posible comunicarse');
  });

  it('maneja respuestas 400 y 500 sin crear una cotización', async () => {
    // Valida: UI-REQ-005, UI-REQ-006
    vi.stubGlobal('fetch', vi.fn()
      .mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: vi.fn().mockResolvedValue({ detail: { message: 'Solicitud inválida' } })
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: vi.fn().mockRejectedValue(new Error('not json'))
      }));

    const params = { weight_kg: 1, customer_type: 'VIP', shipping_type: 'EXPRESS' };
    const badRequest = await fetchQuoteFromApi(params);
    const serverError = await fetchQuoteFromApi(params);

    expect(badRequest).toMatchObject({ success: false, status: 400, data: null });
    expect(serverError).toMatchObject({ success: false, status: 500, data: null });
  });

  it('maneja una respuesta exitosa que no contiene JSON', async () => {
    // Valida: UI-REQ-005, UI-REQ-006
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: vi.fn().mockRejectedValue(new Error('invalid json'))
    }));

    const result = await fetchQuoteFromApi({
      weight_kg: 1,
      customer_type: 'VIP',
      shipping_type: 'EXPRESS'
    });

    expect(result).toMatchObject({ success: false, status: 200, data: null });
    expect(result.error).toContain('JSON válido');
  });
});
