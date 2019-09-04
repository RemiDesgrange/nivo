import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _d0eec4f2 = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))
const _5f4f66a5 = () => interopDefault(import('../pages/_massif.vue' /* webpackChunkName: "pages/_massif" */))

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: decodeURI('/'),
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
      path: "/",
      component: _d0eec4f2,
      name: "index"
    }, {
      path: "/:massif",
      component: _5f4f66a5,
      name: "massif"
    }],

  fallback: false
}

export function createRouter() {
  return new Router(routerOptions)
}
