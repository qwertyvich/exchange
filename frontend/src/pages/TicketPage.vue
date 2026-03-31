<!-- src/pages/TicketPage.vue -->
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

      <!-- SPECIAL BLOCK FOR 2101 -->
      <template v-if="isFiatCardTransferGive">
        <!-- CARD / CONTACT -->
        <div
  class="flex items-center md:gap-5 gap-2 bg-bg-inv-tertiary border border-border-secondary backdrop-blur-xl md:p-8 p-6 md:rounded-[28px] rounded-[22px]"
>
  <div class="flex flex-col gap-2 basis-full min-w-0">
    <span class="md:text-xl text-base font-light leading-[140%] text-text-secondary">
      {{ hasMatchedFiatCard ? "Номер карты для перевода" : "Для получения реквизитов свяжитесь с поддержкой" }}
    </span>

    <h4
      v-if="hasMatchedFiatCard"
      class="md:text-2xl text-xl font-medium leading-[130%] break-all"
    >
      {{ matchedFiatInRow.card_id }}
    </h4>

    <a
      v-else-if="managerTelegramHref"
      :href="managerTelegramHref"
      target="_blank"
      rel="noopener noreferrer"
      class="md:text-2xl text-xl font-medium leading-[130%] break-all text-brand hover:text-brand-hover underline"
    >
      {{ managerTelegram }}
    </a>

    <h4
      v-else
      class="md:text-2xl text-xl font-medium leading-[130%] break-all"
    >
      Контакт не указан
    </h4>
  </div>

  <div v-if="canCopyFiatTarget" class="flex gap-2 shrink-0">
            <div class="relative">
              <button type="button" @click="copyAddress">
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
                  class="lucide lucide-copy md:size-14 size-11 p-3 bg-bg-secondary hover:bg-bg-secondary-active transition rounded-[18px] cursor-pointer text-white"
                  aria-hidden="true"
                >
                  <rect width="14" height="14" x="8" y="8" rx="2" ry="2"></rect>
                  <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"></path>
                </svg>
              </button>

              <Transition name="copy-fade">
                <div
                  v-show="copiedToast"
                  class="absolute top-full mt-3 bg-white text-[#0F172A] px-6 py-3 rounded-[18px] shadow-lg text-sm md:text-base font-medium pointer-events-none text-center left-1/2 -translate-x-1/2 max-md:max-w-[calc(100vw-24px)] max-md:whitespace-normal md:whitespace-nowrap"
                >
                  {{ copyToastText }}
                </div>
              </Transition>
            </div>
          </div>
        </div>

        <!-- BANK DETAILS -->
        <div
          v-if="hasMatchedFiatCard"
          class="flex flex-col gap-4 bg-bg-secondary border border-border-secondary md:p-8 p-6 md:rounded-[28px] rounded-[22px]"
        >
          <div class="flex flex-col gap-3">
            <div class="flex flex-col gap-1">
              <span class="md:text-xl text-base font-light leading-[140%] text-text-tertiary">Банк</span>
              <p class="md:text-xl text-base font-medium leading-[140%] break-all">
                {{ matchedFiatInRow.bank_name || "—" }}
              </p>
            </div>

            <div class="flex flex-col gap-1">
              <span class="md:text-xl text-base font-light leading-[140%] text-text-tertiary">ФИО получателя</span>
              <p class="md:text-xl text-base font-medium leading-[140%] break-all">
                {{ matchedFiatInRow.fio || "—" }}
              </p>
            </div>

            <div class="flex flex-col gap-1">
              <span class="md:text-xl text-base font-light leading-[140%] text-text-tertiary">Важно</span>
              <p class="md:text-xl text-base font-medium leading-[140%]">
                После оплаты прикрепите фото развёрнутого чека о переводе
              </p>
            </div>
          </div>

          <!-- FILE PICKER -->
          <div class="flex justify-center">
            <label
              v-if="!uploadedPreviewUrl"
              :class="[
                'inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 shrink-0 outline-none bg-bg-secondary text-text-primary border border-border-primary md:p-6 p-4.5 w-full md:w-fit max-md:rounded-[22px]',
                isFileLocked ? 'opacity-50 cursor-not-allowed pointer-events-none' : 'hover:bg-bg-secondary-hover cursor-pointer'
              ]"
            >
              <input
                class="hidden"
                type="file"
                accept=".jpg,.jpeg,.png,.webp,.heic,.heif,image/jpeg,image/png,image/webp,image/heic,image/heif"
                :disabled="isFileLocked"
                @change="onFileChange"
              />

              <div class="flex justify-center gap-4 items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-paperclip md:size-6 size-5" aria-hidden="true">
                  <path d="m16 6-8.414 8.586a2 2 0 0 0 2.829 2.829l8.414-8.586a4 4 0 1 0-5.657-5.657l-8.379 8.551a6 6 0 1 0 8.485 8.485l8.379-8.551"></path>
                </svg>
                <p class="md:text-xl text-base font-medium leading-[140%]">Прикрепить файл</p>
              </div>
            </label>

            <div
              v-else
              class="w-full max-w-full md:w-[220px] md:max-w-[220px] bg-bg-tertiary border border-border-secondary rounded-[22px] p-3 mx-auto"
            >
              <div class="flex flex-col gap-3">
                <img
                  :src="uploadedPreviewUrl"
                  alt="preview"
                  class="w-full h-[180px] md:h-[150px] object-contain rounded-[16px] bg-black/20"
                />

                <div class="flex justify-center">
                  <label
                    :class="[
                      'inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[18px] text-sm font-medium transition-all duration-150 shrink-0 outline-none bg-bg-secondary text-text-primary border border-border-primary py-3 px-4',
                      isFileLocked ? 'opacity-50 cursor-not-allowed pointer-events-none' : 'hover:bg-bg-secondary-hover cursor-pointer'
                    ]"
                  >
                    <input
                      class="hidden"
                      type="file"
                      accept=".jpg,.jpeg,.png,.webp,.heic,.heif,image/jpeg,image/png,image/webp,image/heic,image/heif"
                      :disabled="isFileLocked"
                      @change="onFileChange"
                    />
                    Заменить файл
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- DEFAULT SEND ADDRESS FOR OTHER DIRECTIONS -->
      <template v-else>
        <div
          class="flex items-center md:gap-5 gap-2 bg-bg-inv-tertiary border border-border-secondary backdrop-blur-xl md:p-8 p-6 md:rounded-[28px] rounded-[22px]"
        >
          <div class="flex flex-col gap-2 basis-full">
            <span class="md:text-xl text-base font-light leading-[140%] text-text-secondary">Адрес отправки</span>
            <h4 class="md:text-2xl text-xl font-medium leading-[130%] line-clamp-1 break-all">
              {{ sendAddress || "—" }}
            </h4>
          </div>

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
                  class="absolute top-full mt-3 bg-white text-[#0F172A] px-6 py-3 rounded-[18px] shadow-lg text-sm md:text-base font-medium pointer-events-none text-center left-1/2 -translate-x-1/2 max-md:max-w-[calc(100vw-24px)] max-md:whitespace-normal md:whitespace-nowrap"
                >
                  Адрес скопирован
                </div>
              </Transition>
            </div>
          </div>
        </div>
      </template>

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
      <button
        class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 shrink-0 outline-none text-text-primary border border-border-primary hover:border-border-secondary md:p-6 p-4.5 w-full"
        type="button"
        :disabled="timeState !== 'running' || loadingCancel || ticket?.status !== 'new'"
        @click="cancelTicket"
      >
        <p class="md:text-xl text-base font-medium leading-[140%] px-1">
          {{ loadingCancel ? "Отмена..." : "Отменить сделку" }}
        </p>
      </button>

      <button
        class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 shrink-0 outline-none bg-bg-inv-primary hover:bg-bg-inv-hover text-text-inv-primary md:p-6 p-4.5 w-full"
        type="button"
        :disabled="timeState !== 'running' || loadingConfirm || ticket?.status !== 'new'"
        @click="confirmTicket"
      >
        <p class="md:text-xl text-base font-medium leading-[140%] px-1">
          {{ loadingConfirm ? "Ожидайте..." : "Подтвердить перевод" }}
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
  { id: "tether", backendId: 5, symbol: "USDT", name: "Tether BEP20", icon: "/img/tether_bnb.svg?v=032" },
  { id: "tether", backendId: 6, symbol: "USDT", name: "Tether SOL", icon: "/img/tether_solana.svg?v=032" },

  { id: "dai", backendId: 7, symbol: "DAI", name: "DAI ERC20", icon: "/img/dai.svg?v=032" },
  { id: "usd-coin", backendId: 8, symbol: "USDC", name: "USDC ERC20", icon: "/img/usdc.svg?v=032" },
  { id: "solana", backendId: 9, symbol: "SOL", name: "Solana", icon: "/img/solana-sol-logo.png?v=032" },
  { id: "litecoin", backendId: 10, symbol: "LTC", name: "Litecoin", icon: "/img/lite.svg?v=032" },
  { id: "tron", backendId: 11, symbol: "TRX", name: "TRON", icon: "/img/tron.svg?v=032" },
  { id: "dogecoin", backendId: 12, symbol: "DOGE", name: "Dogecoin", icon: "/img/doge.svg?v=032" },
];

const RUB_METHODS = [
  { id: "rub-sbp", backendId: 2001, symbol: "RUB", name: "СБП", icon: "/img/sbp.svg?v=032", type: "fiat", fiat: "rub", rubKind: "sbp" },
  { id: "rub-qr", backendId: 2011, symbol: "RUB", name: "Сбер QR наличные", icon: "/img/qr_sber.svg?v=032", type: "fiat", fiat: "rub", rubKind: "qr" },
  { id: "rub-sber", backendId: 2002, symbol: "RUB", name: "Сбер", icon: "/img/sber.svg?v=032.svg", type: "fiat", fiat: "rub", rubKind: "card" },
  { id: "rub-alfa", backendId: 2003, symbol: "RUB", name: "Альфа-банк", icon: "/img/alpha.svg?v=032", type: "fiat", fiat: "rub", rubKind: "card" },
  { id: "rub-cash", backendId: 2010, symbol: "RUB", name: "Наличные", icon: "/img/rub_nal.svg?v=032", type: "fiat", fiat: "rub", rubKind: "cash" },
  { id: "rub-card-in", backendId: 2101, symbol: "RUB", name: "Перевод на карту", icon: "/img/sbp.svg?v=032", type: "fiat", fiat: "rub", rubKind: "card_transfer" },
];

const RUB_PLACEHOLDERS = {
  sbp: "Номер телефона и банк",
  card: "Номер карты",
  cash: "Город",
  qr: "Город снятия",
  card_transfer: "Адрес кошелька",
};

const byBackendId = new Map([...currencies, ...RUB_METHODS].map((x) => [x.backendId, x]));

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

const publicSettings = ref({
  deposit_wallets: {},
  fiat_in: {},
  info: {},
});

const copiedToast = ref(false);
const copyToastText = ref("Адрес скопирован");
let toastTimer = null;

/**
 * Upload state
 */
const uploadedFile = ref(null);

const uploadedPreviewUrl = ref("");
let previewObjectUrl = null;

const ALLOWED_FILE_TYPES = [
  "image/jpeg",
  "image/png",
  "image/webp",
  "image/heic",
  "image/heif",
];

const ALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"];

/**
 * Timer
 */
const timeState = ref("running");
const totalSeconds = ref(0);
let tmr = null;

const ttlSeconds = computed(() => {
  return isFiatCardTransferGive.value ? 20 * 60 : 3 * 60 * 60;
});

const stopTimer = () => {
  if (tmr) {
    clearInterval(tmr);
    tmr = null;
  }
};

const parseCreatedAtMs = (v) => {
  if (!v) return NaN;
  const d = new Date(String(v));
  return d.getTime();
};

const computeRemaining = () => {
  const createdAtMs = parseCreatedAtMs(ticket.value?.created_at);
  if (!Number.isFinite(createdAtMs) || createdAtMs <= 0) return 0;

  const deadline = createdAtMs + ttlSeconds.value * 1000;
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
 * Helpers
 */
const formatAmount = (v, sym) => {
  const n = Number(v);
  if (!Number.isFinite(n)) return "—";
  const digits = sym === "RUB" ? 2 : 8;
  return n.toLocaleString("en-US", { maximumFractionDigits: digits, useGrouping: false });
};

const normalizeSpaces = (v) => String(v ?? "").replace(/\s+/g, " ").trim();

const toNumber = (v) => {
  const n = Number(v);
  return Number.isFinite(n) ? n : NaN;
};

const isAllowedImageFile = (file) => {
  const type = String(file?.type || "").toLowerCase();
  const name = String(file?.name || "").toLowerCase();

  if (ALLOWED_FILE_TYPES.includes(type)) return true;
  return ALLOWED_FILE_EXTENSIONS.some((ext) => name.endsWith(ext));
};

/**
 * Special 2101 logic
 */
const isFiatCardTransferGive = computed(() => Number(ticket.value?.give?.currency_backend_id) === 2101);

const fiatInRows = computed(() => {
  const raw = publicSettings.value?.fiat_in || {};
  return Object.values(raw)
    .map((row) => ({
      from: toNumber(row?.from),
      to: toNumber(row?.to),
      card_id: String(row?.card_id || ""),
      bank_name: String(row?.bank_name || ""),
      fio: String(row?.FIO || ""),
      rate: toNumber(row?.rate),
    }))
    .filter((x) => Number.isFinite(x.from) && Number.isFinite(x.to))
    .sort((a, b) => a.from - b.from);
});

const matchedFiatInRow = computed(() => {
  if (!isFiatCardTransferGive.value) return null;
  const giveAmount = Number(ticket.value?.give?.amount);
  if (!Number.isFinite(giveAmount)) return null;
  return fiatInRows.value.find((x) => giveAmount >= x.from && giveAmount <= x.to) || null;
});
const hasMatchedFiatCard = computed(() => {
  return !!normalizeSpaces(matchedFiatInRow.value?.card_id || "");
});

const managerTelegramRaw = computed(() => {
  return normalizeSpaces(publicSettings.value?.info?.Telegram_oper || "");
});

const managerTelegram = computed(() => {
  const v = managerTelegramRaw.value;
  if (!v) return "";
  return v.startsWith("@") ? v : `@${v}`;
});

const managerTelegramHref = computed(() => {
  const v = managerTelegramRaw.value.replace(/^@/, "");
  return v ? `https://t.me/${v}` : "";
});

const fiatTargetTitle = computed(() => {
  if (!matchedFiatInRow.value) return "Свяжитесь с менеджером";
  return "Номер карты для перевода";
});

const fiatTargetValue = computed(() => {
  if (matchedFiatInRow.value?.card_id) return matchedFiatInRow.value.card_id;
  return managerTelegram.value || "Контакт менеджера не указан";
});

const canCopyFiatTarget = computed(() => {
  return isFiatCardTransferGive.value && hasMatchedFiatCard.value;
});

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

const timeLineText = computed(() => {
  if (ticket.value?.status === "not_confirmed") return "";
  if (ticket.value?.status === "completed") return "";
  if (timeState.value === "running") return countdownText.value;
  if (timeState.value === "expired") return "Время истекло";
  if (timeState.value === "cancelled") return "Отменена";
  return "";
});

const timeLineClass = computed(() => {
  if (ticket.value?.status === "not_confirmed") return "text-transparent";
  if (ticket.value?.status === "completed") return "text-transparent";
  return "text-danger";
});

const giveIcon = computed(() => {
  const id = ticket.value?.give?.currency_backend_id;
  return (id && byBackendId.get(id)?.icon) || "/img/bit.svg?v=032";
});

const getIcon = computed(() => {
  const id = Number(ticket.value?.get?.currency_backend_id);
  if (!id) return "/img/ether.svg?v=032";

  const localItem = byBackendId.get(id);
  if (localItem?.icon) return localItem.icon;

  const wallets = publicSettings.value?.deposit_wallets || {};
  const settingsItem = wallets[String(id)];

  if (settingsItem?.symbol) {
    return `/img/${String(settingsItem.symbol).toUpperCase()}.svg?v=032.svg`;
  }

  return "/img/ether.svg?v=032";
});

const payoutLabel = computed(() => {
  const getId = ticket.value?.get?.currency_backend_id;
  if (!getId) return "Реквизиты";

  const item = byBackendId.get(getId);
  if (!item) return "Реквизиты";

  if (item.fiat === "rub") return RUB_PLACEHOLDERS[item.rubKind] || "Реквизиты";
  return `${ticket.value?.get?.symbol || ""} адрес`;
});

const isFileLocked = computed(() => {
  return (
    loadingConfirm.value ||
    ticket.value?.status === "not_confirmed" ||
    ticket.value?.status === "completed" ||
    !hasMatchedFiatCard.value
  );
});
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
      timeState.value = "completed";
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
    publicSettings.value = s || {};

    const giveId = ticket.value?.give?.currency_backend_id;
    if (!giveId) return;

    if (Number(giveId) !== 2101) {
      const wallets = s?.deposit_wallets || {};
      const w = wallets[String(giveId)];
      sendAddress.value = w?.address || "";
      return;
    }

    sendAddress.value = "";
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
    let res;

    // Только для 2101 с приложенным файлом отправляем multipart
    if (isFiatCardTransferGive.value && uploadedFile.value) {
      const formData = new FormData();
      formData.append("receipt", uploadedFile.value);

      res = await fetch(`/api/tickets/${encodeURIComponent(ticket.value.id)}/confirm`, {
        method: "PATCH",
        body: formData,
      });
    } else {
      // Для обычных сделок и для 2101 без файла — обычный PATCH без body
      res = await fetch(`/api/tickets/${encodeURIComponent(ticket.value.id)}/confirm`, {
        method: "PATCH",
      });
    }

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
    let valueToCopy = "";

    if (isFiatCardTransferGive.value) {
      valueToCopy = fiatTargetValue.value;
      copyToastText.value = matchedFiatInRow.value ? "Номер карты скопирован" : "Контакт скопирован";
    } else {
      valueToCopy = sendAddress.value;
      copyToastText.value = "Адрес скопирован";
    }

    if (!valueToCopy) return;

    await navigator.clipboard.writeText(valueToCopy);

    copiedToast.value = true;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (copiedToast.value = false), 1800);
  } catch {}
};

const onFileChange = (e) => {
  const file = e?.target?.files?.[0];
  if (!file) return;

  const allowedTypes = [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/heic",
    "image/heif",
  ];

  if (!allowedTypes.includes(String(file.type || "").toLowerCase())) {
    return;
  }

  uploadedFile.value = file;

  if (previewObjectUrl) {
    URL.revokeObjectURL(previewObjectUrl);
    previewObjectUrl = null;
  }

  previewObjectUrl = URL.createObjectURL(file);
  uploadedPreviewUrl.value = previewObjectUrl;
};

onMounted(async () => {
  await fetchTicket();
  await fetchSettings();
});

onBeforeUnmount(() => {
  stopTimer();
  if (toastTimer) clearTimeout(toastTimer);

  uploadedFile.value = null;
  uploadedPreviewUrl.value = "";

  if (previewObjectUrl) {
    URL.revokeObjectURL(previewObjectUrl);
    previewObjectUrl = null;
  }
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