import { describe, expect, it } from 'vitest';

import { formatMoney, validateWeightInput } from '../../src/services/quotationService';

describe('validateWeightInput', () => {
  it('rechaza un valor vacío', () => {
    // Valida: UI-REQ-002, UI-AC-001
    expect(validateWeightInput('')).toMatchObject({
      isValid: false,
      isRejected: false,
      message: 'El peso del paquete es obligatorio.'
    });
  });

  it('rechaza texto y más de dos decimales', () => {
    // Valida: UI-REQ-002, UI-AC-001
    expect(validateWeightInput('abc').isValid).toBe(false);
    expect(validateWeightInput('1.234').message).toBe(
      'El peso no puede tener más de dos cifras decimales.'
    );
  });

  it.each([
    ['0.00', 'El peso debe ser mayor a 0.00 kg'],
    ['-1.00', 'El peso debe ser mayor a 0.00 kg']
  ])('rechaza el peso %s', (weight, message) => {
    expect(validateWeightInput(weight)).toMatchObject({
      isValid: false,
      message
    });
  });

  it('rechaza pesos superiores a 20 kg', () => {
    // Valida: UI-AC-003
    const result = validateWeightInput('20.01');

    expect(result.isValid).toBe(false);
    expect(result.isRejected).toBe(true);
    expect(result.message).toContain('20.00 kg');
  });

  it.each(['0.01', '5.00', '5.01', '20.00'])('acepta el límite %s', (weight) => {
    expect(validateWeightInput(weight)).toMatchObject({
      isValid: true,
      isRejected: false,
      weight: Number(weight)
    });
  });

  it('acepta coma decimal', () => {
    expect(validateWeightInput('1,50')).toMatchObject({
      isValid: true,
      weight: 1.5
    });
  });
});

describe('formatMoney', () => {
  it('formatea importes con dos decimales', () => {
    expect(formatMoney('26.29')).toBe('$26.29 USD');
    expect(formatMoney(5)).toBe('$5.00 USD');
  });

  it('usa cero para importes no numéricos', () => {
    expect(formatMoney('no válido')).toBe('$0.00 USD');
  });
});
