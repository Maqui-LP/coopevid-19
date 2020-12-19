<template>
  <div class="estadisticas">
    <h1>Aqui encontraras estadisticas utiles</h1>
    <EstadisticasPorTipoCentro />
    <div class="mt-4">
      <EstadisticasCentrosPorMuni/>
    </div>
    <div class="mt-4">
      <EstadisticasPorTurnosCentro />
    </div>
  </div>
</template>

<script>

import EstadisticasPorTipoCentro from  '@/components/EstadisticasPorTipoCentro.vue'
import EstadisticasCentrosPorMuni from '@/components/EstadisticasCentrosPorMuni.vue'
import EstadisticasPorTurnosCentro from '@/components/EstadisticasPorTurnosCentro.vue'

export default {
  name: 'Estadisticas',
  components:{
    EstadisticasCentrosPorMuni,
    EstadisticasPorTipoCentro,
    EstadisticasPorTurnosCentro
  },
}
</script>