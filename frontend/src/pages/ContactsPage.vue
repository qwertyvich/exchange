<template>
  <component :is="currentContactsPage" />
</template>

<script setup>
import { computed, onMounted, ref } from "vue";

import ContactsPage0 from "./ContactsPage0.vue";
import ContactsPage1 from "./ContactsPage1.vue";
import ContactsPage2 from "./ContactsPage2.vue";

const mode = ref("0");

const currentContactsPage = computed(() => {
  if (mode.value === "1") return ContactsPage1;
  if (mode.value === "2") return ContactsPage2;
  return ContactsPage0;
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