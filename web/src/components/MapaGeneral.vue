<template>
  <div style="height: 550px;">
    <l-map 
      style="height: 90%; width: 100%"
      :zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
    >
      <l-tile-layer :url="url" > </l-tile-layer>
      <ul v-for="(element, index) in coordinates" :key="index">
        <l-marker @click="showModal(element)" :lat-lng="element.coord"></l-marker>
      </ul>
    </l-map>
    <b-modal ref="my-modal" ok-only>
      <div class="d-block text-center">
        <h3>{{selectedCenter.nombre}}</h3>
        <h6>Dirección: {{selectedCenter.direccion}}</h6>
        <h6>Email: {{selectedCenter.email}}</h6>
        <h6>Hora de apertura: {{selectedCenter.hora_apertura}}</h6>
        <h6>Hora de cierr: {{selectedCenter.hora_cierr}}</h6>
        <h6>Telefono: {{selectedCenter.telefono}}</h6>
      </div>
    </b-modal>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet'
export default {
  name:'MapaGeneral',
  components: {
    LMap,
    LTileLayer,
    LMarker  
  },
  data () {
    return  {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 14,
      center: [-34.9187, -57.956],
      // markerLatLng: [-34.9206722, -57.9561499],
      centros: null,
      coordinates:[],
      selectedCenter:'',
    }
  },
  beforeCreate: function () {
    fetch("http://localhost:5000/api/centros/all",{
      "method": "GET",
    })
  .then(response => {
    return response.json()
    .then(body => this.centros = body.centros)
    .then(() =>{
      this.centros.forEach(element => {
        var array = [element.lat, element.long];
        element["coord"] = array;        
        this.coordinates.push(element);
      });
    });
  });
  },
  methods: {
    zoomUpdated(zoom) {
        this.zoom = zoom
    },
    centerUpdated(center) {
      this.center = center
    },
    showModal(element) {
      this.selectedCenter = element;
      this.$refs['my-modal'].show();
    },
    hideModal(){
      this.$refs['my-modal'].hide();
    }
  }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
