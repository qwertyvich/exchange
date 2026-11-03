import { tr, localeTag } from './i18n';
import { ref } from 'vue';

export const siteSettings = ref(null);
export const marketRates = ref({ directions: {}, currencies: [] });
export const siteReady = ref(false);
export const siteError = ref('');
export const publicReviews = ref(null);
let settingsRequest, ratesRequest, reviewsRequest, bootRequest;

async function json(url, options = {}) {
  const response = await fetch(url, { ...options, signal: AbortSignal.timeout(15000) });
  if (!response.ok) throw new Error(tr("Не удалось загрузить данные ({p0})", { p0: (response.status) }));
  return response.json();
}

export function getPublicSettings(force = false) {
  if (siteSettings.value && !force) return Promise.resolve(siteSettings.value);
  if (settingsRequest) return settingsRequest;
  settingsRequest = json('/api/settings/public', force ? { cache: 'no-cache' } : {}).then(data => {
    siteSettings.value = data;
    return data;
  }).finally(() => { settingsRequest = null; });
  return settingsRequest;
}

export function refreshRates() {
  if (ratesRequest) return ratesRequest;
  ratesRequest = json('/api/rates').then(data => { marketRates.value = data; return data; })
    .finally(() => { ratesRequest = null; });
  return ratesRequest;
}

export function getReviews(force = false) {
  if (publicReviews.value && !force) return Promise.resolve(publicReviews.value);
  if (reviewsRequest) return reviewsRequest;
  reviewsRequest = json('/api/reviews/public').then(data => { publicReviews.value = data; return data; })
    .finally(() => { reviewsRequest = null; });
  return reviewsRequest;
}

let poller;
export function bootstrapSite() {
  if (bootRequest) return bootRequest;
  siteError.value = '';
  bootRequest = Promise.all([getPublicSettings(), refreshRates()]).then(() => {
    siteReady.value = true;
    // Reviews load before navigation, independently of the exchange screen.
    getReviews().catch(() => {});
    if (!poller) poller = setInterval(() => {
      if (document.visibilityState === 'visible') refreshRates().catch(() => {});
    }, 30000);
  }).catch(() => { siteError.value = tr("Не удалось подключиться к серверу. Попробуйте ещё раз."); })
    .finally(() => { bootRequest = null; });
  return bootRequest;
}

export async function reloadSiteSettings() {
  await getPublicSettings(true);
  await refreshRates();
}
