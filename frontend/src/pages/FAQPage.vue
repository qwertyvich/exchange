<template>
  <component :is="currentFaqPage" />
</template>

<script setup>
import { computed, onMounted, ref } from "vue";

import FAQPage0 from "./FAQPage0.vue";
import FAQPage1 from "./FAQPage1.vue";
import FAQPage2 from "./FAQPage2.vue";

const mode = ref("0");

const currentFaqPage = computed(() => {
  if (mode.value === "1") return FAQPage1;
  if (mode.value === "2") return FAQPage2;
  return FAQPage0;
});

async function loadMode() {
  try {
    const res = await fetch("/api/settings/public", { method: "GET" });
    if (!res.ok) return;

    const data = await res.json();
    mode.value = String(data?.mode ?? "0");
  } catch {
    mode.value = "0";
  }
}

onMounted(() => {
  loadMode();
});
</script>