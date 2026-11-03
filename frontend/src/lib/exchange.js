import { tr, localeTag } from './i18n';
import { computed, watch } from 'vue';
import { marketRates } from './siteState';

export function useExchange(give, get, giveAmount, getAmount, lastEdited) {
  const direction = computed(() => marketRates.value.directions?.[`${give.value?.backendId}:${get.value?.backendId}`]);
  const rate = computed(() => {
    const row = direction.value;
    if (!row) return 0;
    if (!row.tiers?.length) return Number(row.rate) || 0;
    const tier = row.tiers.find(t => {
      const amount = lastEdited.value === 'get' ? Number(getAmount.value) / t.rate : Number(giveAmount.value);
      return amount >= t.from && amount <= t.to;
    });
    return Number(tier?.rate || row.rate) || 0;
  });
  const print = (n, digits = 8) => Number.isFinite(n) ? String(Number(n.toFixed(digits))) : '';
  const recalcGetFromGive = () => {
    const digits = Number(get.value?.backendId) < 2000 ? 8 : 2;
    const n = Number(giveAmount.value);
    // Match server's round-down rule. The signed quote on submit is authoritative.
    getAmount.value = n > 0 && rate.value > 0 ? print(Math.floor(n * rate.value * 10 ** digits + 1e-8) / 10 ** digits, digits) : '';
  };
  const recalcGiveFromGet = () => {
    const n = Number(getAmount.value);
    giveAmount.value = n > 0 && rate.value > 0 ? print(n / rate.value, 12) : '';
  };
  watch([rate, () => give.value?.backendId, () => get.value?.backendId], () => {
    if (lastEdited.value === 'give') recalcGetFromGive();
    else recalcGiveFromGet();
  });
  const limitsInGive = computed(() => ({ giveMin: print(direction.value?.min_give || 0), giveMax: print(direction.value?.max_give || 0) }));
  const limitsInGet = computed(() => ({
    getMin: print(Math.max(direction.value?.min_get || 0, (direction.value?.min_give || 0) * rate.value)),
    getMax: print(Math.min(direction.value?.max_get || Infinity, (direction.value?.max_give || 0) * rate.value)),
  }));
  const hasRates = computed(() => rate.value > 0 && Number(direction.value?.max_give) > 0);
  const rateText = computed(() => rate.value ? `1 ${give.value.symbol} = ${print(rate.value, 8)} ${get.value.symbol}` : tr("Курс временно недоступен"));
  return { direction, exchangeRate: rate, rateText, limitsInGive, limitsInGet, hasRates, recalcGetFromGive, recalcGiveFromGet };
}

export async function lockQuote(payload) {
  const response = await fetch('/api/quote', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ give_id: payload.give.currency_backend_id, get_id: payload.get.currency_backend_id, amount: String(payload.give.amount) }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || tr("Не удалось рассчитать обмен"));
  payload.quote_token = data.quote_token;
  payload.give.amount = Number(data.give_amount);
  payload.get.amount = Number(data.get_amount);
  payload.fee_percent = data.fee_percent;
  return data;
}
