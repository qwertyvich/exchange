<template>
  <details ref="details" class="languageMenu" data-language-menu @click.stop @toggle="measure">
    <summary ref="trigger" :aria-label="tr('Выбрать язык')" :style="{ '--option-height': `${height}px` }">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6" /></svg>
      <span>{{ currentLanguage }}</span>
    </summary>
    <div class="languageOptions" role="group" :aria-label="tr('Язык сайта')" :style="{ '--option-height': `${height}px` }">
      <button v-for="language in ['ru', 'en']" :key="language" type="button" :lang="language" :aria-pressed="locale === language" @click="select(language)">{{ language.toUpperCase() }}</button>
    </div>
  </details>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { currentLanguage, locale, setLanguage, tr } from '../lib/i18n';
const details = ref(null), trigger = ref(null), height = ref(48);
let observer;
function measure() { if (trigger.value) height.value = trigger.value.getBoundingClientRect().height; }
function close() { if (details.value) details.value.open = false; }
function select(language) { setLanguage(language); close(); }
function outside(event) { if (!details.value?.contains(event.target)) close(); }
function keydown(event) { if (event.key === 'Escape') close(); }
onMounted(() => {
  observer = new ResizeObserver(measure); observer.observe(trigger.value); measure();
  document.addEventListener('pointerdown', outside, true);
  document.addEventListener('keydown', keydown);
});
onBeforeUnmount(() => {
  observer?.disconnect(); document.removeEventListener('pointerdown', outside, true); document.removeEventListener('keydown', keydown);
});
defineExpose({ close });
</script>

<style scoped>
.languageMenu{font-size:14px;position:relative;flex-shrink:0;color:var(--color-text-primary,#f3f4f8)}
summary{display:flex;align-items:center;justify-content:center;gap:6px;list-style:none;cursor:pointer;border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:12px;font-size:14px;font-weight:500;line-height:21px;background:rgba(255,255,255,.035)}
summary::-webkit-details-marker{display:none}summary svg{color:#9297a3;transition:transform .15s}summary span{padding:0 6px;min-width:32px;text-align:center;box-sizing:border-box}
details[open] summary svg{transform:rotate(180deg)}summary:hover{background:rgba(255,255,255,.07)}summary:focus-visible,button:focus-visible{outline:2px solid #a494f6;outline-offset:2px}
.languageOptions{position:absolute;top:calc(100% + 8px);left:0;right:0;width:100%;box-sizing:border-box;z-index:100;border:1px solid rgba(255,255,255,.1);border-radius:14px;overflow:hidden;background:#1c2536;box-shadow:0 12px 30px #050b1833}
.languageOptions button{display:flex;align-items:center;justify-content:center;box-sizing:border-box;width:100%;height:var(--option-height);padding:0;border:0;color:inherit;background:transparent;font-size:inherit;cursor:pointer;line-height:1}
.languageOptions button:hover,.languageOptions button[aria-pressed=true]{background:rgba(255,255,255,.055)}
@media(min-width:768px){.languageMenu{font-size:16px}summary{font-size:16px;line-height:24px}}
@media(min-width:1280px){summary{padding:16px;border-radius:18px}.languageOptions{border-radius:18px}}
</style>
