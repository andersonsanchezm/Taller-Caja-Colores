import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import QuoteForm from '../../src/components/QuoteForm.vue'

describe('QuoteForm — pruebas UI', () => {
  it('emite el peso escrito por el usuario', async () => {
    // Valida: UI-REQ-001, UI-AC-001
    const wrapper = mount(QuoteForm)
    const input = wrapper.get('#weight_input')

    await input.setValue('5.01')

    expect(wrapper.emitted('update:weight')).toEqual([['5.01']])
  })

  it('emite cliente, envío y submit', async () => {
    // Valida: UI-REQ-001, UI-REQ-003, UI-AC-002
    const wrapper = mount(QuoteForm)
    const buttons = wrapper.findAll('button')

    await buttons.find((button) => button.text().includes('VIP')).trigger('click')
    await buttons.find((button) => button.text().toUpperCase().includes('EXPRESS')).trigger('click')
    await wrapper.get('form').trigger('submit')

    expect(wrapper.emitted('update:customerType')).toEqual([['VIP']])
    expect(wrapper.emitted('update:shippingType')).toEqual([['EXPRESS']])
    expect(wrapper.emitted('submit')).toHaveLength(1)
  })

  it('muestra error y bloqueo de rechazo', () => {
    // Valida: UI-REQ-005, UI-AC-003
    const wrapper = mount(QuoteForm, {
      props: {
        validationError: 'Envío rechazado',
        isRejected: true
      }
    })

    expect(wrapper.get('[role="alert"]').text()).toContain('Envío Rechazado')
  })

  it('no permite submit ni reset mientras carga', async () => {
    const wrapper = mount(QuoteForm, { props: { isLoading: true } })

    await wrapper.get('form').trigger('submit')
    await wrapper.findAll('button').at(-1).trigger('click')

    expect(wrapper.emitted('submit')).toBeUndefined()
    expect(wrapper.emitted('reset')).toBeUndefined()
  })
})
