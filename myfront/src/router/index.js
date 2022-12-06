import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import MyOrderView from '../views/MyOrderView.vue'
import EditOrderView from '../views/EditOrderView.vue'
import SpectateView from '../views/SpectateView'

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
  },
  {
    path: '/edit-order/:idRoomOrder',
    component: EditOrderView
  },
  {
    path: '/spectate',
    component: SpectateView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
