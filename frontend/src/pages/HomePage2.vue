<template>
  <div class="relative flex flex-col min-h-screen">
    <div
      v-if="hasBanner"
      class="flex-shrink-0 w-full pt-16 max-sm:pt-8 flex items-center justify-center"
      role="banner"
    >
      <span
        class="min-w-0 bg-warning px-4 xl:px-12 py-2.5 rounded-xl font-semibold mx-4 z-20 text-center text-xs md:text-sm text-[#0F172A] leading-snug"
        v-html="bannerText"
      ></span>
    </div>

    <img
      alt="bg"
      loading="lazy"
      width="1920"
      height="1080"
      decoding="async"
      class="!inset-0 !absolute !w-full !h-full"
      src="/_next/static/media/bg.png"
    />

    <div
      class="flex flex-col md:justify-between gap-6 md:py-18 py-8 max-w-225 w-full self-center grow basis-full relative z-10 container"
    >
    <div class="hero-marquee-wrap">
  <div class="hero-marquee">
    <div class="hero-marquee-track">
      <div class="hero-marquee-item">
        <img src="/img/banks/sberbank.svg" alt="Sber" />
      </div>
      <div class="hero-marquee-item">
        <img src="/img/banks/tbank.svg" alt="TBank" />
      </div>
      <div class="hero-marquee-item">
        <img src="/img/banks/alfabank.svg" alt="Alfa Bank" />
      </div>
      <div class="hero-marquee-item">
        <img src="/img/banks/sbp.svg" alt="SBP" />
      </div>

      <!-- дубль для бесконечной прокрутки -->
      <div class="hero-marquee-item">
        <img src="/img/banks/sberbank.svg" alt="Sber" />
      </div>
      <div class="hero-marquee-item">
        <img src="/img/banks/tbank.svg" alt="TBank" />
      </div>
      <div class="hero-marquee-item">
        <img src="/img/banks/alfabank.svg" alt="Alfa Bank" />
      </div>
      <div class="hero-marquee-item">
        <img src="/img/banks/sbp.svg" alt="SBP" />
      </div>
    </div>
  </div>
</div>
      <div class="flex flex-col md:gap-6 gap-3 text-white">
        <h1 class="md:text-7xl text-[32px] font-medium leading-[110%] text-center"><br>
          Скоростной обмен <br />
          иностранных валют
        </h1>
        <span class="md:text-xl text-base font-light leading-[140%] text-center max-w-110 self-center">
          Обмен рублей или USDT на валюту страны с выдачей наличных или переводом на банковский счёт
        </span>
      </div>

      <form
        class="flex flex-col md:gap-6 gap-2 md:p-12 p-6 md:rounded-[64px] rounded-[40px] bg-bg-tertiary border border-border-secondary"
        @submit.prevent="onSubmit"
      >
        <div v-if="topError" class="md:text-base text-sm font-medium leading-[150%] text-danger text-center">
          {{ topError }}
        </div>

        <div class="grid md:grid-cols-2 grid-cols-1 md:gap-6 gap-2 relative">
          <!-- GIVE -->
          <div data-slot="form-item" class="grid gap-2">
            <label
              ref="giveFieldRef"
              for="give-input"
              class="flex items-center gap-4 md:px-8 px-7 md:py-4 py-3 bg-bg-primary hover:bg-bg-hover border border-border-secondary rounded-[28px] transition duration-150 w-full has-[input:focus]:border-border-active max-md:flex-row"
            >
              <div class="flex flex-col gap-1 grow max-md:items-start relative">
                <span class="md:text-base text-xs font-light leading-[150%] text-text-tertiary">Вносите</span>

                <input
                  id="give-input"
                  inputmode="decimal"
                  :placeholder="`0 ${giveCurrency?.symbol || ''}`"
                  class="md:text-[32px] text-2xl font-medium leading-[120%] outline-none max-w-full w-full max-md:text-left text-white bg-transparent"
                  type="number"
                  min="0"
                  step="any"
                  v-model="giveAmountStr"
                  @input="onGiveInput"
                />

                <p class="md:text-base text-sm font-medium leading-[150%] text-text-secondary">
                  <template v-if="isGiveCardTransfer">
                    {{ giveRangeText }}
                  </template>
                  <template v-else>
                    <span class="cursor-pointer" @click="setGiveAmount(limitsInGive.giveMin)">
                      {{ limitsInGive.giveMin }}
                    </span>
                    -
                    <span class="cursor-pointer" @click="setGiveAmount(limitsInGive.giveMax)">
                      {{ limitsInGive.giveMax }}
                    </span>
                  </template>
                </p>
              </div>

              <button
                ref="giveBtnRef"
                type="button"
                @click="toggleDropdown('give')"
                aria-label="Выбрать валюту (вносите)"
              >
                <div
                  class="flex justify-center items-center bg-bg-secondary border border-border-primary md:rounded-[28px] rounded-[22px] md:size-19 size-16 overflow-hidden"
                >
                  <img
                    :alt="giveCurrency?.name || ''"
                    loading="lazy"
                    width="36"
                    height="36"
                    decoding="async"
                    class="md:size-9 size-8 object-contain rounded-[10px]"
                    :src="giveCurrency?.icon || ''"
                    style="color: transparent"
                  />
                </div>
              </button>
            </label>
          </div>

          <!-- GET -->
          <div data-slot="form-item" class="grid gap-2">
            <label
              ref="getFieldRef"
              for="get-input"
              class="flex items-center gap-4 md:px-8 px-7 md:py-4 py-3 bg-bg-primary hover:bg-bg-hover border border-border-secondary rounded-[28px] transition duration-150 w-full has-[input:focus]:border-border-active max-md:flex-row flex-row-reverse"
            >
              <div class="flex flex-col gap-1 grow max-md:items-start relative items-end">
                <span class="md:text-base text-xs font-light leading-[150%] text-text-tertiary">Получаете</span>

                <input
                  id="get-input"
                  inputmode="decimal"
                  :placeholder="`0 ${getCurrency?.symbol || ''}`"
                  class="md:text-[32px] text-2xl font-medium leading-[120%] outline-none max-w-full w-full max-md:text-left text-right text-white bg-transparent"
                  type="number"
                  min="0"
                  step="any"
                  v-model="getAmountStr"
                  @input="onGetInput"
                />

                <p class="md:text-base text-sm font-medium leading-[150%] text-text-secondary text-right max-md:text-left">
                  {{ getRateText }}
                </p>
              </div>

              <button
  ref="getBtnRef"
  type="button"
  @click="toggleDropdown('get')"
  aria-label="Выбрать валюту (получаете)"
>
  <div
    class="flex justify-center items-center bg-bg-secondary border border-border-primary md:rounded-[28px] rounded-[22px] md:size-19 size-16"
  >
    <div class="md:size-9 size-8 rounded-full overflow-hidden flex items-center justify-center bg-transparent">
      <img
        :alt="getCurrency?.name || ''"
        loading="lazy"
        width="36"
        height="36"
        decoding="async"
        class="w-full h-full object-cover rounded-full"
        :src="getCurrency?.icon || ''"
        style="color: transparent; clip-path: inset(0 round 100px);"
      />
    </div>
  </div>
</button>
            </label>
          </div>

          <!-- SWAP -->
          <button
            type="button"
            class="absolute md:size-14 size-9 bg-bg-secondary md:rounded-[16px] rounded-[12px] flex justify-center items-center border border-border-primary top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 max-md:rotate-90"
            aria-label="Поменять местами"
            disabled
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
              class="lucide lucide-arrow-right-left md:size-8 size-5 text-white opacity-40"
              aria-hidden="true"
            >
              <path d="m16 3 4 4-4 4"></path>
              <path d="M20 7H4"></path>
              <path d="m8 21-4-4 4-4"></path>
              <path d="M4 17h16"></path>
            </svg>
          </button>
        </div>

        <div class="grid md:grid-cols-2 grid-cols-1 md:gap-6 gap-2">
          <div data-slot="form-item" class="grid gap-2">
            <div class="flex flex-col gap-1" data-slot="form-control" aria-invalid="false">
              <div class="relative w-full">
                <input
                  id="telegram"
                  placeholder=" "
                  class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60 field-sizing-fixed text-white"
                  autocomplete="off"
                  v-model.trim="telegram"
                  :aria-invalid="!!telegramError"
                />
                <label
                  for="telegram"
                  class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
                >Telegram</label>
              </div>
              <p v-if="telegramError" class="md:text-base text-sm font-medium leading-[150%] text-danger">
                {{ telegramError }}
              </p>
            </div>
          </div>

          <div data-slot="form-item" class="grid gap-2">
            <div class="flex flex-col gap-1" data-slot="form-control" aria-invalid="false">
              <div class="relative w-full">
                <input
                  id="wallet"
                  placeholder=" "
                  class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60 field-sizing-fixed text-white"
                  autocomplete="off"
                  v-model.trim="wallet"
                  :aria-invalid="!!walletError"
                />
                <label
                  for="wallet"
                  class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
                >{{ getWalletLabel }}*</label>
              </div>
              <p v-if="walletError" class="md:text-base text-sm font-medium leading-[150%] text-danger">
                {{ walletError }}
              </p>
            </div>
          </div>
        </div>

        <div class="grid items-center md:grid-cols-2 grid-cols-1 md:gap-6 gap-4 max-md:mt-2">
          <div class="md:pl-8 max-md:text-center">
            <span class="md:text-base text-sm font-light leading-[150%] text-text-tertiary">
              Cрок выдачи — 5-60 минут, в зависимости от загруженности менеджера
            </span>
          </div>

          <button
            data-slot="button"
            class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-brand hover:bg-brand-hover text-text-primary data-[state=active]:bg-brand-active data-[state=active]:text-text-inv-primary md:py-6 py-4.5 max-md:rounded-[22px]"
            type="submit"
            :disabled="!canExchange || isSubmitting"
          >
            <p class="md:text-xl text-base font-medium leading-[140%]">
              {{ isSubmitting ? "Загрузка..." : "Обменять" }}
            </p>
          </button>
        </div>

        <Teleport to="body">
          <div
            v-if="openDropdown"
            class="fixed inset-0"
            :style="{ zIndex: 2147483647 }"
            @click="closeDropdown"
          >
            <div
              class="fixed md:rounded-[28px] rounded-[22px] border border-border-secondary overflow-hidden shadow-2xl backdrop-blur-md bg-[#0B1220] pointer-events-auto"
              :style="{ ...dropdownStyle, '--row': '76px' }"
              @click.stop
            >
              <div
                class="overflow-y-auto overflow-x-hidden hide-scrollbar"
                :style="{ height: 'calc(var(--row) * 3)' }"
              >
                <button
                  v-for="c in dropdownOptions"
                  :key="openDropdown + '-' + c.backendId + '-' + c.symbol + '-' + c.id"
                  type="button"
                  class="w-full px-6 py-0 flex items-stretch transition duration-150 hover:bg-white/10 border-b border-white/5 last:border-b-0"
                  :style="{ height: 'var(--row)' }"
                  @click="selectCurrency(openDropdown, c)"
                >
                  <div
                    v-if="!isMobile && openDropdown === 'give'"
                    class="w-full h-full flex items-center justify-between"
                  >
                    <div class="flex flex-col text-left leading-tight">
                      <span class="text-white text-xl font-medium">{{ c.name }}</span>
                      <span class="text-white text-base font-light">
                        {{ c.symbol }}
                      </span>
                    </div>

                    <div class="flex flex-col items-center justify-center gap-1 shrink-0">
                      <div class="md:size-9 size-8 rounded-full overflow-hidden flex items-center justify-center bg-transparent">
  <img
    :alt="c.name"
    class="w-full h-full object-cover drop-shadow rounded-full"
    :src="c.icon"
    style="clip-path: inset(0 round 100px);"
  />
</div>
                      <span class="text-white text-sm font-medium">{{ c.symbol }}</span>
                    </div>
                  </div>

                  <div
                    v-else-if="!isMobile && openDropdown === 'get'"
                    class="w-full h-full flex items-center justify-between"
                  >
                    <div class="flex flex-col items-center justify-center gap-1 shrink-0">
                      <div class="md:size-9 size-8 rounded-full overflow-hidden flex items-center justify-center bg-transparent">
  <img
    :alt="c.name"
    class="w-full h-full object-cover drop-shadow rounded-full"
    :src="c.icon"
    style="clip-path: inset(0 round 100px);"
  />
</div>
                      <span class="text-white text-sm font-medium">{{ c.symbol }}</span>
                    </div>

                    <div class="flex flex-col text-right leading-tight">
                      <span class="text-white text-xl font-medium">{{ c.name }}</span>
                      <span class="text-white text-base font-light">
                        {{ c.symbol }}
                      </span>
                    </div>
                  </div>

                  <div v-else class="w-full h-full flex items-center justify-between">
                    <div class="flex flex-col text-left leading-tight">
                      <span class="text-white text-lg font-medium">{{ c.name }}</span>
                      <span class="text-white text-base font-light">
                        {{ c.symbol }}
                      </span>
                    </div>

                    <div class="flex flex-col items-center justify-center gap-1 shrink-0">
                      <div class="md:size-9 size-8 rounded-full overflow-hidden flex items-center justify-center bg-transparent">
  <img
    :alt="c.name"
    class="w-full h-full object-cover drop-shadow rounded-full"
    :src="c.icon"
    style="clip-path: inset(0 round 100px);"
  />
</div>
                      <span class="text-white text-sm font-medium">{{ c.symbol }}</span>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </Teleport>
      </form>
    </div>
  </div>

  <section
    aria-label="Notifications alt+T"
    tabindex="-1"
    aria-live="polite"
    aria-relevant="additions text"
    aria-atomic="false"
  ></section>
  <div hidden id="S:1"></div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch, nextTick } from "vue";

const limitsFromSettings = ref({
  giveMin: 800,
  giveMax: 600000,
  getMin: 700,
  getMax: 1000000,
});

const isMobile = ref(false);
const updateIsMobile = () => {
  isMobile.value = window.innerWidth < 768;
};

const RUB_INPUT_METHODS = ref([
  {
    id: "rub-card-in",
    backendId: 2101,
    symbol: "RUB",
    name: "Перевод на карту",
    icon: "/img/sbp.svg?v=032",
    type: "fiat",
    fiat: "rub",
    rubKind: "card_transfer",
  },
]);

const USDT_INPUTS = ref([
  { id: "tether", backendId: 3, symbol: "USDT", name: "Tether TRC20", icon: "/img/tether_trc20.svg?v=032" },
  { id: "tether", backendId: 4, symbol: "USDT", name: "Tether ERC20", icon: "/img/tether_erc20.svg?v=032" },
  { id: "tether", backendId: 5, symbol: "USDT", name: "Tether BEP20", icon: "/img/tether_bnb.svg?v=032" },
  { id: "tether", backendId: 6, symbol: "USDT", name: "Tether SOL", icon: "/img/tether_solana.svg?v=032" },
]);

const EMPTY_GET_CURRENCY = {
  id: "cash-out-empty",
  backendId: 2102,
  symbol: "",
  name: "",
  icon: "",
  type: "fiat",
  fiat: "cash_out",
  rubKind: "cash",
  course_rub: 0,
  course_usdt: 0,
};

const publicSettings = ref({
  mode: "2",
  banner: "",
  percent: 2,
  giveMin: 800,
  giveMax: 600000,
  getMin: 700,
  getMax: 1000000,
  deposit_wallets: {},
  fiat_in: {},
  fiat_in_methods: {},
});

const bannerText = computed(() => String(publicSettings.value?.banner || "").trim());
const hasBanner = computed(() => !!bannerText.value);

const fiatOutOptions = computed(() => {
  const raw = publicSettings.value?.deposit_wallets || {};

  return Object.entries(raw)
    .filter(([key, row]) => Number(key) >= 2102 && row && typeof row === "object")
    .map(([key, row]) => {
      const symbol = String(row?.symbol || "").trim().toUpperCase();
      const name = String(row?.name || symbol || `Валюта ${key}`).trim();

      return {
        id: `cash-out-${key}`,
        backendId: Number(key),
        symbol,
        name,
        icon: symbol ? `/img/${symbol}.svg?v=032.svg` : "/img/placeholder.svg",
        type: "fiat",
        fiat: "cash_out",
        rubKind: "cash",
        course_rub: Number(row?.course_rub),
        course_usdt: Number(row?.course_usdt),
      };
    })
    .filter((x) => x.symbol.length > 0);
});

const giveOptions = computed(() => [...RUB_INPUT_METHODS.value, ...USDT_INPUTS.value]);
const getOptions = computed(() => fiatOutOptions.value);
const dropdownOptions = computed(() => (openDropdown.value === "give" ? giveOptions.value : getOptions.value));

const giveCurrency = ref(RUB_INPUT_METHODS.value[0]);
const getCurrency = ref({ ...EMPTY_GET_CURRENCY });

const giveAmountStr = ref("");
const getAmountStr = ref("");
const telegram = ref("");
const wallet = ref("");

const isSubmitting = ref(false);
const submitError = ref("");
const lastEdited = ref("give");

const openDropdown = ref(null);
const giveBtnRef = ref(null);
const getBtnRef = ref(null);
const giveFieldRef = ref(null);
const getFieldRef = ref(null);
const dropdownStyle = ref({ top: "0px", left: "0px", width: "280px" });

const toNumber = (v) => {
  const n = Number(String(v).replace(",", "."));
  return Number.isFinite(n) ? n : 0;
};

const formatNum = (v, decimals = 8) => {
  const n = Number(v);
  if (!Number.isFinite(n)) return "0";
  const d = n >= 1 ? Math.min(6, decimals) : decimals;
  return n.toLocaleString("en-US", { maximumFractionDigits: d, useGrouping: false });
};

const normalizeSpaces = (s) => String(s ?? "").replace(/\s+/g, " ").trim();

const isGiveFiat = computed(() => giveCurrency.value?.type === "fiat");
const isGiveCardTransfer = computed(() => Number(giveCurrency.value?.backendId) === 2101);

const limitsUsd = computed(() => ({
  giveMin: Number(limitsFromSettings.value.giveMin || 0),
  giveMax: Number(limitsFromSettings.value.giveMax || 0),
  getMin: Number(limitsFromSettings.value.getMin || 0),
  getMax: Number(limitsFromSettings.value.getMax || 0),
}));

const fiatInRows = computed(() => {
  const raw = publicSettings.value?.fiat_in || {};
  return Object.entries(raw)
    .map(([key, row]) => ({
      key,
      from: Number(row?.from),
      to: Number(row?.to),
      rate: Number(row?.rate),
      card_id: String(row?.card_id || ""),
      bank_name: String(row?.bank_name || ""),
      fio: String(row?.FIO || ""),
    }))
    .filter((x) => Number.isFinite(x.from) && Number.isFinite(x.to) && Number.isFinite(x.rate))
    .sort((a, b) => a.from - b.from);
});

const fiatInMin = computed(() => (fiatInRows.value.length ? fiatInRows.value[0].from : 0));
const fiatInMax = computed(() =>
  fiatInRows.value.length ? fiatInRows.value[fiatInRows.value.length - 1].to : 0
);

const currentFiatInRow = computed(() => {
  if (!isGiveCardTransfer.value) return null;
  const amount = toNumber(giveAmountStr.value);
  if (!amount) return null;
  return fiatInRows.value.find((x) => amount >= x.from && amount <= x.to) || null;
});

const activeCourse = computed(() => {
  if (!getCurrency.value?.symbol) return 0;
  return isGiveCardTransfer.value
    ? Number(getCurrency.value.course_rub) || 0
    : Number(getCurrency.value.course_usdt) || 0;
});

const moscowDateText = computed(() => {
  const formatter = new Intl.DateTimeFormat("ru-RU", {
    timeZone: "Europe/Moscow",
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
  return formatter.format(new Date());
});

const getRateText = computed(() => {
  if (!getCurrency.value?.symbol) return "Выберите валюту";
  if (!activeCourse.value) return "Курс не задан";
  return `курс ${formatNum(activeCourse.value, 6)} ${getCurrency.value.symbol} на ${moscowDateText.value}`;
});

const limitsInGive = computed(() => {
  if (isGiveCardTransfer.value) {
    return {
      giveMin: formatNum(fiatInMin.value, 2),
      giveMax: formatNum(fiatInMax.value, 2),
    };
  }

  return {
    giveMin: formatNum(limitsUsd.value.giveMin, 2),
    giveMax: formatNum(limitsUsd.value.giveMax, 2),
  };
});

const giveRangeText = computed(() => {
  if (!isGiveCardTransfer.value) {
    return `${limitsInGive.value.giveMin} - ${limitsInGive.value.giveMax}`;
  }

  const amount = toNumber(giveAmountStr.value);

  if (!amount) {
    return `${formatNum(fiatInMin.value, 2)} - ${formatNum(fiatInMax.value, 2)} RUB`;
  }

  const row = currentFiatInRow.value;
  if (!row) {
    return `${formatNum(fiatInMin.value, 2)} - ${formatNum(fiatInMax.value, 2)} RUB`;
  }

  return `${formatNum(row.rate, 2)} RUB за 1 USD`;
});

const recalcGetFromGive = () => {
  const give = toNumber(giveAmountStr.value);

  if (!give || !getCurrency.value?.symbol) {
    getAmountStr.value = "";
    return;
  }

  const course = activeCourse.value;
  if (!course) {
    getAmountStr.value = "";
    return;
  }

  const result = give / course;
  getAmountStr.value = formatNum(result, 6);
};

const recalcGiveFromGet = () => {
  const get = toNumber(getAmountStr.value);

  if (!get || !getCurrency.value?.symbol) {
    giveAmountStr.value = "";
    return;
  }

  const course = activeCourse.value;
  if (!course) {
    giveAmountStr.value = "";
    return;
  }

  const result = get * course;
  giveAmountStr.value = formatNum(result, 6);
};

const giveAmountN = computed(() => toNumber(giveAmountStr.value));
const getAmountN = computed(() => toNumber(getAmountStr.value));

const giveMinN = computed(() => toNumber(limitsInGive.value.giveMin));
const giveMaxN = computed(() => toNumber(limitsInGive.value.giveMax));

const hasRates = computed(() => !!getCurrency.value?.symbol && !!activeCourse.value);

const amountError = computed(() => {
  if (!getCurrency.value?.symbol) return "Выберите валюту получения";
  if (!activeCourse.value) return "Курс для выбранной валюты не задан";
  if (!giveAmountStr.value && !getAmountStr.value) return "";

  if (lastEdited.value === "give") {
    if (!giveAmountN.value) return "";

    if (giveAmountN.value < giveMinN.value) {
      return `Минимум для внесения: ${limitsInGive.value.giveMin} ${giveCurrency.value.symbol}`;
    }

    if (giveAmountN.value > giveMaxN.value) {
      return `Максимум для внесения: ${limitsInGive.value.giveMax} ${giveCurrency.value.symbol}`;
    }

    if (isGiveCardTransfer.value && !currentFiatInRow.value) {
      return "Сумма не попадает ни в один доступный интервал";
    }
  } else {
    if (!getAmountN.value) return "";

    // проверяем пересчитанную левую сумму
    if (!giveAmountN.value) return "";

    if (giveAmountN.value < giveMinN.value) {
      return `Минимум для внесения: ${limitsInGive.value.giveMin} ${giveCurrency.value.symbol}`;
    }

    if (giveAmountN.value > giveMaxN.value) {
      return `Максимум для внесения: ${limitsInGive.value.giveMax} ${giveCurrency.value.symbol}`;
    }

    if (isGiveCardTransfer.value && !currentFiatInRow.value) {
      return "Сумма не попадает ни в один доступный интервал";
    }
  }

  return "";
});

const validateTelegramUsername = (s) => {
  const raw = normalizeSpaces(s);
  if (!raw) return "";

  const cleaned = raw
    .replace(/^https?:\/\/t\.me\//i, "")
    .replace(/^t\.me\//i, "")
    .replace(/^@/, "");

  return /^[A-Za-z][A-Za-z0-9_]{4,31}$/.test(cleaned) ? "" : "Некорректный формат Telegram";
};

const telegramError = computed(() => validateTelegramUsername(telegram.value));
const walletError = computed(() => "");
const topError = computed(() => submitError.value || amountError.value || "");

const canExchange = computed(() => {
  const hasRequired = !!telegram.value.trim() && !!wallet.value.trim();
  const hasAmount = giveAmountN.value > 0 && getAmountN.value > 0;
  const noFieldErrors = !telegramError.value && !walletError.value;

  return hasRates.value && hasRequired && hasAmount && !amountError.value && noFieldErrors;
});

const getWalletLabel = computed(() => "Город снятия / IBAN");

const selectCurrency = (side, c) => {
  if (side === "give") {
    giveCurrency.value = c;
  } else {
    getCurrency.value = c;
  }

  openDropdown.value = null;

  if (lastEdited.value === "give") recalcGetFromGive();
  else recalcGiveFromGet();
};

const closeDropdown = () => {
  openDropdown.value = null;
};

const positionDropdown = () => {
  const el = openDropdown.value === "give" ? giveFieldRef.value : getFieldRef.value;
  if (!el) return;

  const rect = el.getBoundingClientRect();
  const width = rect.width;
  const top = rect.bottom + 8;
  let left = rect.left;

  const padding = 12;
  if (left < padding) left = padding;
  if (left + width > window.innerWidth - padding) left = window.innerWidth - width - padding;

  dropdownStyle.value = { top: `${top}px`, left: `${left}px`, width: `${width}px` };
};

const toggleDropdown = async (side) => {
  openDropdown.value = openDropdown.value === side ? null : side;
  if (openDropdown.value) {
    await nextTick();
    positionDropdown();
  }
};

const onReposition = () => {
  if (openDropdown.value) positionDropdown();
};

const setGiveAmount = (vStr) => {
  lastEdited.value = "give";
  giveAmountStr.value = String(vStr);
  recalcGetFromGive();
};

const onGiveInput = () => {
  lastEdited.value = "give";
};

const onGetInput = () => {
  lastEdited.value = "get";
};

async function loadPublicSettings() {
  try {
    const res = await fetch("/api/settings/public", { method: "GET" });
    if (!res.ok) return;

    const data = await res.json();
    publicSettings.value = data || {};

    const next = {
      giveMin: Number(data?.giveMin),
      giveMax: Number(data?.giveMax),
      getMin: Number(data?.getMin),
      getMax: Number(data?.getMax),
    };

    if (Number.isFinite(next.giveMin)) limitsFromSettings.value.giveMin = next.giveMin;
    if (Number.isFinite(next.giveMax)) limitsFromSettings.value.giveMax = next.giveMax;
    if (Number.isFinite(next.getMin)) limitsFromSettings.value.getMin = next.getMin;
    if (Number.isFinite(next.getMax)) limitsFromSettings.value.getMax = next.getMax;

    const method2101 = data?.fiat_in_methods?.["2101"];
    if (method2101) {
      RUB_INPUT_METHODS.value = [
        {
          id: "rub-card-in",
          backendId: 2101,
          symbol: String(method2101.symbol || "RUB"),
          name: String(method2101.name || "Перевод на карту"),
          icon: String(method2101.icon || "/img/sbp.svg?v=032"),
          type: "fiat",
          fiat: "rub",
          rubKind: "card_transfer",
        },
      ];
    }
  } catch {}
}

const onSubmit = async () => {
  if (!canExchange.value) return;
  if (isSubmitting.value) return;

  isSubmitting.value = true;
  submitError.value = "";

  const payload = {
    give: {
      currency_backend_id: giveCurrency.value.backendId,
      coingecko_id: isGiveFiat.value ? "rub" : giveCurrency.value.id,
      symbol: giveCurrency.value.symbol,
      amount: giveAmountN.value,
    },
    get: {
      currency_backend_id: getCurrency.value.backendId,
      coingecko_id: null,
      symbol: getCurrency.value.symbol,
      amount: getAmountN.value,
    },
    fee_percent: 0,

    get_is_fiat: true,
    fiat_code: isGiveCardTransfer.value ? "rub" : "usdt",
    rub_kind: "cash",

    client: {
      telegram: telegram.value.trim(),
      payout_details: wallet.value.trim(),
    },

    rates_snapshot: {
      give_usd: isGiveFiat.value ? null : 1,
      give_rub: isGiveFiat.value ? activeCourse.value || null : null,
      get_usd: null,
    },

    created_at: new Date().toISOString(),
  };

  try {
    const token = localStorage.getItem("token") || "";

    const res = await fetch("/api/tickets", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      credentials: "include",
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      try {
        const j = await res.json();
        submitError.value = j?.detail || "Не удалось создать обмен. Попробуйте ещё раз.";
      } catch {
        submitError.value = "Не удалось создать обмен. Попробуйте ещё раз.";
      }
      return;
    }

    const data = await res.json();
    const ticketId = data?.ticket_id;

    if (!ticketId) {
      submitError.value = "Сервер не вернул ticket_id. Попробуйте ещё раз.";
      return;
    }

    window.location.href = `/tickets/${ticketId}`;
  } catch {
    submitError.value = "Ошибка сети. Попробуйте ещё раз.";
  } finally {
    isSubmitting.value = false;
  }
};

watch(
  [giveAmountStr, () => giveCurrency.value?.backendId, () => getCurrency.value?.backendId],
  () => {
    if (lastEdited.value === "give") recalcGetFromGive();
  }
);

watch(getAmountStr, () => {
  if (lastEdited.value === "get") recalcGiveFromGet();
});

watch(openDropdown, async (v) => {
  if (!v) return;
  await nextTick();
  positionDropdown();
});

onMounted(async () => {
  updateIsMobile();
  window.addEventListener("resize", updateIsMobile);

  await loadPublicSettings();

  giveCurrency.value = RUB_INPUT_METHODS.value[0] || giveOptions.value[0];
  getCurrency.value = getOptions.value[0] || { ...EMPTY_GET_CURRENCY };

  window.addEventListener("resize", onReposition);
  window.addEventListener("scroll", onReposition, true);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateIsMobile);
  window.removeEventListener("resize", onReposition);
  window.removeEventListener("scroll", onReposition, true);
});
</script>

<style scoped>
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.hide-scrollbar::-webkit-scrollbar {
  width: 0;
  height: 0;
}

.hero-marquee-wrap {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 8px;
}

.hero-marquee {
  position: relative;
  width: min(100%, 860px);
  overflow: hidden;
  pointer-events: none;
  mask-image: linear-gradient(to right, transparent 0%, black 12%, black 88%, transparent 100%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 12%, black 88%, transparent 100%);
}

.hero-marquee-track {
  display: flex;
  align-items: center;
  gap: 56px;
  width: max-content;
  animation: hero-marquee-move 28s linear infinite;
  will-change: transform;
}

.hero-marquee-item {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.78;
}

.hero-marquee-item img {
  height: 34px;
  width: auto;
  max-width: 160px;
  object-fit: contain;
  display: block;
  filter: brightness(0) invert(1);
}

@keyframes hero-marquee-move {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}

@media (max-width: 768px) {
  .hero-marquee-wrap {
    margin-bottom: 6px;
  }

  .hero-marquee {
    width: 100%;
  }

  .hero-marquee-track {
    gap: 34px;
    animation-duration: 22s;
  }

  .hero-marquee-item img {
    height: 24px;
    max-width: 110px;
  }
}
</style>