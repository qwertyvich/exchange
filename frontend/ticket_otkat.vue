<!-- src/pages/Ticket.vue -->
<template>
  <div class="flex flex-col md:gap-12 gap-9 md:py-24 py-8 max-w-225 w-full self-center grow basis-full container text-white">
    <!-- HEADER -->
    <div class="flex flex-col md:gap-4 gap-3">
      <div class="flex flex-col items-center gap-2">
        <h2 class="md:text-5xl text-[28px] font-medium leading-[120%] text-center">Заявка</h2>
        <p class="md:text-2xl text-base font-medium leading-[130%] text-white/80 text-center break-all">
          #{{ ticketId }}
        </p>
      </div>

      <div class="flex flex-col items-center gap-2">
        <h4 class="md:text-2xl text-xl font-medium leading-[130%] text-text-secondary text-center">
          {{ statusLine }}
        </h4>

        <!-- ✅ без дубля: вторая строка только про время/финал -->
        <p
          class="md:text-xl text-base font-medium leading-[140%] tabular-nums"
          :class="timeLineClass"
        >
          {{ timeLineText }}
        </p>
      </div>
    </div>

    <!-- BODY -->
    <div class="flex flex-col md:gap-6 gap-2">
      <!-- GIVE -> GET -->
      <div class="flex max-md:flex-col items-center md:gap-6 gap-2 relative max-md:mb-2.5">
        <!-- GIVE CARD -->
        <div
          class="flex gap-2 items-center bg-bg-tertiary border border-border-secondary backdrop-blur-xl md:p-8 p-6 md:rounded-[28px] rounded-[22px] md:basis-full w-full"
        >
          <div class="flex gap-4 items-center grow">
            <img
              :alt="ticket?.give?.symbol || 'GIVE'"
              loading="lazy"
              width="36"
              height="36"
              decoding="async"
              class="md:size-9 size-8 object-contain"
              :src="giveIcon"
              style="color: transparent"
            />
            <h3 class="md:text-[32px] text-2xl font-medium leading-[120%]">
              {{ ticket ? formatAmount(ticket.give.amount, ticket.give.symbol) : "—" }}
            </h3>
          </div>
          <span class="md:text-xl text-base font-light leading-[140%] text-text-secondary">
            {{ ticket?.give?.symbol || "" }}
          </span>
        </div>

        <!-- ARROW -->
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
          class="lucide lucide-arrow-right md:size-7 size-13 max-md:border border-border-secondary backdrop-blur-xl shrink-0 max-md:absolute left-1/2 top-1/2 max-md:-translate-x-1/2 max-md:-translate-y-1/2 max-md:rotate-90 max-md:bg-bg-tertiary rounded-[22px] max-md:p-3 z-10 text-white"
          aria-hidden="true"
        >
          <path d="M5 12h14"></path>
          <path d="m12 5 7 7-7 7"></path>
        </svg>

        <!-- GET CARD -->
        <div
          class="flex gap-2 items-center bg-bg-tertiary border border-border-secondary backdrop-blur-xl md:p-8 p-6 md:rounded-[28px] rounded-[22px] md:basis-full w-full"
        >
          <div class="flex gap-4 items-center grow">
            <img
              :alt="ticket?.get?.symbol || 'GET'"
              loading="lazy"
              width="36"
              height="36"
              decoding="async"
              class="md:size-9 size-8 object-contain"
              :src="getIcon"
              style="color: transparent"
            />
            <h3 class="md:text-[32px] text-2xl font-medium leading-[120%]">
              {{ ticket ? formatAmount(ticket.get.amount, ticket.get.symbol) : "—" }}
            </h3>
          </div>
          <span class="md:text-xl text-base font-light leading-[140%] text-text-secondary">
            {{ ticket?.get?.symbol || "" }}
          </span>
        </div>
      </div>

      <!-- SEND ADDRESS -->
      <div
        class="flex items-center md:gap-5 gap-2 bg-bg-inv-tertiary border border-border-secondary backdrop-blur-xl md:p-8 p-6 md:rounded-[28px] rounded-[22px]"
      >
        <div class="flex flex-col gap-2 basis-full">
          <span class="md:text-xl text-base font-light leading-[140%] text-text-secondary">Адрес отправки</span>
          <h4 class="md:text-2xl text-xl font-medium leading-[130%] line-clamp-1 break-all">
            {{ sendAddress || "—" }}
          </h4>
        </div>

        <!-- COPY -->
        <div class="flex gap-2 shrink-0">
          <div class="relative">
            <button type="button" @click="copyAddress" :disabled="!sendAddress">
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
                class="lucide lucide-copy md:size-14 size-11 p-3 bg-bg-secondary hover:bg-bg-secondary-active transition rounded-[18px] cursor-pointer text-white disabled:opacity-40"
                aria-hidden="true"
              >
                <rect width="14" height="14" x="8" y="8" rx="2" ry="2"></rect>
                <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"></path>
              </svg>
            </button>

            <Transition name="copy-fade">
              <div
                v-show="copiedToast"
                class="absolute top-full mt-3 bg-white text-[#0F172A] px-6 py-3 rounded-[18px] shadow-lg text-sm md:text-base font-medium pointer-events-none text-center
                       left-1/2 -translate-x-1/2
                       max-md:max-w-[calc(100vw-24px)] max-md:whitespace-normal
                       md:whitespace-nowrap"
              >
                Адрес скопирован
              </div>
            </Transition>
          </div>
        </div>
      </div>

      <!-- TELEGRAM + PAYOUT -->
      <div class="grid md:grid-cols-2 grid-cols-1 md:gap-6 gap-2">
        <div class="flex flex-col gap-2 basis-full md:p-8 p-6 bg-bg-secondary border border-border-secondary md:rounded-[28px] rounded-[22px]">
          <span class="md:text-xl text-base font-light leading-[140%] text-text-tertiary">Telegram</span>
          <p class="md:text-xl text-base font-medium leading-[140%] break-all">
            {{ ticket?.client?.telegram || "—" }}
          </p>
        </div>

        <div class="flex flex-col gap-2 basis-full md:p-8 p-6 bg-bg-secondary border border-border-secondary md:rounded-[28px] rounded-[22px]">
          <span class="md:text-xl text-base font-light leading-[140%] text-text-tertiary">
            {{ payoutLabel }}
          </span>
          <p class="md:text-xl text-base font-medium leading-[140%] break-all">
            {{ ticket?.client?.payout_details || "—" }}
          </p>
        </div>
      </div>
    </div>

    <!-- ACTIONS -->
    <div class="ticketActions">
      <!-- CANCEL -->
      <button
        class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 shrink-0 outline-none
               text-text-primary border border-border-primary hover:border-border-secondary md:p-6 p-4.5 w-full"
        type="button"
        :disabled="timeState !== 'running' || loadingCancel || ticket?.status !== 'new'"
        @click="cancelTicket"
      >
        <p class="md:text-xl text-base font-medium leading-[140%] px-1">
          {{ loadingCancel ? "Отмена..." : "Отменить сделку" }}
        </p>
      </button>

      <!-- CONFIRM -->
      <button
        class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 shrink-0 outline-none
               bg-bg-inv-primary hover:bg-bg-inv-hover text-text-inv-primary md:p-6 p-4.5 w-full"
        type="button"
        :disabled="timeState !== 'running' || loadingConfirm || ticket?.status !== 'new'"
        @click="confirmTicket"
      >
        <p class="md:text-xl text-base font-medium leading-[140%] px-1">
          {{ loadingConfirm ? "Проверяем..." : "Подтвердить перевод" }}
        </p>
      </button>
    </div>

    <a class="w-fit self-center" target="_blank" href="/contacts">
      <button
        class="inline-flex w-full items-center justify-center gap-1.5 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 text-text-primary hover:text-text-hover data-[state=active]:text-text-active md:p-0 p-0"
      >
        <p class="md:text-xl text-base font-medium leading-[140%] px-1 text-brand hover:text-brand-hover transition duration-150">
          Связаться с поддержкой
        </p>
      </button>
    </a>

    <div v-if="loading" class="text-center text-text-secondary">Загрузка…</div>
    <div v-if="error" class="text-center text-danger">{{ error }}</div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

/**
 * Dictionaries
 */
const currencies = [
  { id: "bitcoin", backendId: 1, symbol: "BTC", name: "Bitcoin", icon: "/img/bit.svg?v=032" },
  { id: "ethereum", backendId: 2, symbol: "ETH", name: "Ethereum", icon: "/img/ether.svg?v=032" },
  { id: "tether", backendId: 3, symbol: "USDT", name: "Tether TRC20", icon: "/img/tether_trc20.svg?v=032" },
  { id: "tether", backendId: 4, symbol: "USDT", name: "Tether ERC20", icon: "/img/tether_erc20.svg?v=032" },
  { id: "dai", backendId: 5, symbol: "DAI", name: "DAI ERC20", icon: "/img/dai.svg?v=032" },
  { id: "usd-coin", backendId: 6, symbol: "USDC", name: "USDC ERC20", icon: "/img/usdc.svg?v=032" },
  { id: "solana", backendId: 7, symbol: "SOL", name: "Solana", icon: "/img/solana-sol-logo.png?v=032" },
  { id: "litecoin", backendId: 8, symbol: "LTC", name: "Litecoin", icon: "/img/lite.svg?v=032" },
  { id: "tron", backendId: 9, symbol: "TRX", name: "TRON", icon: "/img/tron.svg?v=032" },
  { id: "dogecoin", backendId: 10, symbol: "DOGE", name: "Dogecoin", icon: "/img/doge.svg?v=032" },
];

const RUB_METHODS = [
  { id: "rub-sbp", backendId: 2001, symbol: "RUB", name: "СБП", icon: "/img/sbp.svg?v=032", type: "fiat", fiat: "rub", rubKind: "sbp" },
  { id: "rub-qr", backendId: 2011, symbol: "RUB", name: "Сбер QR наличные", icon: "/img/qr_sber.svg?v=032", type: "fiat", fiat: "rub", rubKind: "qr" },
  { id: "rub-sber", backendId: 2002, symbol: "RUB", name: "Сбер", icon: "/img/sber.svg?v=032.svg", type: "fiat", fiat: "rub", rubKind: "card" },
  { id: "rub-alfa", backendId: 2003, symbol: "RUB", name: "Альфа-банк", icon: "/img/alpha.svg?v=032", type: "fiat", fiat: "rub", rubKind: "card" },
  { id: "rub-cash", backendId: 2010, symbol: "RUB", name: "Наличные", icon: "/img/rub_nal.svg?v=032", type: "fiat", fiat: "rub", rubKind: "cash" },
];

const RUB_PLACEHOLDERS = {
  sbp: "Номер телефона и банк",
  card: "Номер карты",
  cash: "Город",
  qr: "Город снятия",
};

const byBackendId = new Map([...currencies, ...RUB_METHODS].map((x) => [x.backendId, x]));

/**
 * Cookie helpers for timer start
 */

/**
 * Route
 */
const route = useRoute();
const ticketId = computed(() => String(route.params.id || ""));

/**
 * State
 */
const ticket = ref(null);
const loading = ref(false);
const error = ref("");

const sendAddress = ref("");
const loadingCancel = ref(false);
const loadingConfirm = ref(false);

const copiedToast = ref(false);
let toastTimer = null;

/**
 * Timer
 */
const timeState = ref("running"); // running | expired | cancelled | confirmed
const totalSeconds = ref(0);
let tmr = null;

const TTL_SECONDS = 3 * 60 * 60;

const stopTimer = () => {
  if (tmr) {
    clearInterval(tmr);
    tmr = null;
  }
};

const parseCreatedAtMs = (v) => {
  if (!v) return NaN;
  const d = new Date(String(v)); // created_at уже с +00:00 (из бэка)
  return d.getTime();
};

const computeRemaining = () => {
  const createdAtMs = parseCreatedAtMs(ticket.value?.created_at);
  if (!Number.isFinite(createdAtMs) || createdAtMs <= 0) return 0;

  const deadline = createdAtMs + TTL_SECONDS * 1000;
  return Math.max(0, Math.floor((deadline - Date.now()) / 1000));
};

const tick = () => {
  const remaining = computeRemaining();
  totalSeconds.value = remaining;

  if (remaining === 0 && ticket.value?.status === "new") {
    timeState.value = "expired";
    stopTimer();
  }
};

const startTimer = () => {
  stopTimer();
  tmr = setInterval(tick, 1000);
  tick();
};

/**
 * Derived
 */
const countdownText = computed(() => {
  const s = Math.max(0, totalSeconds.value);
  const hh = String(Math.floor(s / 3600)).padStart(2, "0");
  const mm = String(Math.floor((s % 3600) / 60)).padStart(2, "0");
  const ss = String(s % 60).padStart(2, "0");
  return `${hh}:${mm}:${ss}`;
});

const statusLine = computed(() => {
  const st = ticket.value?.status || "new";
  if (st === "not_confirmed") return "Ожидайте подтверждения";
  if (st === "new") return "Ожидаем получение средств";
  if (st === "cancelled") return "Сделка отменена";
  if (st === "completed") return "Сделка подтверждена";
  return "В обработке";
});

// ✅ вторая строка (под статусом) — только время/итог, без дубля
const timeLineText = computed(() => {
  if (ticket.value?.status === "not_confirmed") return "";
  if (ticket.value?.status === "completed") return "";// ничего, чтобы не дублировать статус
  if (timeState.value === "running") return countdownText.value;
  if (timeState.value === "expired") return "Время истекло";
  if (timeState.value === "cancelled") return "Отменена";
  return "";
});

const timeLineClass = computed(() => {
  if (ticket.value?.status === "not_confirmed") return "text-transparent";
  if (ticket.value?.status === "completed") return "text-transparent"; // скрыть строку полностью
  return "text-danger";
});

const giveIcon = computed(() => {
  const id = ticket.value?.give?.currency_backend_id;
  return (id && byBackendId.get(id)?.icon) || "/img/bit.svg?v=032";
});

const getIcon = computed(() => {
  const id = ticket.value?.get?.currency_backend_id;
  return (id && byBackendId.get(id)?.icon) || "/img/ether.svg?v=032";
});

const payoutLabel = computed(() => {
  const getId = ticket.value?.get?.currency_backend_id;
  if (!getId) return "Реквизиты";

  const item = byBackendId.get(getId);
  if (!item) return "Реквизиты";

  if (item.fiat === "rub") return RUB_PLACEHOLDERS[item.rubKind] || "Реквизиты";
  return `${ticket.value?.get?.symbol || ""} адрес`;
});

const formatAmount = (v, sym) => {
  const n = Number(v);
  if (!Number.isFinite(n)) return "—";
  const digits = sym === "RUB" ? 2 : 8;
  return n.toLocaleString("en-US", { maximumFractionDigits: digits, useGrouping: false });
};

/**
 * API
 */
const fetchTicket = async () => {
  loading.value = true;
  error.value = "";
  try {
    const res = await fetch(`/api/tickets/${encodeURIComponent(ticketId.value)}`);
    if (!res.ok) {
      const txt = await res.text().catch(() => "");
      error.value = `Ошибка: ${res.status} ${txt}`.slice(0, 250);
      ticket.value = null;
      stopTimer();
      return;
    }

    ticket.value = await res.json();

    if (ticket.value?.status === "cancelled") {
      timeState.value = "cancelled";
      totalSeconds.value = 0;
      stopTimer();
      return;
    }

    if (ticket.value?.status === "completed") {
  // сделка завершена — таймер не показываем/не запускаем
      timeState.value = "completed";     // любое значение, лишь бы != running
      totalSeconds.value = 0;
      stopTimer();
      return;
    }

    if (ticket.value?.status === "not_confirmed") {
      timeState.value = "confirmed";
      totalSeconds.value = 0;
      stopTimer();
      return;
    }

    // running
    timeState.value = "running";
    startTimer();

    if (totalSeconds.value === 0) {
      timeState.value = "expired";
      stopTimer();
    }
  } catch (e) {
    error.value = `Ошибка загрузки: ${String(e)}`.slice(0, 250);
    ticket.value = null;
    stopTimer();
  } finally {
    loading.value = false;
  }
};

const fetchSettings = async () => {
  try {
    const res = await fetch("/api/settings/public");
    if (!res.ok) return;
    const s = await res.json();

    const giveId = ticket.value?.give?.currency_backend_id;
    if (!giveId) return;

    const wallets = s?.deposit_wallets || {};
    const w = wallets[String(giveId)];
    if (w?.address) sendAddress.value = w.address;
  } catch {}
};

const cancelTicket = async () => {
  if (!ticket.value?.id) return;
  if (timeState.value !== "running") return;

  loadingCancel.value = true;
  try {
    const res = await fetch(`/api/tickets/${encodeURIComponent(ticket.value.id)}/cancel`, { method: "PATCH" });
    if (res.ok) {
      ticket.value.status = "cancelled";
      timeState.value = "cancelled";
      totalSeconds.value = 0;
      stopTimer();
    }
  } finally {
    loadingCancel.value = false;
  }
};

const confirmTicket = async () => {
  if (!ticket.value?.id) return;
  if (timeState.value !== "running") return;
  if (ticket.value.status !== "new") return;

  loadingConfirm.value = true;
  try {
    const res = await fetch(`/api/tickets/${encodeURIComponent(ticket.value.id)}/confirm`, { method: "PATCH" });
    if (res.ok) {
      ticket.value.status = "not_confirmed";
      timeState.value = "confirmed";
      totalSeconds.value = 0;
      stopTimer();
    }
  } finally {
    loadingConfirm.value = false;
  }
};

const copyAddress = async () => {
  try {
    if (!sendAddress.value) return;
    await navigator.clipboard.writeText(sendAddress.value);

    copiedToast.value = true;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (copiedToast.value = false), 1800);
  } catch {}
};

onMounted(async () => {
  await fetchTicket();
  await fetchSettings();
});

onBeforeUnmount(() => {
  stopTimer();
  if (toastTimer) clearTimeout(toastTimer);
});
</script>

<style scoped>
.copy-fade-enter-active,
.copy-fade-leave-active {
  transition: opacity 220ms ease;
}
.copy-fade-enter-from,
.copy-fade-leave-to {
  opacity: 0;
}
.copy-fade-enter-to,
.copy-fade-leave-from {
  opacity: 1;
}

.ticketActions {
  width: 100%;
  display: flex;
  flex-direction: column-reverse;
  gap: 8px;
  align-items: stretch;
}
@media (min-width: 768px) {
  .ticketActions {
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 24px;
  }
  .ticketActions > button {
    width: auto;
  }
}
</style>