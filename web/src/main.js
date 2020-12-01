import Vue from 'vue'
import App from './App.vue'
import router from './router' // Router being imported

Vue.config.productionTip = false

new Vue({
  router,  // router added to the Vue instance
  render: function (h) { return h(App) }
}).$mount('#app')
