<template>
  <header class="mb-6 sm:mb-8">
    <div class="flex items-start gap-3.5 pb-6 border-b border-slate-200">
      <!-- Isotipo y logotipo de FastExpress -->
      <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-blue-700 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-blue-500/20 shrink-0">
        <svg class="w-7 h-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
          <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
          <line x1="12" y1="22.08" x2="12" y2="12"></line>
          <path d="m17 13 4-2.3"></path>
        </svg>
      </div>

      <!-- Títulos y subtítulos -->
      <div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md border border-blue-100">
            FastExpress Logistics
          </span>
          <span class="text-xs text-slate-400 font-medium hidden sm:inline">
            Módulo de Calidad de Software
          </span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mt-0.5">
          Cotización de envíos
        </h1>
        <p class="text-sm text-slate-500 mt-1 max-w-2xl">
          Calcula el costo estimado de tu paquete en tiempo real con verificación de reglas de negocio y límites operativos.
        </p>
      </div>
    </div>
  </header>
</template>
