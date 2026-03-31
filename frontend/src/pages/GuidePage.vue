<template>
  <div class="flex flex-col items-center md:gap-12 gap-9 md:py-24 py-8 max-w-225 w-full self-center grow basis-full container text-white">
    <h2 class="md:text-5xl text-[28px] font-medium leading-[120%]">Инструкция</h2>

    <div class="w-full flex flex-col md:gap-6 gap-4">
      <div class="flex flex-col gap-2">
        <h3 class="md:text-3xl text-2xl font-medium leading-[120%]">
          Как получить наличные по QR-коду?
        </h3>
      </div>

      <div class="grid xl:grid-cols-4 md:grid-cols-2 grid-cols-1 md:gap-6 gap-4 w-full">
        <div
          v-for="(step, idx) in qrSteps"
          :key="step.id"
          class="step-card flex flex-col bg-bg-tertiary border border-border-secondary rounded-[28px] overflow-hidden"
        >
          <div class="relative p-4">
            <div class="step-badge">
              Шаг {{ idx + 1 }}
            </div>

            <div class="step-image-wrap">
              <img
                :src="step.img"
                :alt="step.title"
                loading="lazy"
                class="step-image"
              />
            </div>
          </div>

          <div class="flex flex-col gap-3 px-5 pb-6 pt-1 grow">
            <h4 class="md:text-2xl text-xl font-medium leading-[130%]">
              {{ step.title }}
            </h4>
            <p class="md:text-lg text-base font-light leading-[155%] text-white whitespace-pre-line">
              {{ step.text }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="flex flex-col md:gap-4 gap-3 w-full">
      <div class="flex flex-col gap-2">
        <h3 class="md:text-3xl text-2xl font-medium leading-[120%]">
          Какие банкоматы подходят для получения?
        </h3>
      </div>

      <div
        v-for="(item, idx) in countryFaqItems"
        :key="item.id"
        class="flex flex-col bg-bg-tertiary rounded-[28px]"
      >
        <h3 class="flex">
          <button
            type="button"
            class="flex flex-1 items-center justify-between gap-3 text-left md:p-8 p-6 transition-all outline-none disabled:pointer-events-none disabled:opacity-50"
            :aria-expanded="openIndex === idx ? 'true' : 'false'"
            :aria-controls="`faq-panel-${item.id}`"
            @click="toggle(idx)"
          >
            <div class="flex items-center gap-4 min-w-0">
              <div class="country-flag-box shrink-0">
                <img
                  :src="item.icon"
                  :alt="item.symbol"
                  loading="lazy"
                  class="country-flag-img"
                />
              </div>

              <div class="flex flex-col min-w-0">
                <h4 class="md:text-2xl text-xl font-medium leading-[130%]">
                  {{ item.q }}
                </h4>
                <span class="md:text-base text-sm font-light leading-[150%] text-text-secondary">
                  {{ item.symbol }}
                </span>
              </div>
            </div>

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
              class="pointer-events-none md:size-7 size-6 shrink-0 translate-y-0.5 transition-transform duration-300 ease-out"
              :class="openIndex === idx ? 'rotate-180' : 'rotate-0'"
              aria-hidden="true"
            >
              <path d="m6 9 6 6 6-6"></path>
            </svg>
          </button>
        </h3>

        <div
          :id="`faq-panel-${item.id}`"
          role="region"
          class="overflow-hidden"
          :class="openIndex === idx ? 'faq-open' : 'faq-closed'"
          :style="panelStyle(idx)"
        >
          <div class="md:px-8 px-6 pb-6 md:pb-8 pt-0">
            <p class="country-answer md:text-xl text-base font-light leading-[155%] text-white whitespace-pre-line">
              {{ item.a }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="w-full flex flex-col md:gap-6 gap-4">
      <div class="flex flex-col gap-2">
        <h3 class="md:text-3xl text-2xl font-medium leading-[120%]">
          Денежные средства на банковский счет
        </h3>
        <p class="md:text-xl text-base font-light leading-[150%] text-text-secondary">
          При обмене укажите IBAN и ФИО
        </p>
      </div>

      <div class="flex flex-col gap-2">
        <div class="flex flex-col gap-2 basis-full md:p-8 p-6 bg-bg-secondary border border-border-secondary md:rounded-[28px] rounded-[22px]">
          <span class="md:text-xl text-base font-light leading-[140%] text-text-tertiary">
            Важно
          </span>
          <p class="md:text-xl text-base font-medium leading-[140%] break-all">
            Указывайте IBAN полностью и ФИО получателя как в банковских реквизитах.
          </p>
        </div>

        
      </div>
    </div>

    <RouterLink to="/contacts" class="w-full">
      <button
        data-slot="button"
        class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-brand hover:bg-brand-hover text-text-primary data-[state=active]:bg-brand-active data-[state=active]:text-text-inv-primary md:py-6 md:px-7 py-4.5 px-5.5 max-md:rounded-[22px]"
        type="button"
      >
        <p class="md:text-xl text-base font-medium leading-[140%]">
          Связаться с поддержкой
        </p>
      </button>
    </RouterLink>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onBeforeUnmount, ref } from "vue";
import { RouterLink } from "vue-router";

const publicSettings = ref({
  deposit_wallets: {},
});

const qrSteps = [
  {
    id: "step-1",
    img: "/img/inst-1.png",
    title: "Найдите банкомат и оплатите заявку",
    text: "Найдите подходящий банкомат и оплатите заявку на обмен по реквизитам ",
  },
  {
    id: "step-2",
    img: "/img/inst-2.png",
    title: "Сканируйте QR",
    text: "Отсканируйте QR-код банкомата и отправьте его менеджеру, либо введите данные и PIN-код, которые сообщил менеджер.",
  },
  {
    id: "step-3",
    img: "/img/inst-3.png",
    title: "Получите и пересчитайте деньги",
    text: "После выдачи наличных обязательно пересчитайте сумму сразу у банкомата.",
  },
  {
    id: "step-4",
    img: "/img/inst-4.png",
    title: "Оставьте отзыв о сервисе",
    text: "Если всё прошло успешно, оставьте отзыв о работе сервиса в соответсвующем разделе",
  },
];

const ATM_HINTS = {
  THB: "Подойдут ATM следующих банков: Kasikorn Bank, Bangkok Bank, Krungsri, SCB Bank.",
  TRY: "Подойдут ATM следующих банков: Garanti BBVA, Ziraat Bankası, Yapı Kredi, Türkiye İş Bankası.",
  EGP: "Подойдут ATM следующих банков: CIB, Banque Misr, National Bank of Egypt.",
  AED: "Подойдут ATM следующих банков: Emirates NBD, First Abu Dhabi Bank (FAB), ADCB, Dubai Islamic Bank.",
  VND: "Подойдут ATM следующих банков: Vietcombank, BIDV, VietinBank.",
  IDR: "Подойдут ATM следующих банков: BCA, CIMB Niaga, BRI, Mandiri.",
  MVR: "Подойдут ATM следующих банков: Bank of Maldives (BML), State Bank of India (SBI), Maldives Islamic Bank (MIB). Лучше использовать банкоматы в аэропорту, при отделениях банков и в туристических зонах.",
  LKR: "Подойдут ATM следующих банков: Commercial Bank, Sampath Bank, People’s Bank.",
  GEL: "Подойдут ATM следующих банков: TBC Bank, Bank of Georgia, Liberty Bank.",
  AZN: "Подойдут ATM следующих банков: eManat ATM, Unibank ATM, Yelo Bank.",
  CNY: "Подойдут ATM следующих банков: ICBC, Bank of China, China Construction Bank, Agricultural Bank of China.",
  MYR: "Подойдут ATM следующих банков: Maybank, CIMB, RHB Bank, Public Bank.",
  INR: "Подойдут ATM следующих банков: HDFC Bank, ICICI Bank, Axis Bank, State Bank of India.",
  JPY: "Подойдут ATM следующих банков: Seven Bank, Japan Post Bank, а также ATM при крупных банковских точках и аэропортах.",
  KRW: "Подойдут ATM следующих банков: Shinhan Bank, Woori Bank, Hana Bank, KB Kookmin Bank. Лучше искать ATM с пометкой Global ATM.",
  PHP: "Подойдут ATM следующих банков: BDO, BPI, Metrobank.",
  TWD: "Подойдут ATM следующих банков: Cathay United Bank, E.SUN Bank, Taipei Fubon Bank.",
  HKD: "Подойдут ATM следующих банков: HSBC, Hang Seng Bank, Bank of China (Hong Kong).",
  SGD: "Подойдут ATM следующих банков: DBS/POSB, OCBC, UOB."
};

const fallbackCountryText =
  "Подходят крупные сетевые банкоматы в торговых центрах, отделениях банков и других безопасных местах.";

const countryFaqItems = computed(() => {
  const wallets = publicSettings.value?.deposit_wallets || {};

  return Object.entries(wallets)
    .filter(([key, row]) => Number(key) >= 2102 && row && typeof row === "object" && row.symbol)
    .map(([key, row]) => {
      const symbol = String(row.symbol || "").trim().toUpperCase();
      const name = String(row.name || symbol).trim();

      return {
        id: `country-${key}`,
        q: name,
        a: ATM_HINTS[symbol] || fallbackCountryText,
        symbol,
        icon: `/img/${symbol}.svg?v=032.svg`,
      };
    });
});

const openIndex = ref(0);
const heights = ref({});

function measure(idx) {
  const item = countryFaqItems.value[idx];
  if (!item) return;

  const el = document.getElementById(`faq-panel-${item.id}`);
  if (!el) return;

  const inner = el.firstElementChild;
  if (!inner) return;

  heights.value[item.id] = inner.scrollHeight;
}

function measureAll() {
  countryFaqItems.value.forEach((_, idx) => measure(idx));
}

function toggle(idx) {
  openIndex.value = openIndex.value === idx ? -1 : idx;
  nextTick(() => measureAll());
}

function panelStyle(idx) {
  const item = countryFaqItems.value[idx];
  if (!item) return { maxHeight: "0px" };

  const isOpen = openIndex.value === idx;
  const h = heights.value[item.id] ?? 0;
  return { maxHeight: isOpen ? `${h}px` : "0px" };
}

function onResize() {
  measureAll();
}

async function loadPublicSettings() {
  try {
    const res = await fetch("/api/settings/public", { method: "GET" });
    if (!res.ok) return;

    const data = await res.json();
    publicSettings.value = data || {};
    nextTick(() => measureAll());
  } catch {}
}

onMounted(() => {
  loadPublicSettings();
  nextTick(() => measureAll());
  window.addEventListener("resize", onResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", onResize);
});
</script>

<style scoped>
.step-card {
  min-height: 560px;
}

.step-badge {
  position: absolute;
  top: 28px;
  left: 28px;
  z-index: 2;
  background: rgba(15, 23, 42, 0.88);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 18px;
  padding: 10px 16px;
  font-size: 28px;
  line-height: 1.1;
  font-weight: 600;
  color: #fff;
}

.step-image-wrap {
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: 22px;
  border: 1px solid rgba(148, 163, 184, 0.16);
  background: #0b1220;
}

.step-image {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.country-flag-box {
  width: 48px;
  height: 48px;
  min-width: 48px;
  border-radius: 9999px;
  overflow: hidden;
  background: #0b1220;
  border: 1px solid rgba(148, 163, 184, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
}

.country-flag-img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  border-radius: 9999px;
  clip-path: inset(0 round 9999px);
}

.country-answer {
  font-size: 20px;
}

.faq-open,
.faq-closed {
  transition: max-height 360ms ease, opacity 260ms ease;
  will-change: max-height, opacity;
}

.faq-open {
  opacity: 1;
}

.faq-closed {
  opacity: 0;
}

@media (max-width: 1279px) {
  .step-card {
    min-height: 520px;
  }
}

@media (max-width: 767px) {
  .step-card {
    min-height: auto;
  }

  .step-badge {
    top: 20px;
    left: 20px;
    padding: 8px 14px;
    font-size: 22px;
  }

  .country-flag-box {
    width: 42px;
    height: 42px;
    min-width: 42px;
  }

  .country-answer {
    font-size: 16px;
  }
}
</style>