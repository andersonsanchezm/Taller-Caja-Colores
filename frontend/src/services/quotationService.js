/**
 * Módulo de validación de entradas de cotización para FastExpress.
 * 
 * Centraliza las validaciones de datos del formulario en el frontend,
 * garantizando que las entradas cumplan con los límites operativos antes
 * de comunicarse con la API de cotización.
 */

import { PRICING_RULES } from '../constants/pricingRules';

/**
 * Formatea un valor numérico a representación monetaria en USD con dos decimales.
 * 
 * @param {number|string} amount
 * @returns {string} Ejemplo: "$25.04 USD"
 */
export function formatMoney(amount) {
  const num = Number(amount);
  if (isNaN(num)) return '$0.00 USD';
  return `$${num.toFixed(2)} USD`;
}

/**
 * Valida minuciosamente el peso del paquete en el formulario antes de llamar a la API.
 * 
 * Reglas de validación:
 * 1. Campo no vacío ni indefinido: "El peso del paquete es obligatorio."
 * 2. Formato numérico decimal válido.
 * 3. Máximo 2 cifras decimales: "El peso no puede tener más de dos cifras decimales."
 * 4. Peso mayor a 0.00 kg: "El peso debe ser mayor a 0.00 kg"
 * 5. Peso hasta 20.00 kg. Si supera 20.00 kg se rechaza con la alerta:
 *    "Envío Rechazado: El peso excede el límite máximo permitido de 20.00 kg"
 * 
 * @param {string|number} rawValue
 * @returns {{ isValid: boolean, isRejected: boolean, message: string|null, weight: number|null }}
 */
export function validateWeightInput(rawValue) {
  if (rawValue === '' || rawValue === null || rawValue === undefined) {
    return {
      isValid: false,
      isRejected: false,
      message: 'El peso del paquete es obligatorio.',
      weight: null
    };
  }

  // Normalizar representación en string para verificar formato y decimales
  const strValue = String(rawValue).trim().replace(',', '.');

  // Validar formato numérico decimal
  if (!/^-?\d+(\.\d+)?$/.test(strValue)) {
    return {
      isValid: false,
      isRejected: false,
      message: 'Ingresa un valor numérico válido (ej. 4.50).',
      weight: null
    };
  }

  // Verificar cantidad de decimales (máximo 2 cifras permitidas)
  const dotIndex = strValue.indexOf('.');
  if (dotIndex !== -1) {
    const decimalPlaces = strValue.length - dotIndex - 1;
    if (decimalPlaces > 2) {
      return {
        isValid: false,
        isRejected: false,
        message: 'El peso no puede tener más de dos cifras decimales.',
        weight: null
      };
    }
  }

  const numValue = Number(strValue);

  if (!isFinite(numValue)) {
    return {
      isValid: false,
      isRejected: false,
      message: 'El peso debe ser un número finito válido.',
      weight: null
    };
  }

  // Validación: peso menor o igual a cero
  if (numValue <= 0) {
    return {
      isValid: false,
      isRejected: false,
      message: 'El peso debe ser mayor a 0.00 kg',
      weight: null
    };
  }

  // Validación: peso superior al límite máximo permitido (20.00 kg)
  if (numValue > PRICING_RULES.MAX_WEIGHT) {
    return {
      isValid: false,
      isRejected: true,
      message: 'Envío Rechazado: El peso excede el límite máximo permitido de 20.00 kg',
      weight: null
    };
  }

  // Valor válido dentro del rango (0.00, 20.00] kg
  return {
    isValid: true,
    isRejected: false,
    message: null,
    weight: numValue
  };
}
