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