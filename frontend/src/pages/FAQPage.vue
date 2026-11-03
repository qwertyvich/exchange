<template>
  <component :is="currentFaqPage" />
</template>

<script setup>
import { computed } from "vue";
import { siteSettings } from "../lib/siteState";
import FAQPage0 from "./FAQPage0.vue";
import FAQPage1 from "./FAQPage1.vue";
import FAQPage2 from "./FAQPage2.vue";

const mode = computed(() => String(siteSettings.value?.mode ?? "0"));
const currentFaqPage = computed(() => {
  if (mode.value === "1") return FAQPage1;
  if (mode.value === "2") return FAQPage2;
  return FAQPage0;
});
</script>