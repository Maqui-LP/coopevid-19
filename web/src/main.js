import Vue from 'vue'
import App from './App.vue'
import router from './router' // Router being imported
import 'leaflet/dist/leaflet.css'
import { Icon } from 'leaflet'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


Vue.config.productionTip = false

// Install BootstrapVue
Vue.use(BootstrapVue)
// Install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

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
