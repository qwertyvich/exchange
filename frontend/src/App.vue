<template>
  <div class="appShell">
    <Header />

    <main class="appScroll">
      <RouterView />
    </main>

    <!-- GLOBAL LOADER -->
    <Transition name="loaderFade">
      <div
        v-if="showLoader"
        class="loaderOverlay"
        aria-label="Loading"
        role="status"
      >
        <img
          class="loaderGif"
          :src="loaderSrc"
          alt="Loading..."
          loading="eager"
          decoding="async"
        />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import Header from "./components/Header.vue";
import { RouterView, useRouter } from "vue-router";
import { onMounted, ref } from "vue";

/**
 * Путь к твоей гифке:
 * положи её в /public/img/loading.gif -> "/img/loading.gif"
 */
const loaderSrc = "/img/loading.gif";

const showLoader = ref(true);
const router = useRouter();

// минимальное время показа (чтобы не мигало)
const MIN_MS = 1000;

const hideWithMinDelay = (startedAt) => {
  const elapsed = Date.now() - startedAt;
  const wait = Math.max(0, MIN_MS - elapsed);
  setTimeout(() => (showLoader.value = false), wait);
};

onMounted(() => {
  // Первый вход: показываем загрузку коротко и плавно скрываем
  const t0 = Date.now();
  // даём DOM/стилям и первой странице отрендериться
  requestAnimationFrame(() => {
    requestAnimationFrame(() => hideWithMinDelay(t0));
  });

  // (опционально) показывать лоадер при смене страниц
  router.beforeEach((to, from, next) => {
    // если хочешь только на главной — раскомментируй if
    if (to.path !== "/") return next();

    showLoader.value = true;
    next();
  });

  router.afterEach(() => {
    const t = Date.now();
    // чуть позже скрываем, чтобы не было "дёргания"
    setTimeout(() => hideWithMinDelay(t), 0);
  });
});
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

.appShell {
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