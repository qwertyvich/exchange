<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const { t, locale } = useI18n()
const theme = ref(localStorage.getItem('theme') || 'light')

const nav = computed(() => [
  { to: '/', label: t('dashboard') },
  { to: '/accounts', label: t('accounts') },
  { to: '/proxies', label: t('proxies') },
  { to: '/templates', label: t('templates') },
  { to: '/settings', label: t('settings') },
  ...(auth.isAdmin ? [{ to: '/admin', label: t('admin') }] : []),
])

function setLocale(value: string) {
  locale.value = value
  localStorage.setItem('locale', value)
}

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  localStorage.setItem('theme', theme.value)
  document.documentElement.dataset.theme = theme.value
}

function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(() => {
  document.documentElement.dataset.theme = theme.value
})
</script>

<template>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">{{ t('app') }}</div>
      <nav>
        <RouterLink v-for="item in nav" :key="item.to" :to="item.to">{{ item.label }}</RouterLink>
      </nav>
    </aside>
    <div class="main">
      <header class="topbar">
        <div class="user">{{ auth.user?.username }} · {{ auth.user?.role }}</div>
        <div class="topbar-actions">
          <select :value="locale" @change="setLocale(($event.target as HTMLSelectElement).value)">
            <option value="ru">RU</option>
            <option value="en">EN</option>
          </select>
          <button class="ghost" @click="toggleTheme">{{ theme === 'dark' ? t('light') : t('dark') }}</button>
          <button class="ghost" @click="logout">{{ t('logout') }}</button>
        </div>
      </header>
      <main class="content">
        <slot />
      </main>
    </div>
  </div>
</template>
