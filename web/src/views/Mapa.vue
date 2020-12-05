<template>
  <div class="mapa">
    <MapaGeneral msg="Aca va el mapa con todos los centros"/>
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
  </div>
</template>

<script>
import MapaGeneral from '@/components/MapaGeneral.vue'

export default {
  name: 'mapa',
  components: {
    MapaGeneral
  }
}
</script>
