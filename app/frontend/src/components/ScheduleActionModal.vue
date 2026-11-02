<script setup lang="ts">
import { reactive } from 'vue'
import { useI18n } from 'vue-i18n'
import { api } from '../api/client'

const props = defineProps<{
  accountId?: number | null
}>()

const emit = defineEmits<{
  close: []
  saved: []
}>()

const { t } = useI18n()

const form = reactive({
  action_type: 'enable_keepalive',
  payload_json: '{}',
  mode: 'now',
  scheduled_for: '',
  loading: false,
  error: '',
})

async function submit() {
  form.loading = true
  form.error = ''
  try {
    const payload: Record<string, string | number | null> = {
      action_type: form.action_type,
      payload_json: form.payload_json || '{}',
      telegram_account_id: props.accountId || null,
    }
    if (form.mode === 'schedule' && form.scheduled_for) {
      payload.scheduled_for = new Date(form.scheduled_for).toISOString()
    }
    await api.post('/scheduled-actions', payload)
    emit('saved')
  } catch (error: any) {
    form.error = error?.response?.data?.detail || t('scheduleActionError')
  } finally {
    form.loading = false
  }
}
</script>

<template>
  <div class="modal-backdrop" @click.self="emit('close')">
    <form class="modal" @submit.prevent="submit">
      <div class="modal-head">
        <h2>{{ t('scheduleAction') }}</h2>
        <button type="button" class="ghost" @click="emit('close')">{{ t('close') }}</button>
      </div>
      <label>{{ t('actionType') }}
        <select v-model="form.action_type">
          <option value="change_name">change_name</option>
          <option value="change_username">change_username</option>
          <option value="change_bio">change_bio</option>
          <option value="upload_photo">upload_photo</option>
          <option value="send_message">send_message</option>
          <option value="create_channel">create_channel</option>
          <option value="create_group">create_group</option>
          <option value="post_to_channel">post_to_channel</option>
          <option value="enable_keepalive">enable_keepalive</option>
          <option value="disable_keepalive">disable_keepalive</option>
        </select>
      </label>
      <label>{{ t('payloadJson') }}<textarea v-model="form.payload_json" /></label>
      <div class="tabs">
        <button type="button" :class="{ active: form.mode === 'now' }" @click="form.mode = 'now'">{{ t('executeNow') }}</button>
        <button type="button" :class="{ active: form.mode === 'schedule' }" @click="form.mode = 'schedule'">{{ t('scheduleFor') }}</button>
      </div>
      <label v-if="form.mode === 'schedule'">{{ t('scheduleDateTime') }}<input v-model="form.scheduled_for" type="datetime-local" /></label>
      <p v-if="form.error" class="error">{{ form.error }}</p>
      <div class="modal-actions">
        <button type="button" class="ghost" @click="emit('close')">{{ t('cancel') }}</button>
        <button :disabled="form.loading">{{ t('submit') }}</button>
      </div>
    </form>
  </div>
</template>
