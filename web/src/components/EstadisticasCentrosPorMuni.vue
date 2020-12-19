<template>
    <div class="container card">
        <h3>Porcentaje de centros por municipio</h3>
      <ve-bar :data="chartData" ></ve-bar>
    </div>
</template>

<script>
  export default {
    data () {
      return {
        municipio:[],
        chartData: {
          columns: ['municipio', 'cant'],
          rows: []
        }
      }
    },
    beforeCreate() {
      fetch(`${process.env.VUE_APP_API_BASE}/centros/estadisticas/por_municipio`)
        .then((resp)=> resp.json())
        .then(data => {
          this.chartData.rows = data.resp;
        })
    }
  }
</script>