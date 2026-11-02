<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { api } from '../api/client'
import AppLayout from '../layouts/AppLayout.vue'

const { t } = useI18n()
const form = ref({ global_api_id: null as number | null, global_api_hash: '', default_online_ping_minutes: 5, message_rate_limit_per_minute: 5 })
const masked = ref('')
const saved = ref(false)

async function load() {
  const { data } = await api.get('/settings')
  form.value.global_api_id = data.global_api_id
  form.value.default_online_ping_minutes = data.default_online_ping_minutes || Math.max(1, Math.floor((data.default_online_ping_interval || 300) / 60))
  form.value.message_rate_limit_per_minute = data.message_rate_limit_per_minute || 5
  masked.value = data.global_api_hash_masked || ''
}

async function save() {
  const payload = { ...form.value, global_api_hash: form.value.global_api_hash || undefined }
  const { data } = await api.put('/settings', payload)
  masked.value = data.global_api_hash_masked || ''
  form.value.global_api_hash = ''
  saved.value = true
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="page-head"><h1>{{ t('settings') }}</h1><button @click="save">{{ t('save') }}</button></div>
    <section class="panel settings-form">
      <label>{{ t('globalApiId') }}<input v-model.number="form.global_api_id" type="number" /></label>
      <label>{{ t('globalApiHash') }}<input v-model="form.global_api_hash" type="password" :placeholder="masked" /></label>
      <p class="hint">{{ t('savedApiHash') }}: {{ masked || '-' }}</p>
      <label>{{ t('pingIntervalMinutes') }}<input v-model.number="form.default_online_ping_minutes" type="number" min="1" /></label>
      <label>{{ t('messageRateLimit') }}<input v-model.number="form.message_rate_limit_per_minute" type="number" min="1" max="60" /></label>
      <p class="hint">{{ t('secretWarning') }}</p>
      <p v-if="saved" class="hint">{{ t('settingsSaved') }}</p>
    </section>
  </AppLayout>
</template>
