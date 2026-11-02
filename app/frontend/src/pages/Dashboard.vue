<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { api } from '../api/client'
import AppLayout from '../layouts/AppLayout.vue'

const { t } = useI18n()
const accounts = ref<any[]>([])
const actions = ref<any[]>([])
const proxies = ref<any[]>([])

onMounted(async () => {
  const [a, s, p] = await Promise.all([api.get('/accounts'), api.get('/scheduled-actions'), api.get('/proxies')])
  accounts.value = a.data
  actions.value = s.data
  proxies.value = p.data
})
</script>

<template>
  <AppLayout>
    <div class="page-head"><h1>{{ t('dashboard') }}</h1></div>
    <div class="cards">
      <div class="card"><span>{{ t('totalAccounts') }}</span><strong>{{ accounts.length }}</strong></div>
      <div class="card"><span>{{ t('pendingActions') }}</span><strong>{{ actions.filter(x => x.status === 'pending').length }}</strong></div>
      <div class="card"><span>{{ t('failedProxies') }}</span><strong>{{ proxies.filter(x => x.status === 'failed').length }}</strong></div>
    </div>
  </AppLayout>
</template>
