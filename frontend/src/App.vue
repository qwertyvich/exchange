<template>
  <div class="appShell" :class="{ homeMotionReady: siteRevealed }">
    <img v-if="route.path === '/'" class="appBackground" src="/_next/static/media/bg.png" alt="" aria-hidden="true" fetchpriority="high" />
    <Header v-if="siteReady" />
    <CasperMascot :active="route.path === '/' && siteRevealed" />

    <div class="appScroll">
      <main class="appContent" :class="{ appContentWithFooter: route.path !== '/' }">
        <RouterView v-if="siteReady" />
      </main>
      <footer v-if="siteReady && route.path !== '/'" class="siteFooter">
        <p>{{ tr("Все права защищены") }}</p>
      </footer>
    </div>

    <!-- GLOBAL LOADER -->
    <Transition name="loaderFade" @after-leave="siteRevealed = true">
      <div
        v-if="!siteReady"
        class="loaderOverlay"
        aria-label="Loading"
        role="status"
      >
        <div class="bootStatus">
          <span class="casperLoader"><CasperFigure /></span>
          <p role="status">{{ tr(siteError) || tr("Загружаем обменник…") }}</p>
          <button v-if="siteError" type="button" @click="bootstrapSite">{{ tr("Повторить") }}</button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { tr, localeTag } from './lib/i18n';
import Header from './components/Header.vue';
import CasperFigure from './components/CasperFigure.vue';
import CasperMascot from './components/CasperMascot.vue';
import { RouterView, useRoute } from 'vue-router';
const route = useRoute();
import { onMounted, ref } from 'vue';
import { siteReady, siteError, bootstrapSite } from './lib/siteState';
const siteRevealed = ref(siteReady.value);
onMounted(bootstrapSite);
</script>

<style>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  overflow: hidden;
  overflow-x: hidden;
  background: #0f172a;

  font-family: Onest, "Onest Fallback", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  font-weight: 400;
}

#app {
  width: 100%;
  height: 100%;
  overflow: hidden;
  overflow-x: hidden;
}

.appBackground { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; pointer-events: none; }
.appShell {
  position: relative;
  width: 100%;
  height: 100dvh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  overflow-x: hidden;
  background: #0f172a;
}

.appScroll {
  flex: 1;
  min-height: 0;
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  scrollbar-width: none;
}
.appScroll::-webkit-scrollbar {
  width: 0;
  height: 0;
}

.appContentWithFooter {
  min-height: 100%;
}

.siteFooter {
  position: relative;
  margin-top: clamp(220px, 30dvh, 400px);
  padding: 8px 24px calc(8px + env(safe-area-inset-bottom, 0px));
  border-top: 1px solid rgba(173, 195, 231, .1);
  background: linear-gradient(135deg, #111e35, #0b1425);
  color: #a3afc4;
  text-align: center;
  font-size: 14px;
  line-height: 1.5;
}
.siteFooter p { margin: 0; }

.bootStatus { text-align: center; color: #fff; }
.bootStatus button { cursor: pointer; padding: 12px 24px; border-radius: 14px; margin-top: 16px; }
@media (min-width: 1280px) and (max-width: 1399px) {
  .siteHeader { column-gap: 12px; }
  .siteHeader > .siteNavigation { position: static; left: auto; translate: none; transform: none; }
}
/* Loader overlay */
.loaderOverlay {
  position: fixed;
  inset: 0;
  z-index: 999999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f172a;
}

.casperLoader { display: block; width: 104px; height: 104px; margin: 0 auto 20px; animation: casper-loading 2.5s ease-in-out infinite; }
@keyframes casper-loading { 0%, 100% { transform: translateY(3px); } 50% { transform: translateY(-5px); } }
@media (prefers-reduced-motion: reduce) { .casperLoader { animation: none; } }

/* smooth fade */
.loaderFade-enter-active,
.loaderFade-leave-active {
  transition: opacity 260ms ease;
}
.loaderFade-enter-from,
.loaderFade-leave-to {
  opacity: 0;
}
.loaderFade-enter-to,
.loaderFade-leave-from {
  opacity: 1;
}
</style>
