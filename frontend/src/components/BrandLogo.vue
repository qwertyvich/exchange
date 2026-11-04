<template>
  <span class="casperBrand">
    <span class="casperBrand__scene" :data-casper-home-anchor="menu ? undefined : ''"><CasperFigure /></span>
    <span class="casperBrand__wordmark"><span>Casper</span><span>Exchange</span></span>
  </span>
</template>

<script setup>
import CasperFigure from './CasperFigure.vue';
defineProps({ menu: Boolean });
</script>

<style>
.casperBrand { display: flex; align-items: center; gap: 8px; max-width: 100%; }
.casperBrand__scene { position: relative; display: block; flex: 0 0 52px; width: 52px; height: 52px; }
.casperBrand__wordmark { display: flex; flex-direction: column; font-size: 23px; line-height: 1.06; letter-spacing: -.65px; font-weight: 650; color: #f5f8ff; }
.casperBrand__wordmark > span:last-child { color: #6795ff; font-weight: 600; }
body.casper-live .siteBrandBar [data-casper-home-anchor] > .casperFigure { visibility: hidden; }
@media (max-width: 1279px) {
  .casperBrand__scene { flex-basis: 48px; width: 48px; height: 48px; }
  .casperBrand__wordmark { font-size: 21px; }
}
@media (max-width: 359px) {
  .casperBrand { gap: 5px; }
  .casperBrand__scene { flex-basis: 36px; width: 36px; height: 36px; }
  .casperBrand__wordmark { font-size: 16px; letter-spacing: -.4px; }
}
</style>
