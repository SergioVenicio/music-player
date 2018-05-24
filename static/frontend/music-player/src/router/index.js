import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import '../assets/css/bootstrap.css'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    }
  ]
})
