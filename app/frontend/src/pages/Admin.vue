<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { api } from '../api/client'
import AppLayout from '../layouts/AppLayout.vue'

const { t } = useI18n()
const active = ref('users')
const users = ref<any[]>([])
const logs = ref<any[]>([])
const actions = ref<any[]>([])

async function load() {
  const [u, l, a] = await Promise.all([
    api.get('/admin/users'),
    api.get('/admin/audit-logs'),
    api.get('/admin/scheduled-actions'),
  ])
  users.value = u.data
  logs.value = l.data
  actions.value = a.data
}

async function cancel(id: number) {
  await api.post(`/admin/scheduled-actions/${id}/cancel`)
  await load()
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="page-head"><h1>{{ t('admin') }}</h1></div>
    <div class="tabs">
      <button :class="{ active: active === 'users' }" @click="active = 'users'">{{ t('users') }}</button>
      <button :class="{ active: active === 'logs' }" @click="active = 'logs'">{{ t('auditLogs') }}</button>
      <button :class="{ active: active === 'actions' }" @click="active = 'actions'">{{ t('scheduledActions') }}</button>
      <button :class="{ active: active === 'settings' }" @click="active = 'settings'">{{ t('systemSettings') }}</button>
    </div>
    <div v-if="active === 'users'" class="table-wrap"><table><tbody><tr v-for="u in users" :key="u.id"><td>{{ u.id }}</td><td>{{ u.username }}</td><td>{{ u.role }}</td><td>{{ u.is_active }}</td></tr></tbody></table></div>
    <div v-if="active === 'logs'" class="table-wrap"><table><tbody><tr v-for="l in logs" :key="l.id"><td>{{ l.created_at }}</td><td>{{ l.username }}</td><td>{{ l.action }}</td><td>{{ l.entity_type }}</td><td>{{ l.details }}</td></tr></tbody></table></div>
    <div v-if="active === 'actions'" class="table-wrap">
      <table>
        <tbody>
          <tr v-for="a in actions" :key="a.id">
            <td>{{ a.id }}</td>
            <td>{{ a.telegram_account_id || '-' }}</td>
            <td>{{ a.action_type }}</td>
            <td>{{ a.status }}</td>
            <td>{{ a.scheduled_for }}</td>
            <td>{{ a.error || '-' }}</td>
            <td><button v-if="a.status === 'pending'" class="ghost" @click="cancel(a.id)">{{ t('cancel') }}</button></td>
          </tr>
        </tbody>
      </table>
    </div>
    <section v-if="active === 'settings'" class="panel"><p>{{ t('secretWarning') }}</p></section>
  </AppLayout>
</template>
