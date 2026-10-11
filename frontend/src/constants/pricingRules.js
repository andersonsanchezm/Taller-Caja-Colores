/**
 * Parámetros y definiciones de negocio de FastExpress
 * 
 * Reglas de negocio identificadas en la especificación técnica (BR-01 a BR-04):
 * - BR-01: Tarifa base fija de 5.00 USD.
 * - BR-02: Límites de peso y tramos tarifarios (ligero hasta 5.00 kg, pesado hasta 20.00 kg).
 * - BR-03: Categorías de clientes y porcentajes de descuento.
 * - BR-04: Modalidades de envío y recargos asociados.
 */

export const PRICING_RULES = {
  BASE_RATE: 5.00,
  MIN_WEIGHT: 0.01,
  LIGHT_WEIGHT_LIMIT: 5.00,
  MAX_WEIGHT: 20.00,
  LIGHT_RATE_PER_KG: 2.00,
  HEAVY_RATE_PER_KG: 4.00,
  CURRENCY: 'USD'
};

/**
 * BR-03: Categorías de clientes para selección y presentación en interfaz
 */
export const CUSTOMER_TYPES = {
  NUEVO: {
    id: 'NUEVO',
    label: 'Nuevo',
    discountRate: 0.00,
    discountPercentText: '0 %',
    badgeText: 'Sin descuento',
    description: 'Cliente primerizo o esporádico'
  },
  FRECUENTE: {
    id: 'FRECUENTE',
    label: 'Frecuente',
    discountRate: 0.10,
    discountPercentText: '10 %',
    badgeText: '10% de ahorro',
    description: 'Envíos regulares'
  },
  VIP: {
    id: 'VIP',
    label: 'VIP',
    discountRate: 0.20,
    discountPercentText: '20 %',
    badgeText: '20% de ahorro',
    description: 'Tarifa preferencial corporativa'
  }
};

/**
 * BR-04: Modalidades de envío para selección y presentación en interfaz
 */
export const SHIPPING_TYPES = {
  ESTANDAR: {
    id: 'ESTANDAR',
    label: 'Estándar',
    surchargeRate: 0.00,
    surchargePercentText: '0 %',
    badgeText: 'Sin recargo',
    description: 'Entrega estándar de 3 a 5 días hábiles'
  },
  EXPRESS: {
    id: 'EXPRESS',
    label: 'Express',
    surchargeRate: 0.25,
    surchargePercentText: '25 %',
    badgeText: '+25% de recargo',
    description: 'Entrega prioritaria en 24 a 48 horas'
  }
};
