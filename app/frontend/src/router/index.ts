import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Login from '../pages/Login.vue'
import Dashboard from '../pages/Dashboard.vue'
import AccountManager from '../pages/AccountManager.vue'
import AccountDetail from '../pages/AccountDetail.vue'
import Templates from '../pages/Templates.vue'
import Proxies from '../pages/Proxies.vue'
import Settings from '../pages/Settings.vue'
import Admin from '../pages/Admin.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: Login, meta: { public: true } },
    { path: '/', component: Dashboard },
    { path: '/accounts', component: AccountManager },
    { path: '/accounts/:id', component: AccountDetail },
    { path: '/proxies', component: Proxies },
    { path: '/templates', component: Templates },
    { path: '/settings', component: Settings },
    { path: '/admin', component: Admin, meta: { admin: true } },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!to.meta.public && !auth.isAuthenticated) return '/login'
  if (auth.isAuthenticated && !auth.user) await auth.fetchMe().catch(() => auth.logout())
  if (to.meta.admin && !auth.isAdmin) return '/'
  if (to.path === '/login' && auth.isAuthenticated) return '/'
})

export default router
