<template>
  <span class="casperFigure" aria-hidden="true">
    <img v-if="part !== 'accessories'" class="casperFigure__body" src="/brand/casper-ghost.webp" alt="" width="384" height="384" draggable="false" />
    <template v-if="part !== 'body'">
      <img class="casperFigure__accessory" src="/brand/casper-sunglasses.svg" alt="" width="100" height="100" draggable="false" />
      <img class="casperFigure__accessory" src="/brand/casper-suitcase.svg" alt="" width="100" height="100" draggable="false" />
    </template>
  </span>
</template>

<script setup>
defineProps({ part: { type: String, default: 'full' } });
</script>

<style>
.casperFigure { display: block; position: relative; width: 100%; height: 100%; pointer-events: none; }
.casperFigure > img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; pointer-events: none; user-select: none; }
</style>
