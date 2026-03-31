<!-- Header.vue -->
<template>
  <header class="relative flex justify-between xl:px-12 xl:pt-12 p-4 z-50">
    <!-- LEFT: logo + controls -->
    <div
      class="flex xl:gap-4 max-xl:justify-between gap-7.5 p-3 xl:rounded-[26px] rounded-[22px] bg-bg-tertiary border border-border-secondary max-xl:w-full"
    >
      <RouterLink to="/" class="min-w-0 shrink">
        <img
          alt="logo"
          loading="lazy"
          width="2024"
          height="561"
          decoding="async"
          class="max-h-14 w-auto max-w-full max-xl:max-w-[150px]"
          style="color:transparent"
          src="/_next/static/media/logo-name.webp"
        />
      </RouterLink>

      <div class="ml-auto flex items-center gap-2 shrink-0">
        <!-- Language (desktop) -->
        <details ref="langDetails" class="relative group" @click.stop>
          <summary
            class="list-none cursor-pointer inline-flex items-center justify-center gap-1.5 whitespace-nowrap text-sm font-medium transition-all duration-150 bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary outline-none xl:p-4 p-3 xl:rounded-[18px] rounded-[14px]"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="lucide lucide-chevron-down text-text-tertiary size-4.5 transition-transform duration-150 group-open:rotate-180"
              aria-hidden="true"
            >
              <path d="m6 9 6 6 6-6"></path>
            </svg>
            <p class="md:text-base text-sm font-medium leading-[150%] px-1.5">{{ currentLang }}</p>
          </summary>

          <div class="absolute right-0 mt-2 w-[120px] rounded-[18px] bg-bg-tertiary border border-border-secondary p-2 z-50">
            <button
              type="button"
              class="w-full text-left px-4 py-2 rounded-[14px] hover:bg-bg-secondary-hover text-text-primary"
              @click="setLang('RU')"
            >
              RU
            </button>
            <button
              type="button"
              class="w-full text-left px-4 py-2 rounded-[14px] hover:bg-bg-secondary-hover text-text-primary"
              @click="setLang('EN')"
            >
              EN
            </button>
          </div>
        </details>

        <!-- Burger / X (mobile) -->
        <button
          :class="[
            'inline-flex items-center justify-center gap-1.5 whitespace-nowrap text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none bg-bg-secondary hover:bg-bg-secondary-hover border border-border-primary size-11 p-2 xl:hidden rounded-[14px]',
            isMobileMenuOpen ? 'text-white' : 'text-text-primary',
          ]"
          type="button"
          aria-haspopup="dialog"
          :aria-expanded="isMobileMenuOpen ? 'true' : 'false'"
          @click="toggleMobileMenu"
        >
          <svg
            v-if="!isMobileMenuOpen"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="lucide lucide-menu size-7"
            aria-hidden="true"
          >
            <path d="M4 12h16"></path>
            <path d="M4 18h16"></path>
            <path d="M4 6h16"></path>
          </svg>

          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="lucide lucide-x size-7"
            aria-hidden="true"
          >
            <path d="M18 6 6 18"></path>
            <path d="M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- CENTER NAV (desktop) -->
    <div
    class="absolute left-1/2 -translate-x-1/2 flex gap-2 p-3 rounded-[26px] bg-bg-tertiary border border-border-secondary max-xl:hidden"
    >
    <RouterLink to="/" :class="navBase" exact-active-class="bg-bg-secondary-active border-border-active">
        <p class="md:text-base text-sm font-medium leading-[150%]">Обмен</p>
    </RouterLink>

    <RouterLink to="/faq" :class="navBase" active-class="bg-bg-secondary-active border-border-active">
        <p class="md:text-base text-sm font-medium leading-[150%]">FAQ</p>
    </RouterLink>

    <RouterLink to="/contacts" :class="navBase" active-class="bg-bg-secondary-active border-border-active">
        <p class="md:text-base text-sm font-medium leading-[150%]">Контакты</p>
    </RouterLink>

    <RouterLink to="/guide" :class="navBase" active-class="bg-bg-secondary-active border-border-active">
        <p class="md:text-base text-sm font-medium leading-[150%]">Инструкция</p>
    </RouterLink>

    <RouterLink to="/review" :class="navBase" active-class="bg-bg-secondary-active border-border-active">
        <p class="md:text-base text-sm font-medium leading-[150%]">Отзывы</p>
    </RouterLink>
    </div>

    <!-- RIGHT AUTH (desktop) -->
<div class="flex *:grow-0 *:shrink gap-2 p-3 rounded-[26px] bg-bg-tertiary border border-border-secondary max-xl:hidden">
  <!-- NOT AUTH -->
  <template v-if="!user">
    <RouterLink
      to="/login"
      class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none bg-bg-inv-primary hover:bg-bg-inv-hover text-text-inv-primary rounded-[18px] py-4 px-5"
    >
      <p class="md:text-base text-sm font-medium leading-[150%]">Вход</p>
    </RouterLink>

    <RouterLink
      to="/registration"
      class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none text-text-primary border border-border-primary hover:border-border-secondary rounded-[18px] py-4 px-5"
    >
      <p class="md:text-base text-sm font-medium leading-[150%]">Регистрация</p>
    </RouterLink>
  </template>

  <!-- AUTH -->
  <template v-else>
    <!-- имя (в стиле кнопки "Вход") -->
    <RouterLink
      to="/profile"
      class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none bg-bg-inv-primary hover:bg-bg-inv-hover text-text-inv-primary rounded-[18px] py-4 px-5"
    >
      <p class="md:text-base text-sm font-medium leading-[150%]">{{ user.name }}</p>
    </RouterLink>

    <!-- выйти -->
    <button
      type="button"
      @click="logout"
      class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none text-text-primary border border-border-primary hover:border-border-secondary rounded-[18px] py-4 px-5"
    >
      <p class="md:text-base text-sm font-medium leading-[150%]">Выйти</p>
    </button>
  </template>
</div>

    <!-- ✅ MOBILE MENU (как в оригинале: шапка отдельным блоком, потом отступ, потом кнопки) -->
    <Teleport to="body">
      <Transition name="overlayFade">
        <div v-if="isMobileMenuOpen" class="fixed inset-0 z-[9000]" @click.self="closeMobileMenu">
          <div class="absolute inset-0 bg-black/25"></div>

          <Transition name="slideDown">
            <div class="relative mx-4 mt-4">
              <!-- BLOCK 1: header bar -->
              <div class="rounded-[26px] bg-bg-tertiary border border-border-secondary p-3">
                <div class="flex items-center justify-between">
                  <RouterLink to="/" class="flex items-center gap-3 min-w-0" @click="closeMobileMenu">
                    <img
                      alt="logo"
                      loading="lazy"
                      width="2024"
                      height="561"
                      decoding="async"
                      class="max-h-14 w-auto max-w-full max-xl:max-w-[150px]"
                      style="color:transparent"
                      src="/_next/static/media/logo-name.webp"
                    />
                  </RouterLink>

                  <div class="flex items-center gap-2 shrink-0">
                    <!-- language (mobile) same style -->
                    <details ref="langDetailsMobile" class="relative group" @click.stop>
                      <summary
                        class="list-none cursor-pointer inline-flex items-center justify-center gap-1.5 whitespace-nowrap text-sm font-medium transition-all duration-150 bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary outline-none p-3 rounded-[14px]"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          class="lucide lucide-chevron-down text-text-tertiary size-4.5 transition-transform duration-150 group-open:rotate-180"
                          aria-hidden="true"
                        >
                          <path d="m6 9 6 6 6-6"></path>
                        </svg>
                        <p class="text-sm font-medium leading-[150%] px-1.5">{{ currentLang }}</p>
                      </summary>

                      <div class="absolute right-0 mt-2 w-[120px] rounded-[18px] bg-bg-tertiary border border-border-secondary p-2 z-50">
                        <button
                          type="button"
                          class="w-full text-left px-4 py-2 rounded-[14px] hover:bg-bg-secondary-hover text-text-primary"
                          @click="setLang('RU')"
                        >
                          RU
                        </button>
                        <button
                          type="button"
                          class="w-full text-left px-4 py-2 rounded-[14px] hover:bg-bg-secondary-hover text-text-primary"
                          @click="setLang('EN')"
                        >
                          EN
                        </button>
                      </div>
                    </details>

                    <!-- close -->
                    <button
                      class="inline-flex items-center justify-center size-11 rounded-[14px] bg-bg-secondary/40 hover:bg-bg-secondary/55 border border-white/25 text-white shrink-0"
                      type="button"
                      aria-label="Закрыть меню"
                      @click="closeMobileMenu"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="22"
                        height="22"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="lucide lucide-x"
                        aria-hidden="true"
                      >
                        <path d="M18 6 6 18"></path>
                        <path d="M6 6l12 12"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <!-- spacing like original -->
              <div class="h-4"></div>

              <!-- BLOCK 2: nav + auth -->
              <div class="rounded-[26px] bg-bg-tertiary border border-border-secondary p-3">
                <div class="grid gap-2">
                <RouterLink to="/" :class="mobileNavBase" exact-active-class="bg-bg-secondary-active border-border-active" @click="closeMobileMenu">
                    Обмен
                </RouterLink>

                <RouterLink to="/faq" :class="mobileNavBase" active-class="bg-bg-secondary-active border-border-active" @click="closeMobileMenu">
                    FAQ
                </RouterLink>

                <RouterLink to="/contacts" :class="mobileNavBase" active-class="bg-bg-secondary-active border-border-active" @click="closeMobileMenu">
                    Контакты
                </RouterLink>

                <RouterLink to="/guide" :class="mobileNavBase" active-class="bg-bg-secondary-active border-border-active" @click="closeMobileMenu">
                    Инструкция
                </RouterLink>

                <RouterLink to="/review" :class="mobileNavBase" active-class="bg-bg-secondary-active border-border-active" @click="closeMobileMenu">
                    Отзывы
                </RouterLink>
                </div>

                <div class="mt-2 p-3 rounded-[22px] bg-bg-tertiary border border-border-secondary">
                  <div class="grid grid-cols-2 gap-2">
                <!-- NOT AUTH -->
                <template v-if="!user">
                  <RouterLink
                    to="/login"
                    class="w-full rounded-[18px] py-4 px-5 bg-bg-inv-primary hover:bg-bg-inv-hover text-text-inv-primary font-medium text-center"
                    @click="closeMobileMenu"
                  >
                    Вход
                  </RouterLink>

                  <RouterLink
                    to="/registration"
                    class="w-full rounded-[18px] py-4 px-5 border border-border-primary hover:border-border-secondary text-text-primary font-medium text-center"
                    @click="closeMobileMenu"
                  >
                    Регистрация
                  </RouterLink>
                </template>

                <!-- AUTH -->
                <template v-else>
                  <RouterLink
                    to="/profile"
                    class="w-full rounded-[18px] py-4 px-5 bg-bg-inv-primary hover:bg-bg-inv-hover text-text-inv-primary font-medium text-center"
                    @click="closeMobileMenu"
                  >
                    {{ user.name }}
                  </RouterLink>

                  <button
                    type="button"
                    class="w-full rounded-[18px] py-4 px-5 border border-border-primary hover:border-border-secondary text-text-primary font-medium text-center"
                    @click="logout"
                  >
                    Выйти
                  </button>
                </template>
              </div>
                </div>
              </div>

            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </header>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";
import { onBeforeUnmount, onMounted, ref, watch } from "vue";

const isMobileMenuOpen = ref(false);
const router = useRouter();
const user = ref(null); // null или {id,name,email,role,is_superuser}

function getToken() {
  return localStorage.getItem("token") || "";
}

async function loadMe() {
  const token = getToken();
  if (!token) {
    user.value = null;
    return;
  }

  try {
    const res = await fetch("/api/me", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) {
      // токен истёк/битый
      localStorage.removeItem("token");
      user.value = null;
      return;
    }

    user.value = await res.json();
  } catch (e) {
    user.value = null;
  }
}

function logout() {
  localStorage.removeItem("token");
  user.value = null;
  closeMobileMenu();
  router.push("/");
}

// language
const currentLang = ref("RU");
const langDetails = ref(null);
const langDetailsMobile = ref(null);

function closeLangAll() {
  if (langDetails.value) langDetails.value.open = false;
  if (langDetailsMobile.value) langDetailsMobile.value.open = false;
}

function setLang(lang) {
  currentLang.value = lang;
  closeLangAll();
}

onMounted(() => document.addEventListener("click", closeLangAll));
onBeforeUnmount(() => document.removeEventListener("click", closeLangAll));

onMounted(loadMe);

// слушаем событие от LoginPage.vue, чтобы обновлять имя сразу
function onAuthChanged() {
  loadMe();
}
onMounted(() => window.addEventListener("auth-changed", onAuthChanged));
onBeforeUnmount(() => window.removeEventListener("auth-changed", onAuthChanged));

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
}
function closeMobileMenu() {
  isMobileMenuOpen.value = false;
  closeLangAll();
}

function onKeydown(e) {
  if (e.key === "Escape") closeMobileMenu();
}

function syncOverlayClass() {
  document.body.classList.toggle("overlay-open", isMobileMenuOpen.value);
}

onMounted(() => {
  window.addEventListener("keydown", onKeydown);
  syncOverlayClass();
});
onBeforeUnmount(() => {
  window.removeEventListener("keydown", onKeydown);
  document.body.classList.remove("overlay-open");
});

watch(isMobileMenuOpen, syncOverlayClass);

const navBase =
  "inline-flex items-center justify-center gap-1.5 p-4 whitespace-nowrap text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none rounded-[18px] py-4 px-5 border border-border-primary bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary";

const mobileNavBase =
  "w-full rounded-[18px] py-4 px-5 border border-border-primary font-medium transition-all duration-150 bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary text-center";

  
</script>

<style scoped>
details > summary::-webkit-details-marker {
  display: none;
}
details > summary {
  list-style: none;
}

/* overlay fade */
.overlayFade-enter-active,
.overlayFade-leave-active {
  transition: opacity 150ms ease;
}
.overlayFade-enter-from,
.overlayFade-leave-to {
  opacity: 0;
}

/* menu slide down */
.slideDown-enter-active,
.slideDown-leave-active {
  transition: transform 180ms ease, opacity 180ms ease;
}
.slideDown-enter-from,
.slideDown-leave-to {
  transform: translateY(-14px);
  opacity: 0;
}
</style>

<style>
/* blur background + disable clicks on app (overlay stays clickable because teleported outside #app) */
body.overlay-open #app {
  filter: blur(10px);
  pointer-events: none;
}
body.overlay-open {
  overflow: hidden;
}
</style>