<template>
  <div class="appShell">
    <img v-if="route.path === '/'" class="appBackground" src="/_next/static/media/bg.png" alt="" aria-hidden="true" fetchpriority="high" />
    <Header v-if="siteReady" />

    <main class="appScroll">
      <RouterView v-if="siteReady" />
    </main>

    <!-- GLOBAL LOADER -->
    <Transition name="loaderFade">
      <div
        v-if="!siteReady"
        class="loaderOverlay"
        aria-label="Loading"
        role="status"
      >
        <div class="bootStatus">
          <img class="loaderGif" src="/img/loading.gif" alt="" width="160" height="160" />
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
import { RouterView, useRoute } from 'vue-router';
const route = useRoute();
import { onMounted } from 'vue';
import { siteReady, siteError, bootstrapSite } from './lib/siteState';
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

.loaderGif {
  width: 160px;
  height: 160px;
  object-fit: contain;
}

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