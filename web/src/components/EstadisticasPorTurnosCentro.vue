<template>
    <div class="container card">
        <h3>Porcentaje de turnos por centro</h3>
        <ve-pie :data="chartData" :settings="chartSettings"></ve-pie>
    </div>
</template>

<script>
  export default {
    data () {
      this.chartSettings = {
        roseType: 'radius'
      }
      return {
        chartData: {
          columns: ['centro', 'turnos'],
          rows: []
        }
      }
    },
    beforeCreate() {
      fetch(`${process.env.VUE_APP_API_BASE}/centros/estadisticas/turnos`)
        .then((response) => response.json())
        .then((data) => {
          this.chartData.rows = data.turnos_centros
        })
    }
  }
</script>