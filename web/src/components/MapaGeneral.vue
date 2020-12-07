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
        <l-marker @click="clickHandler(element)" :lat-lng="element.coord"></l-marker>
      </ul>
    </l-map>
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
      markerLatLng: [-34.9206722, -57.9561499],
      centros: null,
      coordinates:[],
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
        console.log(element);
        // this.coordinates.push(array);
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
    clickHandler(latlng) {
      console.log(latlng)
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
