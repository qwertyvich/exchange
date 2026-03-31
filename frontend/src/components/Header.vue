<template>
  <component :is="currentHeader" />
</template>

<script setup>
import { computed, onMounted, ref } from "vue";

import Header0 from "./Header0.vue";
import Header1 from "./Header1.vue";
import Header2 from "./Header2.vue";

const mode = ref("0");

const currentHeader = computed(() => {
  if (mode.value === "1") return Header1;
  if (mode.value === "2") return Header2;
  return Header0;
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