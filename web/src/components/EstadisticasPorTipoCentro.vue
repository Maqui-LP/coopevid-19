<template>
    <div class="container card">
        <h3>Porcentaje de centros por tipo de donaciones</h3>
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
          columns: ['tipo', 'cantidad'],
          rows: [ ]
        }
      }
    },
    beforeCreate() {
      fetch(`${process.env.VUE_APP_API_BASE}/centros/estadisticas/porTipos`)
        .then((response) => response.json())
        .then((data) => {
          console.log(data.response)
          this.chartData.rows = data.response
        })
    }
  }
</script>