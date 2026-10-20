export const validQuoteResponse = {
  weight_kg: '5.01',
  customer_type: 'VIP',
  shipping_type: 'EXPRESS',
  base_rate: '5.00',
  rate_per_kg: '4.00',
  weight_charge: '20.04',
  subtotal: '25.04',
  discount_rate: '0.20',
  discount: '5.01',
  surcharge_rate: '0.25',
  surcharge: '6.26',
  total: '26.29',
  currency: 'USD'
}

export const validationErrorResponse = {
  detail: {
    code: 'WEIGHT_OUT_OF_RANGE',
    message: 'El peso debe estar entre 0.01 y 20.00 kg.',
    field: 'weight_kg'
  }
}

export function mockFetchResponse(body, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    statusText: status === 200 ? 'OK' : 'Error',
    json: async () => body
  }
}
