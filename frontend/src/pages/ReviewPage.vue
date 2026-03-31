<template>
  <div class="flex flex-col md:gap-12 gap-9 md:py-24 py-8 max-w-225 w-full self-center grow basis-full container text-white">
    <div class="flex flex-col gap-3 items-center text-center">
      <h2 class="md:text-5xl text-[28px] font-medium leading-[120%]">Отзывы о сервисе</h2>
    </div>

    <div class="flex max-lg:flex-col md:gap-6 gap-4.5 w-full items-start">
      <!-- LEFT: REVIEWS -->
      <div class="flex flex-col gap-4.5 basis-full min-w-0">
        <div
          v-if="loadingReviews"
          class="text-text-secondary md:text-base text-sm font-light leading-[150%]"
        >
          Загрузка отзывов...
        </div>

        <div
          v-else-if="reviews.length === 0"
          class="text-text-secondary md:text-base text-sm font-light leading-[150%]"
        >
          Пока отзывов нет.
        </div>

        <template v-else>
          <div
            v-for="(review, index) in paginatedReviews"
            :key="`${currentPage}-${index}-${review.name}`"
            class="border border-border-secondary bg-bg-tertiary rounded-[28px] md:px-7 px-5 md:py-6 py-5"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="flex flex-col gap-3 min-w-0 basis-full">
                <p class="md:text-lg text-sm font-light leading-[140%] text-text-primary break-words">
                  {{ review.text }}
                </p>

                <h4 class="md:text-xl text-lg font-medium leading-[130%] break-all">
                  {{ review.name }}
                </h4>
              </div>

              <div class="flex items-center gap-1 shrink-0 pt-1">
                <svg
                  v-for="star in 5"
                  :key="`review-star-${index}-${star}`"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  class="md:size-5 size-4.5"
                  :class="star <= review.mark ? 'text-brand' : 'text-text-tertiary'"
                >
                  <path
                    d="M12 3.6l2.48 5.03 5.55.81-4.01 3.91.95 5.52L12 16.27 7.03 18.87l.95-5.52-4.01-3.91 5.55-.81L12 3.6Z"
                    :fill="star <= review.mark ? 'currentColor' : 'transparent'"
                    stroke="currentColor"
                    stroke-width="1.8"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>
            </div>
          </div>

          <!-- PAGINATION -->
          <div class="min-h-[56px] md:min-h-[64px] flex items-center justify-center">
            <div
              class="flex justify-center items-center md:gap-3 gap-2 md:pt-4 pt-2 flex-wrap"
              :class="totalPages > 1 ? 'opacity-100' : 'opacity-0 pointer-events-none'"
            >
              <button
                type="button"
                class="inline-flex items-center justify-center md:size-14 size-11 rounded-full border border-brand text-text-primary transition-all duration-150 hover:bg-bg-secondary disabled:opacity-30 disabled:pointer-events-none"
                :disabled="currentPage === 1 || totalPages <= 1"
                @click="goToPage(currentPage - 1)"
                aria-label="Предыдущая страница"
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
                  class="md:size-6 size-5"
                  aria-hidden="true"
                >
                  <path d="m15 18-6-6 6-6"></path>
                </svg>
              </button>

              <button
              v-for="page in visiblePages"
              :key="`page-${page}`"
                type="button"
                class="inline-flex items-center justify-center md:size-14 size-11 rounded-full border text-base md:text-lg font-medium transition-all duration-150"
                :class="page === currentPage
                  ? 'border-brand bg-brand text-text-primary shadow-[0_0_26px_rgba(139,123,255,0.45)]'
                  : 'border-brand text-text-primary hover:bg-bg-secondary'"
                @click="goToPage(page)"
              >
                {{ page }}
              </button>

              <button
                type="button"
                class="inline-flex items-center justify-center md:size-14 size-11 rounded-full border border-brand text-text-primary transition-all duration-150 hover:bg-bg-secondary disabled:opacity-30 disabled:pointer-events-none"
                :disabled="currentPage === totalPages || totalPages <= 1"
                @click="goToPage(currentPage + 1)"
                aria-label="Следующая страница"
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
                  class="md:size-6 size-5"
                  aria-hidden="true"
                >
                  <path d="m9 18 6-6-6-6"></path>
                </svg>
              </button>
            </div>
          </div>
        </template>
      </div>

      <!-- RIGHT: LINKS -->
      <div class="flex flex-col md:gap-6 gap-4.5 basis-full lg:max-w-[410px] w-full">
        <div class="px-8 py-7 flex flex-col gap-3 bg-bg-tertiary rounded-[28px] border border-border-secondary">
          <h3 class="md:text-2xl text-xl font-medium leading-[130%]">
            Отзывы на авторитетных площадках
          </h3>

          <p class="md:text-base text-sm font-light leading-[150%] text-text-secondary">
            Вы можете ознакомиться с репутацией сервиса на внешних источниках.
          </p>
        </div>

        <div class="flex flex-col md:gap-4.5 gap-3">
          <a target="_blank" :href="reviewLinks.antiswap" rel="noopener noreferrer">
            <button
              data-slot="button"
              class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 shrink-0 outline-none bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary data-[state=active]:bg-bg-secondary-active md:py-6 py-4.5"
              type="button"
            >
              <p class="md:text-lg text-base font-medium leading-[140%]">Antiswap</p>
            </button>
          </a>

          <a target="_blank" :href="reviewLinks.exnode" rel="noopener noreferrer">
            <button
              data-slot="button"
              class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 shrink-0 outline-none bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary data-[state=active]:bg-bg-secondary-active md:py-6 py-4.5"
              type="button"
            >
              <p class="md:text-lg text-base font-medium leading-[140%]">Exnode</p>
            </button>
          </a>

          <a target="_blank" :href="reviewLinks.kursexpert" rel="noopener noreferrer">
            <button
              data-slot="button"
              class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 shrink-0 outline-none bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary data-[state=active]:bg-bg-secondary-active md:py-6 py-4.5"
              type="button"
            >
              <p class="md:text-lg text-base font-medium leading-[140%]">KursExpert</p>
            </button>
          </a>

          <a target="_blank" :href="reviewLinks.telegram_reviews" rel="noopener noreferrer">
            <button
              data-slot="button"
              class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 shrink-0 outline-none bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary data-[state=active]:bg-bg-secondary-active md:py-6 py-4.5"
              type="button"
            >
              <p class="md:text-lg text-base font-medium leading-[140%]">Telegram отзывы</p>
            </button>
          </a>

          
        </div>
      </div>
    </div>

    <!-- FORM -->
    <div class="w-full bg-bg-tertiary rounded-[28px] border border-border-secondary md:px-8 px-6 md:py-7 py-6">
      <div class="grid lg:grid-cols-2 grid-cols-1 md:gap-6 gap-4.5">
        <div class="flex flex-col gap-4">
          <h3 class="md:text-2xl text-xl font-medium leading-[130%]">
            Оставить свой отзыв
          </h3>

          <div class="flex items-center gap-1">
            <button
              v-for="star in 5"
              :key="`form-star-${star}`"
              type="button"
              class="transition duration-150 hover:scale-105"
              @click="selectedMark = star"
              aria-label="Выбрать оценку"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                class="md:size-6 size-5"
                :class="star <= selectedMark ? 'text-brand' : 'text-text-tertiary'"
              >
                <path
                  d="M12 3.6l2.48 5.03 5.55.81-4.01 3.91.95 5.52L12 16.27 7.03 18.87l.95-5.52-4.01-3.91 5.55-.81L12 3.6Z"
                  :fill="star <= selectedMark ? 'currentColor' : 'transparent'"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linejoin="round"
                />
              </svg>
            </button>
          </div>

          <p class="md:text-base text-sm font-light leading-[150%] text-text-secondary">
            Помогите нам стать лучше!
          </p>
        </div>

        <div class="flex flex-col md:gap-6 gap-4.5">
          <div class="flex flex-col gap-2 grow">
            <div class="relative w-full">
              <input
                v-model.trim="authorName"
                data-slot="input"
                id="review_name"
                placeholder=" "
                class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60"
              >
              <label
                for="review_name"
                class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
              >
                Ваше имя
              </label>
            </div>

            <div class="relative w-full">
              <input
                v-model.trim="username"
                data-slot="input"
                id="review_username"
                placeholder=" "
                class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60"
              >
              <label
                for="review_username"
                class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
              >
                @username Telegram
              </label>
            </div>

            <div class="flex flex-col md:gap-3 gap-2 grow">
              <div class="relative w-full">
                <textarea
                  v-model.trim="message"
                  data-slot="textarea"
                  id="review_text"
                  placeholder=" "
                  class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex min-h-21.5 max-h-64 w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60 h-32.5"
                  style="height: 134px;"
                ></textarea>
                <label
                  for="review_text"
                  class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 bg-bg-primary peer-hover:bg-bg-hover md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-12 md:peer-placeholder-shown:-translate-y-4.5 peer-placeholder-shown:-translate-y-6.5 peer-placeholder-shown:scale-125"
                >
                  Текст отзыва
                </label>
              </div>
            </div>
          </div>

          <button
            data-slot="button"
            class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-brand hover:bg-brand-hover text-text-primary data-[state=active]:bg-brand-active data-[state=active]:text-text-inv-primary md:py-6 py-4.5 max-md:rounded-[22px]"
            type="button"
            :disabled="isSending || !authorName.trim() || !message.trim()"
            @click="sendAsk"
          >
            <p class="md:text-xl text-base font-medium leading-[140%]">
              {{ isSending ? 'Отправка...' : 'Оставить отзыв' }}
            </p>
          </button>
        </div>
      </div>
    </div>
  </div>

  <Teleport to="body">
    <Transition name="toastSmooth">
      <div
        v-if="toastVisible"
        class="fixed inset-0 z-[9999] flex items-center justify-center pointer-events-none"
        role="status"
        aria-live="polite"
      >
        <div
          class="px-9 py-2.4 rounded-[22px] text-white text-lg md:text-xl font-semibold shadow-lg"
          style="background:#3b82f6;"
        >
          ㅤ{{ toastText }}ㅤ
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";

const REVIEWS_PER_PAGE = 5;

const authorName = ref("");
const username = ref("");
const message = ref("");
const isSending = ref(false);
const selectedMark = ref(0);

const publicSettings = ref({});
const reviews = ref([]);
const loadingReviews = ref(false);
const currentPage = ref(1);

const info = computed(() => publicSettings.value?.info || {});

const telegramChannelLink = computed(() => {
  const u = info.value?.Telegram_chanel || "";
  if (!u) return "#";
  return u.startsWith("http") ? u : `https://t.me/${u.replace("@", "")}`;
});

const reviewLinks = ref({
  antiswap: "#",
  exnode: "#",
  kursexpert: "#",
  telegram_reviews: "#",
});

const toastVisible = ref(false);
const toastText = ref("Скопировано");
let timer = null;

function showToast(text) {
  toastText.value = text;
  toastVisible.value = true;

  if (timer) clearTimeout(timer);
  timer = setTimeout(() => {
    toastVisible.value = false;
  }, 1600);
}

async function loadPublicSettings() {
  try {
    const res = await fetch("/api/settings/public", { method: "GET" });
    if (!res.ok) return;

    const data = await res.json();
    publicSettings.value = data || {};
  } catch {
    // молча
  }
}

async function loadReviews() {
  loadingReviews.value = true;

  try {
    const res = await fetch("/api/reviews/public", { method: "GET" });
    if (!res.ok) {
      reviews.value = [];
      return;
    }

    const data = await res.json();

    reviews.value = Array.isArray(data)
      ? data.map((item) => ({
          name: String(item?.name || "").trim(),
          text: String(item?.text || "").trim(),
          mark: Math.min(5, Math.max(1, Number(item?.mark || 0))),
        })).filter((item) => item.name && item.text)
      : [];
  } catch {
    reviews.value = [];
  } finally {
    loadingReviews.value = false;
  }
}

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(reviews.value.length / REVIEWS_PER_PAGE));
});

const paginatedReviews = computed(() => {
  const start = (currentPage.value - 1) * REVIEWS_PER_PAGE;
  return reviews.value.slice(start, start + REVIEWS_PER_PAGE);
});

const visiblePages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  const windowSize = 5;

  if (total <= windowSize) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }

  let start = current - 2;
  let end = current + 2;

  if (start < 1) {
    start = 1;
    end = windowSize;
  }

  if (end > total) {
    end = total;
    start = total - windowSize + 1;
  }

  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
});

function goToPage(page) {
  const safePage = Math.min(totalPages.value, Math.max(1, Number(page) || 1));
  currentPage.value = safePage;
}

watch(totalPages, (pages) => {
  if (currentPage.value > pages) currentPage.value = pages;
});

async function sendAsk() {
  if (!authorName.value.trim() || !message.value.trim() || isSending.value) return;

  isSending.value = true;

  try {
    const composedMessage =
      `Новый отзыв с сайта\n` +
      `Имя: ${authorName.value.trim()}\n` +
      `Оценка: ${selectedMark.value || 0}/5\n` +
      `Отзыв: ${message.value.trim()}`;

    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value.trim() || "@unknown",
        message: composedMessage,
      }),
    });

    if (!res.ok) {
      const t = await res.text();
      throw new Error(t || `HTTP ${res.status}`);
    }

    authorName.value = "";
    username.value = "";
    message.value = "";
    selectedMark.value = 0;

    showToast("Отправлено");
  } catch (e) {
    console.error("sendAsk error:", e);
    showToast("Ошибка");
  } finally {
    isSending.value = false;
  }
}

onMounted(() => {
  loadPublicSettings();
  loadReviews();
});
</script>

<style scoped>
.toastSmooth-enter-active,
.toastSmooth-leave-active {
  transition: opacity 420ms ease, transform 420ms ease;
}

.toastSmooth-enter-from,
.toastSmooth-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.98);
}

.toastSmooth-enter-to,
.toastSmooth-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}
</style>