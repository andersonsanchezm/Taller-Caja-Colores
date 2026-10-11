<script setup>
import { ref } from 'vue'
import Header from './components/Header.vue'
import QuoteForm from './components/QuoteForm.vue'
import QuoteReceipt from './components/QuoteReceipt.vue'
import { validateWeightInput } from './services/quotationService'
import { fetchQuoteFromApi } from './services/apiService'

// Estado del formulario
const weight = ref('')
const customerType = ref('NUEVO')
const shippingType = ref('ESTANDAR')

// Estados de validación y procesamiento
const validationError = ref(null)
const isRejected = ref(false)
const isLoading = ref(false)

// Estado del resultado devuelto por la API
const currentQuote = ref(null)
const apiError = ref(null)

// Acción de cálculo de cotización mediante la API REST
const handleCalculate = async () => {
  // 1. Validación de entrada en el frontend para feedback inmediato
  const validation = validateWeightInput(weight.value)

  if (!validation.isValid) {
    validationError.value = validation.message
    isRejected.value = validation.isRejected
    currentQuote.value = null
    apiError.value = null
    return
  }

  // Entrada válida
  validationError.value = null
  isRejected.value = false
  apiError.value = null
  isLoading.value = true

  try {
    // Solicitud exclusiva al backend HTTP
    const result = await fetchQuoteFromApi({
      weight_kg: weight.value,
      customer_type: customerType.value,
      shipping_type: shippingType.value
    })

    if (result.success) {
      currentQuote.value = result.data
      apiError.value = null
    } else {
      currentQuote.value = null
      if (result.isRejected) {
        isRejected.value = true
        validationError.value = result.error
      } else {
        apiError.value = result.error
      }
    }
  } catch (err) {
    currentQuote.value = null
    apiError.value = `Ocurrió un error inesperado al procesar la cotización: ${err.message}`
  } finally {
    isLoading.value = false
  }
}

// Acción de reinicio / limpieza del formulario
const handleReset = () => {
  weight.value = ''
  customerType.value = 'NUEVO'
  shippingType.value = 'ESTANDAR'
  validationError.value = null
  isRejected.value = false
  isLoading.value = false
  currentQuote.value = null
  apiError.value = null
}
</script>

<template>
  <div class="min-h-screen bg-slate-100 flex flex-col justify-center py-8 sm:py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-6xl mx-auto w-full my-auto">
      <!-- Encabezado general -->
      <Header />

      <!-- Tarjeta Principal del Dashboard dividida en 2 columnas -->
      <main class="bg-white rounded-3xl shadow-xl shadow-slate-200/60 border border-slate-200/80 overflow-hidden">
        <div class="grid grid-cols-1 lg:grid-cols-12 divide-y lg:divide-y-0 lg:divide-x divide-slate-200">
          <!-- Columna Izquierda: Formulario de Cotización (7 de 12 columnas en desktop) -->
          <div class="p-6 sm:p-8 lg:col-span-7 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between pb-4 mb-6 border-b border-slate-100">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-blue-600"></div>
                  <h2 class="text-base font-bold text-slate-800">
                    Datos del envío
                  </h2>
                </div>
                <span class="text-xs text-slate-400 font-medium">
                  Paso 1 de 2: Parámetros
                </span>
              </div>

              <!-- Componente de Formulario -->
              <QuoteForm
                :weight="weight"
                :customer-type="customerType"
                :shipping-type="shippingType"
                :validation-error="validationError"
                :is-rejected="isRejected"
                :is-loading="isLoading"
                @update:weight="weight = $event"
                @update:customer-type="customerType = $event"
                @update:shipping-type="shippingType = $event"
                @submit="handleCalculate"
                @reset="handleReset"
              />
            </div>

            <!-- Ayuda o nota al pie del formulario -->
            <div class="mt-8 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
              <span class="flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                Validación estricta de límites (BVA)
              </span>
              <span>Reglas BR-01 a BR-04</span>
            </div>
          </div>

          <!-- Columna Derecha: Panel de Resultados / Recibo Comercial (5 de 12 columnas en desktop) -->
          <div class="p-6 sm:p-8 lg:col-span-5 bg-slate-50/70 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between pb-4 mb-6 border-b border-slate-200/80">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
                  <h2 class="text-base font-bold text-slate-800">
                    Resultado estimado
                  </h2>
                </div>
                <span class="text-xs text-slate-400 font-medium">
                  Paso 2 de 2: Liquidación
                </span>
              </div>

              <!-- Componente de Recibo Comercial -->
              <QuoteReceipt
                :quote="currentQuote"
                :api-error="apiError"
              />
            </div>

            <!-- Resumen de tramos informativos -->
            <div class="mt-6 pt-4 border-t border-slate-200/60 text-[11px] text-slate-500 space-y-1">
              <div class="flex justify-between">
                <span>Tramo ligero (0.01 a 5.00 kg):</span>
                <span class="font-mono font-medium text-slate-700">$2.00 USD/kg</span>
              </div>
              <div class="flex justify-between">
                <span>Tramo pesado (5.01 a 20.00 kg):</span>
                <span class="font-mono font-medium text-slate-700">$4.00 USD/kg</span>
              </div>
              <div class="flex justify-between text-rose-600">
                <span>Límite máximo permitido:</span>
                <span class="font-mono font-bold">20.00 kg</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
