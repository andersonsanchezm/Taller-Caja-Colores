import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import QuoteForm from '../../src/components/QuoteForm.vue'

describe('QuoteForm — snapshots', () => {
  it('mantiene el formulario inicial', () => {
    expect(mount(QuoteForm).html()).toMatchSnapshot()
  })

  it('mantiene el formulario con error de validación', () => {
    expect(mount(QuoteForm, {
      props: { validationError: 'El peso debe ser mayor a 0.00 kg' }
    }).html()).toMatchSnapshot()
  })

  it('mantiene el formulario en carga', () => {
    expect(mount(QuoteForm, { props: { isLoading: true } }).html()).toMatchSnapshot()
  })
})
