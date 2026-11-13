import { createRouter, createWebHistory } from 'vue-router'

import LandingView from '../views/LandingView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  { path: '/', name: 'landing', component: LandingView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: () => import('../views/ResetPasswordView.vue'),
  },
]

// 1. Create the router first
const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 2. Attach the navigation guard AFTER router is initialized
router.beforeEach((to, from, next) => {
  // Check for the token key that your handleLogin actually saves
  const isAuthenticated = localStorage.getItem('access_token') || localStorage.getItem('sb-access-token') || localStorage.getItem('scripter_session')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router