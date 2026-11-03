<!-- homepage.vue -->
<template>
  <div data-exchange-mode="0" class="flex flex-col grow basis-full relative">
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
      <div class="flex flex-col md:gap-6 gap-3 text-white">
        <h1 class="md:text-7xl text-[32px] font-medium leading-[110%] text-center">
          {{ tr("Скоростной") }} <br />
          {{ tr("обмен криптовалют") }}
        </h1>
        <span class="md:text-xl text-base font-light leading-[140%] text-center max-w-110 self-center">
          {{ tr("Безопасный и удобный способ обмена криптовалюты за считанные минуты, без AML и KYC проверки") }}
        </span>
      </div>

      <form
        class="flex flex-col md:gap-6 gap-2 md:p-12 p-6 md:rounded-[64px] rounded-[40px] bg-bg-tertiary border border-border-secondary"
        @submit.prevent="onSubmit"
      >
        <!-- error над стрелками -->
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
                  <span class="cursor-pointer" @click="setGiveAmount(limitsInGive.giveMin)">{{ limitsInGive.giveMin }}</span>
                  -
                  <span class="cursor-pointer" @click="setGiveAmount(limitsInGive.giveMax)">{{ limitsInGive.giveMax }}</span>
                </p>
              </div>

              <button
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
                  v-model="getAmountStr"
                  @input="lastEdited = 'get'"
                />

                <p class="md:text-base text-sm font-medium leading-[150%] text-text-secondary">
                  <span class="cursor-pointer" @click="setGetAmount(limitsInGet.getMin)">{{ limitsInGet.getMin }}</span>
                  -
                  <span class="cursor-pointer" @click="setGetAmount(limitsInGet.getMax)">{{ limitsInGet.getMax }}</span>
                </p>
              </div>

              <button
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
            class="absolute md:size-14 size-9 bg-bg-secondary md:rounded-[16px] rounded-[12px] flex justify-center items-center cursor-pointer border border-border-primary top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 max-md:rotate-90"
            @click="swapCurrencies"
            :aria-label="tr(&quot;Поменять местами&quot;)"
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
              class="lucide lucide-arrow-right-left md:size-8 size-5 text-white"
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
          <!-- TELEGRAM -->
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

          <!-- WALLET -->
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
              {{ tr("Комиссия сервиса:") }} <span class="text-white">{{ feePercent }}%</span> •
              {{ tr(rateText) }}
            </div>
          </div>

          <button
          data-slot="button"
          class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-brand hover:bg-brand-hover text-text-primary data-[state=active]:bg-brand-active data-[state=active]:text-text-inv-primary md:py-6 py-4.5 max-md:rounded-[22px]"
          type="submit"
          :disabled="!canExchange || isSubmitting"
        >
          <p class="md:text-xl text-base font-medium leading-[140%]">
            {{ isSubmitting ? tr("Загрузка...") : tr("Обменять") }}
          </p>
        </button>
        </div>

        <!-- блок для будущего ручного добавления направлений -->
        <!--
        TODO (на перспективу):
        Здесь будет конфиг направлений, которые ты добавляешь вручную, например:
        const directions = [
          { from: 'bitcoin', to: 'ethereum', enabled: true, customFeePercent: 4 },
          { from: 'toncoin', to: 'tether', enabled: false },
          ...
        ]
        И логика, чтобы пользователь мог выбирать только разрешённые пары.
        -->

        <!-- ✅ TELEPORT DROPDOWN -->
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
                  <!-- DESKTOP: GIVE -->
                  <div
                    v-if="!isMobile && dropdownSide === 'give'"
                    class="w-full h-full flex items-center justify-between"
                  >
                    <div class="flex flex-col text-left leading-tight">
                      <span class="text-white text-xl font-medium">{{ tr(c.name) }}</span>
                      <span style="color:#fff !important;" class="text-white/70 text-base font-light">
                        {{ c.symbol }}
                      </span>
                    </div>

                    <div class="flex flex-col items-center justify-center gap-1 shrink-0">
                      <img :alt="c.name" class="w-12 h-12 object-contain drop-shadow" :src="c.icon" />
                      <span style="color:#fff !important;" class="text-white/70 text-sm font-medium">{{ c.symbol }}</span>
                    </div>
                  </div>

                  <!-- DESKTOP: GET -->
                  <div
                    v-else-if="!isMobile && dropdownSide === 'get'"
                    class="w-full h-full flex items-center justify-between"
                  >
                    <div class="flex flex-col items-center justify-center gap-1 shrink-0">
                      <img :alt="c.name" class="w-12 h-12 object-contain drop-shadow" :src="c.icon" />
                      <span style="color:#fff !important;" class="text-white/70 text-sm font-medium">{{ c.symbol }}</span>
                    </div>

                    <div class="flex flex-col text-right leading-tight">
                      <span class="text-white text-xl font-medium">{{ tr(c.name) }}</span>
                      <span style="color:#fff !important;" class="text-white/70 text-base font-light">
                        {{ c.symbol }}
                      </span>
                    </div>
                  </div>

                  <!-- MOBILE -->
                  <div v-else class="w-full h-full flex items-center justify-between">
                    <div class="flex flex-col text-left leading-tight">
                      <span class="text-white text-lg font-medium">{{ tr(c.name) }}</span>
                      <span style="color:#fff !important;" class="text-white/70 text-base font-light">
                        {{ c.symbol }}
                      </span>
                    </div>

                    <div class="flex flex-col items-center justify-center gap-1 shrink-0">
                      <img :alt="c.name" class="w-12 h-12 object-contain drop-shadow" :src="c.icon" />
                      <span style="color:#fff !important;" class="text-white/70 text-sm font-medium">{{ c.symbol }}</span>
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

/**
 * Комиссия сервиса
 */
const feePercent = ref(4);
const feeMul = computed(() => (100 - Number(feePercent.value || 0)) / 100);
const limitsFromSettings = ref({
  giveMin: 500,
  giveMax: 600000,
  getMin: 400,
  getMax: 1000000,
});
/**
 * Mobile breakpoint
 */
const isMobile = ref(false);
const updateIsMobile = () => {
  isMobile.value = window.innerWidth < 768;
};

/**
 * Криптовалюты (CoinGecko ids)
 */
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

/**
 * RUB как "fiat" для правого списка
 * Важно: id = "rub" это vs_currency, не coin id.
 */
const RUB_METHODS = [
  { id: "rub-sbp",   backendId: 2001, symbol: "RUB", name: tr("СБП"),        icon: "/img/sbp.svg?v=032",  type: "fiat", fiat: "rub", rubKind: "sbp" },
  { id: "rub-qr",    backendId: 2011, symbol: "RUB", name: tr("Сбер QR наличные"),         icon: "/img/qr_sber.svg?v=032",   type: "fiat", fiat: "rub", rubKind: "qr" },
  { id: "rub-sber",  backendId: 2002, symbol: "RUB", name: tr("Сбер"),       icon: "/img/sber.svg?v=032", type: "fiat", fiat: "rub", rubKind: "card" },
  { id: "rub-alfa",  backendId: 2003, symbol: "RUB", name: tr("Альфа-банк"), icon: "/img/alpha.svg?v=032", type: "fiat", fiat: "rub", rubKind: "card" },
  { id: "rub-cash",  backendId: 2010, symbol: "RUB", name: tr("Наличные"),   icon: "/img/rub_nal.svg?v=032", type: "fiat", fiat: "rub", rubKind: "cash" },
  
];

const giveOptions = computed(() => currencies.value); // слева только крипта
const getOptions = computed(() => [...currencies.value, ...RUB_METHODS]); // справа крипта + RUB
const dropdownOptions = computed(() => (dropdownSide.value === "give" ? giveOptions.value : getOptions.value));

/**
 * Резервы (пример)
 */
const reserves = ref({
  bitcoin: 12,
  ethereum: 350,
});

/**
 * Базовые лимиты в USD
 */
const limitsUsd = computed(() => ({
  giveMin: Number(limitsFromSettings.value.giveMin || 0),
  giveMax: Number(limitsFromSettings.value.giveMax || 0),
  getMin: Number(limitsFromSettings.value.getMin || 0),
  getMax: Number(limitsFromSettings.value.getMax || 0),
}));

/**
 * Курсы
 */


/**
 * Выбранные валюты
 */
const giveCurrency = ref(currencies.value[0]);
const getCurrency = ref(currencies.value[1] ?? currencies.value[0]);

/**
 * Поля
 */
const giveAmountStr = ref("");
const getAmountStr = ref("");
const telegram = ref("");
const wallet = ref("");

const isSubmitting = ref(false);
const submitError = ref("");
/**
 * Чтобы не было бесконечных пересчётов
 */
const lastEdited = ref("give"); // 'give' | 'get'

/**
 * Dropdown state + refs for positioning
 */
const openDropdown = ref(null); // 'give' | 'get' | null
const dropdownSide = ref("give");
const giveBtnRef = ref(null);
const getBtnRef = ref(null);
const giveFieldRef = ref(null);
const getFieldRef = ref(null);

const dropdownStyle = ref({ top: "0px", left: "0px", width: "280px" });
const { direction, exchangeRate, rateText, limitsInGive, limitsInGet, hasRates, recalcGetFromGive, recalcGiveFromGet } = useExchange(giveCurrency, getCurrency, giveAmountStr, getAmountStr, lastEdited);

/**
 * Helpers
 */
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

/**
 * Получаем ли справа RUB
 */
const isGetRUB = computed(() => getCurrency.value?.type === "fiat" && getCurrency.value.fiat === "rub");

/**
 * Цены
 */
const giveAmountN = computed(() => toNumber(giveAmountStr.value));
const getAmountN = computed(() => toNumber(getAmountStr.value));

const giveMinN = computed(() => toNumber(limitsInGive.value.giveMin));
const giveMaxN = computed(() => toNumber(limitsInGive.value.giveMax));
const getMinN = computed(() => toNumber(limitsInGet.value.getMin));
const getMaxN = computed(() => toNumber(limitsInGet.value.getMax));

// курс готов?

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

const topError = computed(() => submitError.value || amountError.value || "");

const canExchange = computed(() => {
  const hasRequired = !!telegram.value.trim() && !!wallet.value.trim();
  const hasAmount = giveAmountN.value > 0 && getAmountN.value > 0;

  const noFieldErrors = !telegramError.value && !walletError.value;

  return hasRates.value && hasRequired && hasAmount && !amountError.value && noFieldErrors;
});
/**
 * Wallet label (если RUB — другой текст)
 */
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

/**
 * VALIDATION
 * - Telegram: username (не ссылка, без @)
 * - Wallet: крипто-адреса по маскам, для RUB(card) — номер карты
 * - Для sbp/qr/cash — только непусто (как сейчас)
 */
const normalizeSpaces = (s) => String(s ?? "").replace(/\s+/g, " ").trim();

const validateTelegramUsername = (s) => {
  const raw = normalizeSpaces(s);
  if (!raw) return "";

  // разрешаем ввод с @, но проверяем username без @
  const v = raw.startsWith("@") ? raw.slice(1) : raw;

  // Telegram username: 5–32, только латиница/цифры/_, начинается с буквы
  const ok = /^[A-Za-z][A-Za-z0-9_]{4,31}$/.test(v);
  return ok ? "" : tr("Некорректный формат Telegram");
};

const validateCardNumber = (s) => {
  const v = String(s ?? "").replace(/\s+/g, "");
  if (!v) return "";
  // 13–19 цифр (подходит под большинство карт; пробелы разрешаем, мы их удаляем)
  const ok = /^\d{13,19}$/.test(v);
  return ok ? "" : tr("Некорректный формат карты");
};

const isEthLike = (id) => ["ethereum", "dai", "usd-coin"].includes(id) || id === "tether"; // tether ERC20 тоже сюда, но он отличается backendId — см. ниже
const validateCryptoAddress = (addr, currency) => {
  const v = normalizeSpaces(addr);
  if (!v) return "";

  const cid = currency?.id;
  const bid = currency?.backendId;

  // ETH + ERC20 (ETH, USDT ERC20 (backendId=4), DAI, USDC)
  if (
    cid === "ethereum" ||
    cid === "dai" ||
    cid === "usd-coin" ||
    bid === 4 || // USDT ERC20
    bid === 5    // USDT BEP20
  ) {
    return /^0x[a-fA-F0-9]{40}$/.test(v) ? "" : tr("Некорректный формат кошелька");
  }

  // BTC
  if (cid === "bitcoin") {
    const legacy = /^[13][1-9A-HJ-NP-Za-km-z]{25,34}$/.test(v);
    const bech32 = /^bc1[0-9a-z]{25,90}$/.test(v);
    return (legacy || bech32) ? "" : tr("Некорректный формат кошелька");
  }

  // TRON / USDT TRC20 / TRX
  if (cid === "tron" || bid === 3 /* USDT TRC20 */) {
    return /^T[1-9A-HJ-NP-Za-km-z]{33}$/.test(v) ? "" : tr("Некорректный формат кошелька");
  }

  // SOL
  if (cid === "solana" || bid === 6) {
  return /^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(v) ? "" : tr("Некорректный формат кошелька");
  }

  // LTC
  if (cid === "litecoin") {
    const legacy = /^[LM3][1-9A-HJ-NP-Za-km-z]{25,34}$/.test(v);
    const bech32 = /^ltc1[0-9a-z]{25,90}$/.test(v);
    return (legacy || bech32) ? "" : tr("Некорректный формат кошелька");
  }

  // DOGE
  if (cid === "dogecoin") {
    return /^D[1-9A-HJ-NP-Za-km-z]{25,34}$/.test(v) ? "" : tr("Некорректный формат кошелька");
  }

  // По умолчанию (если появятся новые монеты) — не валидируем строго
  return "";
};

const telegramError = computed(() => validateTelegramUsername(telegram.value));

const walletError = computed(() => {
  const v = normalizeSpaces(wallet.value);
  if (!v) return "";

  // Если справа RUB
  if (isGetRUB.value) {
    const kind = getCurrency.value?.rubKind;

    // карта: валидируем
    if (kind === "card") return validateCardNumber(v);

    // sbp / qr / cash: только наличие текста
    return "";
  }

  // Если справа крипта — валидируем адрес под выбранную валюту
  return validateCryptoAddress(v, getCurrency.value);
});

/**
 * Выбор валют и swap
 */
const selectCurrency = (side, c) => {
  // слева по-прежнему только крипта
  if (side === "give" && c.type === "fiat") return;

  if (side === "give") {
    giveCurrency.value = c;
  } else {
    getCurrency.value = c;
  }

  openDropdown.value = null;

  if (lastEdited.value === "give") recalcGetFromGive();
  else recalcGiveFromGet();
};

const swapCurrencies = () => {
  // если справа RUB — свап запрещаем (иначе RUB попадёт в "вносите")
  if (isGetRUB.value) return;

  const tmp = giveCurrency.value;
  giveCurrency.value = getCurrency.value;
  getCurrency.value = tmp;

  const tmpA = giveAmountStr.value;
  giveAmountStr.value = getAmountStr.value;
  getAmountStr.value = tmpA;

  if (lastEdited.value === "give") recalcGetFromGive();
  else recalcGiveFromGet();
};

/**
 * Dropdown positioning
 */
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

/**
 * Быстрые установки
 */
const setGiveAmount = (vStr) => {
  lastEdited.value = "give";
  giveAmountStr.value = vStr;
};

const setGetAmount = (vStr) => {
  lastEdited.value = "get";
  getAmountStr.value = vStr;
};

const publicSettings = ref(siteSettings.value || { percent: 4, deposit_wallets: {}, banner: "" });

const bannerText = computed(() => String(publicSettings.value?.banner || "").trim());
const hasBanner = computed(() => !!bannerText.value);

async function loadPublicSettings() {
  try {
    const data = await getPublicSettings();
    publicSettings.value = data || {};

    // ✅ забираем percent из settings.json
    if (typeof data?.percent !== "undefined") {
      feePercent.value = Number(data.percent) || 0;
      if (lastEdited.value === "give") recalcGetFromGive();
      else recalcGiveFromGet();
    }
  } catch {
    // молча оставляем дефолт 4
  }
}
/**
 * Rates fetch with cache + backoff
 */
const fetchPrices = async () => {};
const scheduleNextFetch = () => {};

const fetchPublicSettings = async () => {
  try {
    const data = await getPublicSettings();

    // percent
    const p = Number(data?.percent);
    if (Number.isFinite(p) && p >= 0 && p <= 100) {
      feePercent.value = p;
    }

    // limits
    const next = {
      giveMin: Number(data?.giveMin),
      giveMax: Number(data?.giveMax),
      getMin: Number(data?.getMin),
      getMax: Number(data?.getMax),
    };

    // подставляем только если числа адекватные
    if (Number.isFinite(next.giveMin)) limitsFromSettings.value.giveMin = next.giveMin;
    if (Number.isFinite(next.giveMax)) limitsFromSettings.value.giveMax = next.giveMax;
    if (Number.isFinite(next.getMin)) limitsFromSettings.value.getMin = next.getMin;
    if (Number.isFinite(next.getMax)) limitsFromSettings.value.getMax = next.getMax;
  } catch {
    // если сеть упала — остаются дефолты (4% и текущие лимиты)
  }
};

/**
 * Submit payload
 */
const onSubmit = async () => {
  // 1) базовая валидация
  if (!canExchange.value) return;

  // 2) защита от повторных нажатий
  if (isSubmitting.value) return;

  // 3) старт сабмита
  isSubmitting.value = true;
  if (typeof submitError !== "undefined") submitError.value = "";

  const payload = {
    give: {
      currency_backend_id: giveCurrency.value.backendId,
      coingecko_id: giveCurrency.value.id,
      symbol: giveCurrency.value.symbol,
      amount: giveAmountN.value,
    },
    get: {
      currency_backend_id: getCurrency.value.backendId,
      coingecko_id: isGetRUB.value ? null : getCurrency.value.id,
      symbol: getCurrency.value.symbol,
      amount: getAmountN.value,
    },
    fee_percent: Number(feePercent.value || 0),

    get_is_fiat: !!getCurrency.value.type && getCurrency.value.type === "fiat",
    fiat_code: isGetRUB.value ? "rub" : null,
    rub_kind: isGetRUB.value ? (getCurrency.value.rubKind ?? null) : null,

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
      if (typeof submitError !== "undefined") {
        // попробуем вытащить detail с бэка
        try {
          const j = await res.json();
          submitError.value = j?.detail || tr("Не удалось создать обмен. Попробуйте ещё раз.");
        } catch {
          submitError.value = tr("Не удалось создать обмен. Попробуйте ещё раз.");
        }
      }
      return;
    }

    const data = await res.json();
    const ticketId = data?.ticket_id;

    if (!ticketId) {
      if (typeof submitError !== "undefined") {
        submitError.value = tr("Сервер не вернул ticket_id. Попробуйте ещё раз.");
      }
      return;
    }

    // ✅ редирект на страницу тикета
    window.location.href = `/tickets/${ticketId}`;
  } catch (e) {
    if (typeof submitError !== "undefined") {
      submitError.value = e?.message || tr("Ошибка сети. Попробуйте ещё раз.");
    }
  } finally {
    // если редирект случился — код ниже не выполнится, это ок
    isSubmitting.value = false;
  }
};

/**
 * Watchers
 */
watch([giveAmountStr, () => giveCurrency.value.id, () => getCurrency.value.id], () => {
  if (lastEdited.value === "give") recalcGetFromGive();
});

watch(getAmountStr, () => {
  if (lastEdited.value === "get") recalcGiveFromGet();
});

watch(openDropdown, async (v) => {
  if (!v) return;
  await nextTick();
  positionDropdown();
});

/**
 * Mounted
 */
onMounted(async () => {
  updateIsMobile();
  window.addEventListener("resize", updateIsMobile);
  await loadPublicSettings();

  await fetchPublicSettings(); 
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
/* Скрываем полосу прокрутки, но оставляем скролл */
.hide-scrollbar {
  -ms-overflow-style: none; /* IE/Edge legacy */
  scrollbar-width: none; /* Firefox */
}
.hide-scrollbar::-webkit-scrollbar {
  width: 0;
  height: 0;
}
</style>



