import Vue from 'vue'
import Base from './Base.vue'
import VueRouter from 'vue-router'
import IndexPage from './pages/index.vue'
import mock from './mock/mock'

Vue.use(VueRouter)

let router = new VueRouter({
  mode:'history',
  routes:[
    {
      path:'/',
      component:IndexPage
    }
  ]
})

new Vue({
  el: '#app',
  router,
  components:{
    Base
  },
  template:'<Base/>'
})

