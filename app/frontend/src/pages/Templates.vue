<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { api } from '../api/client'
import AppLayout from '../layouts/AppLayout.vue'

const { t } = useI18n()
const templateTypes = ['post', 'reply', 'bio', 'channel_description', 'generic']
const templates = ref<any[]>([])
const loading = ref(false)
const notice = ref('')
const error = ref('')
const filters = reactive({ search: '', type: '' })
const draft = reactive({ type: 'generic', title: '', body: '', locale: '' })

async function load() {
  loading.value = true
  error.value = ''
  try {
    const params: Record<string, string | number> = { limit: 100 }
    if (filters.search.trim()) params.search = filters.search.trim()
    if (filters.type) params.type = filters.type
    templates.value = (await api.get('/templates', { params })).data
  } catch (err: any) {
    error.value = err?.response?.data?.detail || t('loadTemplatesError')
  } finally {
    loading.value = false
  }
}

async function create() {
  if (!draft.title.trim() || !draft.body.trim()) return
  try {
    await api.post('/templates', {
      type: draft.type,
      title: draft.title.trim(),
      body: draft.body,
      locale: draft.locale.trim() || null,
    })
    draft.type = 'generic'
    draft.title = ''
    draft.body = ''
    draft.locale = ''
    notice.value = t('templateCreated')
    await load()
  } catch (err: any) {
    error.value = err?.response?.data?.detail || t('saveTemplateError')
  }
}

async function save(item: any) {
  try {
    await api.put(`/templates/${item.id}`, {
      type: item.type,
      title: item.title,
      body: item.body,
      locale: item.locale || null,
    })
    notice.value = t('templateSaved')
    await load()
  } catch (err: any) {
    error.value = err?.response?.data?.detail || t('saveTemplateError')
  }
}

async function remove(id: number) {
  try {
    await api.delete(`/templates/${id}`)
    notice.value = t('templateDeleted')
    await load()
  } catch (err: any) {
    error.value = err?.response?.data?.detail || t('deleteTemplateError')
  }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <h1>{{ t('templates') }}</h1>
      <button class="ghost" @click="load">{{ t('refresh') }}</button>
    </div>

    <div v-if="notice" class="notice success-notice">{{ notice }}</div>
    <div v-if="error" class="notice error-notice">{{ error }}</div>

    <section class="panel">
      <h2>{{ t('createTemplate') }}</h2>
      <div class="template-form">
        <select v-model="draft.type">
          <option v-for="type in templateTypes" :key="type" :value="type">{{ t(`templateType.${type}`) }}</option>
        </select>
        <input v-model="draft.title" :placeholder="t('title')" />
        <input v-model="draft.locale" :placeholder="t('templateLocale')" />
      </div>
      <textarea v-model="draft.body" :placeholder="t('templateBody')" />
      <p class="hint">{{ t('templateVariables') }}</p>
      <button @click="create">{{ t('create') }}</button>
    </section>

    <section class="panel">
      <div class="toolbar">
        <input v-model="filters.search" :placeholder="t('searchTemplates')" @keyup.enter="load" />
        <select v-model="filters.type" @change="load">
          <option value="">{{ t('allTemplateTypes') }}</option>
          <option v-for="type in templateTypes" :key="type" :value="type">{{ t(`templateType.${type}`) }}</option>
        </select>
      </div>
      <button class="ghost" @click="load">{{ t('search') }}</button>
    </section>

    <div class="list">
      <section v-for="item in templates" :key="item.id" class="panel">
        <div class="template-form">
          <select v-model="item.type">
            <option v-for="type in templateTypes" :key="type" :value="type">{{ t(`templateType.${type}`) }}</option>
          </select>
          <input v-model="item.title" />
          <input v-model="item.locale" :placeholder="t('templateLocale')" />
        </div>
        <textarea v-model="item.body" />
        <div class="row-actions">
          <span class="badge muted">{{ item.locale || t('noLocale') }}</span>
          <button @click="save(item)">{{ t('save') }}</button>
          <button class="ghost danger-link" @click="remove(item.id)">{{ t('delete') }}</button>
        </div>
      </section>
      <section v-if="loading || !templates.length" class="panel">
        <p class="hint">{{ loading ? t('loading') : t('empty') }}</p>
      </section>
    </div>
  </AppLayout>
</template>
