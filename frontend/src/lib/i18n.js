import { computed, ref, watch } from 'vue';
import english from '../locales/en.json';

const STORAGE_KEY = 'palma.locale';
const defaultTitle = document.title;
function savedLanguage() {
  try { return localStorage.getItem(STORAGE_KEY) === 'en' ? 'en' : 'ru'; }
  catch { return 'ru'; }
}
export const locale = ref(savedLanguage());
export const localeTag = computed(() => locale.value === 'en' ? 'en-GB' : 'ru-RU');
export const currentLanguage = computed(() => locale.value.toUpperCase());
const reverse = new Map(Object.entries(english).map(([ru, en]) => [en, ru]));
const escapeRegex = text => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const patterns = Object.entries(english).flatMap(([ru, en]) => {
  if (!/\{\w+\}/.test(ru)) return [];
  return [ru, en].map(text => {
    const names = [];
    const source = text.split(/(\{\w+\})/).map(part => {
      if (/^\{\w+\}$/.test(part)) { names.push(part.slice(1, -1)); return '(.+?)'; }
      return escapeRegex(part);
    }).join('');
    return { key: ru, names, regex: new RegExp(`^${source}$`) };
  });
});

// Keys are the original copy, kept explicitly in templates rather than translated DOM nodes.
export function tr(message, parameters = {}) {
  if (typeof message !== 'string') return message;
  let source = reverse.get(message) || message;
  if (!english[source]) {
    for (const pattern of patterns) {
      const match = message.match(pattern.regex);
      if (match) {
        source = pattern.key;
        parameters = Object.fromEntries(pattern.names.map((name, i) => [name, match[i + 1]]));
        break;
      }
    }
  }
  const translated = locale.value === 'en' ? (english[source] || source) : source;
  return translated.replace(/\{(\w+)\}/g, (match, key) => {
    if (parameters[key] == null) return match;
    const value = String(parameters[key]);
    const canonical = reverse.get(value) || value;
    return locale.value === 'en' ? (english[canonical] || value) : canonical;
  });
}

export function setLanguage(language) {
  const next = String(language).toLowerCase();
  if (next !== 'ru' && next !== 'en') return;
  locale.value = next;
  try { localStorage.setItem(STORAGE_KEY, next); } catch { /* private browsing */ }
}

watch(locale, value => {
  document.documentElement.lang = value;
  document.title = value === 'en' ? defaultTitle.replace('Моментальный обмен валют', 'Instant currency exchange') : defaultTitle;
}, { immediate: true });

window.addEventListener('storage', event => {
  if (event.key === STORAGE_KEY) locale.value = event.newValue === 'en' ? 'en' : 'ru';
});
