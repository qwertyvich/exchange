<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { api } from '../api/client'
import AppLayout from '../layouts/AppLayout.vue'

type ProxyItem = {
  id: number
  name: string
  type: string
  host: string
  port: number
  username: string | null
  password_masked: string | null
  status: string
  last_checked_at: string | null
  last_error: string | null
}

const { t } = useI18n()
const proxies = ref<ProxyItem[]>([])
const loading = ref(false)
const checkingId = ref<number | null>(null)
const errorMessage = ref('')
const successMessage = ref('')
const filters = reactive({ status: '', type: '' })
const form = reactive({
  id: null as number | null,
  name: '',
  type: 'http',
  host: '',
  port: 8080,
  username: '',
  password: '',
})

const filteredProxies = computed(() =>
  proxies.value.filter((proxy) => {
    const statusOk = !filters.status || proxy.status === filters.status
    const typeOk = !filters.type || proxy.type === filters.type
    return statusOk && typeOk
  }),
)

function clearNotice() {
  errorMessage.value = ''
  successMessage.value = ''
}

function notifyError(error: unknown, fallback: string) {
  const detail = (error as any)?.response?.data?.detail
  errorMessage.value = typeof detail === 'string' ? detail : fallback
}

async function load() {
  loading.value = true
  clearNotice()
  try {
    const { data } = await api.get<ProxyItem[]>('/proxies', { params: { limit: 200, offset: 0 } })
    proxies.value = data
  } catch (error) {
    notifyError(error, t('loadProxiesError'))
  } finally {
    loading.value = false
  }
}

function resetForm() {
  form.id = null
  form.name = ''
  form.type = 'http'
  form.host = ''
  form.port = 8080
  form.username = ''
  form.password = ''
}

function editProxy(proxy: ProxyItem) {
  form.id = proxy.id
  form.name = proxy.name
  form.type = proxy.type
  form.host = proxy.host
  form.port = proxy.port
  form.username = proxy.username || ''
  form.password = ''
}

async function saveProxy() {
  loading.value = true
  clearNotice()
  const payload: Record<string, string | number> = {
    name: form.name,
    type: form.type,
    host: form.host,
    port: Number(form.port),
  }
  if (form.username.trim()) payload.username = form.username.trim()
  if (form.password.trim()) payload.password = form.password.trim()
  try {
    if (form.id) {
      await api.put(`/proxies/${form.id}`, payload)
      successMessage.value = t('proxyUpdated')
    } else {
      await api.post('/proxies', payload)
      successMessage.value = t('proxyCreated')
    }
    resetForm()
    await load()
  } catch (error) {
    notifyError(error, t('saveProxyError'))
  } finally {
    loading.value = false
  }
}

async function deleteProxy(id: number) {
  loading.value = true
  clearNotice()
  try {
    await api.delete(`/proxies/${id}`)
    successMessage.value = t('proxyDeleted')
    await load()
  } catch (error) {
    notifyError(error, t('deleteProxyError'))
  } finally {
    loading.value = false
  }
}

async function checkProxy(id: number) {
  checkingId.value = id
  clearNotice()
  try {
    await api.post(`/proxies/${id}/check`)
    successMessage.value = t('proxyChecked')
    await load()
  } catch (error) {
    notifyError(error, t('checkProxyError'))
  } finally {
    checkingId.value = null
  }
}

function badgeClass(value: string) {
  if (value === 'working') return 'badge ok'
  if (value === 'failed') return 'badge danger'
  return 'badge muted'
}

function formatDate(value: string | null) {
  if (!value) return '-'
  return new Intl.DateTimeFormat(undefined, { dateStyle: 'short', timeStyle: 'short' }).format(new Date(value))
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <h1>{{ t('proxies') }}</h1>
      <button class="ghost" @click="load">{{ t('refresh') }}</button>
    </div>

    <div v-if="errorMessage" class="notice error-notice">{{ errorMessage }}</div>
    <div v-if="successMessage" class="notice success-notice">{{ successMessage }}</div>

    <section class="panel proxy-form" @submit.prevent>
      <label>{{ t('name') }}<input v-model="form.name" required /></label>
      <label>{{ t('proxyType') }}
        <select v-model="form.type">
          <option value="http">http</option>
          <option value="https">https</option>
          <option value="socks5">socks5</option>
        </select>
      </label>
      <label>{{ t('proxyHost') }}<input v-model="form.host" required /></label>
      <label>{{ t('proxyPort') }}<input v-model.number="form.port" type="number" min="1" max="65535" required /></label>
      <label>{{ t('proxyUsername') }}<input v-model="form.username" /></label>
      <label>{{ t('proxyPassword') }}<input v-model="form.password" type="password" :placeholder="t('leaveBlankToKeep')" /></label>
      <div class="form-actions">
        <button :disabled="loading" @click="saveProxy">{{ form.id ? t('save') : t('create') }}</button>
        <button type="button" class="ghost" @click="resetForm">{{ t('cancel') }}</button>
      </div>
    </section>

    <div class="account-controls panel">
      <select v-model="filters.status" :aria-label="t('statusFilter')">
        <option value="">{{ t('allStatuses') }}</option>
        <option value="unchecked">unchecked</option>
        <option value="working">working</option>
        <option value="failed">failed</option>
      </select>
      <select v-model="filters.type" :aria-label="t('proxyType')">
        <option value="">{{ t('allProxyTypes') }}</option>
        <option value="http">http</option>
        <option value="https">https</option>
        <option value="socks5">socks5</option>
      </select>
    </div>

    <div class="table-wrap">
      <div v-if="loading" class="loading-row">{{ t('loading') }}</div>
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>{{ t('name') }}</th>
            <th>{{ t('proxyType') }}</th>
            <th>{{ t('proxyHost') }}</th>
            <th>{{ t('proxyPort') }}</th>
            <th>{{ t('proxyUsername') }}</th>
            <th>{{ t('proxyPassword') }}</th>
            <th>{{ t('proxyStatus') }}</th>
            <th>{{ t('lastChecked') }}</th>
            <th>{{ t('lastError') }}</th>
            <th>{{ t('actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="proxy in filteredProxies" :key="proxy.id">
            <td>{{ proxy.id }}</td>
            <td>{{ proxy.name }}</td>
            <td>{{ proxy.type }}</td>
            <td>{{ proxy.host }}</td>
            <td>{{ proxy.port }}</td>
            <td>{{ proxy.username || '-' }}</td>
            <td>{{ proxy.password_masked || '-' }}</td>
            <td><span :class="badgeClass(proxy.status)">{{ proxy.status }}</span></td>
            <td>{{ formatDate(proxy.last_checked_at) }}</td>
            <td class="muted-cell">{{ proxy.last_error || '-' }}</td>
            <td class="row-actions">
              <button class="link" :disabled="checkingId === proxy.id" @click="checkProxy(proxy.id)">{{ t('checkProxy') }}</button>
              <button class="link" @click="editProxy(proxy)">{{ t('edit') }}</button>
              <button class="link danger-link" @click="deleteProxy(proxy.id)">{{ t('delete') }}</button>
            </td>
          </tr>
          <tr v-if="!loading && !filteredProxies.length"><td colspan="11">{{ t('empty') }}</td></tr>
        </tbody>
      </table>
    </div>
  </AppLayout>
</template>
