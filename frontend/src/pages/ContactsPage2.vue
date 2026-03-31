<template>
  <div class="flex flex-col items-center md:gap-12 gap-9 md:py-24 py-8 max-w-225 w-full self-center grow basis-full container text-white">
    <h2 class="md:text-5xl text-[28px] font-medium leading-[120%]">Связаться с нами</h2>

    <div class="flex max-md:flex-col md:gap-6 gap-4.5 w-full">
      <div class="flex flex-col md:gap-6 gap-4.5 basis-full">
        <div class="flex flex-col md:gap-4.5 gap-3">
          <a target="_blank" :href="telegramOperLink" rel="noopener noreferrer">
  <button
    data-slot="button"
    class="inline-flex w-full items-center justify-center gap-3 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary data-[state=active]:bg-bg-secondary-active md:py-6 py-4.5"
    type="button"
  >
    <img :src="telegaIcon" alt="Telegram" class="size-5 md:size-6 object-contain shrink-0" />
    <p class="md:text-xl text-base font-medium leading-[140%]">Telegram</p>
  </button>
</a>

          <a target="_blank" :href="telegramChannelLink" rel="noopener noreferrer">
            <button
              data-slot="button"
              class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&amp;_svg]:pointer-events-none shrink-0 [&amp;_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary data-[state=active]:bg-bg-secondary-active md:py-6 py-4.5"
              type="button"
            >
            <img :src="telegaIcon" alt="Telegram" class="size-5 md:size-6 object-contain shrink-0" />
              <p class="md:text-xl text-base font-medium leading-[140%]">Telegram-канал</p>
            </button>
          </a>

          <!-- Session -->
          <button
                data-slot="tooltip-trigger"
                class="inline-flex w-full items-center justify-center gap-3 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary data-[state=active]:bg-bg-secondary-active md:py-6 py-4.5"
                type="button"
                data-state="closed"
                @click="copy('session')"
                >
                <img :src="whatsIcon" alt="WhatsApp" class="size-5 md:size-6 object-contain shrink-0" />
                <p class="md:text-xl text-base font-medium leading-[140%]">WhatsApp</p>
                </button>

          <!-- TOX -->
          
        </div>

        <div class="px-8 py-7 flex items-center gap-4 text-text-secondary bg-bg-tertiary rounded-[28px] border border-border-secondary">
          <h4 class="md:text-2xl text-xl font-medium leading-[130%] basis-full">24/7</h4>
          <span class="md:text-base text-sm font-light leading-[150%] shrink-0">Режим работы</span>
        </div>
      </div>

      <div class="px-8 py-7 flex flex-col md:gap-6 gap-4.5 bg-bg-tertiary rounded-[28px] border border-border-secondary basis-full">
        <div class="flex flex-col gap-2 grow">
          <div class="relative w-full">
            <input
              v-model.trim="username"
              data-slot="input"
              id="_r_66_"
              placeholder=" "
              class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60"
            >
            <label
              for="_r_66_"
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
                id="_r_67_"
                placeholder=" "
                class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex min-h-21.5 max-h-64 w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60 h-32.5"
                style="height: 134px;"
              ></textarea>
              <label
                for="_r_67_"
                class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 bg-bg-primary peer-hover:bg-bg-hover md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-12 md:peer-placeholder-shown:-translate-y-4.5 peer-placeholder-shown:-translate-y-6.5 peer-placeholder-shown:scale-125"
              >
                Что вас интересует?
              </label>
            </div>
          </div>
        </div>

        <button
          data-slot="button"
          class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&amp;_svg]:pointer-events-none shrink-0 [&amp;_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-brand hover:bg-brand-hover text-text-primary data-[state=active]:bg-brand-active data-[state=active]:text-text-inv-primary md:py-6 py-4.5 max-md:rounded-[22px]"
          type="button"
          :disabled="isSending || !message.trim()"
          @click="sendAsk"
        >
          <p class="md:text-xl text-base font-medium leading-[140%]">
            {{ isSending ? 'Отправка...' : 'Отправить' }}
          </p>
        </button>
      </div>
    </div>
  </div>

  <!-- Toast -->
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
import { computed, onMounted, ref } from "vue";
import telegaIcon from "/img/telega.svg";
import whatsIcon from "/img/whats.svg";

// ===== Form state =====
const username = ref("");
const message = ref("");
const isSending = ref(false);

// ===== Public settings (settings.json -> /api/settings/public) =====
const publicSettings = ref({});

const info = computed(() => publicSettings.value?.info || {});

const telegramOperLink = computed(() => {
  const u = info.value?.Telegram_oper || "";
  if (!u) return "https://t.me/";
  return u.startsWith("http") ? u : `https://t.me/${u.replace("@", "")}`;
});

const telegramChannelLink = computed(() => {
  const u = info.value?.Telegram_chanel || "";
  if (!u) return "https://t.me/";
  return u.startsWith("http") ? u : `https://t.me/${u.replace("@", "")}`;
});

// ===== Copy data (впиши реальные значения) =====
const COPY_DATA = ref({
  session: "",
  tox: "",
});

// ===== Toast =====
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

// ===== Copy to clipboard =====
async function copy(key) {
  const text = COPY_DATA.value[key];
  if (!text) {
    showToast("Нет данных");
    return;
  }

  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      showToast("Скопировано");
      return;
    }
  } catch (e) {
    // fallback below
  }

  try {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand("copy");
    document.body.removeChild(ta);

    showToast(ok ? "Скопировано" : "Не удалось");
  } catch (_) {
    showToast("Не удалось");
  }
}

// ===== Send to backend =====
async function sendAsk() {
  if (!message.value.trim() || isSending.value) return;

  isSending.value = true;

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value.trim() || "@unknown",
        message: message.value.trim(),
      }),
    });

    if (!res.ok) {
      const t = await res.text();
      throw new Error(t || `HTTP ${res.status}`);
    }

    username.value = "";
    message.value = "";

    showToast("Отправлено");
  } catch (e) {
    console.error("sendAsk error:", e);
    showToast("Ошибка");
  } finally {
    isSending.value = false;
  }
}

async function loadPublicSettings() {
  try {
    const res = await fetch("/api/settings/public", { method: "GET" });
    if (!res.ok) return;

    const data = await res.json();
    publicSettings.value = data || {};

    // прокидываем значения для копирования
    COPY_DATA.value.session = data?.info?.Session_id || "";
    COPY_DATA.value.tox = data?.info?.Tox || "";
  } catch {
    // молча
  }
}

onMounted(() => {
  loadPublicSettings();
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