import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import QuoteReceipt from '../../src/components/QuoteReceipt.vue'

const quote = {
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

describe('QuoteReceipt — snapshots', () => {
  it('mantiene el estado vacío', () => {
    expect(mount(QuoteReceipt).html()).toMatchSnapshot()
  })

  it('mantiene el estado de error', () => {
    expect(mount(QuoteReceipt, { props: { apiError: 'Backend no disponible' } }).html())
      .toMatchSnapshot()
  })

  it('mantiene el recibo exitoso', () => {
    expect(mount(QuoteReceipt, { props: { quote } }).html()).toMatchSnapshot()
  })
})
