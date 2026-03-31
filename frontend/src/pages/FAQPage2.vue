<template>
  <div class="flex flex-col items-center md:gap-12 gap-9 md:py-24 py-8 max-w-225 w-full self-center grow basis-full container text-white">
    <h2 class="md:text-5xl text-[28px] font-medium leading-[120%]">FAQ</h2>

    <div class="flex flex-col md:gap-4 gap-3 w-full">
      <div
        v-for="(item, idx) in faqItems"
        :key="item.id"
        class="flex flex-col bg-bg-tertiary rounded-[28px]"
      >
        <h3 class="flex">
          <button
            type="button"
            class="flex flex-1 items-center justify-between gap-2 text-left md:p-8 p-6 transition-all outline-none disabled:pointer-events-none disabled:opacity-50"
            :aria-expanded="openIndex === idx ? 'true' : 'false'"
            :aria-controls="`faq-panel-${item.id}`"
            @click="toggle(idx)"
          >
            <h4 class="md:text-2xl text-xl font-medium leading-[130%]">
              {{ item.q }}
            </h4>

            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24" height="24"
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
            <!-- ✅ ответ: белый и крупнее -->
            <p class="md:text-xl text-base font-light leading-[150%] text-white whitespace-pre-line">
              {{ item.a }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- ✅ кнопка как в оригинале по размеру -->
    <RouterLink to="/contacts" class="w-full">
      <button
        data-slot="button"
        class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-brand hover:bg-brand-hover text-text-primary data-[state=active]:bg-brand-active data-[state=active]:text-text-inv-primary md:py-6 md:px-7 py-4.5 px-5.5 max-md:rounded-[22px]"
        type="button"
      >
        <p class="md:text-xl text-base font-medium leading-[140%]">Задать вопрос</p>
      </button>
    </RouterLink>
  </div>
</template>

<script setup>
import { nextTick, onMounted, onBeforeUnmount, ref } from "vue";
import { RouterLink } from "vue-router";

// ✅ сюда вставляй ответы
const faqItems = ref([
  {
    id: "aml-kyc",
    q: "Как быстро я получу наличные после оплаты?",
    a: "Вы получаете средства в течение 5–20 минут после подтверждения платежа. Точное время зачисления зависит от выбранного способа получения: через банкомат или на банковский счёт. В редких случаях, при повышенной нагрузке на местные банки, обработка может занять немного больше времени - об этом менеджер предупреждает заранее.",
  },
  {
    id: "worktime",
    q: "Нужен ли мне заграничный банковский счёт, чтобы воспользоваться сервисом?",
    a: "Нет, тайский банковский счёт не обязателен. Вы можете получить деньги\n"+
 " через банкомат, используя инструкцию, "+
 "\nСчёт в заграничном банке нужен только в том случае, если вы хотите получить деньги напрямую на него.",
  },
  {
    id: "mix",
    q: "Есть ли скрытые комиссии или дополнительные платежи?",
    a: "Мы работаем без скрытых комиссий. Курс фиксируется в момент вашей заявки (длительность фиксации курса - 30 минут), менеджер называет итоговую сумму, которую вы получите на руки или на счёт. В случае наличия внешних банковских комиссий (например, за перевод между банками), мы заранее сообщаем о них до начала операции.",
  },
  {
    id: "time",
    q: "Можно ли у вас обменять крупную сумму?",
    a: "Да, мы работаем как с небольшими, так и с крупными суммами. Для подобных обменов мы заранее резервируем необходимый объём средств и согласовываем детали: сумму, способ получения, ориентировочное время и, при необходимости, разделение выдачи на несколько операций или банкоматов.",
  },
  {
    id: "more",
    q: "Насколько безопасно снимать деньги через банкомат по вашим инструкциям?",
    a: "Все операции проводятся по проверенным и безопасным сценариям. Вы получаете пошаговую инструкцию от менеджера, следуете ей и снимаете деньги в банкомате. Мы также подсказываем, какие банкоматы лучше выбирать и на что обратить внимание при снятии.",
  },
  {
    id: "clean",
    q: "Могу ли я перевести рубли и получить заграничную валюту",
    a: "Да, конечно. Вы можете осуществить обмен с безналичных рублей на валюту выбранной страны. Минимальная сумма обмена по рублям: 10.000 ₽",
  },
  {
    id: "cancel",
    q: "Можно ли отменить или изменить сделку после ее подтверждения?",
    a: "К сожалению, после того как сделка была подтверждена и отправлена в блокчейн, она не может быть отменена или изменена. Поэтому мы рекомендуем тщательно проверять все данные перед подтверждением обмена.",
  },
]);

// один открытый пункт (как на оригинале)
const openIndex = ref(0);

// высоты для плавного раскрытия
const heights = ref({});

function measure(idx) {
  const id = faqItems.value[idx].id;
  const el = document.getElementById(`faq-panel-${id}`);
  if (!el) return;
  const inner = el.firstElementChild;
  if (!inner) return;
  heights.value[id] = inner.scrollHeight;
}

function measureAll() {
  faqItems.value.forEach((_, idx) => measure(idx));
}

function toggle(idx) {
  openIndex.value = openIndex.value === idx ? -1 : idx;
  nextTick(() => measureAll());
}

function panelStyle(idx) {
  const id = faqItems.value[idx].id;
  const isOpen = openIndex.value === idx;
  const h = heights.value[id] ?? 0;
  return { maxHeight: isOpen ? `${h}px` : "0px" };
}

function onResize() {
  measureAll();
}

onMounted(() => {
  nextTick(() => measureAll());
  window.addEventListener("resize", onResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", onResize);
});
</script>

<style scoped>
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
</style>