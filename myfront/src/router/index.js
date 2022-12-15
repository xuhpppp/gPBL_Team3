import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import MyOrderView from '../views/MyOrderView.vue'
import EditOrderView from '../views/EditOrderView.vue'
import SpectateView from '../views/SpectateView'
import TestView from '../views/TestView'
import FaceRecognitionView from '../views/FaceRecognitionView'
import InsertDatasetView from '../views/InsertDatasetView'
import AdminDashboard from '../views/AdminDashboard.vue'
import Recognition from '../components/Version2/table/Recognition.vue'


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
  },
  {
    path: '/face',
    component: FaceRecognitionView
  },
  {
    path: '/insert',
    component: InsertDatasetView
  },
  {
    path: '/test',
    component: TestView
  },
  {
    path: '/admin',
    component: AdminDashboard,
    children: [
      {
        path: 'recognition',
        component: Recognition
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  linkActiveClass: 'active',
  routes
})

export default router
