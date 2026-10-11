<script setup>
import { computed } from 'vue'
import { CUSTOMER_TYPES, SHIPPING_TYPES } from '../constants/pricingRules'

const props = defineProps({
  weight: {
    type: [String, Number],
    default: ''
  },
  customerType: {
    type: String,
    default: 'NUEVO'
  },
  shippingType: {
    type: String,
    default: 'ESTANDAR'
  },
  validationError: {
    type: String,
    default: null
  },
  isRejected: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:weight',
  'update:customerType',
  'update:shippingType',
  'submit',
  'reset'
])

// Opciones de clientes en arreglo para iterar de manera ordenada
const customerOptions = computed(() => Object.values(CUSTOMER_TYPES))

// Opciones de modalidades de envío en arreglo
const shippingOptions = computed(() => Object.values(SHIPPING_TYPES))

const onWeightInput = (event) => {
  emit('update:weight', event.target.value)
}

const onSelectCustomer = (typeId) => {
  emit('update:customerType', typeId)
}

const onSelectShipping = (typeId) => {
  emit('update:shippingType', typeId)
}

const handleSubmit = () => {
  if (props.isLoading) return
  emit('submit')
}

const handleReset = () => {
  if (props.isLoading) return
  emit('reset')
}
</script>

<template>
  <form @submit.prevent="handleSubmit" novalidate class="space-y-6">
    <!-- Alerta crítica de Envío Rechazado (Requisito 5.2) -->
    <div
      v-if="isRejected"
      role="alert"
      class="p-4 rounded-xl bg-rose-50 border-2 border-rose-300 text-rose-900 shadow-sm transition-all"
    >
      <div class="flex items-start gap-3">
        <div class="p-1 rounded-lg bg-rose-100 text-rose-700 shrink-0">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
        </div>
        <div>
          <h3 class="text-sm font-bold text-rose-900">
            Envío Rechazado: El peso excede el límite máximo permitido de 20.00 kg
          </h3>
          <p class="text-xs text-rose-700 mt-1 leading-relaxed">
            Nuestra política operativa solo admite paquetes con un peso máximo de hasta 20.00 kg. Para cargas superiores a 20.00 kg, comunícate con el área de transporte de carga pesada.
          </p>
        </div>
      </div>
    </div>

    <!-- Campo A: Peso del paquete -->
    <div>
      <div class="flex items-center justify-between mb-1.5">
        <label for="weight_input" class="block text-sm font-semibold text-slate-800">
          Peso del paquete (kg) <span class="text-rose-500">*</span>
        </label>
        <span class="text-xs text-slate-400 font-mono">
          Rango: (0.00, 20.00] kg
        </span>
      </div>

      <div class="relative">
        <input
          id="weight_input"
          name="weight"
          type="number"
          step="0.01"
          min="0"
          max="25"
          :value="weight"
          @input="onWeightInput"
          placeholder="Ej. 4.50 kg (Máx. 20.00 kg)"
          class="w-full px-4 py-2.5 rounded-xl border font-medium text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 transition-all"
          :class="[
            validationError
              ? isRejected
                ? 'border-rose-400 bg-rose-50/40 focus:border-rose-500 focus:ring-rose-200 text-rose-900'
                : 'border-amber-400 bg-amber-50/40 focus:border-amber-500 focus:ring-amber-200 text-amber-900'
              : 'border-slate-300 bg-white hover:border-slate-400 focus:border-blue-600 focus:ring-blue-100'
          ]"
          :aria-invalid="Boolean(validationError)"
          aria-describedby="weight-help weight-error"
        />

        <div class="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none text-slate-400 font-medium text-sm">
          kg
        </div>
      </div>

      <!-- Mensaje de error de validación (Requisito 5.1, 5.3) -->
      <div
        v-if="validationError && !isRejected"
        id="weight-error"
        role="alert"
        class="mt-2 text-xs font-semibold text-amber-700 flex items-center gap-1.5"
      >
        <svg class="w-4 h-4 shrink-0 text-amber-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path>
          <line x1="12" y1="9" x2="12" y2="13"></line>
          <line x1="12" y1="17" x2="12.01" y2="17"></line>
        </svg>
        <span>{{ validationError }}</span>
      </div>

      <!-- Texto de ayuda complementario -->
      <p id="weight-help" class="mt-1.5 text-xs text-slate-500 flex items-center gap-1">
        <svg class="w-3.5 h-3.5 text-slate-400 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
        <span>Ingresa un peso mayor a 0.00 kg y hasta 20.00 kg</span>
      </p>
    </div>

    <!-- Campo B: Tipo de cliente -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <label class="block text-sm font-semibold text-slate-800">
          Tipo de cliente
        </label>
        <span class="text-xs text-slate-400">
          Aplica descuento comercial
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
        <button
          v-for="customer in customerOptions"
          :key="customer.id"
          type="button"
          @click="onSelectCustomer(customer.id)"
          class="relative p-3 rounded-xl border text-left transition-all focus:outline-none focus:ring-2 focus:ring-blue-500"
          :class="[
            customerType === customer.id
              ? 'border-blue-600 bg-blue-50/70 shadow-xs ring-1 ring-blue-600'
              : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/60'
          ]"
        >
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold tracking-tight text-slate-900">
              {{ customer.id }}
            </span>
            <span
              class="w-4 h-4 rounded-full border flex items-center justify-center transition-colors"
              :class="[
                customerType === customer.id
                  ? 'border-blue-600 bg-blue-600 text-white'
                  : 'border-slate-300 bg-white'
              ]"
            >
              <svg v-if="customerType === customer.id" class="w-2.5 h-2.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </span>
          </div>

          <div class="mt-1 flex items-baseline gap-1.5">
            <span
              class="text-xs font-extrabold px-1.5 py-0.5 rounded"
              :class="[
                customer.discountRate > 0
                  ? 'bg-emerald-100 text-emerald-800'
                  : 'bg-slate-100 text-slate-600'
              ]"
            >
              {{ customer.discountPercentText }} dto.
            </span>
          </div>

          <p class="text-[11px] text-slate-500 mt-1 line-clamp-1">
            {{ customer.description }}
          </p>
        </button>
      </div>
    </div>

    <!-- Campo C: Tipo de envío -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <label class="block text-sm font-semibold text-slate-800">
          Tipo de envío
        </label>
        <span class="text-xs text-slate-400">
          Tiempo y prioridad
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <button
          v-for="shipping in shippingOptions"
          :key="shipping.id"
          type="button"
          @click="onSelectShipping(shipping.id)"
          class="relative p-3.5 rounded-xl border text-left transition-all focus:outline-none focus:ring-2 focus:ring-blue-500"
          :class="[
            shippingType === shipping.id
              ? 'border-blue-600 bg-blue-50/70 shadow-xs ring-1 ring-blue-600'
              : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/60'
          ]"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="text-sm font-bold text-slate-900">
                {{ shipping.label }}
              </span>
              <span
                class="text-[10px] font-bold px-1.5 py-0.5 rounded uppercase"
                :class="[
                  shipping.surchargeRate > 0
                    ? 'bg-amber-100 text-amber-800 border border-amber-200'
                    : 'bg-slate-100 text-slate-600 border border-slate-200'
                ]"
              >
                {{ shipping.surchargeRate > 0 ? '+25% recargo' : 'Sin recargo' }}
              </span>
            </div>

            <span
              class="w-4 h-4 rounded-full border flex items-center justify-center transition-colors"
              :class="[
                shippingType === shipping.id
                  ? 'border-blue-600 bg-blue-600 text-white'
                  : 'border-slate-300 bg-white'
              ]"
            >
              <svg v-if="shippingType === shipping.id" class="w-2.5 h-2.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </span>
          </div>

          <p class="text-xs text-slate-500 mt-1.5">
            {{ shipping.description }}
          </p>
        </button>
      </div>
    </div>

    <!-- Campo D: Botones de acción -->
    <div class="pt-2 flex flex-col sm:flex-row gap-3">
      <!-- Botón Principal: Calcular cotización -->
      <button
        type="submit"
        :disabled="isLoading"
        class="flex-1 py-3 px-5 rounded-xl bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white font-bold text-sm shadow-md shadow-blue-500/25 transition-all flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        <!-- Spinner mientras está cargando -->
        <svg
          v-if="isLoading"
          class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>

        <svg v-else class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M5 12h14"></path>
          <path d="m12 5 7 7-7 7"></path>
        </svg>

        <span>{{ isLoading ? 'Calculando cotización...' : 'Calcular cotización' }}</span>
      </button>

      <!-- Botón Secundario: Limpiar formulario -->
      <button
        type="button"
        @click="handleReset"
        :disabled="isLoading"
        class="py-3 px-4 rounded-xl border border-slate-300 hover:bg-slate-100 active:bg-slate-200 text-slate-700 font-semibold text-sm transition-all flex items-center justify-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-slate-400"
      >
        <svg class="w-4 h-4 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
          <path d="M3 3v5h5"></path>
        </svg>
        <span>Limpiar formulario</span>
      </button>
    </div>
  </form>
</template>
