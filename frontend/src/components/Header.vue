<template>
  <component :is="currentHeader" />
</template>

<script setup>
import { computed } from "vue";
import { siteSettings } from "../lib/siteState";
import Header0 from "./Header0.vue";
import Header1 from "./Header1.vue";
import Header2 from "./Header2.vue";

const mode = computed(() => String(siteSettings.value?.mode ?? "0"));
const currentHeader = computed(() => {
  if (mode.value === "1") return Header1;
  if (mode.value === "2") return Header2;
  return Header0;
});
</script>

<style>
.siteBrandBar { border-radius: 26px; }
.siteMenuToggle {
  background: rgba(28, 38, 57, .4);
  border: 1px solid rgba(255, 255, 255, .25);
  color: #fff;
}
.siteMenuToggle:hover { background: rgba(45, 59, 83, .55); }
@media (max-width: 1279px) {
  .siteBrandBar, .siteBrandRow { column-gap: 12px; }
}
.siteNavLink[aria-current="page"] {
  border-color: #83b1ff;
  box-shadow: inset 0 0 0 1px rgba(131, 177, 255, .28);
}
</style>
