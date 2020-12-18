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
          columns: ['date', 'cost'],
          rows: [
            { 'date': 'Comida', 'cost': 20 },
            { 'date': 'Ropa', 'cost': 10 },
            { 'date': 'Higiene Personal', 'cost': 10 },
            { 'date': 'Higiene del Hogar', 'cost': 30 },
            { 'date': 'Muebles', 'cost': 30 },
          ]
        }
      }
    }
  }
</script>