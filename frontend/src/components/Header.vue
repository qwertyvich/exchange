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
.siteNavLink[aria-current="page"] {
  border-color: #83b1ff;
  box-shadow: inset 0 0 0 1px rgba(131, 177, 255, .28);
}
</style>
