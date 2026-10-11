<script setup>
import { computed } from 'vue'
import { CUSTOMER_TYPES, SHIPPING_TYPES } from '../constants/pricingRules'

const props = defineProps({
  quote: {
    type: Object,
    default: null
  },
  apiError: {
    type: String,
    default: null
  }
})

// Mapeos para presentar etiquetas amigables
const customerInfo = computed(() => {
  if (!props.quote) return null
  return CUSTOMER_TYPES[props.quote.customer_type] || { label: props.quote.customer_type }
})

const shippingInfo = computed(() => {
  if (!props.quote) return null
  return SHIPPING_TYPES[props.quote.shipping_type] || { label: props.quote.shipping_type }
})

// Formateador de moneda en USD
const formatUSD = (value) => {
  const num = Number(value)
  if (isNaN(num)) return '$0.00 USD'
  return `$${num.toFixed(2)} USD`
}
</script>

<template>
  <div class="h-full flex flex-col">
    <!-- Caso 1: Error de API o Comunicación del Servidor -->
    <div
      v-if="apiError"
      class="bg-rose-50 border border-rose-200 rounded-2xl p-6 text-slate-800 flex flex-col justify-center items-center text-center h-full min-h-[320px]"
    >
      <div class="w-12 h-12 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mb-3">
        <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
      </div>
      <h3 class="text-base font-bold text-rose-900">
        Error al procesar la cotización
      </h3>
      <p class="text-xs text-rose-700 mt-1 max-w-sm">
        {{ apiError }}
      </p>
    </div>

    <!-- Caso 2: Cotización Válida Calculada (Recibo Comercial) -->
    <div
      v-else-if="quote"
      class="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden flex flex-col"
    >
      <!-- Cabecera del Recibo -->
      <div class="bg-gradient-to-r from-slate-900 to-slate-800 text-white p-5">
        <div class="flex items-center justify-between">
          <div>
            <span class="text-[10px] font-mono tracking-widest uppercase text-slate-400">
              Desglose Oficial
            </span>
            <h3 class="text-lg font-bold text-white tracking-tight">
              Recibo de cotización
            </h3>
          </div>
          <div class="text-right">
            <span class="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-1 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30">
              <span class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
              FastExpress API
            </span>
          </div>
        </div>

        <div class="mt-3 pt-3 border-t border-slate-700/60 grid grid-cols-3 gap-2 text-xs">
          <div>
            <div class="text-[10px] text-slate-400 uppercase">Peso facturado</div>
            <div class="font-mono font-semibold text-slate-200">{{ quote.weight_kg }} kg</div>
          </div>
          <div>
            <div class="text-[10px] text-slate-400 uppercase">Cliente</div>
            <div class="font-semibold text-slate-200 truncate">{{ customerInfo.label }}</div>
          </div>
          <div>
            <div class="text-[10px] text-slate-400 uppercase">Envío</div>
            <div class="font-semibold text-slate-200 truncate">{{ shippingInfo.label }}</div>
          </div>
        </div>
      </div>

      <!-- Cuerpo del Recibo: Detalle de Rubros devueltos por el backend -->
      <div class="p-5 flex-1 space-y-3.5 bg-slate-50/50 text-sm">
        <!-- Rubro 1: Tarifa Base -->
        <div class="flex items-center justify-between text-slate-700">
          <div>
            <span class="font-medium text-slate-900">Tarifa base fija</span>
            <p class="text-[11px] text-slate-500">Cargo administrativo por orden (BR-01)</p>
          </div>
          <span class="font-mono font-semibold text-slate-900">
            {{ formatUSD(quote.base_rate) }}
          </span>
        </div>

        <!-- Rubro 2: Costo por Peso y Tramo -->
        <div class="flex items-center justify-between text-slate-700">
          <div>
            <div class="flex items-center gap-1.5">
              <span class="font-medium text-slate-900">Costo por peso</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-200 font-mono text-slate-700">
                ${{ quote.rate_per_kg }}/kg
              </span>
            </div>
            <p class="text-[11px] text-slate-500">
              {{ quote.weight_kg }} kg × ${{ quote.rate_per_kg }}/kg
              <span v-if="Number(quote.weight_kg) <= 5.00" class="text-blue-600 font-medium">(Tramo ≤ 5.00 kg)</span>
              <span v-else class="text-indigo-600 font-medium">(Tramo &gt; 5.00 kg)</span>
            </p>
          </div>
          <span class="font-mono font-semibold text-slate-900">
            {{ formatUSD(quote.weight_charge) }}
          </span>
        </div>

        <!-- Subtotal -->
        <div class="pt-2 pb-2 border-t border-slate-200 flex items-center justify-between">
          <span class="text-xs uppercase tracking-wider font-bold text-slate-600">
            Subtotal (Base + Peso)
          </span>
          <span class="font-mono font-bold text-slate-900">
            {{ formatUSD(quote.subtotal) }}
          </span>
        </div>

        <!-- Descuento -->
        <div class="flex items-center justify-between text-slate-700">
          <div>
            <div class="flex items-center gap-1.5">
              <span class="font-medium text-slate-900">Descuento aplicado</span>
              <span
                class="text-[10px] px-1.5 py-0.5 rounded font-mono"
                :class="Number(quote.discount) > 0 ? 'bg-emerald-100 text-emerald-800 font-bold' : 'bg-slate-200 text-slate-600'"
              >
                -{{ (Number(quote.discount_rate) * 100).toFixed(0) }}%
              </span>
            </div>
            <p class="text-[11px] text-slate-500">
              Beneficio cliente {{ quote.customer_type }} (BR-03)
            </p>
          </div>
          <span
            class="font-mono font-semibold"
            :class="Number(quote.discount) > 0 ? 'text-emerald-600' : 'text-slate-400'"
          >
            {{ Number(quote.discount) > 0 ? `-${formatUSD(quote.discount)}` : formatUSD(quote.discount) }}
          </span>
        </div>

        <!-- Recargo -->
        <div class="flex items-center justify-between text-slate-700">
          <div>
            <div class="flex items-center gap-1.5">
              <span class="font-medium text-slate-900">Recargo aplicado</span>
              <span
                class="text-[10px] px-1.5 py-0.5 rounded font-mono"
                :class="Number(quote.surcharge) > 0 ? 'bg-amber-100 text-amber-800 font-bold' : 'bg-slate-200 text-slate-600'"
              >
                +{{ (Number(quote.surcharge_rate) * 100).toFixed(0) }}%
              </span>
            </div>
            <p class="text-[11px] text-slate-500">
              Modalidad {{ quote.shipping_type }} (BR-04)
            </p>
          </div>
          <span
            class="font-mono font-semibold"
            :class="Number(quote.surcharge) > 0 ? 'text-amber-700' : 'text-slate-400'"
          >
            {{ Number(quote.surcharge) > 0 ? `+${formatUSD(quote.surcharge)}` : formatUSD(quote.surcharge) }}
          </span>
        </div>

        <!-- Línea perforada estilo ticket -->
        <div class="relative py-2">
          <div class="border-b-2 border-dashed border-slate-300"></div>
        </div>

        <!-- Total Destacado -->
        <div class="p-4 rounded-xl bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200/80 flex items-center justify-between">
          <div>
            <span class="text-xs uppercase font-extrabold tracking-wider text-blue-900 block">
              Total a pagar
            </span>
            <span class="text-[11px] text-blue-700">
              Impuestos y cargos incluidos
            </span>
          </div>
          <div class="text-right">
            <span class="text-2xl sm:text-3xl font-black font-mono text-blue-950 tracking-tight">
              {{ formatUSD(quote.total) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Pie del Recibo -->
      <div class="px-5 py-3 bg-slate-100/80 border-t border-slate-200 text-[11px] text-slate-500 flex items-center justify-between">
        <span class="flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          Cotización oficial calculada por el backend
        </span>
        <span class="font-mono text-slate-400">USD</span>
      </div>
    </div>

    <!-- Caso 3: Estado Vacío (Requisito 4.4) -->
    <div
      v-else
      class="bg-white rounded-2xl border-2 border-dashed border-slate-200 p-8 flex flex-col items-center justify-center text-center h-full min-h-[380px]"
    >
      <div class="w-16 h-16 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-400 mb-4 shadow-2xs">
        <svg class="w-8 h-8 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <line x1="10" y1="9" x2="8" y2="9"></line>
        </svg>
      </div>

      <h3 class="text-base font-bold text-slate-800">
        Tu cotización aparecerá aquí
      </h3>
      <p class="text-xs text-slate-500 mt-1.5 max-w-xs leading-relaxed">
        Ingresa el peso de tu paquete y selecciona el tipo de cliente y envío. Luego haz clic en <strong>"Calcular cotización"</strong> para ver el desglose detallado.
      </p>

      <div class="mt-6 flex items-center gap-2 text-[11px] text-slate-400">
        <span class="w-2 h-2 rounded-full bg-slate-300"></span>
        <span>Sin importes provisionales ni cálculos previos</span>
      </div>
    </div>
  </div>
</template>
