import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import SacarTurno from './views/SacarTurno.vue'
import CargarCentro from './views/CargarCentro.vue'
import Estadisticas from './views/Estadisticas.vue'
import Mapa from './views/Mapa.vue'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/estadisticas',
    name: 'estadisticas',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Estadisticas
    
  },
  {
    path: '/sacar_turno',
    name: 'sacar_turno',
    component: SacarTurno
  },
  {
    path: '/cargar_centro',
    name: 'cargar_centro',
    component: CargarCentro
  },
  {
    path: '/mapa',
    name: 'mapa',
    component: Mapa
  }
]

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
