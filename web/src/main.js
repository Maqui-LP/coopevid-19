import Vue from 'vue'
import App from './App.vue'
import router from './router' // Router being imported
import 'leaflet/dist/leaflet.css'
import { Icon } from 'leaflet'

Vue.config.productionTip = false

new Vue({
  router,  // router added to the Vue instance
  render: function (h) { return h(App) }
}).$mount('#app')

delete Icon.Default.prototype._getIconUrl
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dis/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/master-shadow.png')
})
