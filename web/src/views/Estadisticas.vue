<template>
  <div class="estadisticas">
    <h1>Aqui encontraras estadisticas utiles</h1>
    <EstadisticasPorTipoCentro />
    <EstadisticasPorTurnosCentro />
  </div>
</template>

<script>

import EstadisticasPorTipoCentro from  '@/components/EstadisticasPorTipoCentro.vue'
import EstadisticasPorTurnosCentro from '@/components/EstadisticasPorTurnosCentro.vue'

export default {
  name: 'Estadisticas',
  components:{
    EstadisticasPorTipoCentro,
    EstadisticasPorTurnosCentro
  },
}
</script>