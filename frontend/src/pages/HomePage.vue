<template>
  <component :is="currentHomepage" />
</template>

<script setup>
import { computed, onMounted, ref } from "vue";

import HomepageMode0 from "./HomePage0.vue";
import HomepageMode1 from "./HomePage1.vue";
import HomepageMode2 from "./HomePage2.vue";

const mode = ref("0");

const currentHomepage = computed(() => {
  if (mode.value === "1") return HomepageMode1;
  if (mode.value === "2") return HomepageMode2;
  return HomepageMode0;
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