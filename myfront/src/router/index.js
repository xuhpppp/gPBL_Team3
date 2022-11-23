import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import MyOrderView from '../views/MyOrderView.vue'

const routes = [
  {
    path: '/',
    component: HomeView
  },
  {
    path: '/order',
    component: MyOrderView
  },
  {
    path: '/login',
    component: LoginView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
