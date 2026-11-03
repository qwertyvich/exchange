<template>
  <section class="adminSettings">
    <div class="adminToolbar">
      <div><h2>{{ tr("Управление обменником") }}</h2><p>{{ tr("Курсы, реквизиты и режим сайта в одном месте.") }}</p></div>
      <button class="primary" type="button" :disabled="saving || loading" @click="save">{{ saving ? tr("Сохраняем…") : tr("Сохранить изменения") }}</button>
    </div>
    <p v-if="error" class="adminError" role="alert">{{ tr(error) }}</p>
    <p v-if="success" class="adminSuccess" role="status">{{ tr("Изменения сохранены. Сайт использует новые настройки.") }}</p>
    <p v-if="loading">{{ tr("Загружаем настройки…") }}</p>
    <template v-else-if="draft">
      <nav class="adminSections" :aria-label="tr(&quot;Разделы настроек&quot;)">
        <button v-for="tab in tabs" :key="tab.id" type="button" :class="{selected: section === tab.id}" @click="section = tab.id">{{ tr(tab.label) }}</button>
      </nav>
      <div v-if="section === 'general'" class="adminGrid">
        <article class="adminCard">
          <h3>{{ tr("Режим работы") }}</h3><p>{{ tr("Меняется состав доступных направлений. Дизайн страниц сохраняется.") }}</p>
          <label v-for="mode in modes" :key="mode.value" class="modeCard" :class="{selected: draft.mode === mode.value}">
            <input v-model="draft.mode" type="radio" :value="mode.value"><span><strong>{{ tr(mode.title) }}</strong><small>{{ tr(mode.text) }}</small></span>
          </label>
        </article>
        <article class="adminCard">
          <h3>{{ tr("Комиссия и лимиты") }}</h3><p>{{ tr("Автоматический курс уже включает комиссию. Ручной курс применяется без дополнительного вычета.") }}</p>
          <label>{{ tr("Комиссия по умолчанию, %") }}<input v-model.number="draft.percent" type="number" min="0" max="99.99" step="0.01"></label>
          <div class="adminGrid">
            <label>{{ tr("Минимум отдаваемой суммы, USD") }}<input v-model.number="draft.giveMin" type="number" min="0"></label>
            <label>{{ tr("Максимум отдаваемой суммы, USD") }}<input v-model.number="draft.giveMax" type="number" min="0"></label>
            <label>{{ tr("Минимум получаемой суммы, USD") }}<input v-model.number="draft.getMin" type="number" min="0"></label>
            <label>{{ tr("Максимум получаемой суммы, USD") }}<input v-model.number="draft.getMax" type="number" min="0"></label>
          </div>
          <label>{{ tr("Объявление на главной") }}<input v-model="draft.banner" :placeholder="tr(&quot;Оставьте пустым, чтобы скрыть&quot;)"></label>
        </article>
      </div>
      <article v-else-if="section === 'rates'" class="adminCard">
        <h3>{{ tr("Курсы направлений") }}</h3>
        <p>{{ tr("Сначала применяется ручной курс направления, затем перенесённые ручные курсы и тарифы, затем рыночный курс с комиссией. Обратное направление настраивается отдельно.") }}</p>
        <div class="marketStatus" :class="{warning: marketRates.stale}">
          {{ tr("Источник:") }} {{ marketRates.source || tr("ожидание данных") }} · {{ marketRates.updated_at ? new Date(marketRates.updated_at * 1000).toLocaleString(localeTag) : tr("ещё не обновлялся") }}
          <span v-if="marketRates.stale"> {{ tr("· Рыночные данные устарели, автоматические направления недоступны") }}</span>
        </div>
        <label>{{ tr("Направление") }}<select v-model="selectedPair"><option v-for="pair in pairChoices" :key="pair.key" :value="pair.key">{{ pair.label }}</option></select></label>
        <template v-if="selectedPair && selectedRule">
          <div class="ratePreview">{{ selectedLabel }}<br><strong>{{ tr(preview) }}</strong></div>
          <div class="adminGrid">
            <label>{{ tr("Клиент получает за 1 единицу отдаваемой валюты") }}<input v-model="selectedRule.rate" type="number" min="0" step="any" :placeholder="tr(&quot;Пусто — использовать тариф / рынок&quot;)"></label>
            <label>{{ tr("Комиссия автоматического курса, %") }}<input v-model="selectedRule.fee_percent" type="number" min="0" max="99.99" step="0.01" :placeholder="String(draft.percent)"></label>
            <label>{{ tr("Минимум в отдаваемой валюте") }}<input v-model="selectedRule.min_amount" type="number" min="0" step="any" :placeholder="tr(&quot;Пусто — общий лимит&quot;)"></label>
            <label>{{ tr("Максимум в отдаваемой валюте") }}<input v-model="selectedRule.max_amount" type="number" min="0" step="any" :placeholder="tr(&quot;Пусто — общий лимит&quot;)"></label>
          </div>
          <button type="button" @click="clearRule">{{ tr("Сбросить настройки направления") }}</button>
        </template>
        <p class="adminHint">{{ tr("У иностранных валют ниже сохранены старые курсы «RUB/USDT за 1 единицу». Чтобы перейти на автоматический курс, очистите их в разделе реквизитов. Для нового ручного курса используйте поле выше.") }}</p>
        <ul class="overrides"><li v-for="(rule, pair) in existingRules" :key="pair">{{ labelPair(pair) }}: <strong>{{ rule.rate || tr("автоматический") }}</strong></li></ul>
      </article>
      <div v-else-if="section === 'wallets'" class="adminGrid">
        <article v-for="(wallet, key) in draft.deposit_wallets" :key="key" class="adminCard">
          <h3>{{ tr(wallet.name || wallet.symbol || key) }} <small>#{{ key }}</small></h3>
          <label>{{ tr("Название") }}<input v-model="wallet.name"></label>
          <template v-if="Number(key) >= 2102">
            <label>{{ tr("Код валюты") }}<input v-model="wallet.symbol" placeholder="TRY"></label>
            <label>{{ tr("RUB за 1") }} {{ wallet.symbol }} {{ tr("— старый ручной курс") }}<input v-model="wallet.course_rub" type="number" min="0" step="any" :placeholder="tr(&quot;Пусто — рынок&quot;)"></label>
            <label>{{ tr("USDT за 1") }} {{ wallet.symbol }} {{ tr("— старый ручной курс") }}<input v-model="wallet.course_usdt" type="number" min="0" step="any" :placeholder="tr(&quot;Пусто — рынок&quot;)"></label>
          </template>
          <label v-else>{{ tr("Адрес / реквизиты") }}<input v-model="wallet.address"></label>
        </article>
        <article v-for="(tier, key) in draft.fiat_in" :key="`tier-${key}`" class="adminCard">
          <h3>{{ tr("Приём рублей · тариф") }} {{ key }}</h3>
          <div class="adminGrid"><label>{{ tr("От, RUB") }}<input v-model.number="tier.from" type="number"></label><label>{{ tr("До, RUB") }}<input v-model.number="tier.to" type="number"></label></div>
          <label>{{ tr("RUB за 1 USD (включая маржу)") }}<input v-model.number="tier.rate" type="number" step="any"></label>
          <label>{{ tr("Номер карты") }}<input v-model="tier.card_id"></label><label>{{ tr("Банк") }}<input v-model="tier.bank_name"></label><label>{{ tr("Получатель") }}<input v-model="tier.FIO"></label>
        </article>
      </div>
      <article v-else-if="section === 'contacts'" class="adminCard">
        <h3>{{ tr("Контакты для клиентов") }}</h3>
        <label v-for="field in contactFields" :key="field.key">{{ tr(field.label) }}<input v-model="draft.info[field.key]"></label>
      </article>
      <article v-else-if="section === 'telegram'" class="adminCard">
        <h3>{{ tr("Уведомления в Telegram") }}</h3>
        <p>{{ tr("Заявка сохраняется в базе сразу. Сообщение попадает в очередь и отправляется отдельно; при ошибке доставка повторяется. Отправку можно включить или выключить через TELEGRAM_ENABLED в настройках окружения.") }}</p>
        <label>{{ tr("Токен бота") }}<input v-model="draft.bot.API_TOKEN" type="password" autocomplete="new-password"></label>
        <label>{{ tr("ID чата заявок") }}<input v-model="draft.bot.CHAT_ID"></label>
        <label>{{ tr("ID чата сообщений с сайта") }}<input v-model="draft.bot.MESS_CHAT"></label>
        <label>{{ tr("Публичный адрес сайта") }}<input v-model="draft.bot.domain" placeholder="https://example.com"></label>
        <p class="adminHint">{{ tr("Переменные окружения Telegram и PUBLIC_URL имеют приоритет. Для отправки включите TELEGRAM_ENABLED в .env и пересоздайте backend.") }}</p>
      </article>
    </template>
  </section>
</template>

<script setup>
import { tr, localeTag } from '../lib/i18n';
import { ref, computed, onMounted } from 'vue';
import { marketRates, reloadSiteSettings } from '../lib/siteState';
const loading = ref(true), saving = ref(false), error = ref(''), success = ref(false), draft = ref(null), section = ref('general'), selectedPair = ref('');
const tabs = [{id:'general',label:tr("Основное")},{id:'rates',label:tr("Курсы")},{id:'wallets',label:tr("Реквизиты и тарифы")},{id:'contacts',label:tr("Контакты")},{id:'telegram',label:'Telegram'}];
const modes = [{value:'0',title:tr("Криптовалютный обмен"),text:tr("Криптовалюта → криптовалюта или рубли")},{value:'1',title:tr("Криптовалюта и карты"),text:tr("Добавляется покупка криптовалюты с рублёвой карты")},{value:'2',title:tr("Иностранные валюты"),text:tr("Рубли или USDT → иностранная валюта")}];
const contactFields = [{key:'Telegram_oper',label:tr("Telegram оператора")},{key:'Telegram_chanel',label:tr("Telegram канал")},{key:'Session_id',label:'Session ID'},{key:'Tox',label:'Tox'}];
const catalog = computed(() => Object.fromEntries((marketRates.value.currencies || []).map(c => [c.id,c])));
const labelCurrency = id => { const c=catalog.value[id]; return c ? `${c.symbol} · ${tr(c.name)}` : id; };
const labelPair = pair => pair.split(':').map(labelCurrency).join(' → ');
const pairChoices = computed(() => Object.keys(marketRates.value.directions || {}).map(key => ({key,label:labelPair(key)})));
const selectedLabel = computed(() => labelPair(selectedPair.value));
const selectedRule = computed(() => {
  if (!draft.value || !selectedPair.value) return null;
  return draft.value.direction_rates[selectedPair.value] ||= {};
});
const existingRules = computed(() => Object.fromEntries(Object.entries(draft.value?.direction_rates || {}).filter(([,r]) => Object.values(r).some(v => v !== '' && v != null))));
const preview = computed(() => {
  const n=Number(selectedRule.value?.rate || marketRates.value.directions?.[selectedPair.value]?.rate || 0);
  if (!n) return tr("Курс пока недоступен");
  const [a,b]=selectedPair.value.split(':');
  return `1 ${catalog.value[a]?.symbol} = ${n.toLocaleString(localeTag.value, {maximumFractionDigits:8})} ${catalog.value[b]?.symbol}`;
});
function headers() { return {'Content-Type':'application/json',Authorization:`Bearer ${localStorage.getItem('token') || ''}`}; }
onMounted(async () => {
  try {
    const response=await fetch('/api/admin/settings',{headers:headers()});
    if(!response.ok) throw new Error(tr("Не удалось загрузить настройки"));
    draft.value=await response.json(); draft.value.direction_rates ||= {}; draft.value.info ||= {}; draft.value.bot ||= {};
    selectedPair.value=pairChoices.value[0]?.key || '';
  } catch(e){ error.value=e.message; } finally {loading.value=false;}
});
function clearRule(){ if(draft.value && selectedPair.value) draft.value.direction_rates[selectedPair.value]={}; }
async function save(){
  if(!draft.value)return;
  saving.value=true; error.value='';success.value=false;
  try{
    const payload=JSON.parse(JSON.stringify(draft.value));
    for(const rule of Object.values(payload.direction_rates)) for(const key of Object.keys(rule)) if(rule[key] === '') delete rule[key];
    const response=await fetch('/api/admin/settings',{method:'PUT',headers:headers(),body:JSON.stringify(payload)});
    const data=await response.json();if(!response.ok)throw new Error(typeof data.detail === 'string' ? data.detail : tr("Проверьте значения полей"));
    await reloadSiteSettings();success.value=true;
  }catch(e){error.value=e.message;}finally{saving.value=false;}
}
</script>

<style scoped>
.adminSettings{display:grid;gap:20px;min-width:0;color:#f2f3fa}.adminToolbar{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}h2{font-size:24px;font-weight:600}h3{font-size:18px;font-weight:600}p,small{color:#b1b7c8;line-height:1.6}small{font-size:12px}button{cursor:pointer;border:1px solid #3a4057;border-radius:14px;padding:12px 16px;background:#21293b;color:#f2f3fa}button:disabled{opacity:.5;cursor:wait}.primary,.adminSections .selected{background:#7060cf;border-color:#a08fea}.adminSections{display:flex;gap:8px;flex-wrap:wrap}.adminGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.adminCard{display:grid;align-content:start;gap:16px;padding:24px;border:1px solid #343c50;border-radius:22px;background:#101a2c;min-width:0}.adminCard label{display:grid;gap:8px;font-size:14px;color:#ced3e2}input:not([type=radio]),select{width:100%;min-width:0;box-sizing:border-box;padding:12px 14px;border:1px solid #3b4358;border-radius:12px;background:#1a2438;color:#fff;outline:none}input:focus,select:focus{border-color:#a08fea}input::placeholder{color:#929cb3}.modeCard{display:flex!important;align-items:center;gap:12px!important;border:1px solid #3b4358;border-radius:14px;padding:16px;cursor:pointer}.modeCard.selected{border-color:#aa95ef;background:#262140}.modeCard span{display:grid;gap:4px}.marketStatus,.ratePreview{padding:16px;border:1px solid #3b4358;border-radius:14px;background:#1c2840}.warning{border-color:#b88a49}.ratePreview strong{font-size:20px}.adminError{color:#ffa4a4}.adminSuccess{color:#9be2b5}.adminHint{font-size:13px}.overrides{display:grid;gap:8px;padding:0;list-style:none}@media(max-width:850px){.adminGrid{grid-template-columns:1fr}.adminCard{padding:18px}.adminToolbar .primary{width:100%}}
</style>
