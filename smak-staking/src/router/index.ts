import Vue from 'vue'
import VueRouter from 'vue-router'
import Staking from '../views/staking/Staking'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Staking
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
