<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { api } from '../api/client'

const props = defineProps<{
  modelValue?: string
  accountId?: number | string
  type?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const { t } = useI18n()
const templates = ref<any[]>([])
const selectedId = ref('')
const preview = ref('')
const loading = ref(false)
const error = ref('')

const filteredTemplates = computed(() => {
  if (!props.type) return templates.value
  return templates.value.filter((template) => template.type === props.type || template.type === 'generic')
})

async function loadTemplates() {
  loading.value = true
  error.value = ''
  try {
    templates.value = (await api.get('/templates', { params: { limit: 200 } })).data
  } catch (err: any) {
    error.value = err?.response?.data?.detail || t('loadTemplatesError')
  } finally {
    loading.value = false
  }
}

async function loadPreview() {
  preview.value = ''
  if (!selectedId.value || !props.accountId) return
  try {
    preview.value = (await api.get(`/templates/${selectedId.value}/render`, { params: { account_id: props.accountId } })).data.rendered_body
  } catch (err: any) {
    error.value = err?.response?.data?.detail || t('templatePreviewError')
  }
}

function applyTemplate() {
  const selected = templates.value.find((template) => String(template.id) === selectedId.value)
  emit('update:modelValue', preview.value || selected?.body || props.modelValue || '')
}

watch(selectedId, loadPreview)
watch(() => props.accountId, loadPreview)
onMounted(loadTemplates)
</script>

<template>
  <div class="template-selector">
    <div class="send-row">
      <select v-model="selectedId">
        <option value="">{{ loading ? t('loading') : t('chooseTemplate') }}</option>
        <option v-for="template in filteredTemplates" :key="template.id" :value="String(template.id)">
          {{ template.title }} · {{ template.type }}
        </option>
      </select>
      <button class="ghost" :disabled="!selectedId" @click="applyTemplate">{{ t('applyTemplate') }}</button>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div v-if="preview" class="template-preview">
      <small>{{ t('preview') }}</small>
      <p>{{ preview }}</p>
    </div>
  </div>
</template>
