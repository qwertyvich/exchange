import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
import ru from './i18n/ru.json'
import en from './i18n/en.json'
import './styles.css'

const savedLocale = localStorage.getItem('locale') || 'ru'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: { ru, en },
})

createApp(App).use(createPinia()).use(router).use(i18n).mount('#app')
