<template>
  <div class="estadisticas">
    <h1>Aqui encontraras estadisticas utiles</h1>
    <EstadisticasPorTipoCentro />
  </div>
</template>

<script>

import EstadisticasPorTipoCentro from  '@/components/EstadisticasPorTipoCentro.vue'

export default {
  name: 'Estadisticas',
  components:{
    EstadisticasPorTipoCentro
  },
}
</script>