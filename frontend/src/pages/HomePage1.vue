<template>
  <div data-exchange-mode="1" class="flex flex-col grow basis-full relative">
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

<div
      class="flex flex-col md:justify-between gap-6 md:py-18 py-8 max-w-225 w-full self-center grow basis-full relative z-10 container"
    >
      <div data-home-intro="heading" class="flex flex-col md:gap-6 gap-3 text-white">
        <h1 class="md:text-7xl text-[32px] font-medium leading-[110%] text-center">
          {{ tr("Скоростной") }} <br />
          {{ tr("обмен криптовалют") }}
        </h1>
        <span class="md:text-xl text-base font-light leading-[140%] text-center max-w-110 self-center">
          {{ tr("Безопасный и удобный способ обмена криптовалюты за считанные минуты, без AML и KYC проверки") }}
        </span>
      </div>

      <form data-home-intro="form"
        class="flex flex-col md:gap-6 gap-2 md:p-12 p-6 md:rounded-[64px] rounded-[40px] bg-bg-tertiary border border-border-secondary"
        @submit.prevent="onSubmit"
      >
        <div v-if="topError" class="md:text-base text-sm font-medium leading-[150%] text-danger text-center">
          {{ tr(topError) }}
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
                <span class="md:text-base text-xs font-light leading-[150%] text-text-tertiary">{{ tr("Вносите") }}</span>

                <input
                  id="give-input"
                  inputmode="decimal"
                  :placeholder="0"
                  class="md:text-[32px] text-2xl font-medium leading-[120%] outline-none max-w-full w-full max-md:text-left text-white bg-transparent"
                  type="number"
                  min="0"
                  step="any"
                  v-model="giveAmountStr"
                  @input="lastEdited = 'give'"
                />

                <p class="md:text-base text-sm font-medium leading-[150%] text-text-secondary">
                  <template v-if="isGiveCardTransfer">
                    {{ tr(giveRangeText) }}
                  </template>
                  <template v-else>
                    <span class="cursor-pointer" @click="setGiveAmount(limitsInGive.giveMin)">{{ limitsInGive.giveMin }}</span>
                    -
                    <span class="cursor-pointer" @click="setGiveAmount(limitsInGive.giveMax)">{{ limitsInGive.giveMax }}</span>
                  </template>
                </p>
              </div>

              <button class="homePressable"
                ref="giveBtnRef"
                type="button"
                @click="toggleDropdown('give')"
                :aria-label="tr(&quot;Выбрать валюту (вносите)&quot;)"
              >
                <div
                  class="flex justify-center items-center bg-bg-secondary border border-border-primary md:rounded-[28px] rounded-[22px] md:size-19 size-16"
                >
                  <img
                    :alt="giveCurrency.name"
                    loading="lazy"
                    width="36"
                    height="36"
                    decoding="async"
                    class="md:size-9 size-8 object-contain"
                    :src="giveCurrency.icon"
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
                <span class="md:text-base text-xs font-light leading-[150%] text-text-tertiary">{{ tr("Получаете") }}</span>

                <input
                  id="get-input"
                  inputmode="decimal"
                  :placeholder="0"
                  class="md:text-[32px] text-2xl font-medium leading-[120%] outline-none max-w-full w-full max-md:text-left text-right text-white bg-transparent"
                  type="number"
                  min="0"
                  step="any"
                  :readonly="isGiveCardTransfer"
                  :disabled="isGiveCardTransfer"
                  v-model="getAmountStr"
                  @input="onGetInput"
                />

                <p class="md:text-base text-sm font-medium leading-[150%] text-text-secondary">
                  <span
                    :class="isGiveCardTransfer ? 'opacity-50 cursor-default' : 'cursor-pointer'"
                    @click="!isGiveCardTransfer && setGetAmount(limitsInGet.getMin)"
                  >{{ limitsInGet.getMin }}</span>
                  -
                  <span
                    :class="isGiveCardTransfer ? 'opacity-50 cursor-default' : 'cursor-pointer'"
                    @click="!isGiveCardTransfer && setGetAmount(limitsInGet.getMax)"
                  >{{ limitsInGet.getMax }}</span>
                </p>
              </div>

              <button class="homePressable"
                ref="getBtnRef"
                type="button"
                @click="toggleDropdown('get')"
                :aria-label="tr(&quot;Выбрать валюту (получаете)&quot;)"
              >
                <div
                  class="flex justify-center items-center bg-bg-secondary border border-border-primary md:rounded-[28px] rounded-[22px] md:size-19 size-16"
                >
                  <img
                    :alt="getCurrency.name"
                    loading="lazy"
                    width="36"
                    height="36"
                    decoding="async"
                    class="md:size-9 size-8 object-contain"
                    :src="getCurrency.icon"
                    style="color: transparent"
                  />
                </div>
              </button>
            </label>
          </div>

          <!-- SWAP -->
          <button
            type="button"
            class="homePressable absolute md:size-14 size-9 bg-bg-secondary md:rounded-[16px] rounded-[12px] flex justify-center items-center cursor-pointer border border-border-primary top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 max-md:rotate-90"
            @click="swapCurrencies"
            :aria-label="tr(&quot;Поменять местами&quot;)"
            :disabled="isGiveCardTransfer"
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
              class="homeSwapIcon lucide lucide-arrow-right-left md:size-8 size-5 text-white"
              :style="{ rotate: `${swapRotation}deg` }"
              :class="isGiveCardTransfer ? 'opacity-40' : ''"
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
                  data-slot="input"
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
                {{ tr(telegramError) }}
              </p>
            </div>
          </div>

          <div data-slot="form-item" class="grid gap-2">
            <div class="flex flex-col gap-1" data-slot="form-control" aria-invalid="false">
              <div class="relative w-full">
                <input
                  data-slot="input"
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
                >{{ tr(getWalletLabel) }}*</label>
              </div>
              <p v-if="walletError" class="md:text-base text-sm font-medium leading-[150%] text-danger">
                {{ tr(walletError) }}
              </p>
            </div>
          </div>
        </div>

        <div class="grid items-center md:grid-cols-2 grid-cols-1 md:gap-6 gap-4 max-md:mt-2">
          <div class="md:pl-8 max-md:text-center">
            <span class="md:text-base text-sm font-light leading-[150%] text-text-tertiary">
              {{ tr("Cрок зачисления — 5-60 минут, в зависимости от загруженности блокчейна") }}
            </span>
            <div class="md:text-sm text-xs font-medium mt-2 text-text-secondary max-md:text-center">
              <template v-if="!isGiveCardTransfer">
                {{ tr("Комиссия сервиса:") }} <span class="text-white">{{ feePercent }}%</span> •
              </template>
              {{ tr(rateText) }}
            </div>
          </div>

          <button
            data-slot="button"
            class="homePressable inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-brand hover:bg-brand-hover text-text-primary data-[state=active]:bg-brand-active data-[state=active]:text-text-inv-primary md:py-6 py-4.5 max-md:rounded-[22px]"
            type="submit"
            :disabled="!canExchange || isSubmitting"
          >
            <p class="md:text-xl text-base font-medium leading-[140%]">
              {{ isSubmitting ? tr("Загрузка...") : tr("Обменять") }}
            </p>
          </button>
        </div>

        <Teleport to="body">
          <Transition name="glass-dropdown" :duration="currencyMenuDuration">
          <div
            v-if="openDropdown"
            class="currencyPopover"
            data-currency-popover
            :style="{ ...dropdownStyle, zIndex: 2147483647 }"
            @click.stop
          >
            <div
              class="currencyMenuSurface md:rounded-[28px] rounded-[22px] border border-border-secondary overflow-hidden shadow-2xl backdrop-blur-md bg-[#0B1220]"
              :style="{ '--row': '76px' }"
              data-currency-menu
              style="pointer-events: auto"
              @click.stop
            >
              <div
                class="overflow-y-auto overflow-x-hidden hide-scrollbar"
                data-currency-scroll
                @wheel.stop
                :style="{ maxHeight: 'var(--currency-list-height, 228px)', overflowY: 'auto', pointerEvents: 'auto', overscrollBehaviorY: 'contain', touchAction: 'pan-y' }"
              >
                <button
                  v-for="c in dropdownOptions"
                  :key="dropdownSide + '-' + c.backendId"
                  type="button"
                  class="w-full px-6 py-0 flex items-stretch transition duration-150 hover:bg-white/10 border-b border-white/5 last:border-b-0"
                  :style="{ height: 'var(--row)' }"
                  @click="selectCurrency(dropdownSide, c)"
                >
                  <div
                    v-if="!isMobile && dropdownSide === 'give'"
                    class="w-full h-full flex items-center justify-between"
                  >
                    <div class="flex flex-col text-left leading-tight">
                      <span class="text-white text-xl font-medium">{{ tr(c.name) }}</span>
                      <span class="text-white text-base font-light">
                        {{ c.symbol }}
                      </span>
                    </div>

                    <div class="flex flex-col items-center justify-center gap-1 shrink-0">
                      <img :alt="c.name" class="w-12 h-12 object-contain drop-shadow" :src="c.icon" />
                      <span class="text-white text-sm font-medium">{{ c.symbol }}</span>
                    </div>
                  </div>

                  <div
                    v-else-if="!isMobile && dropdownSide === 'get'"
                    class="w-full h-full flex items-center justify-between"
                  >
                    <div class="flex flex-col items-center justify-center gap-1 shrink-0">
                      <img :alt="c.name" class="w-12 h-12 object-contain drop-shadow" :src="c.icon" />
                      <span class="text-white text-sm font-medium">{{ c.symbol }}</span>
                    </div>

                    <div class="flex flex-col text-right leading-tight">
                      <span class="text-white text-xl font-medium">{{ tr(c.name) }}</span>
                      <span class="text-white text-base font-light">
                        {{ c.symbol }}
                      </span>
                    </div>
                  </div>

                  <div v-else class="w-full h-full flex items-center justify-between">
                    <div class="flex flex-col text-left leading-tight">
                      <span class="text-white text-lg font-medium">{{ tr(c.name) }}</span>
                      <span class="text-white text-base font-light">
                        {{ c.symbol }}
                      </span>
                    </div>

                    <div class="flex flex-col items-center justify-center gap-1 shrink-0">
                      <img :alt="c.name" class="w-12 h-12 object-contain drop-shadow" :src="c.icon" />
                      <span class="text-white text-sm font-medium">{{ c.symbol }}</span>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          </div>
          </Transition>
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
import { tr, localeTag } from '../lib/i18n';
import { marketRates, refreshRates, siteSettings } from "../lib/siteState";
import { useExchange, lockQuote } from "../lib/exchange";
import { useCurrencyDropdown, currencyDropdownPlacement, currencyMenuDuration } from "../lib/currencyDropdown";
import { getPublicSettings } from "../lib/siteState";
import { computed, onBeforeUnmount, onMounted, ref, watch, nextTick } from "vue";

const swapRotation = ref(0);

const feePercent = ref(4);

const limitsFromSettings = ref({
  giveMin: 500,
  giveMax: 600000,
  getMin: 400,
  getMax: 1000000,
});

const isMobile = ref(false);
const updateIsMobile = () => {
  isMobile.value = window.innerWidth < 768;
};

const currencies = ref([
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
]);

const RUB_METHODS = [
  { id: "rub-sbp", backendId: 2001, symbol: "RUB", name: tr("СБП"), icon: "/img/sbp.svg?v=032", type: "fiat", fiat: "rub", rubKind: "sbp" },
  { id: "rub-qr", backendId: 2011, symbol: "RUB", name: tr("Сбер QR наличные"), icon: "/img/qr_sber.svg?v=032", type: "fiat", fiat: "rub", rubKind: "qr" },
  { id: "rub-sber", backendId: 2002, symbol: "RUB", name: tr("Сбер"), icon: "/img/sber.svg?v=032", type: "fiat", fiat: "rub", rubKind: "card" },
  { id: "rub-alfa", backendId: 2003, symbol: "RUB", name: tr("Альфа-банк"), icon: "/img/alpha.svg?v=032", type: "fiat", fiat: "rub", rubKind: "card" },
  { id: "rub-cash", backendId: 2010, symbol: "RUB", name: tr("Наличные"), icon: "/img/rub_nal.svg?v=032", type: "fiat", fiat: "rub", rubKind: "cash" },
];

const RUB_INPUT_METHODS = ref([
  {
    id: "rub-card-in",
    backendId: 2101,
    symbol: "RUB",
    name: tr("Перевод на карту"),
    icon: "/img/sbp.svg?v=032",
    type: "fiat",
    fiat: "rub",
    rubKind: "card_transfer",
  },
]);

const publicSettings = ref(siteSettings.value || {
  mode: "1",
  banner: "",
  percent: 4,
  giveMin: 500,
  giveMax: 600000,
  getMin: 400,
  getMax: 1000000,
  deposit_wallets: {},
  fiat_in: {},
  fiat_in_methods: {},
});

const bannerText = computed(() => String(publicSettings.value?.banner || "").trim());
const hasBanner = computed(() => !!bannerText.value);

const giveOptions = computed(() => [...RUB_INPUT_METHODS.value, ...currencies.value]);
const getOptions = computed(() => [...currencies.value, ...RUB_METHODS]);
const dropdownOptions = computed(() => (dropdownSide.value === "give" ? giveOptions.value : getOptions.value));



const giveCurrency = ref(RUB_INPUT_METHODS.value[0]);
const getCurrency = ref(currencies.value[0]);

const giveAmountStr = ref("");
const getAmountStr = ref("");
const telegram = ref("");
const wallet = ref("");

const isSubmitting = ref(false);
const submitError = ref("");
const lastEdited = ref("give");

const openDropdown = ref(null);
const dropdownSide = ref("give");
const giveBtnRef = ref(null);
const getBtnRef = ref(null);
const giveFieldRef = ref(null);
const getFieldRef = ref(null);
const dropdownStyle = ref({ top: "0px", left: "0px", width: "280px" });
const { direction, exchangeRate, rateText, limitsInGive, limitsInGet, hasRates, recalcGetFromGive, recalcGiveFromGet } = useExchange(giveCurrency, getCurrency, giveAmountStr, getAmountStr, lastEdited);

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
const isGetFiat = computed(() => getCurrency.value?.type === "fiat");
const isGetRUB = computed(() => isGetFiat.value && getCurrency.value?.fiat === "rub");
const isGiveCardTransfer = computed(() => Number(giveCurrency.value?.backendId) === 2101);

const effectiveFeeMul = computed(() => {
  if (isGiveCardTransfer.value) return 1;
  return (100 - Number(feePercent.value || 0)) / 100;
});

const limitsUsd = computed(() => ({
  giveMin: Number(limitsFromSettings.value.giveMin || 0),
  giveMax: Number(limitsFromSettings.value.giveMax || 0),
  getMin: Number(limitsFromSettings.value.getMin || 0),
  getMax: Number(limitsFromSettings.value.getMax || 0),
}));

const reserves = ref({
  bitcoin: 12,
  ethereum: 350,
});

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

const fiatInMin = computed(() => fiatInRows.value.length ? fiatInRows.value[0].from : 0);
const fiatInMax = computed(() => fiatInRows.value.length ? fiatInRows.value[fiatInRows.value.length - 1].to : 0);
const firstFiatRate = computed(() => fiatInRows.value.length ? fiatInRows.value[0].rate : 0);

const currentFiatInRow = computed(() => {
  if (!isGiveCardTransfer.value) return null;
  const amount = toNumber(giveAmountStr.value);
  if (!amount) return null;
  return fiatInRows.value.find((x) => amount >= x.from && amount <= x.to) || null;
});

const isPairAllowed = (give, get) => {
  const giveFiat = give?.type === "fiat";
  const getFiat = get?.type === "fiat";

  if (giveFiat && getFiat) return false;
  if (giveFiat && Number(give?.backendId) !== 2101) return false;

  const giveId = Number(give?.backendId);
  const getId = Number(get?.backendId);

  if (!giveFiat && !getFiat) {
    if (giveId === getId) return false;
  }

  return true;
};

const findFirstAllowedGet = (give) => {
  return getOptions.value.find((x) => isPairAllowed(give, x)) || currencies.value[0];
};

const findFirstAllowedGive = (get) => {
  return giveOptions.value.find((x) => isPairAllowed(x, get)) || RUB_INPUT_METHODS.value[0];
};

const giveRangeText = computed(() => `${limitsInGive.value.giveMin} - ${limitsInGive.value.giveMax} ${giveCurrency.value.symbol}`);
const giveAmountN = computed(() => toNumber(giveAmountStr.value));
const getAmountN = computed(() => toNumber(getAmountStr.value));

const giveMinN = computed(() => toNumber(limitsInGive.value.giveMin));
const giveMaxN = computed(() => toNumber(limitsInGive.value.giveMax));
const getMinN = computed(() => toNumber(limitsInGet.value.getMin));
const getMaxN = computed(() => toNumber(limitsInGet.value.getMax));


const amountError = computed(() => {
  if (!hasRates.value) return tr("Курс временно недоступен. Попробуйте позже.");
  if (!giveAmountStr.value && !getAmountStr.value) return "";
  const n = Number(giveAmountStr.value);
  if (direction.value?.funding_ranges?.length && n > 0 && !direction.value.funding_ranges.some(t => n >= t.from && n <= t.to)) return tr("Сумма не попадает в доступный диапазон приёма рублей");
  if (n < Number(limitsInGive.value.giveMin)) return tr("Минимум для внесения: {p0} {p1}", { p0: (limitsInGive.value.giveMin), p1: (giveCurrency.value.symbol) });
  if (n > Number(limitsInGive.value.giveMax)) return tr("Максимум для внесения: {p0} {p1}", { p0: (limitsInGive.value.giveMax), p1: (giveCurrency.value.symbol) });
  if (direction.value?.tiers?.length && !direction.value.tiers.some(t => n >= t.from && n <= t.to)) return tr("Сумма не попадает в доступный диапазон");
  if (Number(getAmountStr.value) < Number(limitsInGet.value.getMin) || Number(getAmountStr.value) > Number(limitsInGet.value.getMax)) return tr("Сумма получения вне лимитов направления");
  return "";
});

const validateTelegramUsername = (s) => {
  const raw = normalizeSpaces(s);
  if (!raw) return "";

  const cleaned = raw
    .replace(/^https?:\/\/t\.me\//i, "")
    .replace(/^t\.me\//i, "")
    .replace(/^@/, "");

  return /^[A-Za-z][A-Za-z0-9_]{4,31}$/.test(cleaned) ? "" : tr("Некорректный формат Telegram");
};

const validateCardNumber = (s) => {
  const v = String(s ?? "").replace(/\s+/g, "");
  if (!v) return "";
  return /^\d{13,19}$/.test(v) ? "" : tr("Некорректный формат карты");
};

const validateCryptoAddress = (addr, currency) => {
  const v = normalizeSpaces(addr);
  if (!v) return "";

  const cid = currency?.id;
  const bid = currency?.backendId;

  if (
  cid === "ethereum" ||
  cid === "dai" ||
  cid === "usd-coin" ||
  bid === 4 || // USDT ERC20
  bid === 5    // USDT BEP20
) {
  return /^0x[a-fA-F0-9]{40}$/.test(v) ? "" : tr("Некорректный формат кошелька");
}

  if (cid === "bitcoin") {
    const legacy = /^[13][1-9A-HJ-NP-Za-km-z]{25,34}$/.test(v);
    const bech32 = /^bc1[0-9a-z]{25,90}$/.test(v);
    return legacy || bech32 ? "" : tr("Некорректный формат кошелька");
  }

  if (cid === "tron" || bid === 3) {
    return /^T[1-9A-HJ-NP-Za-km-z]{33}$/.test(v) ? "" : tr("Некорректный формат кошелька");
  }

 if (cid === "solana" || bid === 6) {
  return /^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(v) ? "" : tr("Некорректный формат кошелька");
}

  if (cid === "litecoin") {
    const legacy = /^[LM3][1-9A-HJ-NP-Za-km-z]{25,34}$/.test(v);
    const bech32 = /^ltc1[0-9a-z]{25,90}$/.test(v);
    return legacy || bech32 ? "" : tr("Некорректный формат кошелька");
  }

  if (cid === "dogecoin") {
    return /^D[1-9A-HJ-NP-Za-km-z]{25,34}$/.test(v) ? "" : tr("Некорректный формат кошелька");
  }

  return "";
};

const telegramError = computed(() => validateTelegramUsername(telegram.value));

const walletError = computed(() => {
  const v = normalizeSpaces(wallet.value);
  if (!v) return "";

  if (isGetRUB.value) {
    const kind = getCurrency.value?.rubKind;
    if (kind === "card") return validateCardNumber(v);
    return "";
  }

  return validateCryptoAddress(v, getCurrency.value);
});

const directionError = computed(() => {
  if (isGiveFiat.value && isGetFiat.value) {
    return tr("Обмен не возможен");
  }
  return "";
});

const topError = computed(() => submitError.value || directionError.value || amountError.value || "");

const canExchange = computed(() => {
  const hasRequired = !!telegram.value.trim() && !!wallet.value.trim();
  const hasAmount = giveAmountN.value > 0 && getAmountN.value > 0;
  const noFieldErrors = !telegramError.value && !walletError.value;

  return (
    hasRates.value &&
    hasRequired &&
    hasAmount &&
    !directionError.value &&
    !amountError.value &&
    noFieldErrors
  );
});

const getWalletLabel = computed(() => {
  if (!isGetRUB.value) return tr("{p0} адрес", { p0: (getCurrency.value.name) });

  switch (getCurrency.value.rubKind) {
    case "sbp":
      return tr("Номер телефона и банк");
    case "card":
      return tr("Номер карты");
    case "cash":
      return tr("Укажите Ваш город");
    case "qr":
      return tr("Укажите город снятия");
    default:
      return tr("Реквизиты");
  }
});

const selectCurrency = (side, c) => {
  if (side === "give") {
    giveCurrency.value = c;
  } else {
    getCurrency.value = c;
  }

  openDropdown.value = null;

  if (lastEdited.value === "give") {
    recalcGetFromGive();
  } else if (!isGiveCardTransfer.value) {
    recalcGiveFromGet();
  }
};



const swapCurrencies = () => {
  if (isGiveCardTransfer.value) return;

  const nextGive = getCurrency.value;
  const nextGet = giveCurrency.value;

  if (!isPairAllowed(nextGive, nextGet)) return;

  const tmpGive = giveCurrency.value;
  const tmpGet = getCurrency.value;

  giveCurrency.value = tmpGet;
  getCurrency.value = tmpGive;

  const tmpA = giveAmountStr.value;
  giveAmountStr.value = getAmountStr.value;
  getAmountStr.value = tmpA;

  swapRotation.value += 180;

  if (lastEdited.value === "give") recalcGetFromGive();
  else recalcGiveFromGet();
};

const closeDropdown = () => {
  openDropdown.value = null;
};

useCurrencyDropdown(openDropdown, closeDropdown, giveFieldRef, getFieldRef);

const positionDropdown = () => {
  const el = dropdownSide.value === "give" ? giveFieldRef.value : getFieldRef.value;
  if (el) dropdownStyle.value = currencyDropdownPlacement(el);
};

const toggleDropdown = (side) => {
  if (openDropdown.value === side) {
    closeDropdown();
    return;
  }
  dropdownSide.value = side;
  positionDropdown();
  openDropdown.value = side;
};

const onReposition = () => {
  if (openDropdown.value) positionDropdown();
};

const setGiveAmount = (vStr) => {
  lastEdited.value = "give";
  giveAmountStr.value = String(vStr);
};

const setGetAmount = (vStr) => {
  if (isGiveCardTransfer.value) return;
  lastEdited.value = "get";
  getAmountStr.value = String(vStr);
};

const onGetInput = () => {
  if (isGiveCardTransfer.value) return;
  lastEdited.value = "get";
};

async function loadPublicSettings() {
  try {
    const data = await getPublicSettings();
    publicSettings.value = data || {};

    if (typeof data?.percent !== "undefined") {
      feePercent.value = Number(data.percent) || 0;
    }

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
      RUB_INPUT_METHODS.value = [{
        id: "rub-card-in",
        backendId: 2101,
        symbol: String(method2101.symbol || "RUB"),
        name: String(method2101.name || tr("Перевод на карту")),
        icon: String(method2101.icon || "/img/sbp.svg?v=032"),
        type: "fiat",
        fiat: "rub",
        rubKind: "card_transfer",
      }];
    }
  } catch {}
}

const fetchPrices = async () => {};
const scheduleNextFetch = () => {};

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
      coingecko_id: isGetFiat.value ? null : getCurrency.value.id,
      symbol: getCurrency.value.symbol,
      amount: getAmountN.value,
    },
    fee_percent: isGiveCardTransfer.value ? 0 : Number(feePercent.value || 0),

    get_is_fiat: !!getCurrency.value.type && getCurrency.value.type === "fiat",
    fiat_code: (isGiveFiat.value || isGetFiat.value) ? "rub" : null,
    rub_kind: isGetFiat.value
      ? (getCurrency.value.rubKind ?? null)
      : isGiveFiat.value
        ? (giveCurrency.value.rubKind ?? null)
        : null,

    client: {
      telegram: telegram.value.trim(),
      payout_details: wallet.value.trim(),
    },

    rates_snapshot: {},

    created_at: new Date().toISOString(),
  };

  try {
    await lockQuote(payload);
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
        submitError.value = j?.detail || tr("Не удалось создать обмен. Попробуйте ещё раз.");
      } catch {
        submitError.value = tr("Не удалось создать обмен. Попробуйте ещё раз.");
      }
      return;
    }

    const data = await res.json();
    const ticketId = data?.ticket_id;

    if (!ticketId) {
      submitError.value = tr("Сервер не вернул ticket_id. Попробуйте ещё раз.");
      return;
    }

    window.location.href = `/tickets/${ticketId}`;
  } catch (e) {
    submitError.value = e?.message || tr("Ошибка сети. Попробуйте ещё раз.");
  } finally {
    isSubmitting.value = false;
  }
};

watch(
  [giveAmountStr, () => giveCurrency.value.backendId, () => getCurrency.value.backendId],
  () => {
    if (lastEdited.value === "give") recalcGetFromGive();
  }
);

watch(getAmountStr, () => {
  if (lastEdited.value === "get" && !isGiveCardTransfer.value) {
    recalcGiveFromGet();
  }
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

  giveCurrency.value = RUB_INPUT_METHODS.value[0];
  getCurrency.value = findFirstAllowedGet(giveCurrency.value);

  await fetchPrices();
  scheduleNextFetch();

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
</style>