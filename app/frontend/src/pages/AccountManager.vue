<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { api } from '../api/client'
import AppLayout from '../layouts/AppLayout.vue'

type Account = {
  id: number
  phone_number: string | null
  name: string
  display_name?: string
  username: string | null
  geo: string | null
  status: string
  proxy_id: number | null
  proxy_status: string | null
  online_keepalive: boolean
  last_connected_at: string | null
}

type ProxyItem = {
  id: number
  name: string
  status: string
}

type ScheduledAction = {
  id: number
  account_id: number | null
  status: string
}

const { t } = useI18n()
const accounts = ref<Account[]>([])
const proxies = ref<ProxyItem[]>([])
const scheduledActions = ref<ScheduledAction[]>([])
const selectedIds = ref<number[]>([])
const loading = ref(false)
const bulkLoading = ref(false)
const modalOpen = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const filters = reactive({
  search: '',
  status: '',
  geo: '',
  proxyStatus: '',
})

const uploadForm = reactive({
  file: null as File | null,
  phone_number: '',
  geo: '',
  proxy_id: '',
  api_id_override: '',
  api_hash_override: '',
})

const visibleAccounts = computed(() => {
  const search = filters.search.trim().toLowerCase()
  return accounts.value.filter((account) => {
    const displayName = account.display_name || account.name || ''
    const matchesSearch =
      !search ||
      [account.phone_number, displayName, account.username]
        .filter(Boolean)
        .some((value) => String(value).toLowerCase().includes(search))
    const matchesStatus = !filters.status || account.status === filters.status
    const matchesGeo = !filters.geo || account.geo === filters.geo
    const proxyStatus = account.proxy_status || 'unchecked'
    const matchesProxy = !filters.proxyStatus || proxyStatus === filters.proxyStatus
    return matchesSearch && matchesStatus && matchesGeo && matchesProxy
  })
})

const allVisibleSelected = computed(
  () => visibleAccounts.value.length > 0 && visibleAccounts.value.every((account) => selectedIds.value.includes(account.id)),
)

const geoOptions = computed(() =>
  Array.from(new Set(accounts.value.map((account) => account.geo).filter(Boolean) as string[])).sort(),
)

const stats = computed(() => ({
  total: accounts.value.length,
  connected: accounts.value.filter((account) => account.status === 'active').length,
  errors: accounts.value.filter((account) => account.status === 'error').length,
  pending: scheduledActions.value.filter((action) => action.status === 'pending').length,
}))

function notifyError(error: unknown, fallback: string) {
  const detail = (error as any)?.response?.data?.detail
  errorMessage.value = typeof detail === 'string' ? detail : fallback
}

function clearNotice() {
  errorMessage.value = ''
  successMessage.value = ''
}

async function load() {
  loading.value = true
  clearNotice()
  try {
    const [accountsResponse, proxiesResponse, scheduledResponse] = await Promise.all([
      api.get<Account[]>('/accounts', { params: { limit: 200, offset: 0 } }),
      api.get<ProxyItem[]>('/proxies', { params: { limit: 200, offset: 0 } }),
      api.get<ScheduledAction[]>('/scheduled-actions', { params: { limit: 200, offset: 0, status: 'pending' } }),
    ])
    accounts.value = accountsResponse.data
    proxies.value = proxiesResponse.data
    scheduledActions.value = scheduledResponse.data
    selectedIds.value = selectedIds.value.filter((id) => accounts.value.some((account) => account.id === id))
  } catch (error) {
    notifyError(error, t('loadAccountsError'))
  } finally {
    loading.value = false
  }
}

function toggleAll(event: Event) {
  const checked = (event.target as HTMLInputElement).checked
  selectedIds.value = checked ? visibleAccounts.value.map((account) => account.id) : []
}

function resetUploadForm() {
  uploadForm.file = null
  uploadForm.phone_number = ''
  uploadForm.geo = ''
  uploadForm.proxy_id = ''
  uploadForm.api_id_override = ''
  uploadForm.api_hash_override = ''
}

function onFileChange(event: Event) {
  uploadForm.file = (event.target as HTMLInputElement).files?.[0] || null
}

async function submitUpload() {
  if (!uploadForm.file) {
    errorMessage.value = t('sessionFileRequired')
    return
  }
  loading.value = true
  clearNotice()
  try {
    const form = new FormData()
    form.append('file', uploadForm.file)
    if (uploadForm.phone_number.trim()) form.append('phone_number', uploadForm.phone_number.trim())
    if (uploadForm.geo.trim()) form.append('geo', uploadForm.geo.trim())
    if (uploadForm.proxy_id) form.append('proxy_id', uploadForm.proxy_id)
    if (uploadForm.api_id_override) form.append('individual_api_id', uploadForm.api_id_override)
    if (uploadForm.api_hash_override.trim()) form.append('individual_api_hash', uploadForm.api_hash_override.trim())
    await api.post<Account>('/accounts/import-session-with-meta', form)
    successMessage.value = t('uploadComplete')
    modalOpen.value = false
    resetUploadForm()
    await load()
  } catch (error) {
    notifyError(error, t('uploadFailed'))
  } finally {
    loading.value = false
  }
}

async function remove(id: number) {
  loading.value = true
  clearNotice()
  try {
    await api.delete(`/accounts/${id}`)
    successMessage.value = t('accountDeleted')
    await load()
  } catch (error) {
    notifyError(error, t('deleteFailed'))
  } finally {
    loading.value = false
  }
}

async function bulkCheckProxies() {
  await runBulk(async (selected) => {
    const proxyIds = Array.from(new Set(selected.map((account) => account.proxy_id).filter(Boolean) as number[]))
    await Promise.all(proxyIds.map((id) => api.post(`/proxies/${id}/check`)))
  }, t('bulkDone'))
}

async function bulkKeepalive(enabled: boolean) {
  await runBulk(async (selected) => {
    await Promise.all(selected.map((account) => api.put(`/accounts/${account.id}`, { online_keepalive: enabled })))
  }, t(enabled ? 'keepaliveEnabled' : 'keepaliveDisabled'))
}

async function bulkCancelPending() {
  await runBulk(async (selected) => {
    const selectedSet = new Set(selected.map((account) => account.id))
    const pending = scheduledActions.value.filter(
      (action) => action.status === 'pending' && action.account_id !== null && selectedSet.has(action.account_id),
    )
    await Promise.all(pending.map((action) => api.post(`/scheduled-actions/${action.id}/cancel`)))
  }, t('pendingCancelled'))
}

async function runBulk(operation: (selected: Account[]) => Promise<void>, message: string) {
  const selected = accounts.value.filter((account) => selectedIds.value.includes(account.id))
  if (!selected.length) return
  bulkLoading.value = true
  clearNotice()
  try {
    await operation(selected)
    successMessage.value = message
    await load()
  } catch (error) {
    notifyError(error, t('bulkFailed'))
  } finally {
    bulkLoading.value = false
  }
}

function badgeClass(value: string | boolean | null) {
  if (value === true || value === 'active' || value === 'working') return 'badge ok'
  if (value === 'error' || value === 'failed') return 'badge danger'
  if (value === 'pending' || value === 'imported' || value === 'unchecked') return 'badge muted'
  return 'badge'
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
      <h1>{{ t('accounts') }}</h1>
      <button @click="modalOpen = true">{{ t('uploadSession') }}</button>
    </div>

    <div class="cards account-stats">
      <div class="card"><span>{{ t('totalAccounts') }}</span><strong>{{ stats.total }}</strong></div>
      <div class="card"><span>{{ t('connectedAccounts') }}</span><strong>{{ stats.connected }}</strong></div>
      <div class="card"><span>{{ t('errorAccounts') }}</span><strong>{{ stats.errors }}</strong></div>
      <div class="card"><span>{{ t('pendingScheduledActions') }}</span><strong>{{ stats.pending }}</strong></div>
    </div>

    <div v-if="errorMessage" class="notice error-notice">{{ errorMessage }}</div>
    <div v-if="successMessage" class="notice success-notice">{{ successMessage }}</div>

    <div class="account-controls panel">
      <input v-model="filters.search" :placeholder="t('searchAccounts')" />
      <select v-model="filters.status" :aria-label="t('statusFilter')">
        <option value="">{{ t('allStatuses') }}</option>
        <option value="imported">imported</option>
        <option value="active">active</option>
        <option value="disabled">disabled</option>
        <option value="error">error</option>
      </select>
      <select v-model="filters.geo" :aria-label="t('geoFilter')">
        <option value="">{{ t('allGeo') }}</option>
        <option v-for="geo in geoOptions" :key="geo" :value="geo">{{ geo }}</option>
      </select>
      <select v-model="filters.proxyStatus" :aria-label="t('proxyStatusFilter')">
        <option value="">{{ t('allProxyStatuses') }}</option>
        <option value="unchecked">unchecked</option>
        <option value="working">working</option>
        <option value="failed">failed</option>
      </select>
    </div>

    <div v-if="selectedIds.length" class="bulk-bar">
      <strong>{{ t('selectedAccounts', { count: selectedIds.length }) }}</strong>
      <div class="bulk-actions">
        <button class="ghost" :disabled="bulkLoading" @click="bulkCheckProxies">{{ t('checkProxies') }}</button>
        <button class="ghost" :disabled="bulkLoading" @click="bulkKeepalive(true)">{{ t('enableKeepalive') }}</button>
        <button class="ghost" :disabled="bulkLoading" @click="bulkKeepalive(false)">{{ t('disableKeepalive') }}</button>
        <button class="ghost" :disabled="bulkLoading" @click="bulkCancelPending">{{ t('cancelPendingActions') }}</button>
      </div>
    </div>

    <div class="table-wrap">
      <div v-if="loading" class="loading-row">{{ t('loading') }}</div>
      <table>
        <thead>
          <tr>
            <th><input type="checkbox" :checked="allVisibleSelected" @change="toggleAll" /></th>
            <th>#</th>
            <th>{{ t('phone') }}</th>
            <th>{{ t('displayName') }}</th>
            <th>{{ t('tgUsername') }}</th>
            <th>{{ t('geo') }}</th>
            <th>{{ t('proxyStatus') }}</th>
            <th>{{ t('accountStatus') }}</th>
            <th>{{ t('keepalive') }}</th>
            <th>{{ t('lastConnected') }}</th>
            <th>{{ t('actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="account in visibleAccounts" :key="account.id">
            <td><input v-model="selectedIds" type="checkbox" :value="account.id" /></td>
            <td>{{ account.id }}</td>
            <td>{{ account.phone_number || '-' }}</td>
            <td>{{ account.display_name || account.name }}</td>
            <td>{{ account.username || '-' }}</td>
            <td>{{ account.geo || '-' }}</td>
            <td><span :class="badgeClass(account.proxy_status || 'unchecked')">{{ account.proxy_status || 'unchecked' }}</span></td>
            <td><span :class="badgeClass(account.status)">{{ account.status }}</span></td>
            <td><span :class="badgeClass(account.online_keepalive)">{{ account.online_keepalive ? t('enabled') : t('disabled') }}</span></td>
            <td>{{ formatDate(account.last_connected_at) }}</td>
            <td class="row-actions">
              <RouterLink :to="`/accounts/${account.id}`">{{ t('open') }}</RouterLink>
              <RouterLink :to="`/accounts/${account.id}`">{{ t('edit') }}</RouterLink>
              <button class="link danger-link" @click="remove(account.id)">{{ t('delete') }}</button>
            </td>
          </tr>
          <tr v-if="!loading && !visibleAccounts.length"><td colspan="11">{{ t('empty') }}</td></tr>
        </tbody>
      </table>
    </div>

    <div v-if="modalOpen" class="modal-backdrop" @click.self="modalOpen = false">
      <form class="modal" @submit.prevent="submitUpload">
        <div class="modal-head">
          <h2>{{ t('uploadSession') }}</h2>
          <button type="button" class="ghost" @click="modalOpen = false">{{ t('close') }}</button>
        </div>
        <label>{{ t('sessionFile') }}<input type="file" accept=".session" required @change="onFileChange" /></label>
        <label>{{ t('phone') }}<input v-model="uploadForm.phone_number" /></label>
        <label>{{ t('geoOptional') }}<input v-model="uploadForm.geo" /></label>
        <label>{{ t('proxyOptional') }}
          <select v-model="uploadForm.proxy_id">
            <option value="">{{ t('noProxy') }}</option>
            <option v-for="proxy in proxies" :key="proxy.id" :value="proxy.id">{{ proxy.name }} · {{ proxy.status }}</option>
          </select>
        </label>
        <label>{{ t('individualApiId') }}<input v-model="uploadForm.api_id_override" type="number" /></label>
        <label>{{ t('individualApiHash') }}<input v-model="uploadForm.api_hash_override" type="password" /></label>
        <div class="modal-actions">
          <button type="button" class="ghost" @click="modalOpen = false">{{ t('cancel') }}</button>
          <button :disabled="loading">{{ t('submit') }}</button>
        </div>
      </form>
    </div>
  </AppLayout>
</template>
