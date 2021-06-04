import Vue from 'vue'
import VueRouter from 'vue-router'
import Staking from '../views/staking/Staking.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Staking',
    component: Staking
  }
]

const router = new VueRouter({
  routes
})

export default router
