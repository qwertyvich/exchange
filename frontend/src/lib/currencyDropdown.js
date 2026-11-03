import { computed, onMounted, onBeforeUnmount, ref } from 'vue';

const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
const reducedMotion = ref(motionPreference.matches);
motionPreference.addEventListener('change', event => { reducedMotion.value = event.matches; });
export const currencyMenuDuration = computed(() => reducedMotion.value ? { enter: 1, leave: 1 } : { enter: 360, leave: 240 });

// Keep the panel attached below the field at every scroll position; never flip it upwards.
export function currencyDropdownPlacement(element) {
  const rect = element.getBoundingClientRect();
  const padding = 12;
  const width = Math.min(rect.width, Math.max(0, window.innerWidth - padding * 2));
  const left = Math.max(padding, Math.min(rect.left, window.innerWidth - width - padding));
  const top = rect.bottom + 8;
  const availableHeight = Math.max(0, Math.min(228, window.innerHeight - top - padding));
  return {
    top: `${top}px`, left: `${left}px`, width: `${width}px`,
    '--currency-list-height': `${availableHeight}px`,
  };
}

// Outside pointer handling never cancels the click/scroll on the page underneath.
export function useCurrencyDropdown(open, close, giveField, getField) {
  function outside(event) {
    if (!open.value) return;
    const target = event.target;
    if (target.closest?.('[data-currency-popover]') || giveField.value?.contains(target) || getField.value?.contains(target)) return;
    close();
  }
  function keydown(event) { if (event.key === 'Escape') close(); }
  onMounted(() => { document.addEventListener('pointerdown', outside, true); document.addEventListener('keydown', keydown); });
  onBeforeUnmount(() => { document.removeEventListener('pointerdown', outside, true); document.removeEventListener('keydown', keydown); });
}
