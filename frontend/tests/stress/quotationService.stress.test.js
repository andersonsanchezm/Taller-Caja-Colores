import { describe, expect, it } from 'vitest'

import { validateWeightInput } from '../../src/services/quotationService'

describe('validación — stress', () => {
  it('procesa repetidamente entradas válidas sin cambiar el resultado', () => {
    // Valida: UI-REQ-002
    for (let index = 0; index < 5000; index += 1) {
      expect(validateWeightInput('5.01')).toMatchObject({
        isValid: true,
        weight: 5.01
      })
    }
  })

  it('procesa repetidamente entradas inválidas sin producir excepciones', () => {
    for (let index = 0; index < 5000; index += 1) {
      expect(validateWeightInput('20.01').isRejected).toBe(true)
      expect(validateWeightInput('1.234').isValid).toBe(false)
    }
  })
})
