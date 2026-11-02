<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { api } from '../api/client'
import TemplateSelector from '../components/TemplateSelector.vue'
import AppLayout from '../layouts/AppLayout.vue'

const { t } = useI18n()
const route = useRoute()
const account = ref<any>(null)
const scheduledActions = ref<any[]>([])
const auditLogs = ref<any[]>([])
const dialogs = ref<any[]>([])
const messages = ref<any[]>([])
const selectedDialogId = ref('')
const notice = ref('')
const error = ref('')
const chatsLoading = ref(false)

const credentials = reactive({ individual_api_id: null as number | null, individual_api_hash: '' })
const keepalive = reactive({ online_keepalive_enabled: false, online_ping_interval_minutes: 15 })
const actionForms = reactive({
  changeName: { first_name: '', last_name: '', mode: 'now', schedule_for: '' },
  changeUsername: { username: '', mode: 'now', schedule_for: '' },
  changeBio: { bio: '', mode: 'now', schedule_for: '' },
  uploadPhoto: { file: null as File | null, mode: 'now', schedule_for: '' },
})
const dialogMessage = ref('')
const usernameMessage = reactive({ username: '', text: '', confirmed: false })

function actionPayload(form: { mode: string; schedule_for: string }) {
  return form.mode === 'schedule' && form.schedule_for ? { schedule_for: new Date(form.schedule_for).toISOString() } : {}
}

function notifyError(err: any, fallback: string) {
  error.value = err?.response?.data?.detail || fallback
}

async function load() {
  account.value = (await api.get(`/accounts/${route.params.id}`)).data
  credentials.individual_api_id = account.value.individual_api_id || null
  credentials.individual_api_hash = ''
  keepalive.online_keepalive_enabled = account.value.online_keepalive_enabled
  keepalive.online_ping_interval_minutes = account.value.online_ping_interval_minutes || 15
  await Promise.all([loadScheduledActions(), loadAuditLogs()])
}

async function loadDialogs() {
  chatsLoading.value = true
  error.value = ''
  try {
    dialogs.value = (await api.get(`/accounts/${route.params.id}/dialogs`)).data
    if (!selectedDialogId.value && dialogs.value.length) {
      selectedDialogId.value = String(dialogs.value[0].id)
      await loadMessages(selectedDialogId.value)
    }
  } catch (err) {
    notifyError(err, t('loadDialogsError'))
  } finally {
    chatsLoading.value = false
  }
}

async function loadMessages(dialogId: string) {
  selectedDialogId.value = dialogId
  chatsLoading.value = true
  error.value = ''
  try {
    messages.value = (await api.get(`/accounts/${route.params.id}/dialogs/${encodeURIComponent(dialogId)}/messages`, { params: { limit: 50, offset: 0 } })).data
  } catch (err) {
    notifyError(err, t('loadMessagesError'))
  } finally {
    chatsLoading.value = false
  }
}

async function loadScheduledActions() {
  scheduledActions.value = (await api.get('/scheduled-actions', { params: { telegram_account_id: route.params.id, limit: 100 } })).data
}

async function loadAuditLogs() {
  try {
    auditLogs.value = (await api.get('/audit-logs', { params: { telegram_account_id: route.params.id, limit: 50 } })).data
  } catch {
    auditLogs.value = []
  }
}

async function saveOverview() {
  error.value = ''
  account.value = (await api.put(`/accounts/${route.params.id}`, account.value)).data
  notice.value = t('accountSaved')
}

async function saveCredentials() {
  error.value = ''
  const payload: Record<string, string | number | null> = { individual_api_id: credentials.individual_api_id }
  if (credentials.individual_api_hash.trim()) payload.individual_api_hash = credentials.individual_api_hash.trim()
  account.value = (await api.put(`/accounts/${route.params.id}/credentials`, payload)).data
  credentials.individual_api_hash = ''
  notice.value = t('credentialsSaved')
}

async function saveKeepalive() {
  try {
    error.value = ''
    account.value = (await api.put(`/accounts/${route.params.id}/keepalive`, keepalive)).data
    notice.value = t('keepaliveSaved')
  } catch (err) {
    notifyError(err, t('keepaliveSaveError'))
  }
}

async function connect() {
  await runAction(() => api.post(`/accounts/${route.params.id}/connect`, {}), t('connectRequested'))
}

async function checkProxy() {
  await runAction(() => api.post(`/accounts/${route.params.id}/check-proxy`, {}), t('proxyChecked'))
}

async function sendToDialog() {
  if (!selectedDialogId.value || !dialogMessage.value.trim()) return
  await runAction(
    () => api.post(`/accounts/${route.params.id}/dialogs/${encodeURIComponent(selectedDialogId.value)}/send-message`, { text: dialogMessage.value.trim() }),
    t('messageSent'),
  )
  dialogMessage.value = ''
  await loadMessages(selectedDialogId.value)
}

async function sendByUsername() {
  await runAction(
    () => api.post(`/accounts/${route.params.id}/send-message-by-username`, usernameMessage),
    t('messageSent'),
  )
  usernameMessage.text = ''
}

async function changeName() {
  const form = actionForms.changeName
  await runAction(
    () => api.post(`/accounts/${route.params.id}/actions/change-name`, { first_name: form.first_name, last_name: form.last_name || null, ...actionPayload(form) }),
    t('actionRequested'),
  )
}

async function changeUsername() {
  const form = actionForms.changeUsername
  await runAction(
    () => api.post(`/accounts/${route.params.id}/actions/change-username`, { username: form.username, ...actionPayload(form) }),
    t('actionRequested'),
  )
}

async function changeBio() {
  const form = actionForms.changeBio
  await runAction(() => api.post(`/accounts/${route.params.id}/actions/change-bio`, { bio: form.bio, ...actionPayload(form) }), t('actionRequested'))
}

async function uploadPhoto() {
  const form = actionForms.uploadPhoto
  if (!form.file) {
    error.value = t('photoRequired')
    return
  }
  const data = new FormData()
  data.append('file', form.file)
  if (form.mode === 'schedule' && form.schedule_for) data.append('schedule_for', new Date(form.schedule_for).toISOString())
  await runAction(() => api.post(`/accounts/${route.params.id}/actions/upload-photo`, data), t('actionRequested'))
}

async function runAction(request: () => Promise<unknown>, message: string) {
  try {
    error.value = ''
    await request()
    notice.value = message
    await Promise.all([load(), loadScheduledActions()])
  } catch (err) {
    notifyError(err, t('actionFailed'))
  }
}

async function cancelAction(id: number) {
  await api.post(`/scheduled-actions/${id}/cancel`)
  await loadScheduledActions()
}

function setPhoto(event: Event) {
  actionForms.uploadPhoto.file = (event.target as HTMLInputElement).files?.[0] || null
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <h1>{{ t('accountDetail') }}</h1>
      <div class="row-actions">
        <button class="ghost" @click="connect">{{ t('connect') }}</button>
        <button class="ghost" @click="checkProxy">{{ t('checkProxy') }}</button>
        <button @click="saveOverview">{{ t('save') }}</button>
      </div>
    </div>

    <div v-if="notice" class="notice success-notice">{{ notice }}</div>
    <div v-if="error" class="notice error-notice">{{ error }}</div>

    <div v-if="account" class="grid">
      <section class="panel">
        <h2>{{ t('overview') }}</h2>
        <label>{{ t('phone') }}<input v-model="account.phone_number" /></label>
        <label>{{ t('displayName') }}<input v-model="account.name" /></label>
        <label>{{ t('tgUsername') }}<input v-model="account.username" /></label>
        <label>{{ t('geo') }}<input v-model="account.geo" /></label>
        <p class="hint">{{ t('accountStatus') }}: {{ account.status }}</p>
      </section>

      <section class="panel">
        <h2>{{ t('proxy') }}</h2>
        <label>Proxy ID<input v-model.number="account.proxy_id" /></label>
        <p class="hint">{{ t('proxyStatus') }}: {{ account.proxy_status || 'unchecked' }}</p>
      </section>

      <section class="panel">
        <h2>{{ t('apiOverride') }}</h2>
        <p class="hint">{{ t('apiOverrideExplanation') }}</p>
        <label>{{ t('individualApiId') }}<input v-model.number="credentials.individual_api_id" type="number" /></label>
        <label>{{ t('individualApiHash') }}<input v-model="credentials.individual_api_hash" type="password" :placeholder="account.individual_api_hash_masked || ''" /></label>
        <p class="hint">{{ t('savedApiHash') }}: {{ account.individual_api_hash_masked || '-' }}</p>
        <button @click="saveCredentials">{{ t('saveCredentials') }}</button>
      </section>

      <section class="panel">
        <h2>{{ t('keepalive') }}</h2>
        <label><input v-model="keepalive.online_keepalive_enabled" type="checkbox" /> {{ t('enabled') }}</label>
        <label>{{ t('pingIntervalMinutes') }}<input v-model.number="keepalive.online_ping_interval_minutes" type="number" min="15" /></label>
        <button @click="saveKeepalive">{{ t('save') }}</button>
      </section>

      <section class="panel account-wide">
        <div class="section-head">
          <h2>{{ t('chats') }}</h2>
          <button class="ghost" @click="loadDialogs">{{ t('loadDialogs') }}</button>
        </div>
        <p class="hint">{{ t('sendByUsernameWarning') }}</p>
        <div class="chats-layout">
          <aside class="dialog-list">
            <button
              v-for="dialog in dialogs"
              :key="dialog.id"
              class="dialog-item"
              :class="{ active: String(dialog.id) === selectedDialogId }"
              @click="loadMessages(String(dialog.id))"
            >
              <strong>{{ dialog.title }}</strong>
              <span>{{ dialog.last_message || dialog.type }}</span>
            </button>
            <p v-if="!dialogs.length" class="hint">{{ chatsLoading ? t('loading') : t('empty') }}</p>
          </aside>
          <div class="messages-pane">
            <div class="messages-list">
              <div v-for="message in messages" :key="message.id" class="message-row">
                <strong>{{ message.sender || '-' }}</strong>
                <span>{{ message.text }}</span>
              </div>
              <p v-if="!messages.length" class="hint">{{ chatsLoading ? t('loading') : t('empty') }}</p>
            </div>
            <div class="send-row">
              <input v-model="dialogMessage" :placeholder="t('messageText')" />
              <button :disabled="!selectedDialogId" @click="sendToDialog">{{ t('send') }}</button>
            </div>
            <TemplateSelector v-model="dialogMessage" :account-id="account.id" type="reply" />
          </div>
        </div>
        <div class="username-send">
          <h2>{{ t('sendByUsername') }}</h2>
          <input v-model="usernameMessage.username" :placeholder="t('tgUsername')" />
          <TemplateSelector v-model="usernameMessage.text" :account-id="account.id" type="reply" />
          <textarea v-model="usernameMessage.text" :placeholder="t('messageText')" />
          <label><input v-model="usernameMessage.confirmed" type="checkbox" /> {{ t('usernameSendConfirm') }}</label>
          <button class="ghost" :disabled="!usernameMessage.confirmed" @click="sendByUsername">{{ t('send') }}</button>
        </div>
      </section>

      <section class="panel account-wide">
        <h2>{{ t('profileActions') }}</h2>
        <div class="action-grid">
          <div class="action-box">
            <h2>{{ t('changeName') }}</h2>
            <input v-model="actionForms.changeName.first_name" :placeholder="t('firstName')" />
            <input v-model="actionForms.changeName.last_name" :placeholder="t('lastName')" />
            <select v-model="actionForms.changeName.mode"><option value="now">{{ t('executeNow') }}</option><option value="schedule">{{ t('scheduleFor') }}</option></select>
            <input v-if="actionForms.changeName.mode === 'schedule'" v-model="actionForms.changeName.schedule_for" type="datetime-local" />
            <button class="ghost" @click="changeName">{{ t('submit') }}</button>
          </div>
          <div class="action-box">
            <h2>{{ t('changeUsername') }}</h2>
            <input v-model="actionForms.changeUsername.username" :placeholder="t('tgUsername')" />
            <select v-model="actionForms.changeUsername.mode"><option value="now">{{ t('executeNow') }}</option><option value="schedule">{{ t('scheduleFor') }}</option></select>
            <input v-if="actionForms.changeUsername.mode === 'schedule'" v-model="actionForms.changeUsername.schedule_for" type="datetime-local" />
            <button class="ghost" @click="changeUsername">{{ t('submit') }}</button>
          </div>
          <div class="action-box">
            <h2>{{ t('changeBio') }}</h2>
            <TemplateSelector v-model="actionForms.changeBio.bio" :account-id="account.id" type="bio" />
            <textarea v-model="actionForms.changeBio.bio" />
            <select v-model="actionForms.changeBio.mode"><option value="now">{{ t('executeNow') }}</option><option value="schedule">{{ t('scheduleFor') }}</option></select>
            <input v-if="actionForms.changeBio.mode === 'schedule'" v-model="actionForms.changeBio.schedule_for" type="datetime-local" />
            <button class="ghost" @click="changeBio">{{ t('submit') }}</button>
          </div>
          <div class="action-box">
            <h2>{{ t('uploadPhoto') }}</h2>
            <input type="file" accept="image/*" @change="setPhoto" />
            <select v-model="actionForms.uploadPhoto.mode"><option value="now">{{ t('executeNow') }}</option><option value="schedule">{{ t('scheduleFor') }}</option></select>
            <input v-if="actionForms.uploadPhoto.mode === 'schedule'" v-model="actionForms.uploadPhoto.schedule_for" type="datetime-local" />
            <button class="ghost" @click="uploadPhoto">{{ t('submit') }}</button>
          </div>
        </div>
      </section>

      <section class="panel account-wide">
        <h2>{{ t('scheduledActions') }}</h2>
        <div class="table-wrap compact-table">
          <table>
            <tbody>
              <tr v-for="action in scheduledActions" :key="action.id">
                <td>{{ action.id }}</td><td>{{ action.action_type }}</td><td>{{ action.status }}</td><td>{{ action.scheduled_for }}</td><td>{{ action.error || '-' }}</td>
                <td><button v-if="action.status === 'pending'" class="link" @click="cancelAction(action.id)">{{ t('cancel') }}</button></td>
              </tr>
              <tr v-if="!scheduledActions.length"><td colspan="6">{{ t('empty') }}</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="panel account-wide">
        <h2>{{ t('auditLogs') }}</h2>
        <div class="table-wrap compact-table">
          <table><tbody><tr v-for="log in auditLogs" :key="log.id"><td>{{ log.created_at }}</td><td>{{ log.action }}</td><td>{{ log.details || '-' }}</td></tr><tr v-if="!auditLogs.length"><td>{{ t('empty') }}</td></tr></tbody></table>
        </div>
      </section>
    </div>
  </AppLayout>
</template>
